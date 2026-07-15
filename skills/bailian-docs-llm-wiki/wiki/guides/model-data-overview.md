# model data overview

百炼平台的模型数据体系为大模型训练与评测提供结构化、可管理的数据支撑，涵盖训练集（SFT/CPT/DPO/图生视频）、评测集及配套的数据处理能力。所有数据均需通过统一的数据管理界面上传与版本控制，地域限制为华北2（北京）。本文档聚焦数据格式、参数约束、使用路径及关键限制，面向开发者提供实操指引。

## 支持的模型/功能

- **训练集类型**：支持文本生成（SFT/CPT/DPO）、多模态理解（Qwen-VL 系列）、图生视频（首帧/首尾帧）三类训练任务。其中 SFT 支持 ChatML 格式多轮对话，CPT 为纯文本 JSONL，DPO 需包含 `chosen`/`rejected` 对比样本；图生视频训练集必须打包为 ZIP，含 `data.jsonl` 及对应图像/视频文件 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集类型**：当前仅支持文本生成类单轮评测集（Excel 或 JSONL 格式），每条记录含 `Prompt` 和 `Completion` 字段，用于自动化或人工评分 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理能力**：提供数据清洗（如敏感信息打码、URL 移除）和数据增强（基于千问-Max 的 Few-Shot 生成）功能，**仅适用于 SFT-文本生成训练集（ChatML 格式）**，不支持 SFT-图片理解、DPO 或 CPT 数据 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

> **注意**：文档 1 中称“支持图生视频（首帧）”、“图生视频（首尾帧）”训练集，而文档 2 明确说明数据清洗/增强“暂不支持[SFT-图片理解训练集]和[DPO-文本生成训练集]”，且未提及图生视频数据处理能力。因此，**图生视频训练集不可进行任何数据清洗或增强操作**，该限制需在实际使用中严格遵守。

## 关键参数

- **`loss_weight`**：SFT（ChatML 和 Thinking 模式）及 DPO 的 `chosen` 字段中支持，取值范围 `0.0 ~ 1.0`，用于调节单条 assistant 输出或 chosen 样本的训练权重。该参数为邀测功能，需联系商务经理开通 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **视觉字段约束**：Qwen-VL 训练中，`system` 消息的 `content` 必须为数组格式 `[{"text":"..."}]`，不可用字符串；图像/视频字段需显式声明 `resized_width`/`resized_height`；Qwen3-VL 坐标为 `[0,999]` 相对坐标，Qwen2.5-VL 为像素绝对坐标。
- **ZIP 包规范**：所有多模态/图生视频训练集必须为 ZIP 格式，最大 2 GB；`data.jsonl` 必须位于根目录；文件名仅支持 ASCII 字母、数字、下划线、连字符；图像单张 ≤ 1024px 宽高、≤ 10MB；图生视频图像/视频分辨率上限为 4096×4096 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 使用方式

- **创建与上传**：通过控制台 [数据管理](https://bailian.console.aliyun.com/#/efm/model_data) 页面上传训练集/评测集，系统自动校验格式与结构。文本类数据（SFT/CPT/DPO）支持 `.jsonl` 直传；多模态/图生视频需打包 ZIP 并确保目录结构合规。
- **数据处理流程**：仅对 SFT-文本生成训练集有效。需先在“数据流”页签创建数据流（含开始→数据清洗→数据增强→结束节点），发布后在“任务列表”中选择目标训练集启动任务。处理结果将生成独立版本（如 V2），原数据集不受影响 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **评测执行**：上传文本生成评测集后，在 [模型评测](https://help.aliyun.com/zh/model-studio/model-evaluation-overview) 页面关联模型并启动评测任务，系统将基于每条 `Prompt` 进行推理，并比对 `Completion` 进行评分。

## 限制和注意事项

- **地域限制**：所有功能（数据上传、清洗、增强、训练、评测）**仅支持华北2（北京）地域**，跨地域调用将失败。
- **格式与兼容性**：
  - SFT 训练不支持 OpenAI 的 `name`、`weight` 参数；
  - Excel 格式仅支持单轮 SFT 训练集（`.xls`/`.xlsx`），多轮必须用 `.jsonl`；
  - 图生视频验证集无需提供视频文件，由系统自动调用模型生成预览。
- **规模建议**：CPT 至少需 1000 万 [Token](../concepts/token.md) 预训练数据；SFT 微调建议 ≥1000 条高质量样本；DPO 偏好数据建议 ≥100 条 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理限制**：无 API 接口，仅支持控制台操作；数据增强每次最多生成 2000 条样本；增强过程依赖千问-Max 模型，不可更换 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)


