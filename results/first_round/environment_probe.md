# First-round environment probe

Date: 2026-09-13 (Asia/Shanghai)

## Reproduction target

The declared Linux lock is Python 3.8.18, PyTorch 1.10.2, torchvision 0.11.3,
CUDA toolkit 11.3, PySC2 3.0.0, SMAC v0.1-beta1 and StarCraft II 4.10.
These versions are a target specification, not a claim that they are
installed on this host.

## Observed host

| Layer | Observation |
|---|---|
| Windows Python | 3.14.4 |
| Windows PyTorch | 2.13.0+cpu; CUDA build `None`; `torch.cuda.is_available() == False` |
| GPU | NVIDIA GeForce RTX 3060 Laptop GPU, 6144 MiB; driver 571.96; `nvidia-smi` CUDA 12.8 |
| WSL | Ubuntu 24.04.4 LTS, WSL2 |
| WSL Python | 3.12.3 |
| WSL PyTorch | not installed |
| WSL SC2 | `SC2_x64` not found |
| WSL SMAC | import failed: `ModuleNotFoundError` |
| WSL PySC2 | import failed: `ModuleNotFoundError` |
| System memory | 16,781,979,648 bytes (about 16 GiB) |

The Windows fallback smoke uses the existing CPU-only PyTorch 2.13.0 and is
reported separately. It is not evidence that the historical Linux lock works.
The first WSL PyTorch install attempt timed out while downloading the Linux
wheel after approximately 304 MB; no Linux smoke result is claimed.
