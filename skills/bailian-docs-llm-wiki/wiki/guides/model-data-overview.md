# model data overview

百炼平台的模型数据管理功能为开发者提供统一的数据集创建、处理与回流能力，支撑模型训练、评测及持续优化。本文档系统梳理了支持的数据类型、关键格式规范、使用路径及约束条件，适用于华北2（北京）和新加坡地域。所有操作均需通过[数据管理](https://bailian.console.aliyun.com/#/efm/model_data)控制台入口进行。

## 支持的模型/功能

百炼支持三类核心数据用途：**训练集**（用于模型调优）、**评测集**（用于效果评估）和**日志回流数据集**（从SLS推理日志生成结构化训练/评测数据）。  
- **训练集**支持四种范式：  
  - **SFT**（监督微调）：覆盖文本生成、多模态理解（Qwen-VL）、图生视频（首帧/首尾帧）；  
  - **DPO**（直接偏好优化）：仅限文本生成场景；  
  - **CPT**（持续预训练）：纯文本格式；  
  - **思考模型（Thinking）**：SFT与DPO均支持`<think>`标签格式，但仅对最后一轮assistant输出生效。  
- **评测集**当前仅支持**文本生成单轮对话**格式（Excel或JSONL），用于自动化或人工评分。  
- **日志回流**可将SLS推理日志转化为SFT/DPO/CPT训练集或文本生成评测集，详见[日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
> **注意**：数据清洗与增强功能[仅支持SFT-文本生成训练集](../../raw/model-user-guide/model-data-overview/data-processing.md)，明确不支持SFT-图片理解、DPO及CPT格式，与文档1中“支持多模态理解训练集”的宽泛表述存在范围差异，实际使用请以文档2为准。

## 关键参数

| 参数 | 适用场景 | 类型 | 必填 | 说明 |
|------|----------|------|------|------|
| `loss_weight` | SFT（所有assistant行）、SFT-Thinking（仅末轮）、DPO（`chosen`字段） | float | 否 | 范围`0.0~1.0`，权重越高训练时影响越大；属邀测参数，需联系商务经理开通。 |
| `resized_width`/`resized_height` | 多模态训练（图像/视频帧） | int | 否 | 指定缩放尺寸，单位像素；图像单边≤1024px，视频帧分辨率≤4096×4096。 |
| `fps`/`sample_fps` | 视频训练（VL模型） | float | 否 | `fps`用于视频文件路径模式，`sample_fps`用于图片帧列表模式；仅Qwen3.5+ VL模型支持。 |
| `video_start`/`video_end` | 视频截取 | float | 否 | 单位秒，需满足`0 ≤ start < end ≤ 视频总时长`。 |
| `foreignKey` | 数据增强输出 | string | — | 系统自动生成标识字段，不影响训练，无需手动删除。 |

## 使用方式

1. **创建数据集**：  
   - 训练/评测集：上传ZIP（含`data.jsonl`根目录文件）或Excel，格式严格遵循[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)要求；  
   - 日志回流：在[模型监控](https://bailian.console.aliyun.com/#/model-telemetry)页开启审计日志与推理日志后，配置时间范围、API Key、模型等参数生成结构化数据集。  

2. **数据处理**：  
   - 仅SFT文本训练集支持清洗（如敏感信息打码、URL移除）与增强（Few-Shot生成）；  
   - 通过[数据管理](https://bailian.console.aliyun.com/?tab=model#/efm/model_data) > 数据流 > 创建任务，选择预置模板或自定义节点链路；  
   - 处理后生成独立版本（如V1→V2），原数据集不受影响。  

3. **版本管理**：  
   - 所有操作（上传、清洗、增强、日志回流）均生成新版本，支持按版本回溯与对比；  
   - OSS挂载数据集不支持“新增版本”，需通过“导入数据”页追加；平台存储数据集支持此操作。

## 限制和注意事项

- **地域限制**：所有功能默认仅限华北2（北京），日志回流额外支持新加坡Region；其他地域不可用。  
- **文件约束**：  
  - ZIP包最大2GB，文件名仅支持ASCII字母、数字、`_`、`-`；  
  - `data.jsonl`必须位于ZIP根目录；  
  - 图像单张≤10MB，格式限`.bmp/.jpeg/.jpg/.png/.tif/.tiff/.webp`；  
  - 图生视频训练集图像/视频分辨率≤4096×4096。  
- **数量限制**：  
  - 日志回流单次上限10万条（可多次追加）；  
  - 数据增强-通用单次最多生成2000条样本；  
  - SFT训练集建议≥1000条优质样本，CPT需≥1000万[Token](../concepts/token.md)。  
- **格式兼容性**：  
  - SFT ChatML不支持OpenAI `name`/`weight`字段；  
  - VL模型`system`消息`content`必须为数组格式`[{"text":"..."}]`，禁用字符串；  
  - DPO数据中`chosen`/`rejected`内容需严格匹配`messages`末轮user输入语义。  
> **注意**：文档1中提及“支持图生视频（首帧）与（首尾帧）训练集”，但文档3明确日志回流**仅支持文本生成场景**，图生视频类日志无法回流，二者能力边界需严格区分。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


