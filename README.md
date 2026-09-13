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
- 当前本机为 Windows 11、约 16 GB 内存，未检测到 `nvidia-smi`。本机适合文档、静态审计和小规模单元测试；全量训练建议使用 Linux + NVIDIA GPU。

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
