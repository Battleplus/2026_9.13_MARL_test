# 实验目录规范

每次运行使用唯一目录：

```text
experiments/<YYYYMMDD>-<env>-<task>-<method>-s<seed>/
  metadata.yaml
  command.txt
  notes.md
  metrics/
  logs/
```

大体积 checkpoint、replay buffer 和原始数据不要直接提交 Git。应记录其受控存储位置、文件大小和 SHA-256，并在 `.gitignore` 中排除。小型测试 fixture 可以提交。

`metadata.yaml` 必须记录代码版本、数据版本、完整参数、软硬件环境、随机种子、退出状态和产物路径。
