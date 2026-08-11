# model data overview

百炼平台的模型数据体系围绕训练集与评测集构建，提供从日志回流、本地/OSS 导入到数据清洗增强的全链路数据管理能力。所有数据集均以结构化 JSONL（或特定场景格式）存储，支持版本化管理，并直接对接模型调优与评测任务。数据处理流程强调质量优先，推荐在发布前对训练集进行清洗与增强。

## 支持的模型/功能

- **数据集类型**：明确分为**训练集**（用于 SFT/DPO/CPT 模型调优）和**评测集**（用于模型效果评估），创建后类型不可变更 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **训练场景支持**：训练集支持文本生成、[多模态](../concepts/multi-modal.md)理解、图生视频（首帧/首尾帧）；评测集**仅支持文本生成场景** [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **核心数据功能**：
  - **日志回流**：将 SLS 推理日志自动转化为结构化训练/评测数据集（JSONL），形成“推理→数据→微调”闭环 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
  - **数据清洗与增强**：仅支持华北2（北京）地域，且**当前仅适用于 SFT-文本生成训练集（ChatML 格式）**，不支持 DPO、CPT 或[多模态](../concepts/multi-modal.md)训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

> **注意**：文档2称“DPO/CPT 训练方法、云存储挂载仅支持北京地域”，而文档1明确日志回流在**华北2（北京）和新加坡**均可用。此处存在地域支持范围矛盾——日志回流功能实际支持新加坡，但 DPO/CPT 训练本身仅限北京。开发者需按具体功能（非数据集类型）确认地域限制。

## 关键参数

| 参数 | 说明 | 约束与取值 |
|------|------|------------|
| **数据集名称** | 唯一标识符 | 最长50字符，支持中文、英文、数字、下划线、连字符、点（文档2）或斜杠（文档1）；建议采用 `功能_模型_时间` 格式命名 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md) |
| **数据集类型** | 训练集 or 评测集 | 创建后不可变更；评测集不支持 OSS 挂载、OSS 导入及图生视频等场景 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |
| **训练方式** | SFT / DPO / CPT | SFT 推荐数据量 ≥1000 条；DPO ≥100 条；CPT 要求 ≥5000 万 [Token](../concepts/token.md)；CPT 和图生视频训练集**不支持草稿状态**，创建即发布 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |
| **时间范围（日志回流）** | 日志筛选窗口 | 仅支持**最近30天内**（含当天），精确到秒；修改将重置 API Key 与模型选择 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md) |
| **单次回流上限** | 日志提取条数 | **10 万条**（硬性上限），超出部分被截断；此为单次任务限制，非数据集总量限制 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md) |

## 使用方式

- **创建数据集**：在控制台 **数据管理 > 数据集 > 新增数据集** 页面完成。必填字段包括名称、类型、训练场景、训练方式、存储位置（平台 OSS 存储 / 云存储挂载）及导入方式（本地上传 / OSS 导入 / 日志回流）。
- **日志回流专用路径**：除通用入口外，还可从 **模型监控列表页顶部按钮**、**模型监控详情页时间选择器旁按钮** 或 **数据管理页新建时选择“日志回流”导入方式** 进入配置表单 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据处理（清洗/增强）**：仅支持已发布的 SFT-文本生成训练集。在 **数据管理 > 数据流** 中创建数据流（含清洗/增强节点），再通过 **任务列表 > 从数据流列表创建任务** 绑定目标训练集。处理完成后自动生成新版本，**不覆盖原版本** [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **版本管理**：支持“继承模式”（基于上一版本增量修改）和“新建模式”（全量替换）。CPT 训练集**不支持数据继承**，每次新增版本必须新建 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 限制和注意事项

- **地域限制**：
  - 日志回流：仅华北2（北京）、新加坡可用；其他 Region 不显示入口 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
  - 数据清洗/增强：**仅华北2（北京）地域可用** [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
  - DPO/CPT 训练：仅北京地域支持（文档2），与日志回流地域不完全重合，需注意组合使用场景。
- **存储与授权**：
  - OSS 挂载模式需额外授权 `AliyunServiceRoleForAccessCusOss` 和 `AliyunServiceRoleForSFMDataHubOSSImport` 角色，且评测集**禁用**该模式 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
  - OSS 导入要求目标 Bucket 添加标签 `bailian-datahub-access=read` [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **功能兼容性**：
  - 评测集**不支持** OSS 导入、OSS 挂载、数据清洗与增强 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)；[数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
  - 数据清洗/增强**仅支持 SFT-文本生成训练集（ChatML 格式）**，明确不支持 SFT-图片理解、DPO、CPT 及非 ChatML 格式 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **操作风险**：
  - 发布与删除操作**不可逆**；已发布版本不可编辑，仅草稿版本可删除 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
  - 关闭审计日志或推理日志后，**已有日志数据不可复原**；推理日志开启后将持续产生 SLS 存储与读写费用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 来源文档

- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)
- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)


