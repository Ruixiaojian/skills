# model data overview

百炼平台的模型数据管理功能为开发者提供统一的数据集创建、处理与回流能力，支撑模型训练、评测及持续优化。本文档系统梳理了平台支持的数据类型、关键参数、使用方式及限制条件，覆盖训练集/评测集构建、数据清洗增强、日志回流三大核心场景，所有能力当前仅在华北2（北京）和新加坡地域可用。

## 支持的模型/功能

百炼支持面向文本生成、多模态理解、图生视频等任务的结构化数据集管理，具体包括：

- **训练集类型**：SFT（监督微调）、DPO（直接偏好优化）、CPT（持续预训练）、思考模型（Thinking）、视觉理解（千问VL）、图生视频（首帧/首尾帧）等，详见[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)；
- **评测集类型**：仅支持文本生成类单轮对话评测集，用于模型泛化能力评估；
- **数据处理能力**：支持对 SFT-文本生成训练集（ChatML 格式）进行清洗（如敏感信息打码、特殊内容移除）与增强（通用/分类/抽取/创作场景），但暂不支持 SFT-图片理解训练集和 DPO 训练集，详见[数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)；
- **日志回流能力**：可将 SLS 推理日志转化为结构化 JSONL 数据集，支持训练集（SFT/DPO/CPT）和评测集，但评测集不支持 OSS 挂载存储，详见[日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 2 明确指出“数据处理支持[SFT-文本生成训练集]，暂不支持[SFT-图片理解训练集]和[DPO-文本生成训练集]”，而文档 1 中 DPO 数据集格式描述完整且无限制说明。此处以文档 2 的明确限制为准——DPO 训练集**不可**用于数据清洗或增强。

## 关键参数

| 参数 | 类型 | 作用 | 适用场景 | 备注 |
|------|------|------|----------|------|
| `loss_weight` | float (0.0–1.0) | 设置 assistant 输出或 chosen/rejected 行的训练权重 | SFT（最后 assistant 或全部 assistant）、DPO（chosen 行） | 属邀测参数，需联系商务经理开通 |
| `resized_width` / `resized_height` | int | 图像/视频帧缩放目标尺寸（像素） | 千问VL 多模态训练 | 图片单张尺寸 ≤ 1024px；图生视频图像分辨率 ≤ 4096×4096 |
| `fps` / `sample_fps` | float | 视频采样帧率 | 千问VL 视频输入、图生视频帧列表模式 | 仅 qwen3.5+ VL 模型支持 |
| `video_start` / `video_end` | float | 视频截取时间范围（秒） | 千问VL 视频输入 | 仅 qwen3.5+ VL 模型支持 |
| `foreignKey` | string | 数据增强生成样本的唯一标识 | 数据增强节点输出 | 系统自动添加，无需手动删除，不影响训练 |

## 使用方式

- **数据集创建**：通过 [数据管理](https://bailian.console.aliyun.com/#/efm/model_data) 统一入口上传 ZIP 压缩包（训练集需含根目录 `data.jsonl` 及关联媒体文件）或 Excel 文件（评测集）；
- **数据处理**：在数据流画布中编排「开始 → 数据清洗 → （可选）条件判断 → 数据增强 → 结束」节点链路，发布后创建任务处理 SFT-文本生成训练集，处理结果自动生成新版本（如 V1 → V2），不覆盖原数据；
- **日志回流**：在[模型监控](https://bailian.console.aliyun.com/#/model-telemetry)或[数据管理](https://bailian.console.aliyun.com/#/efm/data_ass)页面触发，需先完成审计日志与推理日志的授权与开启（顺序不可逆），单次回流上限 10 万条，支持多次追加至同一数据集不同版本。

## 限制和注意事项

- **地域限制**：所有功能（数据集管理、数据处理、日志回流）当前仅在华北2（北京）和新加坡 Region 可用，其他地域不显示对应入口；
- **格式与规模**：
  - SFT/CPT/DPO 训练集必须为 `.jsonl` 格式；评测集支持 `.xlsx`；
  - ZIP 包最大 2 GB（多模态）或 20 MB（图生视频）；图片单张 ≤ 10 MB；视频单个 ≤ 4096×4096 分辨率；
  - CPT 需 ≥1000 万 [Token](../concepts/token.md) 预训练数据；SFT 需 ≥1000 条优质样本；DPO 需 ≥100 条人类偏好样本；
- **存储与版本**：
  - 平台存储数据集支持「新增版本」操作；OSS 挂载数据集**不支持**该操作，须通过「导入数据」页追加；
  - 日志回流创建后，回流位置、数据类型、训练方式均不可更改；
- **安全与合规**：
  - 敏感信息打码等清洗操作需谨慎验证输出完整性，避免误删关键语义；
  - 法律文件、医学记录、方言汇总等高敏或专业领域数据，不建议使用自动清洗/增强，应人工校验；
- **模型兼容性**：
  - `video` 字段的路径模式与帧列表模式仅被 qwen3.5 及后续 VL 模型支持；
  - 思考模型训练时，`<think>` 标签仅允许出现在最后一轮 assistant 输出中，且训练后若关闭思考模式则不应再启用。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


