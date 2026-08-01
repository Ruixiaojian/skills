# model data overview

百炼平台的模型数据管理功能为开发者提供统一的数据集创建、版本控制与处理能力，支撑模型调优（SFT/DPO/CPT）、评测及数据增强等核心场景。数据集分为训练集与评测集两类，支持多种导入方式与结构化处理流程，所有操作均通过控制台完成，API 仅支持引用已发布数据集 ID。数据存储默认使用平台 OSS，亦可挂载用户自有 OSS Bucket。

## 支持的模型/功能

- **训练集**：支持文本生成、多模态理解、图生视频（首帧/首尾帧）四类训练场景；对应训练方法包括 SFT（监督微调）、DPO（直接偏好优化）和 CPT（持续预训练）。其中 SFT 和 DPO 文本生成训练集支持草稿状态，CPT 及图生视频训练集创建即发布。
- **评测集**：仅支持文本生成场景，用于模型泛化能力评估，不可用于训练。
- **数据处理**：仅支持 SFT-文本生成训练集（ChatML 格式），提供数据清洗（如敏感信息打码、特殊内容移除）与数据增强（通用/分类/抽取/创作四类场景）能力；不支持 DPO 或多模态训练集处理 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：将 SLS 推理日志转化为结构化 JSONL 数据集，支持训练集（SFT/DPO/CPT）与评测集（文本生成），当前仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档1称“DPO/CPT 训练方法、云存储挂载仅支持北京地域”，而文档2明确日志回流在**北京和新加坡**均可用。此处以文档2为准，新加坡 Region 同样支持日志回流创建 DPO/CPT 训练集。

## 关键参数

| 参数 | 说明 | 是否必填 | 取值范围/约束 |
|------|------|----------|----------------|
| 数据集名称 | 唯一标识符 | 是 | ≤50 字符，支持中文、英文、数字、下划线、连字符、点（文档1）或斜杠（文档2） |
| 数据集类型 | 训练集 / 评测集 | 是 | 创建后不可变更 |
| 训练场景 | 文本生成 / 多模态理解 / 图生视频（首帧/首尾帧） | 是 | 评测集仅允许“文本生成” |
| 训练方法 | SFT / DPO / CPT | 是 | 仅训练集显示；CPT 不支持草稿与数据继承 |
| 存储位置 | 平台 OSS 存储 / 云存储挂载（OSS 挂载） | 是 | 评测集不支持 OSS 挂载；OSS 挂载需提前添加 Bucket 标签 `bailian-datahub-access=read` [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |
| 导入方式 | 本地上传 / OSS 导入 / 日志回流 | 是 | 评测集不支持 OSS 导入；日志回流单次上限 10 万条，支持多次追加至不同版本 |

## 使用方式

1. **创建数据集**：进入 [数据管理 > 数据集](https://bailian.console.aliyun.com/#/efm/model_data)，点击“新增数据集”，按向导填写参数并选择导入方式。
2. **导入数据**：
   - *本地上传*：直接上传符合格式要求的文件（如 SFT 的 JSONL），支持多文件。
   - *OSS 导入*：需目标 Bucket 已配置标签 `bailian-datahub-access=read`，适用于大批量数据。
   - *日志回流*：需先完成 SLS 审计日志与推理日志授权（含服务关联角色），筛选时间范围（最近30天）、API Key 与模型后触发回流 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
3. **版本管理**：已发布数据集可通过“新增版本”迭代，支持“继承模式”（增量修改）或“新建模式”（全量替换）；CPT 训练集强制新建模式。
4. **数据处理**：仅对 SFT-文本生成训练集（草稿或已发布版本）生效，在“数据流”页签创建清洗/增强任务，输出为独立新版本，原数据集不受影响。

## 限制和注意事项

- **地域限制**：CPT 和图生视频训练集、云存储挂载功能仅限北京地域；数据清洗与增强功能也仅限北京地域 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **不可逆操作**：数据集发布后不可编辑；删除操作不可恢复，仅草稿版本可删除。
- **格式与兼容性**：
  - SFT 文本生成训练集必须为 ChatML 格式 JSONL；DPO/CPT/评测集格式要求详见[调优数据上传规则](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules)。
  - 数据处理不支持非 ChatML 格式，也不支持 DPO、多模态或 CPT 训练集。
- **日志回流限制**：
  - 单次任务最多回流 10 万条日志（非总量限制），可分批追加至不同版本。
  - 预估数据量为近似值，实际结果可能存在偏差。
  - OSS 挂载数据集不支持“新增版本”，只能通过“导入数据”页追加。
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务等下游资源按各自产品计费。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)


