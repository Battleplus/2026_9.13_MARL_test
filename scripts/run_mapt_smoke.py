#!/usr/bin/env python3
"""Run the first MAPT reproducibility gate on an independent synthetic fixture."""

from __future__ import annotations

import argparse
import json
import pickle
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "upstream" / "MAPT"
sys.path.insert(0, str(UPSTREAM))

import torch  # noqa: E402
import transformers  # noqa: E402
from ml_collections import ConfigDict  # noqa: E402

from mat.algorithms.reward_model.models.MultiPrefTransformer import MultiPrefTransformer  # noqa: E402
from mat.algorithms.reward_model.models.encoder_decoder_divide import MultiTransRewardDivideModel  # noqa: E402
from mat.algorithms.reward_model.models.torch_utils import batch_to_torch  # noqa: E402
from mat.algorithms.reward_model.utils.dataloader import load_dataset  # noqa: E402


def make_fixture(path: Path, count: int, seed: int) -> None:
    rng = np.random.default_rng(seed)
    records = []
    obs_dim, n_agent, action_dim, traj_len = 5, 3, 9, 4
    for i in range(count):
        q0 = float(rng.uniform(-1.0, 1.0))
        q1 = float(rng.uniform(-1.0, 1.0))
        if i % 12 == 0:
            q1 = q0
        obs0 = rng.normal(0, 0.05, (traj_len, n_agent, obs_dim)).astype(np.float32)
        obs1 = rng.normal(0, 0.05, (traj_len, n_agent, obs_dim)).astype(np.float32)
        obs0[..., 0] += q0
        obs1[..., 0] += q1
        actions0 = rng.integers(0, action_dim, (traj_len, n_agent, 1), dtype=np.int64)
        actions1 = rng.integers(0, action_dim, (traj_len, n_agent, 1), dtype=np.int64)
        label = 0 if q0 == q1 else (1 if q0 > q1 else -1)
        records.append({
            "traj0": {"obs": obs0, "actions": actions0},
            "traj1": {"obs": obs1, "actions": actions1},
            "label": label,
        })
    with path.open("wb") as handle:
        pickle.dump(records, handle, protocol=4)


def assert_fixture(train, val, info, count):
    assert train["observations0"].shape == (int(count * 0.8), 4, 3, 5)
    assert train["actions0"].shape == (int(count * 0.8), 4, 3, 1)
    assert train["observations0"].dtype == np.float32
    assert train["actions0"].dtype == np.int64
    assert train["timesteps0"].dtype in (np.dtype(np.int32), np.dtype(np.int64))
    assert train["labels"].shape[1:] == (2,)
    assert np.all(np.isin(train["labels"], [0.0, 0.5, 1.0]))
    assert np.allclose(train["labels"].sum(axis=1), 1.0)
    assert val["observations1"].shape[1:] == (4, 3, 5)
    assert info == {"observation_dim": 5, "action_dim": 9, "max_len": 4, "n_agent": 3}


def build_model(device):
    cfg = MultiPrefTransformer.get_default_config()
    cfg.embd_dim = 32
    cfg.pref_attn_embd_dim = 32
    cfg.action_embd_dim = 16
    cfg.n_layer = 1
    cfg.n_head = 4
    cfg.use_lstm = False
    cfg.use_dropout = False
    cfg.scheduler_type = "CosineDecay"
    cfg.trans_lr = 2e-3
    config = transformers.GPT2Config(**ConfigDict(cfg).to_dict())
    trans = MultiTransRewardDivideModel(
        config=config, observation_dim=5, action_dim=9, n_agent=3,
        action_type="Discrete", max_episode_steps=4, device=device,
    )
    return MultiPrefTransformer(config, trans, device)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=64, choices=range(32, 129))
    parser.add_argument("--seed", type=int, default=20260913)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args()
    if args.device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("--device cuda requested but torch.cuda.is_available() is false")
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    device = torch.device(args.device)

    with tempfile.TemporaryDirectory(prefix="mapt_smoke_") as temp:
        temp_path = Path(temp)
        fixture_path = temp_path / "preference_pair_data.pkl"
        make_fixture(fixture_path, args.count, args.seed)
        train, val, info = load_dataset("smac", "3m", str(fixture_path), "Discrete")
        assert_fixture(train, val, info, args.count)

        model = build_model(device)
        batch = batch_to_torch(train, device)
        eval_batch = batch_to_torch(val, device)
        losses = []
        for _ in range(2):
            losses.append(float(model.train(batch)["trans_loss"]))
        eval_loss = float(model.evaluation(eval_batch)["eval_trans_loss"])
        if not all(np.isfinite(losses)) or not np.isfinite(eval_loss):
            raise AssertionError(f"non-finite loss: train={losses}, eval={eval_loss}")
        if losses[-1] >= losses[0]:
            raise AssertionError(f"loss did not decrease: {losses}")

        checkpoint_dir = temp_path / "models"
        checkpoint_dir.mkdir()
        model.save_model(str(checkpoint_dir) + "/", 2)
        checkpoint = checkpoint_dir / "reward_model_2.pt"
        reloaded = build_model(device)
        reloaded.load_model(str(checkpoint))
        inference = batch_to_torch({
            "observations": train["observations0"][:1, :1],
            "actions": train["actions0"][:1, :1],
            "timestep": train["timesteps0"][:1, :1],
            "attn_mask": np.ones((1, 1, 3), dtype=np.float32),
        }, device)
        rewards = reloaded.get_reward(inference)
        if tuple(rewards.shape) != (1, 3, 1) or not torch.isfinite(rewards).all():
            raise AssertionError(f"unexpected inference output: {tuple(rewards.shape)}")

        report = {
            "fixture_count": args.count,
            "schema": {
                "observations": ["float32", "B,T,N,obs_dim"],
                "actions": ["int64", "B,T,N,1"],
                "labels": ["float64", "B,2", "one-hot/soft tie"],
                "mask": ["float32", "B,T,N", "inference ones for valid steps"],
                "trajectory_length": 4,
                "batch_train": int(train["observations0"].shape[0]),
                "batch_val": int(val["observations0"].shape[0]),
            },
            "train_loss": losses,
            "eval_loss": eval_loss,
            "checkpoint_reload": True,
            "inference_shape": list(rewards.shape),
            "device": str(device),
            "torch": torch.__version__,
        }
        rendered = json.dumps(report, indent=2, sort_keys=True)
        print(rendered)
        if args.report is not None:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
