# model data overview

百炼平台的模型数据体系围绕训练集与评测集构建，提供从日志回流、本地/OSS 导入到数据清洗与增强的全链路数据处理能力。所有数据均以结构化 JSONL 格式存储，并支持版本管理、多训练方法适配及跨地域（北京/新加坡）部署。核心目标是为 SFT、DPO、CPT 等模型调优任务提供高质量、合规、可追溯的数据输入。

## 支持的模型/功能

- **训练集类型**：支持文本生成、[多模态](../concepts/multimodal.md)理解、图生视频（首帧/首尾帧）四类训练场景；评测集仅支持文本生成 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **训练方法**：SFT（监督微调）、DPO（直接偏好优化）、CPT（持续预训练），其中 DPO 和 CPT 仅限华北2（北京）地域 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据来源功能**：
  - **日志回流**：将 SLS 推理日志自动转化为结构化训练/评测集（JSONL），支持 SFT/DPO/CPT 训练集和文本生成评测集，当前仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
  - **数据处理（清洗与增强）**：仅支持 SFT-文本生成训练集（ChatML 格式），不支持 SFT-图片理解、DPO 或 CPT 训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

> **注意**：文档 1 明确指出数据处理“暂不支持[SFT-图片理解训练集]和[DPO-文本生成训练集]”，而文档 3 中“训练集与评测集”章节未限定数据处理适用范围，但其“导入方式”表格中将日志回流列为支持 DPO 训练集的导入方式。此处以文档 1 的明确限制为准——**DPO 训练集不可用于数据清洗或增强节点**，仅可用于日志回流生成和模型调优。

## 关键参数

| 参数类别 | 参数名 | 说明 | 约束 |
|----------|--------|------|------|
| **通用** | 数据集名称 | 最长 50 字符，支持中文、英文、数字、下划线、连字符、点 | 创建后不可修改 |
| | 数据集描述 | 最长 200 字符 | 可选 |
| **日志回流专用** | 时间范围 | 仅支持最近 30 天（含当天），精确到秒 | 修改后重置 API Key 与模型选择 |
| | 单次回流上限 | 10 万条日志 | 超出部分被截断，非总量限制 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md) |
| | API Key 过滤 | 支持「全部」「其他」或指定 Key（多选） | 「其他」包含已删除 Key 或跨工作空间日志 |
| **数据处理专用** | `dataSetCount` | 数据清洗/增强节点输出的 messages 数量，系统自动生成且不可更改 | 用于条件判断节点分支逻辑 |
| | 生成样本数（增强） | 数据增强节点中新增样本数量；原数据 + 新增 = 总输出量 | 每次最多生成 2000 条 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md) |

## 使用方式

- **创建数据集**：在[数据管理](https://bailian.console.aliyun.com/#/efm/model_data) > 数据集列表页点击「新增数据集」，依次配置类型（训练集/评测集）、场景、训练方法、存储位置、导入方式（本地上传/OSS 导入/日志回流）及发布选项（草稿/立即发布）。
- **日志回流**：需先在[模型监控](https://bailian.console.aliyun.com/#/model-telemetry)完成审计日志与推理日志的授权及开通（顺序不可逆），再通过任一入口（模型监控页、详情页、数据管理页）填写筛选参数并提交任务 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据清洗与增强**：仅限控制台操作，需先创建数据流（含开始→清洗/增强→结束节点），再基于该数据流创建数据流任务，指定待处理的 SFT-文本生成训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **API 调用**：目前**暂未提供可用的 API 进行数据处理**（如清洗/增强）；模型调优 API 可通过 `training_file_ids` 参数引用已发布的训练集 ID [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

## 限制和注意事项

- **地域限制**：数据处理（清洗/增强）仅适用于华北2（北京）；日志回流仅支持华北2（北京）和新加坡；DPO/CPT 训练方法、云存储挂载仅限北京地域 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **格式限制**：数据处理仅接受 ChatML 格式的 SFT-文本生成训练集（`.jsonl`），不支持其他格式或训练类型 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **版本与编辑**：CPT 和图生视频训练集不支持草稿状态，创建即发布；仅草稿版本可在线编辑内容，已发布版本不可编辑；删除操作不可逆 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **安全与合规**：若训练集含法律文件、医学记录、文学作品、方言汇总、用户评论、技术手册等敏感内容，**不建议使用数据清洗与增强功能**，应跳过相关操作 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **费用提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务分别产生对应账单费用 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 来源文档

- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)
- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)


