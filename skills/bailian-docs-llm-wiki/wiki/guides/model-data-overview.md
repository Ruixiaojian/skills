# model data overview

百炼平台的模型数据体系为模型调优与评测提供统一的数据管理能力，覆盖训练集构建、日志回流、数据清洗与增强等关键环节。所有功能当前仅支持华北2（北京）和新加坡地域，且不同数据类型对格式、规模及处理方式有明确约束。开发者需根据具体任务场景（如SFT、DPO、CPT或图生视频）选择匹配的数据结构与处理路径。

## 支持的模型/功能

- **训练集类型**：支持文本生成（SFT、DPO、CPT）、多模态理解（千问VL）、图生视频（首帧/首尾帧）三类训练集；其中[SFT-文本生成训练集](../../raw/model-user-guide/model-data-overview/data-processing.md)是数据清洗与增强的唯一支持格式，[DPO-文本生成训练集](../../raw/model-user-guide/model-data-overview/data-processing.md)和[SFT-图片理解训练集](../../raw/model-user-guide/model-data-overview/data-processing.md)暂不支持数据处理功能。
- **评测集类型**：支持文本生成评测集（Excel或JSONL格式），用于模型效果评估。
- **日志回流**：支持将SLS推理日志转化为结构化训练集（SFT/DPO/CPT）或评测集，适用于文本生成场景，详见[日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据处理**：提供数据清洗（如敏感信息打码、特殊内容移除）与数据增强（通用/分类/抽取/创作四类场景）能力，仅作用于SFT-文本生成训练集（ChatML格式）。

> **注意**：文档1明确声明“暂不支持[SFT-图片理解训练集](../../raw/model-user-guide/model-data-overview/data-processing.md)和[DPO-文本生成训练集](../../raw/model-user-guide/model-data-overview/data-processing.md)”，而文档2中详细描述了DPO和多模态SFT的格式规范。这意味着DPO和多模态SFT可用于模型调优，但**不可通过控制台数据流进行清洗或增强**——该限制仅针对数据处理功能，不影响其作为原始训练集的使用。

## 关键参数

- **ChatML格式要求**：
  - SFT：`messages`数组必须包含`role`（`system`/`user`/`assistant`）和`content`字段；`assistant`行可选`loss_weight`（0.0–1.0，邀测参数）。
  - DPO：除`messages`外，需包含`chosen`和`rejected`对象，二者均支持`loss_weight`。
  - 多模态SFT：`content`为数组，含`text`或`image`/`video`对象；图像/视频需指定`resized_width`/`resized_height`等元信息。
- **日志回流参数**：时间范围（最近30天）、API Key过滤（全部/其他/指定）、模型选择、训练方式（SFT/DPO/CPT）、存储方式（平台存储/OSS挂载）；其中存储方式、数据类型、训练方式创建后不可更改。
- **数据增强节点参数**：
  - `生成样本数`：单次任务最多2000条；
  - `指令生成依赖样本数`：系统自动调整以避免超Token限制；
  - `过滤相似度阈值`：控制增强结果去重强度（文档1未给出默认值，需参考控制台实际配置）。

## 使用方式

- **训练集/评测集上传**：通过[数据管理](https://bailian.console.aliyun.com/?tab=model#/efm/model_data)页面上传JSONL、Excel或ZIP包（图生视频需含`data.jsonl`及媒体文件），支持版本管理。
- **日志回流**：在[模型监控](https://bailian.console.aliyun.com/#/model-telemetry)或[数据管理](https://bailian.console.aliyun.com/#/efm/data_ass)页发起，需先完成SLS审计日志与推理日志授权（见[日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)）。
- **数据清洗与增强**：通过控制台搭建数据流（含开始→数据清洗→数据增强→结束节点），基于预置模板或自定义算子编排；**目前不提供公开API**，仅支持控制台操作（见[数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)）。
- **数据集追加**：OSS挂载数据集须通过“导入数据”页追加；平台存储数据集支持“新增版本”弹窗操作。

## 限制和注意事项

- **地域限制**：所有功能（数据处理、日志回流、训练集上传）均仅限华北2（北京）和新加坡Region；文档1与文档2多次强调“本文档仅适用于华北2（北京）地域”，文档3补充新加坡支持日志回流。
- **格式硬性约束**：
  - 数据处理仅接受SFT-ChatML格式（`.jsonl`），不支持OpenAI `name`/`weight`字段；
  - 图生视频ZIP包内`data.jsonl`必须位于根目录，媒体文件名全局唯一，单张图≤10MB/1024px；
  - 日志回流单次上限10万条，超量部分被截断。
- **功能边界**：
  - 数据清洗/增强不支持法律文件、医学记录、文学作品等高敏或非结构化文本（见[数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)）；
  - 日志回流产出的数据集可后续进行数据清洗，但原始日志本身不参与清洗流程；
  - OSS挂载数据集不支持“新增版本”，仅能通过“导入数据”页追加。
- **版本管理**：数据处理、日志回流均自动生成新版本，原数据集不受影响；建议处理后人工校验清洗/增强结果的完整性与真实性。

## 来源文档

- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


