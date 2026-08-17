# model data overview

百炼平台的模型数据管理功能为大模型调优与评测提供统一、可版本化、可处理的数据基础设施。它覆盖从数据集创建、导入、清洗增强到版本发布的全生命周期，支持 SFT/DPO/CPT 训练及文本生成类评测任务。所有操作均通过控制台完成，当前暂不提供数据处理 API。

## 支持的模型/功能

- **训练集类型**：支持文本生成、多模态理解、图生视频（首帧/首尾帧）四类训练场景；其中 SFT 和 DPO 仅限文本生成场景，CPT 仅支持文本生成且必须在北京地域使用 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集类型**：仅支持文本生成场景，不支持多模态或图生视频 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理能力**：支持对 **SFT-文本生成训练集（ChatML 格式）** 进行清洗（如敏感信息打码、特殊内容移除）和增强（如 Few-Shot 生成），但**不支持 SFT-多模态训练集、DPO 训练集或 CPT 训练集** [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：支持将 SLS 推理日志转化为结构化 JSONL 数据集，可用于训练集（SFT/DPO/CPT）或评测集，当前仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 1 称“DPO/CPT 训练方法、云存储挂载仅支持北京地域”，而文档 3 明确日志回流在**北京和新加坡**均可用。对于 DPO/CPT 训练本身（非日志回流），仍以文档 1 为准——即仅北京支持；日志回流作为独立数据源通道，在新加坡也可用于生成 DPO/CPT 训练集，但后续训练任务仍需调度至北京执行。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **数据集名称** | 最长 50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3） | 创建后不可修改 |
| **数据集类型** | “训练集”或“评测集”，创建后不可变更 | 评测集仅支持文本生成场景 |
| **训练场景** | 文本生成 / 多模态理解 / 图生视频（首帧）/ 图生视频（首尾帧） | 评测集不显示此字段 |
| **训练方法** | SFT / DPO / CPT（仅训练集） | CPT 不支持草稿、不支持数据继承；DPO 仅北京可用 |
| **存储位置** | 平台 OSS 存储（免费）或云存储挂载（OSS 挂载） | 评测集不支持 OSS 挂载；OSS 挂载需 Bucket 标签 `bailian-datahub-access=read` |
| **导入方式** | 本地上传 / OSS 导入 / 日志回流 | 评测集不支持 OSS 导入；日志回流单次上限 10 万条，支持多次追加 |

## 使用方式

1. **创建数据集**：进入 [数据管理 > 数据集](https://bailian.console.aliyun.com/#/efm/model_data)，点击“新增数据集”，按向导填写名称、类型、场景、方法、存储位置及导入方式。
2. **导入数据**：
   - *本地上传*：直接上传符合格式要求的文件（如 SFT 的 `.jsonl`）；
   - *OSS 导入*：需提前为目标 Bucket 添加标签 `bailian-datahub-access=read`；
   - *日志回流*：需先在[模型监控](https://bailian.console.aliyun.com/#/model-telemetry)完成审计日志 + 推理日志授权，并确保 Region 为北京或新加坡 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
3. **数据处理（可选）**：仅对 SFT-文本生成训练集有效。在数据管理 > 数据流页签创建数据流任务，组合“数据清洗”与“数据增强”节点，系统自动生成新版本（如 V1 → V2），原数据集不受影响 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
4. **版本管理**：支持“继承模式”（增量修改）或“新建模式”（全量替换）；CPT 训练集强制“新建模式”。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据清洗/增强功能仅支持华北2（北京）；日志回流支持北京和新加坡，但生成的 DPO/CPT 训练集若用于训练，仍需在北京地域发起调优任务。
- **格式强约束**：SFT/DPO/CPT/评测集均有严格数据格式要求，务必下载对应模板并校验；数据处理仅接受 ChatML 格式的 SFT 文本训练集，其他格式（如纯 [prompt](prompt.md)-completion 对）将失败。
- **草稿与发布**：SFT/DPO 文本训练集支持草稿；CPT 和所有图生视频训练集**不支持草稿**，创建即发布；发布后版本不可编辑、不可删除，仅草稿版本可删。
- **数据继承限制**：CPT 训练集不支持数据继承，每次新增版本必须重新导入全部数据；日志回流生成的数据集支持追加（通过“导入数据”页或“新增版本”弹窗），但 OSS 挂载数据集不支持“新增版本”操作。
- **计费提示**：数据管理功能本身免费；平台 OSS 存储、OSS 挂载、SLS 日志服务分别按各自产品计费，请查阅最新计费文档。

> **注意**：文档 2 声明“数据处理目前仅支持处理[SFT-文本生成训练集]”，但未明确排除多模态 SFT；而文档 1 在“训练方法与场景”表格中列出“多模态理解”为合法训练场景。实际开发中，**多模态 SFT 训练集不可用于数据清洗/增强**，该能力仅限文本类 SFT。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


