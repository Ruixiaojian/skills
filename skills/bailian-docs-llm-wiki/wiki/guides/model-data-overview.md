# model data overview

百炼平台的模型数据管理功能为大模型调优与评测提供统一的数据集生命周期支持，涵盖训练集（SFT/DPO/CPT/多模态/图生视频）和评测集的创建、导入、版本管理、清洗增强及日志回流。所有数据集均支持结构化格式校验与 OSS 加密存储，核心能力聚焦于开发者实际工作流中的数据准备效率与质量保障。

## 支持的模型/功能

- **训练集类型**：支持文本生成、多模态理解（图/视频→文本）、图生视频（首帧、首尾帧）四类训练场景；对应训练方法包括 SFT（监督微调）、DPO（直接偏好优化）、CPT（持续预训练）。其中 CPT 和图生视频训练集仅支持北京地域，且不支持草稿状态 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集类型**：仅支持文本生成场景，可用于模型泛化能力评估，不支持 OSS 导入和 OSS 挂载存储 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理功能**：支持对 **SFT-文本生成训练集（ChatML 格式）** 进行数据清洗（如敏感信息打码、URL 移除）和数据增强（通用/分类/抽取/创作场景），暂不支持 DPO、多模态或 CPT 训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：支持将 SLS 推理日志转化为结构化 JSONL 数据集，适用于训练集（SFT/DPO/CPT）和评测集（文本生成），当前在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 2 明确指出“数据处理暂不支持 SFT-图片理解训练集和 DPO-文本生成训练集”，而文档 1 中“训练方法与场景”表格未排除 DPO 的数据处理可能性，此处以文档 2 的明确限制为准。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **数据集名称** | 最长 50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3） | 创建后不可修改 |
| **数据集类型** | `训练集` 或 `评测集`，创建后不可变更 | 必填；评测集仅支持文本生成场景 |
| **训练场景** | 文本生成 / 多模态理解 / 图生视频（首帧）/ 图生视频（首尾帧） | 仅训练集需选；多模态/图生视频不支持草稿与数据继承 |
| **训练方法** | SFT / DPO / CPT | CPT 仅北京地域；DPO 仅北京地域；CPT 不支持草稿 |
| **存储位置** | `平台 OSS 存储`（免费，默认）或 `云存储挂载`（OSS 挂载） | 评测集不支持 OSS 挂载；OSS 挂载需额外授权角色 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md) |
| **导入方式** | 本地上传 / OSS 导入 / 日志回流 | 评测集不支持 OSS 导入；日志回流单次上限 10 万条，仅支持最近 30 天日志 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |

## 使用方式

- **创建数据集**：在控制台 **数据管理 > 数据集 > 新增数据集**，按向导填写名称、类型、场景、方法、存储位置及导入方式；SFT/DPO 文本生成支持草稿，CPT/图生视频必须立即发布。
- **数据处理（清洗/增强）**：仅限 SFT-文本生成训练集（ChatML 格式）。在 **数据管理 > 数据流** 创建自定义数据流（如先敏感信息打码、再通用增强），再通过 **任务列表 > 从数据流列表创建任务** 绑定目标训练集。处理结果自动保存为新版本，不覆盖原数据 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：需先在 **模型监控** 页面完成审计日志 + 推理日志双授权（顺序不可逆），再通过模型监控页、模型详情页或数据管理页入口配置时间范围、API Key、模型等参数。平台存储模式下导入完成后自动发布；OSS 挂载模式需手动发布，且不支持“新增版本”操作，须通过“导入数据”页追加 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 2 明确声明“阿里云百炼目前暂未提供可用的 API 进行数据处理”，而文档 1 提到“模型调优 API 可通过 `training_file_ids` 参数引用已发布的训练集 ID”。二者无冲突——前者指数据处理本身无 API，后者指下游调优可编程引用数据集 ID。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据清洗/增强、日志回流（部分功能）均仅限华北2（北京）；日志回流额外支持新加坡 Region [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **格式与兼容性**：数据处理仅接受 ChatML 格式的 SFT-文本生成训练集；多模态、DPO、CPT 训练集无法使用该功能 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。各场景数据格式模板请严格参照 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) 中的“数据格式与模板”章节。
- **不可逆操作**：数据集发布后不可编辑；删除已发布版本或整个数据集均不可恢复；日志回流任务失败后需排查原因并重试，不支持手动终止 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **容量与配额**：单次日志回流上限 10 万条（可多次追加）；OSS 导入需 Bucket 添加 `bailian-datahub-access=read` 标签；CPT 训练建议数据量 ≥5000 万 Token；SFT 建议 ≥1000 条样本 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务分别产生独立费用，详见百炼计费页面。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


