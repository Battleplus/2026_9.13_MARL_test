# 2026-09-13 MARL 复现项目

本仓库用于跟踪多智能体强化学习（MARL）论文的代码审计、环境搭建、实验复现和结果分析。

当前主目标是复现 AAAI 2024 论文：

> Tianchen Zhu, Yue Qiu, Haoyi Zhou, Jianxin Li. **Decoding Global Preferences: Temporal and Cooperative Dependency Modeling in Multi-Agent Preference-Based Reinforcement Learning**.

论文提出 Multi-Agent Preference Transformer（MAPT），用时间维和智能体协作维的全局依赖来学习多智能体偏好奖励。

## 当前结论

- 本批 4 篇论文中，只有 MAPT 是直接面向 MARL 的方法论文，作为主复现对象。
- MAPT 有官方公开仓库：[catezi/MAPT](https://github.com/catezi/MAPT)，但仓库根目录未发现许可证文件，严格来说属于“源码公开”，不能直接认定为具有明确开源许可。
- MAPT 的代码、奖励模型、策略训练入口和 4 个示例任务脚本可见，但论文中的全任务脚本、测试、CI 和完整环境锁定信息不全。
- 官方 README 提供的偏好数据链接在 2026-09-13 实测显示 `This address has expired`，因此数据恢复/重建是当前最大风险。
- 当前本机为 Windows 11、约 16 GB 内存，检测到 RTX 3060 Laptop GPU（6 GB）；当前可用 Windows PyTorch 为 CPU-only fallback。本机已验证小规模闭环；全量训练建议使用 Linux + NVIDIA GPU。

## 当前复现效果

截至 2026-09-14，已使用公开 MAPT 仓库完成本机最小闭环验证。测试使用 64 条独立合成 preference fixture，未使用论文官方偏好数据：

| 项目 | 实测结果 |
|---|---|
| 数据加载 | 通过；train/val = 51/13 |
| observation | `float32`，形状 `B,T,N,obs_dim` |
| action | `int64`，形状 `B,T,N,1` |
| label | `1/-1/0` 正确编码为 one-hot / tie soft label |
| trajectory | `T=4`，`N=3`，SMAC `3m` action dim = 9 |
| reward model loss | `2.577014 → 0.837357`（2 个训练 epoch） |
| eval loss | `0.185735` |
| checkpoint | 保存、重新加载通过 |
| learned reward inference | 通过，输出形状 `(1,3,1)` |

完整原始 JSON 结果见
[windows_fallback_smoke_rerun_2026-09-14.json](results/first_round/windows_fallback_smoke_rerun_2026-09-14.json)。
该结果是 Windows Python 3.14.4 + PyTorch 2.13.0+cpu fallback 的工程链路验证，
不是论文中基于官方数据和 SMAC 长训练得到的最终回报或胜率；正式 `3m` 结果仍待 Linux
环境、SC2/SMAC 和数据阶段门完成。

## 复现上游与许可边界

本项目直接使用公开的 [catezi/MAPT](https://github.com/catezi/MAPT) 仓库
完成复现。上游以 Git submodule 固定在 commit
`0b4ef2712995681febca7631f9a27e1b0dccccbf`；本仓库不复制或重新发布上游完整源码，
而是通过 submodule、补丁、配置、wrapper 和实验证据复现其行为。上游根目录未发现
明确 LICENSE，因此“使用公开仓库进行本地复现”和“将上游源码作为本项目源码重新发布”
是两件不同的事：前者是本项目当前采用的方式，后者暂不进行。

## 仓库导航

- [论文与代码审计](docs/00_paper_code_audit.md)
- [MAPT 复现计划](docs/01_MAPT_reproduction_plan.md)
- [AI 执行话术](docs/02_AI_execution_prompt.md)
- [项目状态](STATUS.md)
- [2026-09-13 进度记录](progress/2026-09-13.md)
- [实验记录规范](experiments/README.md)
- [结果目录规范](results/README.md)

## 工作原则

1. 每次实验必须记录代码提交、环境、数据来源、参数、随机种子和原始日志。
2. 先完成可验证的最小闭环，再扩大任务、基线和随机种子数量。
3. 论文精确数值不是唯一标准；同时检查方法排序、稳定性、奖励模型质量和策略表现。
4. 原始数据不可得时，明确标注为“独立重建”，不得冒充使用了论文原始数据。
5. 所有进度、决定、失败原因和结果都提交到本仓库。
