# 论文与代码审计

审计日期：2026-09-13

## 审计范围

本轮检查了本地文件夹中的 4 篇 PDF，并核对了论文正文、公开仓库和当前可访问性。

## 汇总结论

| 论文 | 与 MARL 的关系 | 代码/资源状态 | 严格开源判断 | 本项目用途 |
|---|---|---|---|---|
| Decoding Global Preferences / MAPT（AAAI 2024） | 直接相关，主方法论文 | 官方公开代码仓库存在 | 仓库未发现 LICENSE；源码公开但许可不明确 | **主复现对象** |
| Deep Reinforcement Learning from Human Preferences（NeurIPS 2017） | 单智能体 PbRL/RLHF 基础 | 有作者关联的 `rl-teacher` 和第三方复现 | `rl-teacher` 与 HumanCompatibleAI 复现均标注 MIT | 理论与奖励学习流程参考，不做主复现 |
| A Survey of Reinforcement Learning from Human Feedback（2025 版本） | 广义 RLHF 综述，不是 MARL 方法 | 未发现该综述的配套实现；文中整理多个库 | 不适用 | 评价方法、工具链和基准参考 |
| A Comprehensive Survey of Reward Models（2025） | 主要面向 LLM 奖励模型，不是 MARL | 有 `awesome-reward-models` 资源列表 | 仓库仅见 README，未发现 LICENSE，也不是训练实现 | 文献索引，不做复现 |

## 1. MAPT

论文：**Decoding Global Preferences: Temporal and Cooperative Dependency Modeling in Multi-Agent Preference-Based Reinforcement Learning**

- 官方代码：[catezi/MAPT](https://github.com/catezi/MAPT)
- 论文入口：[AAAI PDF](https://ojs.aaai.org/index.php/AAAI/article/download/29666/31137)
- 当前审计提交：`0b4ef2712995681febca7631f9a27e1b0dccccbf`
- 论文实验：SMAC、Google Research Football、Bi-DexHands、Multi-agent MuJoCo。
- 论文偏好数据规模：SMAC/Football 各 50,000 对，Bi-DexHands/Ma-MuJoCo 各 30,000 对。
- 论文报告结果取 8 次运行的均值和标准差，训练硬件为单张 NVIDIA Tesla V100。

### 已公开内容

- MAPT 奖励模型核心实现。
- MAT/HAPPO 相关策略训练代码。
- SMAC、Football、Bi-DexHands、Ma-MuJoCo 环境适配代码。
- 奖励模型与策略模型的训练入口。
- 4 组示例脚本：SMAC `3m`、Football `academy_3_vs_1_with_keeper`、Bi-DexHands `DoorOpenInward`、Ma-MuJoCo `HalfCheetah 6x1`。

### 可复现性问题

1. 根目录实际文件是 `requirments.txt`，README 命令却写成 `requirements.txt`。
2. 依赖固定在较旧栈，例如 PyTorch 1.10.2、Gym 0.12.4，并包含可疑占位依赖 `some-package==0.1`。
3. 脚本内含作者机器的绝对路径，必须参数化。
4. `install_sc2.sh` 假设位于 `$EXP_DIR/pymarl`，与当前仓库结构并不一致。
5. 论文包含更多任务，但仓库只有 4 组示例脚本。
6. 仓库没有测试目录、CI 和明确许可证文件。
7. 官方 README 指向的 BUAA AnyShare 数据地址已失效，页面显示 `This address has expired`。
8. 论文声称 8 次运行，但示例脚本只提供 `seed=1`。

### 结论

MAPT 是“有公开实现、但不是一键复现”的项目。最大难点不是模型代码，而是旧环境、失效数据、硬编码路径和实验配置不完整。

## 2. Deep Reinforcement Learning from Human Preferences

- 论文：[arXiv:1706.03741](https://arxiv.org/abs/1706.03741)
- 作者关联实现：[nottombrown/rl-teacher](https://github.com/nottombrown/rl-teacher)，MIT License。
- 较模块化的第三方复现：[HumanCompatibleAI/learning-from-human-preferences](https://github.com/HumanCompatibleAI/learning-from-human-preferences)，MIT License。

该论文是偏好奖励学习的基础来源，但实验是 Atari 与单智能体连续控制，不属于 MARL。原始实现依赖 Python 3.5、旧 MuJoCo、TensorFlow/TRPO/PPO 和 GCS，直接复现成本高且偏离当前项目目标。因此仅复用其 Bradley-Terry 偏好损失、合成教师和奖励模型评价思路。

## 3. A Survey of Reinforcement Learning from Human Feedback

- 论文：[arXiv:2312.14925](https://arxiv.org/abs/2312.14925)

未发现该综述本身的配套实现。综述列出的可用库包括 `imitation`、`Clean-Offline-RLHF`、`APReL`、`POLAR` 和 `trlX`；这些是综述引用的第三方工具，不应写成“综述代码”。本项目主要采用其评价建议：同时评价奖励模型与最终策略，并优先使用合成反馈保证可重复性。

## 4. A Comprehensive Survey of Reward Models

- 论文：[arXiv:2504.12328](https://arxiv.org/abs/2504.12328)
- 配套资源列表：[JLZhong23/awesome-reward-models](https://github.com/JLZhong23/awesome-reward-models)

该仓库是论文列表而不是可运行实现，且目前根目录仅见 README，未发现 LICENSE。论文重点是 LLM 时代的奖励模型，因此不作为本次 MARL 复现对象。

## 推荐优先级

1. **MAPT / SMAC `3m`**：官方脚本存在，最适合做最小闭环。
2. **MAPT / SMAC `3s5z`**：论文提升显著，适合作为核心主结果，但需补脚本和数据。
3. **MAPT 消融**：TPA、CPA 和 LSTM 替换，用于验证因果性而非只追一个最终分数。
4. **`6h_vs_8z` 或 Football `3_vs_1`**：作为跨任务扩展，视算力和环境稳定性决定。
5. Bi-DexHands 与 Ma-MuJoCo 暂缓：依赖和 GPU 成本更高，优先级低于 SMAC。
