# model data overview

百炼平台的模型数据管理功能为开发者提供统一的数据集创建、版本控制、清洗增强与回流能力，支撑模型调优（SFT/DPO/CPT）和评测全流程。数据集按用途分为训练集与评测集，支持多种导入方式与处理策略，所有操作均通过控制台完成，暂不开放 API 接口。核心能力聚焦于文本生成场景，[多模态](../concepts/multimodal.md)与图生视频支持有限且存在地域约束。

## 支持的模型/功能

- **训练集**：支持 SFT（监督微调）、DPO（直接偏好优化）、CPT（持续预训练）三种训练方法，对应文本生成、[多模态](../concepts/multimodal.md)理解、图生视频（首帧/首尾帧）四类训练场景；其中 DPO 和 CPT 仅限北京地域 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集**：仅支持文本生成场景，不可用于[多模态](../concepts/multimodal.md)或图生视频 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理**：仅支持 SFT-文本生成训练集（ChatML 格式），暂不支持 SFT-多模态理解、DPO 或 CPT 训练集的数据清洗与增强 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：支持生成训练集（SFT/DPO/CPT）和评测集（文本生成），当前仅在北京和新加坡 Region 可用；单次回流上限 10 万条，但可多次追加至同一数据集不同版本 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 2 明确指出数据处理“暂不支持[SFT-图片理解训练集](https://help.aliyun.com/zh/model-studio/model-training-overview#2f5553c6d832d)和[DPO-文本生成训练集](https://help.aliyun.com/zh/model-studio/model-training-overview#2f5553c6d832d)”，而文档 1 中“训练集支持4种训练场景”未限定处理能力范围，此处以文档 2 的明确限制为准。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **数据集名称** | 最长 50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3） | 创建后不可修改 |
| **数据集类型** | `训练集` 或 `评测集` | 创建后不可变更 |
| **训练场景** | 文本生成 / 多模态理解 / 图生视频（首帧） / 图生视频（首尾帧） | 评测集仅允许文本生成 |
| **训练方法** | SFT / DPO / CPT | DPO/CPT 仅北京可用；CPT 不支持草稿与数据继承 |
| **存储位置** | 平台 OSS 存储（免费）或云存储挂载（OSS 挂载） | 评测集不支持 OSS 挂载；OSS 挂载需额外授权角色 |
| **导入方式** | 本地上传 / OSS 导入 / 日志回流 | 评测集不支持 OSS 导入；日志回流需先开通审计日志与推理日志 |

## 使用方式

1. **创建数据集**：在 [数据管理 > 数据集](https://bailian.console.aliyun.com/#/efm/model_data) 页面点击「新增数据集」，依次填写名称、类型、场景、方法、存储位置、导入方式及发布配置（草稿/立即发布）。CPT 和图生视频训练集强制立即发布 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
2. **数据处理（清洗/增强）**：仅对 SFT-文本生成训练集有效。在「数据流」页签创建数据流（含开始→数据清洗→数据增强→结束节点），再通过「任务列表」选择目标训练集启动任务。处理结果自动生成新版本，原版本不受影响 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
3. **日志回流**：需先在「模型监控」页面完成审计日志与推理日志的开通及角色授权；然后通过模型监控页、详情页或数据管理页进入日志回流表单，配置时间范围（最近 30 天）、API Key、模型等参数后提交。平台存储模式下导入完成后自动发布 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据清洗/增强、日志回流功能均仅在北京（华北2）可用；日志回流额外支持新加坡 Region [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **格式与兼容性**：SFT 文本生成训练集必须使用 ChatML 格式（`.jsonl`）；多模态/图生视频训练集暂无官方推荐数据量，需自行评估 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **版本与编辑**：仅草稿版本可编辑、删除；已发布版本不可编辑，删除操作不可逆；CPT 训练集不支持数据继承，每次新增版本必须重新导入全部数据 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **日志回流限制**：单次最多回流 10 万条日志；预估数据量仅为近似值，实际条数可能略有差异；OSS 挂载数据集不支持「新增版本」操作，须通过「导入数据」页追加 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务将产生独立费用，请查阅百炼计费文档 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


