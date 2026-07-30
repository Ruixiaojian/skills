# model data overview

百炼平台的模型数据管理功能为开发者提供统一的数据集创建、处理与回流能力，支撑模型训练、评测及持续优化。本文档系统梳理了支持的模型类型、关键参数规范、使用方式及重要限制，适用于华北2（北京）和新加坡地域。所有操作均需通过[数据管理](https://bailian.console.aliyun.com/#/efm/model_data)控制台进行。

## 支持的模型与功能

百炼支持三类核心数据用途：**训练集**（用于模型调优）、**评测集**（用于模型评估）和**日志回流生成的数据集**（从推理日志转化而来）。  
- **训练集**支持文本生成（SFT/DPO/CPT）、[多模态](../concepts/multi-modal.md)理解（Qwen-VL系列）、图生视频（首帧/首尾帧）等场景；其中[SFT-文本生成训练集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)是数据处理功能的唯一支持格式，而[SFT-图片理解训练集](../../raw/model-user-guide/model-data-overview/data-processing.md)和[DPO-文本生成训练集](../../raw/model-user-guide/model-data-overview/data-processing.md)暂不支持清洗与增强。  
- **评测集**当前仅支持文本生成单轮对话格式（Excel或JSONL），用于模型效果量化评估。  
- **日志回流**可将SLS推理日志结构化为训练集（SFT/DPO/CPT）或评测集，但[日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)功能在除华北2（北京）和新加坡外的Region不可用，且评测集不支持OSS挂载存储。

> **注意**：文档1称“目前支持文本生成、[多模态](../concepts/multi-modal.md)理解、图生视频（首帧）、图生视频（首尾帧）训练集”，而文档2明确指出“数据处理仅支持SFT-文本生成训练集”，二者无矛盾——前者描述数据集类型，后者限定数据处理功能的适用范围。但文档2中“暂不支持[SFT-图片理解训练集]”与文档1中“SFT 视觉理解（千问VL）”存在功能覆盖差异，实际使用时需以控制台可用选项为准。

## 关键参数

- **`loss_weight`**：用于SFT和DPO训练数据中调节样本重要性，取值范围`0.0 ~ 1.0`，数值越大权重越高。该参数为邀测功能，需联系商务经理开通。  
- **`resized_width` / `resized_height`**：[多模态](../concepts/multi-modal.md)训练中图像/视频帧的缩放尺寸（像素），影响模型输入分辨率，需与目标模型要求匹配（如Qwen2.5-VL使用绝对坐标，Qwen3-VL使用`[0,999]`相对坐标）。  
- **`fps` / `sample_fps`**：视频训练中帧率参数，`fps`用于视频文件路径模式，`sample_fps`用于图片帧列表模式，仅Qwen3.5+ VL模型支持。  
- **`foreignKey`**：数据增强节点自动添加的标识字段，不影响模型训练，无需手动删除。  
- **时间范围与API Key过滤**：日志回流任务中必填参数，修改时间范围会联动重置API Key和模型选择，需严格按顺序配置。

## 使用方式

1. **数据集创建**：通过[数据管理](https://bailian.console.aliyun.com/#/efm/model_data)上传ZIP包（训练集）或Excel/JSONL文件（评测集），注意压缩包内`data.jsonl`必须位于根目录，图片/视频文件名全局唯一。  
2. **数据清洗与增强**：仅适用于SFT文本生成训练集。在数据流画布中组合“数据清洗”（如敏感信息打码）和“数据增强”（如Few-Shot生成）节点，发布后启动任务，处理结果自动生成新版本（如V1→V2），原数据不受影响。  
3. **日志回流**：需先在[模型监控](https://bailian.console.aliyun.com/#/model-telemetry)完成审计日志与推理日志的授权及开启，再通过任一入口（模型监控页、详情页或数据管理页）配置回流参数。单次上限10万条，支持多次追加至同一数据集的不同版本。

## 限制和注意事项

- **地域限制**：所有功能默认仅限华北2（北京）；日志回流额外支持新加坡Region。  
- **格式与规模**：  
  - SFT训练集最小需**上千条优质样本**，CPT需**千万级[Token](../concepts/token.md)预训练数据**；DPO一般需**上百条人类偏好数据**。  
  - ZIP包最大2GB（训练集）或20MB（图生视频`data.jsonl`），图片单张≤1024px且≤10MB，视频≤4096×4096。  
- **功能边界**：  
  - 数据处理不支持[多模态](../concepts/multi-modal.md)或DPO训练集；  
  - 日志回流评测集不支持OSS挂载；  
  - 图生视频验证集无需提供视频文件，由平台自动调用模型生成预览。  
- **版本管理**：数据清洗、增强及日志回流均生成独立版本，不会覆盖原始数据集，但名称与描述创建后不可修改。  
- **费用与运维**：开启推理日志会产生SLS存储与读写费用，长期不用应及时关闭；OSS挂载需额外授权两个服务角色。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)



