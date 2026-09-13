# 项目状态

最后更新：2026-09-13（第一轮执行后）

## 总体状态

**阶段：P1/P2/P3 最小闭环已完成 Windows fallback；Linux 锁定环境与 SMAC 主结果仍待执行。**

## 阶段看板

| 阶段 | 状态 | 完成条件 |
|---|---|---|
| P0 论文与仓库审计 | 完成 | 确认主论文、代码状态、主要风险和复现范围 |
| P1 环境冻结与代码修复 | 部分完成 | Linux 锁定文件、静态检查和路径/依赖适配已提交；Linux import/smoke 待执行 |
| P2 偏好数据恢复或重建 | 小样本完成，原始数据阻塞 | 64 条独立 fixture 通过 schema 验证；官方数据仍不可得 |
| P3 奖励模型最小闭环 | Windows fallback 通过 | 2 epoch loss 下降，checkpoint 可加载，策略侧 inference 通过；Linux 锁定栈待执行 |
| P4 SMAC `3m` 主结果 | 待执行 | 3 个种子完成，MAPT 表现与论文趋势一致 |
| P5 基线与消融 | 待执行 | MA-MLP、MA-LSTM、MA-Transformer、TPA/CPA 消融完成 |
| P6 困难任务扩展 | 待执行 | 至少完成 `3s5z`，资源允许时增加 `6h_vs_8z` |
| P7 报告与归档 | 待执行 | 表格、曲线、差异分析和复现实验说明齐全 |

## 当前阻塞项

1. MAPT 官方偏好数据分享地址已失效；当前仅有独立合成 fixture，不能称为官方数据。
2. WSL Ubuntu 24.04 的 Python 3.12 不兼容历史 PyTorch 1.10.2；Linux smoke wheel 下载又在约 304 MB 处超时。
3. WSL 当前未安装 SC2 4.10、SMAC v0.1-beta1 或 PySC2；Windows RTX 3060 仅 6 GB 显存，不足以按论文硬件条件承诺长训练。
4. 官方依赖较旧，且安装说明中的依赖文件名与实际文件名不一致；已提交锁定文件和 wrapper。
5. 官方仓库没有明确许可证、测试和 CI；主仓库继续只记录 submodule 指针、补丁和适配脚本。

## 下一步

先在 Linux/Python 3.8.18/PyTorch 1.10.2 环境重跑 `scripts/run_mapt_smoke.py`，补齐 SC2/SMAC 版本记录；通过后才考虑恢复/重建 50,000 对 `3m` 数据和单种子长训练。

## 已验证证据

- Patch dry-run：`git -C upstream/MAPT apply --check patches/mapt/0001-reproducibility.patch` 通过。
- Static：MAPT reward 核心 3 个模块 AST parse、3 个 Linux shell wrapper `bash -n` 通过。
- Windows fallback：`results/first_round/windows_fallback_smoke.json`，Python 3.14.4、PyTorch 2.13.0+cpu、64 条 fixture、loss `2.577014 -> 0.837357`、eval `0.185735`、inference `(1,3,1)`。
