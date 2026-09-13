# 可直接交给另一个 AI 的执行话术

请执行 GitHub 仓库 `https://github.com/Battleplus/2026_9.13_MARL_test` 中的 MAPT 复现项目。

你的目标是复现 AAAI 2024 论文 **Decoding Global Preferences: Temporal and Cooperative Dependency Modeling in Multi-Agent Preference-Based Reinforcement Learning** 的核心 MARL 结果。开始前完整阅读仓库中的 `README.md`、`STATUS.md`、`docs/00_paper_code_audit.md` 和 `docs/01_MAPT_reproduction_plan.md`，并严格按阶段门执行。

工作要求：

1. 所有代码、配置、环境说明、进度、实验元数据、原始日志索引、结果和失败记录都必须提交到 `Battleplus/2026_9.13_MARL_test`，不要只在聊天里汇报。
2. 先完成 P1 环境与代码最小闭环，再做 P2 数据恢复/重建。环境或数据 schema 未通过小样本测试前，不得启动长时间训练。
3. 以官方仓库 `https://github.com/catezi/MAPT` 为上游，记录所用 commit。注意其根目录未发现 LICENSE：不要未经确认直接把上游全部源码重新发布到本仓库。优先提交环境文件、补丁、配置、脚本和复现说明；如确需复制代码，先判断许可并在进度中说明。
4. 官方 README 中的偏好数据链接已经失效。先搜索 release、issue、commit history、fork 或合法镜像；若仍找不到，记录证据并执行独立数据重建，不得把重建数据称为官方数据。
5. 首个任务只做 SMAC `3m`：固定 Linux、Python/PyTorch/CUDA、SC2、SMAC 版本；修复 `requirments.txt`/`requirements.txt` 不一致、`some-package==0.1`、作者绝对路径、安装脚本目录假设和命令行问题。
6. 为数据链路建立最小测试：从数据加载器反推 pickle schema，生成 32-128 条样例，验证 shape、dtype、标签、mask、trajectory length 和 batch 输出，再训练 1-3 个 epoch。要求 loss 有限、可下降、checkpoint 可保存/加载，并能在策略侧完成一次 reward inference。
7. 完成最小闭环后，生成或取得 `3m` 的 50,000 对、长度 16 的偏好数据。先跑 MAPT 单种子作为故障排查，再跑至少 3 个种子。随后补 MA-MLP、MA-LSTM、MA-Transformer。记录 reward-model 指标、平均累计回报、SMAC win rate、训练步数、评估 episode 数、wall-clock、GPU 峰值显存和所有随机种子。
8. `3m` 成功后再做 `3s5z`。目标是复现论文的方法排序和显著差距；论文数值 `3m: 19.98 ± 0.05`、`3s5z: 19.59 ± 0.42` 仅作为对照。若绝对差异超过 10%，检查并记录环境版本、数据生成、reward normalization、episode length、模型 checkpoint 和评估协议差异。
9. 在 `3s5z` 上完成 MAPT-TPA、MAPT-CPA 和 LSTM 替换消融，每个至少 3 个种子。资源充足再考虑 `6h_vs_8z` 或 Football；不要在 SMAC 未稳定前扩展到 Bi-DexHands/Ma-MuJoCo。
10. 每个实验建立 `experiments/<run_id>/metadata.yaml`，包含 Git commit/dirty 状态、环境、任务、算法、种子、数据 SHA-256、完整命令、全部超参数、软硬件版本、开始结束时间、退出码、日志和 checkpoint 路径。失败实验也要保留元数据和根因。
11. 每完成一个小阶段，更新 `STATUS.md` 和当天的 `progress/YYYY-MM-DD.md`，然后提交并推送。提交信息需说明阶段和结果，例如 `p1: make MAPT reward-model smoke test pass`。
12. 不伪造结果，不以单种子宣称复现成功，不删除失败日志，不在条件不同的情况下直接比较绝对数值。连续三次出现相同外部阻塞时，提交一份 blocker 记录，说明证据、已尝试方案和需要的人类输入。

第一轮只执行以下内容并提交：

- 审计仓库当前结构与 Git 状态。
- 建立或更新环境锁定方案。
- 完成 MAPT 上游代码的非侵入式获取方式（submodule、下载脚本或明确补丁流程，需符合许可证约束）。
- 修复并验证最小 import。
- 反推偏好数据 schema，创建小型合成 fixture。
- 运行 reward model 的最小 smoke test，并验证 checkpoint 加载和单次 reward inference。
- 更新状态、进度和下一阶段预计 GPU 成本。

第一轮完成后，先给出仓库提交链接、已通过的测试、尚未解决的 blocker 和进入 `3m` 长训练前的资源需求；不要自动进入长训练，除非仓库计划中的阶段门全部满足且算力已明确可用。
