# model data overview

百炼平台的模型数据体系围绕训练集与评测集的全生命周期管理构建，覆盖数据准备、导入、处理、版本控制及下游调用。核心能力包括结构化数据集创建（支持 SFT/DPO/CPT 等多种训练方法）、基于日志回流的自动化数据采集，以及面向 SFT 文本生成场景的数据清洗与增强功能。所有操作均通过控制台完成，暂不提供 API 接口。

## 支持的模型/功能

- **训练集类型**：支持 SFT（监督微调）、DPO（直接偏好优化）、CPT（持续预训练）三类训练方法，对应文本生成、多模态理解、图生视频（首帧/首尾帧）四种训练场景；其中 SFT 和 DPO 文本生成训练集支持草稿状态，CPT 及图生视频训练集仅支持立即发布 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集类型**：仅支持文本生成场景，可用于模型评测 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理功能**：仅支持 SFT-文本生成训练集（ChatML 格式），暂不支持 SFT-图片理解训练集、DPO 训练集或 CPT 训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流支持**：可将 SLS 推理日志转化为结构化训练集（SFT/DPO/CPT）或评测集（仅文本生成），当前仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 1 明确声明“本文档仅适用于华北2（北京）地域”，而文档 3 指出日志回流“目前仅在华北2（北京）和新加坡 Region 可用”。二者存在地域范围不一致——文档 1 的限制未涵盖新加坡，可能已过时或适用范围更窄，实际使用请以文档 3 的双 Region 支持为准。

## 关键参数

- **数据集元信息**：名称（≤50 字符，支持中英文/数字/下划线/连字符/点）、描述（≤200 字符）、类型（训练集/评测集，创建后不可变更）。
- **训练方法相关参数**：
  - SFT：推荐数据量 ≥1000 条；支持草稿；
  - DPO：推荐数据量 ≥100 条；仅北京地域可用；支持草稿；
  - CPT：推荐数据量 ≥5000 万 [Token](../concepts/token.md)；仅北京地域可用；不支持草稿与数据继承。
- **数据处理节点参数**：
  - `dataSetCount`：系统自动生成，表示当前节点输出的 messages 数量，不可修改；
  - `对话文本`：开始节点唯一输入参数，表示待处理的 ChatML 格式训练集；
  - 数据增强节点中 `生成样本数`：单次任务最多生成 2000 条样本；`指令生成依赖样本数`：受千问-Max 输入 token 限制，系统自动调整。

## 使用方式

- **创建数据集**：在 **[数据管理](https://bailian.console.aliyun.com/#/efm/model_data)** > **数据集** 页面点击 **新增数据集**，依次配置名称、类型、场景、训练方法、存储位置（平台 OSS 存储或云存储挂载）、导入方式（本地上传/OSS 导入/日志回流）及发布选项。
- **数据处理（清洗/增强）**：需先在 **数据管理 > 数据流** 中创建并发布数据流（含开始→数据清洗→数据增强→结束节点），再通过 **任务列表 > 从数据流列表创建任务** 选择目标训练集执行。处理结果将生成独立新版本，不覆盖原数据 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：需先在 **模型监控** 页面完成审计日志与推理日志的开通及角色授权，再通过模型监控页、模型详情页或数据管理页的“日志回流”入口进入表单配置。支持按时间范围（最近 30 天）、API Key、模型等条件筛选，单次上限 10 万条 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、OSS 导入、日志回流均仅限华北2（北京）地域；日志回流额外支持新加坡 Region；数据清洗与增强功能文档标注“仅适用于华北2（北京）”，但未排除其他 Region，建议以控制台实际可用性为准。
- **格式与兼容性**：
  - 数据清洗与增强仅接受 SFT-文本生成训练集，且必须为 ChatML 格式（`.jsonl`），其他格式或训练类型将失败 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)；
  - CPT 训练集不支持数据继承，每次新增版本必须重新导入全部数据。
- **操作约束**：
  - 发布和删除操作均不可逆，已发布版本不可编辑，仅草稿版本可删除；
  - 训练集/评测集类型、训练场景、训练方式、存储方式在创建后均不可更改；
  - 数据流任务执行期间不支持手动终止，需等待完成。
- **安全与合规**：数据导入默认启用 OSS 服务端加密（SSE-OSS，AES256）；敏感信息打码等清洗算子可用于脱敏，但用户须自行评估法律文件、医学记录等高风险数据是否适用该功能 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

## 来源文档

- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


