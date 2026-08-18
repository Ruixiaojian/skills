# model data overview

百炼平台的模型数据管理功能为大模型训练与评测提供统一的数据集生命周期支持，涵盖训练集（SFT/DPO/CPT/多模态/图生视频）和评测集的创建、导入、版本管理、清洗增强及下游调用。所有数据集均支持平台 OSS 存储（免费）或云存储挂载（仅北京地域），但类型与训练方法一经选定不可变更。数据质量直接影响调优效果，建议在发布前通过数据处理功能进行清洗与增强。

## 支持的模型/功能

- **训练集类型**：支持 SFT（监督微调）、DPO（直接偏好优化）、CPT（持续预训练）三类训练方法，对应文本生成、多模态理解、图生视频（首帧/首尾帧）四类场景；其中 DPO 和 CPT 仅限北京地域使用 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集类型**：仅支持文本生成场景，不可用于多模态或图生视频评测，且不支持 OSS 导入 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理功能**：支持对 **SFT-文本生成训练集（ChatML 格式）** 进行清洗（如敏感信息打码、特殊内容移除）和增强（如 Few-Shot 生成），暂不支持 DPO、CPT、多模态训练集的数据处理 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- > **注意**：文档 1 称“SFT 和 DPO 文本生成训练集支持草稿状态”，而文档 2 明确指出“数据处理仅支持 SFT-文本生成训练集，暂不支持 DPO-文本生成训练集”。二者无实质矛盾，但需注意 DPO 训练集虽可存为草稿，却无法参与数据清洗/增强流程。

## 关键参数

| 参数名 | 说明 | 是否必填 | 取值范围/约束 |
|--------|------|----------|----------------|
| 数据集名称 | 数据集唯一标识 | 是 | ≤50 字符，支持中文、英文、数字、下划线、连字符、点 |
| 数据集类型 | 训练集 或 评测集 | 是 | 创建后不可变更 |
| 训练场景 | 文本生成 / 多模态理解 / 图生视频（首帧） / 图生视频（首尾帧） | 是 | 评测集仅允许“文本生成” |
| 训练方法 | SFT / DPO / CPT | 是 | CPT 和图生视频训练集不支持草稿状态 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |
| 存储位置 | 平台 OSS 存储（免费） / 云存储挂载 | 是 | 评测集不支持云存储挂载；云存储挂载仅限北京地域 |
| 导入方式 | 本地上传 / OSS 导入 / 日志回流 | 是 | OSS 导入需 Bucket 标签 `bailian-datahub-access=read`；日志回流仅支持最近 30 天、单次 ≤10 万条 |

> **注意**：文档 1 表格中“草稿支持”列为“支持”对应 SFT/DPO 文本生成，但文档 2 强调“数据处理仅支持 SFT-文本生成训练集”，隐含 DPO 训练集虽可存草稿，但无法进入数据处理流水线——该限制未在文档 1 中体现，属功能边界差异，开发者需以文档 2 为准。

## 使用方式

- **创建数据集**：在控制台 **[数据管理](https://bailian.console.aliyun.com/#/efm/model_data)** > **数据集** 页面点击“新增数据集”，按向导填写参数并选择导入方式（本地上传/OSS 导入/日志回流）；SFT/DPO 文本生成支持多文件上传，CPT/图生视频必须立即发布。
- **数据处理（清洗/增强）**：仅限北京地域，且仅支持已发布的 SFT-文本生成训练集（ChatML 格式）。需先在 **数据流** 页签创建数据流（含开始→数据清洗→数据增强→结束节点），再通过 **任务列表** > **从数据流列表创建任务** 绑定目标训练集启动任务；处理完成后自动生成新版本（如 V1 → V2），原版本不受影响 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **下游调用**：训练集发布后，其 ID 可通过 `training_file_ids` 参数传入模型调优 API；评测集发布后可用于模型评测 API；草稿版本仅支持数据处理，不可用于训练或评测。

## 限制和注意事项

- **地域限制**：DPO、CPT、云存储挂载、数据处理功能均**仅限北京地域**；其他站点仅支持 SFT 文本生成训练集 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **格式与兼容性**：数据处理严格要求 SFT-文本生成训练集为 ChatML 格式（`.jsonl`），不支持其他格式或场景；多模态、图生视频、DPO、CPT 训练集均不可用于数据处理 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **操作不可逆**：数据集发布后不可编辑；已发布版本删除操作不可恢复；草稿版本可删除，但删除整个数据集将移除其所有版本，请谨慎操作。
- **数据量建议**：
  - SFT：建议 ≥1000 条样本；
  - DPO：建议 ≥100 条偏好对；
  - CPT：建议 ≥5000 万 Token；
  - 评测集：应独立于训练集，避免数据泄露。
- **安全与合规**：所有导入数据默认启用 OSS 服务端加密（SSE-OSS，AES256）；敏感信息打码等清洗算子需在数据处理中显式启用，非自动生效。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)


