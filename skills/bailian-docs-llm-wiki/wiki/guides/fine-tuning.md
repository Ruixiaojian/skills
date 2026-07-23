# fine tuning

fine tuning 是指在预训练大模型基础上，使用特定领域或任务的数据进行二次训练，以提升模型在该场景下的效果。百炼平台支持多种调优方式（SFT、CPT、DPO）和多种模态（文本、图像、视频、语音），所有调优任务均需在华北2（北京）地域执行，并依赖有效的 API Key 和相应 RAM 权限。调优产物为独立部署的新模型，而非基础模型的配置扩展。

## 支持的模型/功能

百炼平台支持多模态、多训练方式的 fine tuning：

- **文本生成模型**：支持 Qwen 系列（如 `qwen3-8b`、`qwen2.5-7b-instruct`）、千问-Plus-Character 等，覆盖 CPT、SFT（全参/LoRA）、DPO（全参/LoRA）[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解（千问VL）**：支持 `qwen3-vl-8b-instruct` 等 VL 模型的 SFT 高效训练，需遵循特定 ChatML 格式，且 `system` 消息的 `content` 必须为数组格式 `[{"text":"..."}]` [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **图像生成模型**：支持 `wan2.7-image-pro`、`wan2.7-image` 的 SFT-LoRA 微调，适用于文生图与图生图场景 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成模型**：仅支持万相系列（如 `wan2.7-i2v`、`wan2.2-kf2v-flash`）的 SFT-LoRA 微调，且仅限华北2（北京）地域 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成模型**：仅支持 `cosyvoice-v3-flash` 的 SFT 高效微调（`efficient_sft`），**控制台暂不支持，必须通过 API 发起** [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

> **注意**：文档 4 中称“阿里云百炼推荐您如果**模型支持全参训练，请优先选择全参训练**”，但文档 1、2、7 均明确限定仅支持 `efficient_sft`（LoRA）。实际生产中，图像、视频、语音类模型仅提供 LoRA 微调，该矛盾需以具体模型文档为准。

## 关键参数

不同模态和模型类型的关键参数存在显著差异，开发者需严格按对应文档配置：

- **通用超参**（文本/视觉）：
  - `learning_rate`：文本 SFT 推荐 `3e-4`（高效训练）或 `1e-5`（全参训练）；图像生成推荐 `3e-5`；视频生成固定为 `2e-5`。
  - `n_epochs` / `max_steps`：文本 SFT 默认 `3`，图像生成用 `max_steps=800`，视频生成用 `n_epochs=50`（小数据集）。
  - `batch_size`：文本默认 `16`；图像生成依 `generation_type` 推荐 `t2i:1`/`i2i:4`；视频生成依模型不同为 `1` 或 `4`。
  - `lora_rank` / `lora_alpha`：图像/视频生成推荐 `32`；文本 LoRA 默认 `8`/`16`。

- **模态特有参数**：
  - 图像生成：`max_pixels`（如 `"2k"`）、`val_img_size`（如 `"2k"`）、`generation_type`（`"t2i"` 或 `"i2i"`）。
  - 视频生成：`max_pixels`（像素总数，如 `102400`）、`split`（训练集划分比例，默认 `0.9`）。
  - 语音合成（CosyVoice）：`lm_max_epoch`（LM 训练轮次，推荐 `60`）、`fm_max_epoch`（FM 训练轮次，推荐 `100`），二者共同决定音色还原度与韵律。

- **必填项**：所有 API 调用中，`model`、`training_type`、`training_datasets`（或 `training_file_ids`）及核心超参（如 `n_epochs`、`batch_size`、`max_length`）均为必填，缺失将导致请求失败。

## 使用方式

fine tuning 全流程分为四步，各模态基本一致，但细节差异显著：

1. **准备并上传数据集**  
   - 文本/视觉：需按 ChatML 格式组织 `data.jsonl`，ZIP 包内 `data.jsonl` 必须位于根目录，图片/视频文件名全局唯一 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。  
   - 图像/视频：提供官方样例 ZIP（如 `wan-image-t2i-training-dataset.zip`），上传时 `purpose="fine-tune"`。  
   - 语音：`data.jsonl` 每行含 `wav_fn`（路径前缀必须为 `train/`）和 `text`，音频为 `.wav` 格式，总时长建议 1–10 小时 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

2. **创建微调任务**  
   - 调用 `POST /api/v1/fine-tunes`，传入 `file_id` 或 `training_datasets`，指定 `model` 和 `training_type`（如 `"efficient_sft"`）。  
   - 响应中 `finetuned_output` 为后续部署必需的模型 ID。

3. **查询任务状态**  
   - 轮询 `GET /api/v1/fine-tunes/{job_id}`，直至 `status` 变为 `"SUCCEEDED"`。视频/语音任务耗时数小时，文本/图像通常数十分钟。

4. **部署与调用**  
   - 部署：`POST /api/v1/deployments`，传入 `model_name`（即 `finetuned_output`）和 `plan="lora"`（图像/视频/语音）或 `plan="full"`（文本全参）。  
   - 调用：使用 `deployed_model` 名称发起推理请求，**注意**：微调后模型通常需异步调用（`X-DashScope-Async: enable`），且输入参数（如 `prompt`、`input.media`）需严格匹配原始模型 API 规范。

## 限制和注意事项

- **地域与权限**：所有 fine tuning 操作**强制要求华北2（北京）地域**，且 API Key、OSS Bucket（若挂载）必须同地域。RAM 子账号需显式授予 `dashscope:CreateFineTuneJob`、`dashscope:DeployModel` 等权限 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **数据与成本**：  
  - 图像/视频训练集最小规模要求未明示，但文档 1 提示“50–60 条视频时建议训练 3000–5000 steps”，暗示小样本需更高 epoch。  
  - CosyVoice 训练费用 = `(lm_max_epoch + fm_max_epoch) × 25 × 总秒数 × 0.2元/千Token`，成本随数据量线性增长 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
- **能力边界**：  
  - 微调**无法扩展基础模型能力**：CosyVoice 不能通过调优支持新语种；万相视频模型无法通过微调新增提示词控制能力 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
  - 微调产物为**独立模型**：调用时 `model` 参数必须为 `finetuned_output`，不可与基础模型混用；CosyVoice 产物 `voice` 固定为 `"default"`，失去声音复刻能力。  
- **工程实践**：  
  - 文档 3 明确指出“模型调优也通常作为改进模型表现‘最后的手段’”，应优先尝试 [Prompt 工程](../concepts/prompt-engineering.md)与插件调用 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。  
  - 安全合规类 SFT（如拒绝有害请求）需高质量正负样本，且评测必须使用**未参与训练的独立数据集**，否则结果不可靠 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 来源文档

- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


