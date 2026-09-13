# MAPT 分阶段复现计划

## 一、复现问题

目标不是简单运行官方代码，而是回答三个可检验问题：

1. MAPT 的时间依赖和协作依赖建模能否在相同偏好数据下优于传统多智能体奖励模型？
2. MAPT 学得的奖励能否稳定指导 MAT 策略训练，而不只是在偏好分类上取得更低 loss？
3. 在原始数据不可用时，独立重建的合成教师数据能否复现论文中的相对趋势？

## 二、复现目标与验收标准

### 目标 R0：环境与代码最小闭环

范围：不跑完整训练，只验证代码链路。

验收标准：

- 固定 MAPT commit、Python、PyTorch、CUDA、SMAC 和 SC2 版本。
- 修正依赖文件名、无效依赖、绝对路径和命令行错误。
- 运行静态检查和最小 import 测试。
- 用极小伪造数据跑 1-3 个 reward-model epoch，loss 有限且 checkpoint 可保存/加载。
- 用 checkpoint 完成一次策略侧 reward inference。

### 目标 R1：SMAC `3m` 最小复现

原因：官方同时提供奖励模型和策略模型脚本，是风险最低的任务。

数据：优先恢复官方 `3m_replaybuffer_5w_len16_diff0.5` 数据；如果无法获得，则用相同命名规则与论文描述重建 50,000 对长度 16 的合成偏好。

对照：MAPT、MA-MLP、MA-LSTM、MA-Transformer；先完成 MAPT 与一个最简单基线，再补齐全部基线。

验收标准：

- 每个方法至少 3 个随机种子；最终报告再评估是否扩展到论文的 8 个种子。
- 保存偏好训练/验证准确率、reward loss、策略平均回报、SMAC win rate、训练步数和 wall-clock 时间。
- MAPT 在平均策略回报或 win rate 上稳定优于至少 MA-MLP 与 MA-Transformer。
- 与论文 `3m` 的 MAPT 平均累计回报 `19.98 ± 0.05` 做对照，但不把精确命中作为唯一成功标准。
- 若数值差异超过 10%，给出环境版本、数据生成、归一化、episode length 和评估协议的差异分析。

### 目标 R2：SMAC `3s5z` 核心结果

原因：论文在该困难协作任务上报告 MAPT `19.59 ± 0.42`，并描述约 94% win rate，方法区分度高。

验收标准：

- 从 `3m` 脚本派生并提交完整 `3s5z` 配置。
- 至少 3 个种子；固定训练预算和评估协议。
- MAPT 明显优于 MA-MLP、MA-LSTM、MA-Transformer。
- 复现“方法排序和显著差距”；精确数值作为次级目标。

### 目标 R3：机制消融

任务：优先 `3s5z`，资源允许时增加 `6h_vs_8z`。

变体：

- MAPT-TPA：去掉 temporal-aware preference attention。
- MAPT-CPA：去掉 cooperation-aware preference attention。
- MAPT*：用 LSTM 替换 self-attention。

验收标准：

- 每个变体至少 3 个种子。
- 主模型总体优于 TPA/CPA 消融。
- 输出与论文 Table 2/3 对齐的表格，并分析是否只有某一依赖在特定任务起作用。

### 目标 R4：跨环境扩展（可选）

优先顺序：Football `academy_3_vs_1_with_keeper` > Ma-MuJoCo `HalfCheetah 6x1` > Bi-DexHands。

只有满足以下条件才启动：SMAC 闭环稳定、数据流程可复用、GPU 预算明确、环境许可证和依赖可接受。

## 三、双轨数据策略

### A 轨：官方数据恢复

1. 检查仓库 issue、commit history、fork 和 release 是否存在镜像。
2. 联系作者请求新的下载地址、数据校验值和生成脚本。
3. 获得后记录来源、下载日期、文件列表、大小和 SHA-256。
4. 不把未验证的第三方数据直接标为官方数据。

### B 轨：独立数据重建

