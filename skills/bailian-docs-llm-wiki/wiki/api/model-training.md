# model training

百炼平台的模型调优（model training / fine-tuning）通过 `https://dashscope.aliyuncs.com/api/v1/fine-tunes` 系列 REST 接口，将上传的训练文件与基础模型组合成调优任务，覆盖文本生成、视觉理解、语音合成（CosyVoice）、视频/图像生成（万相）等多类模型，并在调优后通过模型压缩 API 进一步量化产出可部署的精简模型。本文汇总四份原始 API 参考的核心使用方式、超参语义与跨模型差异，便于开发者按场景选型与排查。

> **注意**：调优与微调相关接口当前**仅适用于中国大陆版（北京地域）**，使用前请确认 API Key 归属该地域，否则会因路由错位返回鉴权失败。

## 一、整体流程

所有调优任务都遵循同一条主线，仅参数与状态机覆盖范围不同：

1. **上传数据集** → 通过 [百炼文件管理 API](../../raw/model-api-reference/model-training/model-customization-file-management-service.md) 的 `POST /api/v1/files`（`multipart/form-data`，`purpose=fine-tune`）拿到 `file_id`。
2. **创建调优任务** → `POST /api/v1/fine-tunes`，传入 `model`（基础模型 ID）、`training_file_ids` 和该模型支持的 `training_type` 与 `hyper_parameters`，返回 `job_id`。
3. **轮询任务状态** → `GET /api/v1/fine-tunes/{job_id}`，直至进入终态 `SUCCEEDED` / `FAILED` / `CANCELED`，成功时 `output.finetuned_output` 即为产出模型 ID。
4. （可选）**模型压缩** → 对全参微调产物调用 [模型压缩 API](../../raw/model-api-reference/model-training/model-compression-api-reference.md) 的 `POST /api/v1/fine-tunes/compress/jobs`，量化后用于部署。

任务状态固定为：`PENDING` / `QUEUING` / `RUNNING` / `CANCELING` / `SUCCEEDED` / `FAILED` / `CANCELED`，**同一用户同时只允许一个训练任务执行**（其余进入 `QUEUING`）。

## 二、文件管理 API

文件管理服务在三类调优任务之间共用，详见 [百炼文件管理 API](../../raw/model-api-reference/model-training/model-customization-file-management-service.md)。关键约束：

- 单文件 ≤ **1 GB**；有效文件（未删除）总空间 ≤ **5 GB**；有效文件总数 ≤ **100 个**。
- `purpose` 必填，常用三种用途：
  - `fine-tune`：用于调优任务（包括文本、视频/图像微调）。
  - `file-extract`：用于 Qwen-Long 长上下文内容分析。
  - `batch`：用于创建 Batch 任务。
- 主要接口：`POST /api/v1/files`（支持批量上传）、`GET /api/v1/files`（分页列举，`page_no`/`page_size` 必填）、`GET /api/v1/files/{file_id}`（查询单文件含下载 `url`）、`DELETE /api/v1/files/{file_id}`（删除后释放配额）。
- 返回中 `data.uploaded_files[].file_id` 即后续 `training_file_ids` / `validation_file_ids` 的元素，需妥善保存。

> **注意**：达到空间或数量上限时，单次批量上传可能部分失败，须检查响应里的 `data.failed_uploads`（如 `BadRequest.TooLarge` / `BadRequest.TooMany`），不要假定整批成功。OpenAI 兼容风格接口另见 `OpenAI 兼容-File`，与本节字段不通用。

## 三、文本 / 视觉 / 语音模型调优

主入口为 [模型调优 API 参考](../../raw/model-api-reference/model-training/model-training-api-reference.md)，`POST /api/v1/fine-tunes` 请求体核心字段：

| 字段 | 必选 | 说明 |
| --- | --- | --- |
| `model` | 是 | 基础模型 ID，或已调优产出的模型 ID（用于二次调优）。 |
| `training_file_ids` | 是 | 训练集 `file_id` 数组，来自文件管理 API。 |
| `validation_file_ids` | 否 | 验证集 `file_id` 数组；不传时由 `split` / `max_split_val_dataset_sample` 自动切分（默认 80/20，自动验证集最多 1000 条）。 |
| `hyper_parameters` | 否 | 超参表，**不同模型默认值不同**，需在控制台对应模型/方法处确认。 |
| `training_type` | 否 | `cpt` / `sft` / `efficient_sft` / `dpo_full` / `dpo_lora`。 |
| `job_name` / `model_name` | 否 | 任务展示名 / 调优后模型名。 |
| `finetuned_output_suffix` | 否 | 产出模型 ID 的后缀。 |

### 3.1 通用超参（文本 / 视觉理解）

`n_epochs`、`batch_size`、`max_length` **必填**，三者决定训练时长与费用：

