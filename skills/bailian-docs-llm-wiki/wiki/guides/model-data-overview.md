# model data overview

百炼平台的模型数据体系为模型调优与评测提供结构化、可管理的数据支撑，涵盖训练集、评测集、日志回流及数据处理全流程。所有功能当前仅支持华北2（北京）和新加坡地域，且数据集需符合严格的格式与存储规范。本文档整合核心能力与约束，面向开发者提供可直接落地的实践指南。

## 支持的模型/功能

百炼支持多种模型类型与数据用途的组合：  
- **训练集**：覆盖文本生成（SFT、DPO、CPT）、[多模态](../concepts/multi-modal.md)理解（Qwen-VL 系列）、图生视频（首帧/首尾帧）三大场景；其中 SFT 和 DPO 训练集均采用 ChatML 格式，CPT 为纯文本 JSONL 格式，图生视频需 ZIP 压缩包含 `data.jsonl` 及媒体文件 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **评测集**：当前仅支持文本生成单轮对话 Excel 或 JSONL 格式，用于模型泛化能力评估 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **日志回流**：将 SLS 推理日志自动转化为结构化训练集（SFT/DPO/CPT）或评测集，支持平台存储与 OSS 挂载两种模式，但评测集不支持 OSS 挂载 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
- **数据清洗与增强**：仅支持 SFT 文本生成训练集（ChatML 格式），暂不支持[多模态](../concepts/multi-modal.md)、DPO 或 CPT 数据集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

> **注意**：文档 2 明确指出“暂不支持[SFT-图片理解训练集]和[DPO-文本生成训练集]”，但文档 1 中 SFT 视觉理解与 DPO 均被列为正式支持类型。该矛盾表明**[多模态](../concepts/multi-modal.md)与 DPO 的数据清洗/增强功能尚未上线**，实际使用时应以控制台可用能力为准，不可依赖文档 1 的宽泛描述。

## 关键参数

| 参数 | 适用场景 | 类型 | 必填 | 说明 |
|------|----------|------|------|------|
| `loss_weight` | SFT（所有 assistant 行）、SFT-thinking（仅最后 assistant 行）、DPO（`chosen` 字段） | float | 否 | 范围 `0.0 ~ 1.0`，数值越大训练权重越高；属邀测参数，需联系商务经理开通 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |
| `resized_width` / `resized_height` | 多模态训练（图像/视频） | int | 否 | 图像/视频目标缩放尺寸（像素），影响坐标标注基准（如 Qwen2.5-VL 用绝对像素，Qwen3-VL 用 `[0,999]` 相对坐标） [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |
| `video_start` / `video_end` | 图生视频（首帧模式） | float | 否 | 视频截取起止时间（秒），仅在视频文件路径模式下生效 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |
| `generate_sample_count` | 数据增强节点 | int | 是 | 单次任务最多生成 2000 条样本；原数据集 + 新增样本构成最终训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md) |

## 使用方式

1. **创建数据集**：  
   - 训练/评测集：通过 [数据管理](https://bailian.console.aliyun.com/#/efm/model_data) 上传 ZIP（图生视频）、JSONL（SFT/DPO/CPT）、Excel（评测集）等格式文件；  
   - 日志回流：在[模型监控](https://bailian.console.aliyun.com/#/model-telemetry)页开启审计日志与推理日志后，配置时间范围、API Key、模型等参数触发回流 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  

2. **数据处理（可选）**：  
   - 仅限 SFT 文本训练集：在数据流中编排「数据清洗」（如敏感信息打码）与「数据增强」（基于千问-Max 的 Few-Shot 生成）节点，处理后自动生成新版本，原数据集不受影响 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  

3. **关联模型任务**：  
   - 训练集用于[模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)，评测集用于[模型评测](https://help.aliyun.com/zh/model-studio/model-evaluation-overview)；日志回流产出的数据集可直接作为输入源。

## 限制和注意事项

- **地域限制**：全部功能（训练集管理、日志回流、数据处理）仅在华北2（北京）和新加坡 Region 可用，其他地域控制台不显示对应入口 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
- **格式强约束**：  
  - 所有 ZIP 训练集必须包含根目录下的 `data.jsonl`，且文件名/路径不能含非 ASCII 字符；图片单张 ≤ 10MB、≤ 1024px，视频 ≤ 4096×4096；  
  - 多模态 `system` 消息的 `content` 必须为数组格式 `[{"text":"..."}]`，字符串格式将导致解析失败 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **规模底线**：CPT 需 ≥1000 万 [Token](../concepts/token.md) 预训练数据，SFT 需 ≥1000 条优质样本，DPO 需 ≥100 条偏好数据；低于此规模可能导致调优效果不佳 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **版本管理**：数据清洗、增强或日志回流均生成独立新版本（如 V2），不会覆盖原始数据集，但需手动切换版本用于后续任务 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
- **API 限制**：数据处理暂无开放 API，必须通过控制台操作；日志回流单次上限 10 万条，但可多次追加至同一数据集不同版本 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