1. 用任务真实 reward 作为 deterministic scripted teacher。
2. 训练或取得 MAT/HAPPO 行为策略并保存 replay buffer。
3. 从轨迹中采样成对 segment，`3m` 首先使用长度 16、总计 50,000 对。
4. 用两段轨迹的累计真实 reward 比较生成偏好标签，并明确 tie 与 `diff0.5` 的处理。
5. 输出数据 schema、字段 shape/dtype、标签比例、回报差分分布和 SHA-256。
6. 把 B 轨结果标记为 independent reproduction，不与 A 轨混淆。

数据可行性门：如果无法明确官方 pickle schema，则先从 `pair_dataloader.py` 和训练入口反推 schema，生成 32-128 条样例并通过数据加载测试后，才生成全量数据。

## 四、环境与算力

推荐训练环境：

- Ubuntu 20.04/22.04 或兼容容器。
- Python 3.8 作为首选兼容版本。
- 从官方声明的 PyTorch 1.10.2 开始；若升级，单独记录补丁和行为差异。
- CUDA 版本与 PyTorch wheel 匹配。
- SC2 4.10 与 SMAC v0.1-beta1 作为首个候选组合。
- 单张 NVIDIA GPU；论文使用 Tesla V100。建议至少 16 GB 显存、32 GB 系统内存。
- 预留 50-100 GB 磁盘用于环境、数据、checkpoint 和日志。

当前本机没有检测到 `nvidia-smi` 且仅约 16 GB 内存，不建议在本机承诺完成全量训练。

## 五、执行阶段与预计工期

| 阶段 | 工作 | 预计时间 | 退出条件 |
|---|---|---:|---|
| P1 | 冻结环境、修复安装与路径 | 1-2 天 | import/smoke test 通过 |
| P2 | 恢复数据或完成 schema 与小样本重建 | 1-3 天 | 小数据可被训练器读取 |
| P3 | reward model 最小训练与策略推理 | 1-2 天 | loss/checkpoint/inference 全通过 |
| P4 | `3m` MAPT 三种子 | 2-4 天加排队时间 | 指标与日志完整 |
| P5 | `3m` 基线和消融 | 3-6 天加排队时间 | 可比较表格完成 |
| P6 | `3s5z` 主结果 | 3-6 天加排队时间 | 三种子与差异分析完成 |
| P7 | 扩种子、跨任务、最终报告 | 3-7 天 | 报告可审计 |

预计 2-4 周，实际取决于 GPU 并行度和原始数据是否能恢复。

## 六、实验记录与结果格式

每次运行创建 `experiments/<run_id>/metadata.yaml`，至少包含：

- `run_id`、日期、执行者。
- Git commit 与 dirty 状态。
- 环境/任务/方法/种子。
- 数据版本与 SHA-256。
- 完整启动命令和超参数。
- GPU、CUDA、Python、PyTorch、SMAC、SC2 版本。
- 退出码、开始/结束时间、wall-clock。
- checkpoint、原始日志和评估结果路径。

聚合结果必须同时报告均值、标准差、种子数、训练预算和评估 episode 数。失败运行不得删除，应在进度日志中说明原因。

## 七、停止规则

- 环境或数据 schema 未通过最小测试时，不启动长时间训练。
- 单种子结果不宣称复现成功。
- 训练预算、评估协议或数据来源不同，不直接比较绝对值。
- 连续 3 次相同失败后，记录根因、最小复现和下一项外部依赖，不无限重试。
- 未取得明确许可证前，避免公开发布 MAPT 原代码的修改副本；优先以补丁、说明和实验配置形式记录工作，并请求作者澄清许可。

## 八、最终交付物

1. 可重建环境与版本锁定文件。
2. 数据恢复记录或独立数据生成脚本、schema 和校验值。
3. MAPT 与基线/消融的可运行配置。
4. 原始日志、checkpoint 索引和聚合指标。
5. 对齐论文 Table 1-3 的结果表与曲线。
6. 一份说明“复现了什么、没有复现什么、为何有差异”的最终报告。
