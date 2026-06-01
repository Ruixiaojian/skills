# model training

百炼平台提供模型调优（fine-tuning）能力，支持对文本生成、视觉理解、语音合成、视频生成以及语音识别等多种模型进行定制训练。开发者可通过 HTTP API 完成文件上传、任务创建、状态查询和任务管理的全流程操作。本文汇总了模型调优相关的核心概念、支持的模型类型、关键参数及使用方式。

## 支持的模型与训练方式

百炼平台支持以下几类模型的调优：

| 模型类别 | 代表模型 | 支持的训练方式 | 参考文档 |
|---------|---------|--------------|---------|
| 文本生成 | qwen3-14b 等千问系列 | `sft`、`efficient_sft`、`cpt`、`dpo_full`、`dpo_lora` | [模型调优 API 参考](../../raw/model-api-reference/model-training/model-training-api-reference.md) |
| 视觉理解 | 千问-VL 系列 | `sft`、`efficient_sft` | [模型调优 API 参考](../../raw/model-api-reference/model-training/model-training-api-reference.md) |
| 语音合成 | cosyvoice-v3-flash | `efficient_sft` | [模型调优 API 参考](../../raw/model-api-reference/model-training/model-training-api-reference.md) |
| 视频生成（图生视频） | wan2.5-i2v-preview、wan2.2-i2v-flash、wan2.2-kf2v-flash | `efficient_sft` | [视频生成模型微调API参考](../../raw/model-api-reference/model-training/wan-video-generation-finetune-api-reference.md) |
| 语音识别（热词） | paraformer-realtime-v1、paraformer-v1 等 | `compile_asr_phrase` | [paraformer热词](../../raw/model-api-reference/model-training/paraformer-asr-phrase-manager.md) |

## 整体流程

模型调优的典型流程为：

1. **上传训练数据** — 调用文件管理 API 上传训练文件，获取 `file_id`
2. **创建调优任务** — 指定基础模型、训练文件 ID 和超参数，发起训练
3. **查询任务状态** — 轮询任务状态，直到 `SUCCEEDED` 或 `FAILED`
4. **部署/使用模型** — 训练成功后，使用产出的模型 ID 进行推理调用

## 文件管理

训练数据通过 [百炼文件管理 API](../../raw/model-api-reference/model-training/model-customization-file-management-service.md) 进行上传和管理。上传时 `purpose` 设为 `fine-tune`，返回的 `file_id` 用于后续创建调优任务。

**接口端点：**

| 操作 | 方法 | URL |
|------|------|-----|
| 上传文件 | `POST` | `https://dashscope.aliyuncs.com/api/v1/files` |
| 列举文件 | `GET` | `https://dashscope.aliyuncs.com/api/v1/files` |
| 获取文件详情 | `GET` | `https://dashscope.aliyuncs.com/api/v1/files/{file_id}` |
| 删除文件 | `DELETE` | `https://dashscope.aliyuncs.com/api/v1/files/{file_id}` |

**使用限制：**

- 单个文件最大 1GB
- 有效文件总使用空间配额 5GB
- 有效文件总数量配额 100 个

## 创建调优任务

**接口：** `POST https://dashscope.aliyuncs.com/api/v1/fine-tunes`

### 核心输入参数

| 参数 | 必选 | 说明 |
|------|------|------|
| `model` | 是 | 基础模型 ID，或已调优模型的 ID（二次调优） |
| `training_file_ids` | 是 | 训练集文件 ID 数组 |
| `validation_file_ids` | 否 | 验证集文件 ID 数组；不提供时系统自动按比例划分 |
| `training_type` | 否（视频生成模型为必选） | 训练方法：`sft`、`efficient_sft`、`cpt`、`dpo_full`、`dpo_lora` |
| `hyper_parameters` | 否 | 超参数配置，不同模型支持的参数集合不同 |

### 关键超参数

