# model data overview

百炼平台的模型数据管理功能为大模型训练与评测提供统一、可版本化、可追溯的数据基础设施。它覆盖从数据集创建、导入、清洗增强到下游调优/评测的全生命周期，支持文本生成、[多模态](../concepts/multi-modal.md)理解、图生视频等多种场景。所有数据集均按用途严格区分训练集与评测集，且类型不可变更，需在创建时审慎选择。

## 支持的模型/功能

- **训练集**：支持 SFT（监督微调）、DPO（直接偏好优化）、CPT（持续预训练）三类训练方法，对应文本生成、[多模态](../concepts/multi-modal.md)理解、图生视频（首帧/首尾帧）四类训练场景。其中 CPT 和图生视频训练集仅限北京地域，且不支持草稿状态 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集**：仅支持文本生成场景，用于模型效果客观评估，不可用于训练。
- **日志回流**：将 SLS 推理日志自动转化为结构化训练集或评测集（JSONL 格式），支持 SFT/DPO/CPT 文本生成训练及文本生成评测，当前在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据处理**：仅支持 SFT-文本生成训练集（ChatML 格式）的清洗与增强，暂不支持 DPO、CPT、[多模态](../concepts/multi-modal.md)或图生视频训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

> **注意**：文档 1 称“DPO/CPT 训练方法、云存储挂载仅支持北京地域”，而文档 2 明确日志回流在“北京和新加坡”均可用。经核实，日志回流作为独立功能，其地域支持范围（北京+新加坡）与底层训练方法部署地域（仅北京支持 DPO/CPT 训练任务）不冲突；但若使用日志回流创建 DPO/CPT 训练集，该数据集仍只能在北京地域发起训练任务。此为功能分层设计，非矛盾。

## 关键参数

| 参数 | 说明 | 必填 | 取值约束 |
|------|------|------|-----------|
| 数据集名称 | 唯一标识符 | 是 | ≤50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 2） |
| 数据集类型 | 决定用途与下游能力 | 是 | `训练集` 或 `评测集`（创建后不可变更） |
| 训练场景 | 数据适用的模型输入输出模式 | 是 | `文本生成` / `多模态理解` / `图生视频(首帧)` / `图生视频(首尾帧)`（评测集仅允许 `文本生成`） |
| 训练方法 | 仅训练集填写 | 是 | `SFT`（全站点）、`DPO`（北京）、`CPT`（北京） |
| 存储位置 | 数据物理存放方式 | 是 | `平台 OSS 存储`（免费，自动加密）或 `云存储挂载`（需 OSS 标签 `bailian-datahub-access=read`，仅训练集支持） |
| 导入方式 | 数据来源路径 | 是 | `本地上传`（小批量）、`OSS 导入`（大批量，仅训练集）、`日志回流`（SLS 日志，支持训练集/评测集） |
| 发布配置 | 版本生命周期控制 | 是 | `草稿`（可编辑）或 `立即发布`（不可逆）；CPT 与图生视频训练集强制 `立即发布` |

## 使用方式

1. **创建数据集**：进入 [数据管理 > 数据集](https://bailian.console.aliyun.com/#/efm/model_data)，点击“新增数据集”，按顺序填写上述关键参数，选择导入方式并提交。
2. **导入数据**：
   - *本地上传*：直接拖拽文件，SFT/DPO 文本生成支持多文件。
   - *OSS 导入*：目标 Bucket 需预先添加标签 `bailian-datahub-access=read`。
   - *日志回流*：需先完成审计日志与推理日志授权（文档 2），再在表单中配置时间范围、API Key、模型等筛选条件；单次上限 10 万条，可多次追加至不同版本 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
3. **数据处理（可选）**：对 SFT-文本生成训练集（草稿或已发布版本），在数据集详情页进入“数据处理”，通过预置模板或自定义数据流执行清洗（如敏感信息打码）与增强（如 Few-Shot 生成），结果自动生成新版本 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
4. **版本管理**：同一数据集可创建多版本，支持“继承模式”（增量修改）或“新建模式”（全量替换）；CPT 训练集不支持继承，每次必须新建 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练任务、云存储挂载、数据清洗/增强功能仅在北京地域可用；日志回流功能在北京和新加坡可用。
- **不可变性**：数据集类型、训练场景、训练方法、存储位置创建后不可更改；发布操作不可逆，已发布版本不可编辑；删除操作不可恢复。
- **容量与配额**：数据集数量无上限，单次日志回流上限 10 万条（但数据集总量无上限，可多批次追加）；CPT 训练建议 ≥5000 万 [Token](../concepts/token.md)；SFT 建议 ≥1000 条；DPO 建议 ≥100 条。
- **格式强约束**：各场景有严格数据格式要求（如 SFT 文本需 ChatML JSONL），务必下载对应模板准备数据，否则导入失败。
- **安全与合规**：所有导入数据默认启用 OSS 服务端加密（SSE-OSS）；敏感信息打码等清洗算子需主动启用，法律/医疗等高敏数据不建议使用自动化处理 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务等下游资源按各自产品计费。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)


