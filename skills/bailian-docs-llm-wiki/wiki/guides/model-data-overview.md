# model data overview

百炼平台的模型数据体系围绕训练与评测两大核心场景构建，提供结构化、可管理的数据集支持。本文档汇总了当前支持的模型类型、关键数据格式参数、使用方式及限制条件，面向开发者提供可直接落地的技术参考。所有功能均需在华北2（北京）地域使用。

## 支持的模型/功能

- **训练集类型**：支持文本生成（SFT、DPO、CPT）、多模态理解（Qwen-VL 系列）、图生视频（首帧模式、首尾帧模式）三类训练任务。其中 SFT 支持 ChatML 格式多轮对话，DPO 支持偏好对标注，CPT 为纯文本预训练格式；图生视频训练集需严格按 ZIP 压缩包结构组织图像、视频及 `data.jsonl` 标注文件 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集类型**：当前仅支持文本生成类单轮对话评测集（Excel 或 JSONL 格式），用于模型效果横向对比与迭代评估 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理能力**：提供数据清洗（如敏感信息打码、URL 移除）与数据增强（基于千问-Max 的 Few-Shot 生成）两类算子，**仅适用于 SFT-文本生成训练集（ChatML 格式）**，不支持 SFT-图片理解、DPO 或 CPT 数据集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

> **注意**：文档 1 中称“支持图生视频（首帧）、（首尾帧）训练集”，而文档 2 明确指出“暂不支持[SFT-图片理解训练集]”，但未提及图生视频是否支持数据清洗/增强。结合上下文及控制台实际能力，图生视频类训练集**不支持任何数据清洗或增强操作**——该限制未在文档 1 中说明，属隐含约束。

## 关键参数

- **`loss_weight`**：SFT（所有 assistant 行）和 DPO（`chosen` 字段）中支持，取值范围 `0.0 ~ 1.0`，用于调节单条样本训练权重；属邀测功能，需联系商务经理开通 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **视觉输入字段**：VL 模型要求 `system.content` 必须为数组格式 `[{"text": "..."}]`；图像/视频字段需显式声明 `resized_width`/`resized_height`；视频支持 `fps`（文件路径模式）或 `sample_fps`（帧列表模式）参数 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **坐标规范**：Qwen2.5-VL 使用绝对像素坐标，Qwen3-VL 使用 `[0, 999]` 归一化相对坐标，模型版本不匹配将导致物体定位失效。
- **增强控制参数**：数据增强节点中 `指令生成依赖样本数`（few-shot 数量）、`生成样本数`（最大 2000 条/任务）、`过滤相似度阈值` 共同影响输出质量与多样性 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

## 使用方式

- **数据集创建**：通过控制台 [数据管理](https://bailian.console.aliyun.com/#/efm/model_data) 统一上传 ZIP（VL/图生视频）或 JSONL/XLSX（文本）文件，训练集必须包含根目录 `data.jsonl`，图像/视频文件名全局唯一且不可嵌套路径。
- **数据处理流程**：仅限 SFT 文本训练集，需先在控制台创建数据流（含清洗+增强节点），再基于该数据流启动任务；处理后自动生成新版本（如 V2），原数据集不受影响 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **验证集构建**：图生视频验证集无需提供视频文件，仅需首帧/首尾帧图像 + `data.jsonl`，系统将在评估节点自动调用模型生成预览视频 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 限制和注意事项

- **地域限制**：所有功能仅支持华北2（北京）地域，跨地域调用将失败。
- **格式强约束**：
  - VL 训练集 ZIP 包内文件名仅支持 ASCII 字符（a-z, A-Z, 0-9, `_`, `-`），大小上限 2 GB；
  - 图生视频 ZIP 中 `data.jsonl` 必须位于根目录，图像/视频路径在 JSONL 中仅写文件名（如 `"image_1.jpg"`），**不可带子目录路径**；
  - Excel 评测集仅支持单轮对话，多轮或复杂结构将解析失败。
- **规模建议**：CPT 需 ≥10M Token；SFT 需 ≥1000 条优质样本；DPO 需 ≥100 条偏好对；低于阈值易导致调优效果不佳 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **API 缺失**：数据清洗与增强功能**暂无公开 API**，必须通过控制台操作 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **模型兼容性**：图生视频训练集仅适配 Wan 系列模型；Qwen3.5-VL 及以后版本才支持视频文件路径模式；旧版 VL 模型不兼容新坐标规范。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)


