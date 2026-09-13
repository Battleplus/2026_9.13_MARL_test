# Applying the upstream patch

`0001-reproducibility.patch` is intentionally limited to changes verified by
`git apply --check`: the dependency filename/placeholder fix and the SMAC
policy import path. The executable wrappers in `scripts/` provide the same
path and CLI corrections for the unmodified submodule, including reward
trainer dataset paths, `install_sc2.sh` replacement, and `--log_interval`.

```bash
git -C upstream/MAPT apply --check ../../patches/mapt/0001-reproducibility.patch
git -C upstream/MAPT apply ../../patches/mapt/0001-reproducibility.patch
```

Do not commit changes inside `upstream/MAPT`; the main repository records only
the submodule pointer, patches, wrappers, and experiment evidence.
