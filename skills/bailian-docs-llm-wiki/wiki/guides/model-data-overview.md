# model data overview

百炼平台的模型数据管理功能为开发者提供统一的数据集创建、处理与生命周期管理能力，支撑模型调优（SFT/DPO/CPT）、评测及数据增强等核心场景。所有数据集均按用途严格区分训练集与评测集，支持多版本迭代与多种导入方式，但关键能力（如DPO/CPT、日志回流、数据清洗）存在地域与格式限制，需按规范配置。

## 支持的模型/功能

- **训练集**：支持文本生成、[多模态](../concepts/multi-modal.md)理解、图生视频（首帧/首尾帧）四类训练场景；训练方法覆盖 SFT（监督微调）、DPO（直接偏好优化）和 CPT（持续预训练）[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **评测集**：仅支持文本生成场景，用于模型泛化能力评估，不可用于训练 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **数据处理**：仅支持 SFT-文本生成训练集（ChatML 格式），暂不支持 SFT-[多模态](../concepts/multi-modal.md)、DPO 或 CPT 训练集的数据清洗与增强 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
- **日志回流**：支持将 SLS 推理日志转化为结构化训练集（SFT/DPO/CPT）或评测集（文本生成），当前仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  

> **注意**：文档 1 称 DPO/CPT 仅支持北京地域，而文档 3 明确日志回流在“北京和新加坡”均可用。实际以文档 3 为准——DPO/CPT 训练集本身仍限北京，但日志回流作为其数据来源可在新加坡触发，回流后的数据集仍需在北京地域执行训练任务。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **数据集名称** | 最长 50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3） | 创建后不可修改 |
| **数据集类型** | 必选：`训练集` 或 `评测集`；创建后不可变更 | 评测集不支持 OSS 挂载、图生视频场景及 DPO/CPT 方法 |
| **训练场景 & 方法** | 文本生成 + SFT/DPO/CPT；[多模态](../concepts/multi-modal.md)理解仅支持 SFT；图生视频仅支持 SFT 且不支持草稿 | CPT 和图生视频训练集不支持草稿状态 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |
| **存储位置** | `平台 OSS 存储`（免费，自动发布）或 `OSS 挂载`（需额外授权，不支持评测集） | OSS 挂载数据集不支持“新增版本”，仅可通过“导入数据”追加 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md) |
| **导入方式** | 本地上传（小批量）、OSS 导入（大批量，需 Bucket 标签 `bailian-datahub-access=read`）、日志回流（需 SLS 授权） | 评测集不支持 OSS 导入；日志回流单次上限 10 万条，仅支持最近 30 天日志 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |

## 使用方式

- **创建数据集**：在控制台 **数据管理 > 数据集 > 新增数据集**，依次填写名称/描述 → 选择类型/场景/方法 → 指定存储位置 → 选择导入方式并上传/配置数据 → 设置发布选项（草稿或立即发布）。CPT 和图生视频训练集强制立即发布。  
- **数据处理（清洗/增强）**：仅适用于 SFT-文本生成训练集（ChatML 格式）。通过 **数据管理 > 数据流** 创建自定义数据流（如先敏感信息打码再数据增强），再基于该数据流启动任务，系统自动生成新版本 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
- **日志回流**：需先在 **模型监控** 页面完成审计日志 + 推理日志开通及角色授权（北京/新加坡 Region），再通过模型监控页、详情页或数据管理页入口配置时间范围、API Key、模型等参数创建任务 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
- **版本管理**：支持“继承模式”（增量修改）和“新建模式”（全量替换）；CPT 训练集不支持继承，每次新增版本必须重新导入全部数据 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据清洗/增强、日志回流功能均仅在华北2（北京）可用（文档 2 明确标注“仅适用于北京”，文档 3 扩展至新加坡，但训练任务执行仍需北京）；OSS 挂载也仅限北京。  
- **格式与兼容性**：数据处理仅接受 ChatML 格式 SFT 文本训练集；多模态、DPO、CPT 训练集无法使用数据清洗/增强功能 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
- **不可逆操作**：数据集发布后不可编辑；已发布版本删除不可恢复；OSS 挂载数据集不支持“新增版本”，追加数据必须走“导入数据”流程 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **计费提示**：数据管理功能免费，但存储（平台 OSS 或用户 OSS）、SLS 日志服务、模型调用等下游资源按各自产品计费 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **安全与合规**：所有导入数据默认启用 OSS 服务端加密（SSE-OSS）；敏感信息打码等清洗算子需显式开启，不自动应用 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