- `n_epochs`：数据量 < 10000 推荐 3~5；> 10000 推荐 1~2。
- `max_length`：单条数据 token 上限，**超过即被丢弃**（不会截断），常用 8192。
- `learning_rate` / `lr_scheduler_type`（推荐 `linear` / `Inverse_sqrt`） / `warmup_ratio` / `weight_decay`：常规优化器超参，建议沿用控制台默认值。
- `eval_steps` / `logging_steps`：影响 Validation Loss / Token Accuracy 的回写频率与日志密度。
- `freeze_vit`（**仅千问-VL 视觉理解**）：必须设为 `true` 才能按 Token 用量计费，否则走其他计费方式。

### 3.2 高效微调（`efficient_sft` / `dpo_lora`）

`lora_rank`（推荐 64）、`lora_alpha`、`lora_dropout` 控制 LoRA 低秩矩阵规模与正则强度。**对一个已经高效微调的模型做二次高效微调时，这三个参数必须与上次完全一致**，否则无法继续训练。

### 3.3 混合训练（`sft` / `efficient_sft`）

通过 `data_augmentation=true` 启用百炼提供的预置语料混合，可缓解模型能力退化：

- `augmentation_types`：英/中文对话、数学、代码、通用、NLP；千问 3 系列额外有 `mix_v2`，千问 3 VL 用 `vl_mix`。
- `augmentation_ratio`：与 types 一一对应，取值 0.0~2.0，按比例随机抽取混合，**混合的数据会计入计费 Token**。

### 3.4 Checkpoint 快照（`sft` / `efficient_sft`）

`save_strategy` 选 `epoch` 或 `steps`，配 `save_steps`（建议设为 `eval_steps` 的整数倍）控制保存频率；`save_total_limit` 限制最多保留多少个 Checkpoint 用于发布。

### 3.5 CosyVoice 语音合成专用超参

`cosyvoice-v3-flash` 与文本模型的超参集**不可混用**，必须填入 8 个 LM/FM 参数：`lm_max_epoch`（推荐 60）、`lm_step`、`lm_num`、`lm_batch_size`（推荐 1000）、`fm_max_epoch`（推荐 100）、`fm_step`、`fm_num`、`fm_batch_size`（推荐 2000）。当前**仅支持 `training_type=efficient_sft`**。

### 3.6 任务管理与状态查询

- `GET /api/v1/fine-tunes/{job_id}`：查询任务详情，`SUCCEEDED` 时返回 `finetuned_output`（最终模型 ID）、`usage`（消耗 Token）等。
- 创建任务返回的 `job_id` 形如 `ft-{yyyyMMddHHmm}-{4位uuid}`，用于后续所有查询、日志、取消、删除接口。

## 四、万相视频 / 图像生成模型微调

视频与图像生成模型走同一组 `fine-tunes` 接口，但**超参集合与文本模型完全分离**，详见 [视频/图像生成模型微调 API 参考](../../raw/model-api-reference/model-training/wan-generation-finetune-api-reference.md)。

### 4.1 适用范围

- 同样仅适用于中国内地北京地域。
- 数据集以 `.zip` 形式上传，**API 上传单包 ≤ 1 GB**；超出需走批量上传或线下方式。
- 当前**仅支持 `training_type=efficient_sft`**（LoRA 高效微调）。
- 支持的基础模型：
  - 图生视频-基于首帧：`wan2.5-i2v-preview`、`wan2.2-i2v-flash`。
  - 图生视频-基于首尾帧：`wan2.2-kf2v-flash`。
  - 图像生成（文生图 / 图生图）：`wan2.7-image-pro`。

### 4.2 视频生成模型超参

视频模型按 **epoch** 计数：

- `n_epochs`：建议总训练步数 ≥ **800**，估算公式 `n_epochs = 800 / ceil(数据集大小 / batch_size)`。
- `batch_size`：`wan2.5-i2v-preview` 推荐 2；`wan2.2-i2v-flash` / `wan2.2-kf2v-flash` 推荐 4。
- `eval_epochs`：需 ≥ `n_epochs / 10`。
- `max_pixels`：训练视频最大分辨率（宽×高）；`wan2.5-i2v-preview` 推荐 36864（192×192），`wan2.2-*` 推荐 262144（512×512）；仅超过该值的视频会被缩放。
- `lora_rank` / `lora_alpha` 必须为 2 的幂（如 16/32/64），推荐 32。
- `split` / `max_split_val_dataset_sample` 仅在未传 `validation_file_ids` 时生效，验证集数量取 `min(数据集 × (1 − split), max_split_val_dataset_sample)`。

### 4.3 图像生成模型超参

图像模型按 **step** 计数（与视频模型不同）：

- `max_steps`：训练总步数，建议 ≥ 500，推荐 800。
- `eval_steps`：评估间隔（顺带保存当前 step 的模型）。
- `generation_type`：`t2i`（文生图） / `i2i`（图生图），决定数据格式与推理方式。
- `max_pixels` / `val_img_size` / `max_token_length`：均使用 `"1k"` / `"2k"` 这类字符串值，建议三者保持一致；文生图推荐 `"2k"`，图生图推荐 `"1k"`。
- `gradient_clip`（默认 0.5，-1 表示不裁剪）、`weight_decay`（默认 0.02）；`lora_rank` / `lora_alpha` 同样需为 2 的幂，推荐 32。

