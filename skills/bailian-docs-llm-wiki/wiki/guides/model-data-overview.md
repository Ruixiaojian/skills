# model data overview

百炼平台的模型数据管理功能为大模型训练与评测提供统一的数据集生命周期支持，涵盖训练集（SFT/DPO/CPT/[多模态](../concepts/multi-modal.md)/图生视频）和评测集的创建、导入、版本管理与处理。所有数据集均通过控制台统一管理，支持本地上传、OSS 导入和日志回流三种导入方式，并可选平台 OSS 存储或云存储挂载。数据质量直接影响调优效果，建议在训练前结合[数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)提升数据规范性与多样性。

## 支持的模型/功能

- **训练集类型**：支持文本生成、[多模态](../concepts/multi-modal.md)理解（图/视频→文本）、图生视频（首帧/首尾帧）四类场景；其中 SFT、DPO、CPT 仅适用于文本生成场景，[多模态](../concepts/multi-modal.md)与图生视频暂不支持 DPO/CPT [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集类型**：仅支持文本生成场景，不可用于多模态或图生视频评测。
- **数据处理能力**：仅支持 SFT-文本生成训练集（ChatML 格式）的数据清洗与增强，暂不支持 DPO 训练集、多模态训练集及 CPT 训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流产出**：支持生成训练集（SFT/DPO/CPT）和评测集（文本生成），但仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档1称“DPO/CPT 训练方法、云存储挂载仅支持北京地域”，而文档2明确日志回流在**北京和新加坡**均可用。此处以文档2为准，新加坡 Region 同样支持日志回流创建 DPO/CPT 训练集；但其他训练方式（如本地上传/非日志回流方式创建的 DPO/CPT）仍仅限北京地域，文档1未提及新加坡支持，属信息缺失而非矛盾。

## 关键参数

| 参数 | 说明 | 是否必填 | 取值约束 |
|------|------|----------|----------|
| 数据集名称 | 唯一标识符 | 是 | ≤50 字符，支持中文、英文、数字、下划线、连字符、点（文档1）或斜杠（文档2）；建议按 `功能_模型_时间` 命名（文档2） |
| 数据集类型 | 训练集 / 评测集 | 是 | 创建后不可变更 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |
| 训练场景 | 文本生成 / 多模态理解 / 图生视频（首帧/首尾帧） | 是 | 评测集仅允许“文本生成” |
| 训练方法 | SFT / DPO / CPT | 是（训练集） | CPT 和图生视频训练集不支持草稿状态，创建时只能立即发布 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |
| 存储位置 | 平台 OSS 存储 / 云存储挂载 | 是 | 评测集不支持云存储挂载；OSS 挂载需额外授权角色（文档2） |
| 导入方式 | 本地上传 / OSS 导入 / 日志回流 | 是 | 评测集不支持 OSS 导入；日志回流仅支持最近 30 天日志且单次上限 10 万条 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |

## 使用方式

- **创建流程**：进入「数据管理」>「数据集」>「新增数据集」，依次填写名称/描述 → 选择类型/场景/方法 → 选择存储位置 → 选择并配置导入方式（各方式字段独立）→ 设置发布选项（草稿/立即发布）→ 提交。
- **日志回流专用入口**：除「数据管理」新建外，还可在「模型监控」列表页或详情页直接触发，表单自动预填时间范围、API Key 和模型（文档2）。
- **数据处理**：仅支持对已发布的 SFT-文本生成训练集（ChatML 格式）发起数据流任务，在「数据管理」>「数据流」中搭建清洗/增强节点链路，任务完成后自动生成新版本（V2、V3…），原版本保留 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **版本管理**：同一数据集可创建多版本，支持「继承模式」（增量修改）或「新建模式」（全量替换）；CPT 训练集不支持继承，每次必须新建数据（文档1）。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练集、云存储挂载、数据清洗/增强功能仅限华北2（北京）；日志回流扩展支持新加坡 Region（见上文注意项）。
- **格式与内容限制**：
  - 不支持空数据集创建或发布；
  - 多模态/图生视频训练集无官方推荐数据量，需自行保障样本充足；
  - 数据清洗/增强仅接受 ChatML 格式 SFT 文本训练集，不兼容 DPO、CPT 或多模态数据 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **操作不可逆性**：
  - 发布后的版本不可编辑；
  - 删除已发布版本或整个数据集均不可恢复；
  - 草稿版本可删除，但需谨慎操作（文档1）。
- **日志回流特殊约束**：
  - 必须先开通审计日志，再开通推理日志，关闭顺序相反；
  - 预估数据量仅为近似值，实际回流条数可能略有差异；
  - OSS 挂载数据集不支持「新增版本」，追加数据需通过「导入数据」页操作（文档2）。
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务等下游资源按各自产品计费（文档1）。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)


