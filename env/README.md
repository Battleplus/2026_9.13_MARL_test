# MAPT Linux environment

The historical reproduction target is Python 3.8.18, PyTorch 1.10.2,
torchvision 0.11.3 and CUDA 11.3, matching the oldest stack named by the
upstream project. `mapt-linux-lock.yml` is the declarative environment file.
SC2 4.10 and SMAC v0.1-beta1 are installed separately because SC2 is a
binary distribution and SMAC is not a conda package.

```bash
conda env create -f env/mapt-linux-lock.yml
conda activate mapt-reproduction
bash scripts/install_sc2.sh --sc2-root "$PWD/third_party/StarCraftII"
python scripts/run_mapt_smoke.py --device cpu
```

The current host is Windows 11 with WSL2 Ubuntu 24.04, Python 3.12 and an
RTX 3060 Laptop GPU. It does not satisfy the historical lock as-is: PyTorch
1.10.2 has no Python 3.12 wheel. Until a Python 3.8 environment is created,
the full locked install and SMAC training remain pending. The synthetic
smoke harness is designed to run in a Python 3.8/1.10.2 environment and does
not download or require preference data.

Record the exact environment before any long run:

```bash
python --version
python -c 'import torch; print(torch.__version__, torch.version.cuda, torch.cuda.is_available())'
python -c 'import pysc2; print(getattr(pysc2, "__version__", "unknown"))'
python -c 'import smac; print(getattr(smac, "__version__", "unknown"))'
SC2PATH=/path/to/StarCraftII python -c 'import os; print(os.environ["SC2PATH"])'
nvidia-smi
```