> **注意**：视频模型用 `n_epochs` + `eval_epochs`，图像模型用 `max_steps` + `eval_steps`，两套不可互换。如果模型不收敛，先调 `n_epochs` / `max_steps`，再调 `learning_rate`。

## 五、模型压缩（量化）

模型压缩 API 在调优之后串行使用，详见 [模型压缩 API 参考](../../raw/model-api-reference/model-training/model-compression-api-reference.md)。

### 5.1 前置条件

- 当前**仅支持基于 `qwen3.5-flash-2026-02-23` 的自定义全参微调模型**（SFT / DPO / CPT）；**LoRA 微调模型与已量化模型不支持**。
- 压缩当前限时免费，但产出模型支持的部署单元规格由量化模板决定，部署数量在控制台「模型部署」中配置。

### 5.2 接口列表

所有路径以 `https://dashscope.aliyuncs.com` 为前缀：

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/fine-tunes/compress/templates` | 列举可量化模型及配置模板 |
| POST | `/api/v1/fine-tunes/compress/jobs` | 创建压缩任务 |
| GET | `/api/v1/fine-tunes/compress/jobs` | 列举压缩任务（支持按 `status` / `model` / `quant_spec` / `quant_method` / 时间范围 / `search_key` 等过滤，按 `create_time` 排序与分页） |
| GET | `/api/v1/fine-tunes/compress/jobs/{job_id}` | 查询任务详情 |
| GET | `/api/v1/fine-tunes/compress/jobs/{job_id}/logs` | 获取任务日志（`offset` + `line` 翻页） |
| POST | `/api/v1/fine-tunes/compress/jobs/{job_id}/cancel` | 取消任务 |
| DELETE | `/api/v1/fine-tunes/compress/jobs/{job_id}` | 删除任务 |

### 5.3 创建压缩任务关键参数

- `model`：源全参微调模型 ID。
- `template_id`：通过列举模板接口获得（模板按 模型架构 × 精度 × 目标 MU 规格 绑定，例如 `quant-flash-nvfp4-mlp-nomtp` 对应 W4A4 NVFP4 MU5/MU8/MU9）。
- `hyper_parameters`：可选 Key-Value，**只传想覆盖的超参**；模板的可调参定义里会标明 `type` (`number`/`string`) / `support_values` / `data_range` / `step` / `defaultValue` / `recommend_value` / `required` / `advancedParameter`。
- `custom_calibration_file_ids`：自定义校准数据集（格式 `file-{32hex}`，需先在「数据管理」中创建并发布），**仅当 `calib_input=true` 时生效**。
- `output_model_suffix`：最多 8 字符，仅小写字母与数字。产出模型 ID 命名固定为 `{base_model}-{output_model_suffix}-{job_id}`，例如 `qwen3.5-flash-2026-02-23-test-quant-202604111200-a1b2`。

### 5.4 多语言

`GET /templates` 支持 `lang=zh-CN` / `en-US`，影响 `template_name` / `description` / `display_name` 等展示字段，不影响 `template_id` 等机器可读字段。

## 六、鉴权与异常

- 所有接口通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 鉴权；POST JSON 请求需带 `Content-Type: application/json`。
- HTTP 状态码非 200 表示请求失败，响应体形如 `{"request_id":"...","code":"InvalidParameter","message":"File not found."}`，应优先打印 `code` + `message` 排查。
- Windows CMD 把 `${DASHSCOPE_API_KEY}` 替换为 `%DASHSCOPE_API_KEY%`，PowerShell 替换为 `$env:DASHSCOPE_API_KEY`。

## 七、常见踩坑清单

- 任务串行：同一用户只能并行 1 个训练任务，批量提交会停在 `QUEUING`，建议在调度前先列举状态。
- 超参错配：文本模型的 `n_epochs/batch_size/max_length`、CosyVoice 的 8 个 LM/FM 参数、万相视频模型的 `n_epochs/eval_epochs`、万相图像模型的 `max_steps/eval_steps` 互不兼容，必须按模型类型选用对应集合。
- LoRA 二次训练：高效微调的 `lora_rank` / `lora_alpha` / `lora_dropout` 必须与上次完全一致，否则任务会失败。
- 数据丢弃：文本模型超 `max_length` 的样本会被直接丢弃，不做截断；万相模型超 `max_pixels` 的素材会缩放（行为不同，需注意预处理策略）。
- 文件配额：100 个文件 / 5 GB 上限是租户级硬限制；批量上传可能部分成功，应处理 `failed_uploads`。
- 量化范围：模型压缩仅支持指定基础模型的全参微调产物，LoRA 与已量化模型会被过滤；想压缩 LoRA 产物需先合并权重再做全参训练。

## 来源文档

- [百炼文件管理 API](../../raw/model-api-reference/model-training/model-customization-file-management-service.md)
- [模型调优 API 参考](../../raw/model-api-reference/model-training/model-training-api-reference.md)
- [视频/图像生成模型微调 API 参考](../../raw/model-api-reference/model-training/wan-generation-finetune-api-reference.md)
- [模型压缩 API 参考](../../raw/model-api-reference/model-training/model-compression-api-reference.md)