#### 文本生成 / 视觉理解模型

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `n_epochs` **【必填】** | 训练循环次数 | 数据量 < 10000 时 3~5，> 10000 时 1~2 |
| `batch_size` **【必填】** | 批次大小 | 使用默认值 |
| `max_length` **【必填】** | 单条数据最大 token 长度，超长数据将被丢弃 | 8192 |
| `learning_rate` | 学习率 | 使用默认值 |
| `lr_scheduler_type` | 学习率调整策略 | `linear` 或 `inverse_sqrt` |
| `split` | 训练集占比（无验证集时生效） | 0.8~0.9 |

高效微调（`efficient_sft`、`dpo_lora`）还支持 `lora_rank`、`lora_alpha`、`lora_dropout` 等 LoRA 参数。

> **注意**：对已经高效微调后的模型进行二次微调时，`lora_rank`、`lora_alpha`、`lora_dropout` 三个参数必须与首次保持一致。

#### 视频生成模型

视频生成模型的超参数与文本模型有所不同，增加了 `eval_epochs`（验证间隔）和 `max_pixels`（训练视频最大分辨率）等专用参数，且 `batch_size` 为固定值（wan2.5 为 2，wan2.2 为 4）。详见 [视频生成模型微调API参考](../../raw/model-api-reference/model-training/wan-video-generation-finetune-api-reference.md)。

#### CosyVoice 语音合成模型

CosyVoice（`cosyvoice-v3-flash`）有独立的 8 个超参数（`lm_max_epoch`、`lm_step`、`lm_num`、`lm_batch_size`、`fm_max_epoch`、`fm_step`、`fm_num`、`fm_batch_size`），**全部必填**，不可与文本模型的 `n_epochs` 等混用。

### 混合训练

文本生成模型的 `sft` 和 `efficient_sft` 支持混合训练（`data_augmentation`），训练数据将与百炼提供的通用数据集混合，以提升训练效果、避免模型能力退化。需配合 `augmentation_types` 和 `augmentation_ratio` 使用。

## 任务状态

所有调优任务共享统一的状态机：

| 状态 | 含义 |
|------|------|
| `PENDING` | 训练待开始 |
| `QUEUING` | 正在排队（同时只有一个训练任务可以进行） |
| `RUNNING` | 训练进行中 |
| `CANCELING` | 正在取消 |
| `SUCCEEDED` | 训练成功 |
| `FAILED` | 训练失败 |
| `CANCELED` | 已取消 |

查询任务状态：`GET https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}`

## 语音识别热词

Paraformer 语音识别模型支持通过热词功能改善特定词汇的识别效果。热词通过 SDK 中的 `AsrPhraseManager` 类管理，支持创建、查询、更新和删除操作。热词列表最多 500 个词，权重范围为 `[1, 5]`（提高识别概率）和 `[-6, -1]`（降低识别概率）。

## 限制与注意事项

- **地域限制**：模型调优 API 仅适用于中国大陆版（北京地域）。
- **并发限制**：同时只有一个训练任务可以进行，其余任务处于 `QUEUING` 状态。
- **文件限制**：单文件最大 1GB，有效文件总空间 5GB，总数量 100 个。
- **数据截断**：文本模型训练中，单条数据 token 超过 `max_length` 的将被直接丢弃。
- **视频模型训练时长**：视频生成模型的微调任务通常需要数小时，请耐心等待。
- **VL 模型计费**：千问-VL 模型仅在 `freeze_vit` 设为 `true` 时才能按 Token 用量计费。
- 所有 API 请求需携带 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 头部。

## 来源文档

- [百炼文件管理 API](../../raw/model-api-reference/model-training/model-customization-file-management-service.md)
- [模型调优 API 参考](../../raw/model-api-reference/model-training/model-training-api-reference.md)
- [视频生成模型微调API参考](../../raw/model-api-reference/model-training/wan-video-generation-finetune-api-reference.md)
- [paraformer热词](../../raw/model-api-reference/model-training/paraformer-asr-phrase-manager.md)

