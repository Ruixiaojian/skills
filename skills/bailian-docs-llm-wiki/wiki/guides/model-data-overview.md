# model data overview

百炼平台的模型数据管理功能为大模型训练与评测提供统一的数据集生命周期支持，涵盖训练集（SFT/DPO/CPT/图生视频）和评测集的创建、导入、版本管理、清洗增强及日志回流等核心能力。所有数据集均需在业务空间内统一管理，其类型、场景与训练方法在创建时即锁定，不可变更。

## 支持的模型/功能

- **训练集**：支持四类训练场景：文本生成、多模态理解、图生视频（首帧）、图生视频（首尾帧）；对应训练方法包括 SFT（监督微调）、DPO（直接偏好优化）和 CPT（持续预训练）。其中 CPT 和图生视频训练集仅限北京地域，且不支持草稿状态 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集**：仅支持文本生成场景，可用于模型泛化能力评估，不支持 OSS 导入和 OSS 挂载存储 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理**：支持对 SFT-文本生成训练集（ChatML 格式）进行数据清洗（如敏感信息打码、特殊内容移除）和数据增强（通用/分类/抽取/创作场景），当前仅限华北2（北京）地域 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：将 SLS 推理日志自动转化为结构化 JSONL 数据集，支持训练集（SFT/DPO/CPT）和评测集，目前可用区域为华北2（北京）和新加坡 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 2 明确指出数据处理“暂不支持 SFT-图片理解训练集和 DPO-文本生成训练集”，而文档 1 中“数据处理”章节未限定适用范围，存在表述冲突。以文档 2 的明确限制为准。

## 关键参数

| 参数 | 说明 | 必填 | 取值约束 |
|------|------|------|----------|
| 数据集名称 | 唯一标识符 | 是 | ≤50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）；斜杠也允许（文档 3） |
| 数据集类型 | 训练集 / 评测集 | 是 | 创建后不可变更 |
| 训练场景 | 文本生成 / 多模态理解 / 图生视频（首帧/首尾帧） | 是 | 评测集仅支持文本生成 |
| 训练方法 | SFT / DPO / CPT | 是 | CPT 和图生视频训练集不支持草稿 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |
| 存储位置 | 平台 OSS 存储 / 云存储挂载 | 是 | 评测集禁用云存储挂载；OSS 挂载需额外授权角色 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md) |
| 导入方式 | 本地上传 / OSS 导入 / 日志回流 | 是 | 评测集不支持 OSS 导入；日志回流单次上限 10 万条，仅支持最近 30 天日志 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |

## 使用方式

- **创建数据集**：通过控制台「数据管理」>「数据集」>「新增数据集」完成，按向导填写名称、类型、场景、方法、存储及导入方式。SFT/DPO 文本生成支持多文件本地上传；OSS 导入需目标 Bucket 添加 `bailian-datahub-access=read` 标签；日志回流需先完成 SLS 审计日志与推理日志授权 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理**：仅支持草稿状态的 SFT-文本生成训练集。在「数据管理」>「数据流」中创建数据流任务，组合清洗（如敏感信息打码）与增强（如 Few-Shot 生成）节点，执行后自动生成新版本，原版本不受影响 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：入口包括「模型监控」列表页、「模型监控」详情页及「数据管理」新建数据集页。配置时间范围（最近 30 天）、API Key、模型等筛选条件后提交，平台存储模式下导入完成即自动发布 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **版本管理**：同一数据集可创建多个版本，支持「继承模式」（增量修改）或「新建模式」（全量替换）。CPT 训练集不支持继承，每次新增版本均需重新导入全部数据 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据处理、日志回流（部分功能）均仅限华北2（北京）；日志回流另支持新加坡 Region [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)；[日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **不可逆操作**：数据集发布后不可编辑；已发布版本删除不可恢复；评测集不支持 OSS 导入和挂载 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **格式与兼容性**：SFT-文本生成训练集必须为 ChatML 格式（`.jsonl`）；多模态/图生视频训练集暂无官方推荐数据量；日志回流产出为 JSONL，可直用于下游调优或评测 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)；[数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **容量与配额**：单次日志回流上限 10 万条，但数据集总量无硬限制，可通过多次回流至不同版本累积；OSS 导入无数据量上限；平台 OSS 存储免费，但产生实际存储费用 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)；[日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **安全与合规**：所有导入数据默认启用 OSS 服务端加密（SSE-OSS）；敏感信息打码等清洗算子需显式开启；法律/医疗等高敏数据不建议使用自动化清洗增强 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


