# model data overview

百炼平台的模型数据管理功能为大模型训练与评测提供统一的数据集生命周期支持，涵盖训练集（SFT/DPO/CPT）、评测集的创建、导入、版本管理及后处理。所有数据集均需在业务空间内显式创建并发布，方可用于下游调优或评测任务。数据集类型（训练/评测）和核心元信息（场景、方法、存储方式）在创建后不可变更。

## 支持的模型/功能

- **训练集**：支持文本生成、多模态理解、图生视频（首帧/首尾帧）四类训练场景；对应训练方法包括 SFT（监督微调）、DPO（直接偏好优化）和 CPT（持续预训练）。其中 SFT 和 DPO 文本生成训练集支持草稿状态，CPT 及所有图生视频训练集仅支持立即发布 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集**：仅支持文本生成场景，用于模型效果客观评估，不支持 OSS 导入和云存储挂载 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **日志回流**：将 SLS 推理日志结构化为 JSONL 数据集，支持训练集（SFT/DPO/CPT）和评测集（文本生成），当前仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据清洗与增强**：仅支持 SFT-文本生成训练集（ChatML 格式），提供敏感信息打码、去重、毒性消除等清洗算子，以及基于千问-Max 的 Few-Shot 数据增强能力；该功能目前仅限北京地域 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

> **注意**：文档 1 称“DPO/CPT 训练方法、云存储挂载仅支持北京地域”，而文档 2 明确日志回流在**北京和新加坡**均可用。此处以文档 2 为准——日志回流支持双地域，但数据清洗/增强（文档 3）及 CPT/DPO 的完整训练流程仍仅限北京地域。

## 关键参数

| 参数 | 说明 | 是否必填 | 取值约束 |
|------|------|----------|----------|
| 数据集名称 | 唯一标识符 | 是 | ≤50 字符，支持中文、英文、数字、`_` `-` `.` `/` |
| 数据集类型 | 训练集 / 评测集 | 是 | 创建后不可变更 |
| 训练场景 | 文本生成 / 多模态理解 / 图生视频（首帧/首尾帧） | 是 | 评测集仅允许“文本生成” |
| 训练方法 | SFT / DPO / CPT | 是（训练集） | 评测集此项隐藏；CPT 不支持草稿与数据继承 |
| 存储位置 | 平台 OSS 存储（免费） / 云存储挂载（OSS） | 是 | 评测集不支持云存储挂载；日志回流中评测集禁用 OSS 挂载 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md) |
| 导入方式 | 本地上传 / OSS 导入 / 日志回流 | 是 | 评测集不支持 OSS 导入；日志回流单次上限 10 万条，可多次追加 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |

## 使用方式

1. **创建数据集**：进入 [数据管理 > 数据集](https://bailian.console.aliyun.com/#/efm/model_data)，点击“新增数据集”，按向导填写元信息并选择导入方式。
2. **导入数据**：
   - *本地上传*：适用于小批量数据，支持多文件上传（SFT/DPO 文本生成）；
   - *OSS 导入*：需提前为目标 Bucket 添加标签 `bailian-datahub-access=read`，仅训练集可用；
   - *日志回流*：需先完成审计日志与推理日志授权（含 SLS 角色），筛选时间范围（最近 30 天）、API Key 与模型后触发回流 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
3. **版本管理**：已发布数据集可通过“新增版本”迭代，支持“继承模式”（增量修改）或“新建模式”（全量替换）；CPT 训练集强制新建模式。
4. **数据后处理**：对草稿或已发布 SFT-文本生成训练集，可在 [数据管理 > 数据流](https://bailian.console.aliyun.com/?tab=model#/efm/model_data) 中创建清洗/增强任务，生成独立新版本（如 V1 → V2），原数据不受影响 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

## 限制和注意事项

- **地域限制**：CPT/DPO 训练、数据清洗与增强、云存储挂载功能仅在北京地域可用；日志回流扩展支持新加坡地域，但下游调优仍需在北京执行。
- **不可变性**：数据集类型、训练场景、训练方法、存储位置创建后不可修改；发布操作不可逆，已发布版本不可编辑或删除（仅草稿版本可删）。
- **容量与配额**：
  - 单次日志回流上限 10 万条，但数据集总量无硬限制（可多次回流至不同版本）；
  - OSS 导入无数据量上限，但需确保 Bucket 标签配置正确；
  - CPT 训练建议数据量 ≥ 5000 万 [Token](../concepts/token.md)，SFT 建议 ≥ 1000 条样本，DPO 建议 ≥ 100 条偏好对 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **格式强约束**：各训练场景有严格数据格式要求（如 SFT 文本需 ChatML JSONL），务必下载对应模板校验；多模态/图生视频暂无官方推荐数据量，需按实际场景准备充足样本。
- **计费提示**：数据管理功能本身免费，但存储（平台 OSS 或用户 OSS）、SLS 日志读写、模型调用（如数据增强）将产生独立费用，详见百炼计费文档。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)


