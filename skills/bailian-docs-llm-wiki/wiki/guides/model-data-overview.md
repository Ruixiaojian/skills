# model data overview

百炼平台的模型数据管理功能为大模型训练与评测提供统一的数据集生命周期支持，涵盖训练集（SFT/DPO/CPT/图生视频）和评测集的创建、导入、处理、版本管理及下游调用。所有数据集均需在业务空间内统一管理，其类型、场景与训练方法在创建时确定且不可变更。

## 支持的模型/功能

- **训练集类型**：支持文本生成、多模态理解、图生视频（首帧）、图生视频（首尾帧）四类训练场景；其中 DPO 和 CPT 仅限文本生成场景 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **评测集类型**：仅支持文本生成场景，不可用于多模态或图生视频评测。  
- **数据处理能力**：支持对 **SFT-文本生成训练集（ChatML 格式）** 进行数据清洗（如敏感信息打码、特殊内容移除）和数据增强（通用/分类/抽取/创作场景），暂不支持 SFT-多模态、DPO 或 CPT 训练集的数据处理 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
- **日志回流能力**：支持将 SLS 推理日志转化为结构化 JSONL 数据集，可用于 SFT/DPO/CPT 训练集或文本生成评测集，当前仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  

> **注意**：文档 2 明确指出“暂不支持[SFT-图片理解训练集]和[DPO-文本生成训练集]”，而文档 1 表格中列出“多模态理解”为训练场景，但未说明其是否支持数据处理；实际以文档 2 的限制为准——**多模态训练集不可用于数据清洗或增强**。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **数据集名称** | 最长 50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3） | 创建后不可修改 |
| **数据集类型** | `训练集` 或 `评测集`，创建后不可变更 | 必填 |
| **训练场景** | 文本生成 / 多模态理解 / 图生视频（首帧） / 图生视频（首尾帧）；评测集仅允许文本生成 | 必填 |
| **训练方法** | SFT / DPO / CPT；CPT 和图生视频训练集不支持草稿状态 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) | 必填，创建后锁定 |
| **存储位置** | `平台 OSS 存储`（免费，自动发布）或 `云存储挂载`（需额外授权，不支持评测集） | 创建后不可更改 |
| **导入方式** | 本地上传 / OSS 导入 / 日志回流；其中评测集不支持 OSS 导入 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) | 必填 |

## 使用方式

- **创建数据集**：通过控制台 **[数据管理 > 数据集 > 新增数据集](https://bailian.console.aliyun.com/#/efm/model_data)** 完成，按向导填写名称、类型、场景、方法、存储及导入方式。SFT/DPO 文本训练集支持草稿，CPT/图生视频必须立即发布。  
- **数据处理**：仅适用于已发布的 SFT-文本生成训练集（ChatML 格式）。在 **数据管理 > 数据流** 中创建清洗/增强任务，系统自动生成新版本（如 V1 → V2），原版本不受影响 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
- **日志回流**：需先在 **模型监控 > 开通审计日志与推理日志** 并完成角色授权；随后通过模型监控页、详情页或数据管理页入口配置时间范围、API Key、模型等参数发起回流任务。单次上限 10 万条，支持多次追加至同一数据集的不同版本 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
- **下游调用**：训练集 ID 通过 `training_file_ids` 参数传入模型调优 API；评测集 ID 用于模型评测 API。数据集 CRUD 当前仅支持控制台操作。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据清洗/增强、日志回流功能均**仅限华北2（北京）**；日志回流额外支持新加坡 Region [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
- **格式与兼容性**：  
  - 数据处理仅接受 ChatML 格式的 SFT-文本生成训练集，不支持其他格式或多模态数据 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)；  
  - 日志回流产出 JSONL 格式结构化数据，可直接用于微调或评测；  
  - CPT 训练集不支持数据继承，每次新增版本必须重新导入全部数据 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **操作不可逆性**：  
  - 发布后的数据集版本不可编辑；  
  - 删除操作不可恢复，仅草稿版本可删除；  
  - 数据集类型、训练场景、训练方法、存储位置、导入方式等关键字段创建后不可更改。  
- **容量与配额**：  
  - 单次日志回流上限 10 万条，但数据集总量无硬性上限，可通过多版本追加积累；  
  - 本地上传无单文件大小限制，OSS 导入需目标 Bucket 添加标签 `bailian-datahub-access=read`；  
  - 数据集创建数量无限制，导入数据量无上限（文档 1），但实际受 OSS 存储配额约束。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


