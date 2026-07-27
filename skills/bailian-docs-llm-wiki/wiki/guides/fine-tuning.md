# fine tuning

阿里云百炼平台的 fine tuning 功能支持对多种模态模型（文本、图像、视频、语音）进行监督微调（SFT），主要采用高效微调（LoRA）方式，在控制成本与训练时长的同时，显著提升模型在特定任务、风格或安全合规等维度的表现。该能力仅在华北2（北京）地域可用，需使用对应地域的 API Key，并为子账号授予模型调用、训练和部署权限 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

## 支持的模型/功能

fine tuning 当前覆盖四大类模型：

- **文本生成模型**：支持 Qwen 系列（如 `qwen3-8b`, `qwen3-14b`, `qwen2.5-7b-instruct`）、千问-Plus-Character 等，提供 SFT、CPT、DPO 三种训练方式，其中 SFT 高效训练（`efficient_sft`）为默认推荐方案 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解模型（千问VL）**：支持 `qwen3-vl-8b-instruct` 等，支持 SFT 和 DPO 训练，数据格式需遵循 ChatML 规范，`system` 消息的 `content` 必须为数组格式 `[{"text":"..."}]`。
- **图像生成模型（万相）**：仅支持 `wan2.7-image-pro` 和 `wan2.7-image`，采用 SFT-LoRA 方式，适用于文生图（t2i）与图生图（i2i）两种模式 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成模型（万相）**：支持 `wan2.7-i2v`、`wan2.5-i2v-preview`、`wan2.2-i2v-flash`（首帧）及 `wan2.2-kf2v-flash`（首尾帧），同样基于 SFT-LoRA [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成模型（CosyVoice）**：仅支持 `cosyvoice-v3-flash`，且**当前仅可通过 API 发起调优，控制台暂不支持**，产物为独立部署的单音色模型，调用时 `voice` 参数固定为 `default` [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

> **注意**：文档 3 中表格显示 `Qwen3.7-Plus-2026-05-26` 的 SFT 全参训练（sft）列为“支持”，但文档 4 明确指出“如果您是第一次进行模型调优，请选择您期望的官方模型”，且文档 6 的实操案例中明确使用 `Qwen3-8B` 并强调其支持 LoRA；结合文档 3 备注“Qwen3.7-Plus-2026-05-26 调优后部署请联系商务经理”，可判定该模型的 SFT 全参训练为邀测或受限功能，生产环境应优先选用 `efficient_sft`。

## 关键参数

不同模态模型的超参数命名与含义存在差异，开发者需按模型类型选用：

- **通用文本/视觉模型（API）**：核心必填参数包括 `n_epochs`（循环次数）、`batch_size`（批次大小）、`max_length`（序列长度）、`learning_rate`（学习率）。推荐值因训练方式而异：高效训练（LoRA）学习率建议 `1e-4` 量级，全参训练建议 `1e-5` 量级 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **图像生成模型（万相）**：关键参数为 `max_steps`（总步数）、`eval_steps`（验证间隔）、`learning_rate`、`generation_type`（`t2i` 或 `i2i`）、`max_pixels`/`val_img_size`/`max_token_length`（三者建议保持一致，如 `"2k"`）、`lora_rank`（必须为 2 的幂，如 32）。
- **视频生成模型（万相）**：核心参数为 `n_epochs`、`batch_size`（不同模型推荐值不同，如 `wan2.7-i2v` 推荐为 1）、`learning_rate`、`eval_epochs`、`max_pixels`（整型，单位为像素总数，如 102400）。
- **语音合成模型（CosyVoice）**：参数解耦为 LM（语言模型）与 FM（流匹配模型）两套，如 `lm_max_epoch`、`fm_max_epoch`、`lm_batch_size`、`fm_batch_size`，二者共同决定最终效果与 [Token](../concepts/token.md) 消耗。

所有模型均支持 `lora_rank`（LoRA 秩值）和 `lora_alpha`（缩放因子），其取值需为 2 的幂（如 16、32、64）。

## 使用方式

标准流程为四步：上传数据集 → 创建微调任务 → 查询训练状态 → 部署并调用。

1. **上传数据集**：将训练数据（ZIP 包或 OSS 路径）通过 `/api/v1/files` 接口上传，获取 `file_id`。ZIP 包需满足：`data.jsonl` 位于根目录，图片/音频文件名全局唯一，文件名仅含 ASCII 字符 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
2. **创建微调任务**：调用 `/api/v1/fine-tunes`，传入 `model`、`training_datasets`（含 `file_id`）、`training_type`（如 `efficient_sft`）及 `hyper_parameters`。图像/视频模型使用 `training_file_ids` 字段，文本/视觉模型使用 `training_datasets` 数组。
3. **查询状态**：轮询 `/api/v1/fine-tunes/{job_id}`，直至 `output.status` 变为 `SUCCEEDED`。CosyVoice 任务可能经历 `QUEUING` 状态（平台同一时刻仅运行一个训练任务）。
4. **部署与调用**：训练成功后，使用 `finetuned_output` 作为 `model_name` 调用 `/api/v1/deployments` 部署；待 `status` 变为 `RUNNING` 后，即可像调用基础模型一样发起推理请求（如图像生成需指定 `X-DashScope-Async: enable`）。

## 限制和注意事项

- **地域与权限**：所有 fine tuning 功能均**仅限华北2（北京）地域**，且必须使用该地域的 API Key。RAM 子账号需被授予 `AliyunDashScopeFullAccess` 或等效的模型调用、训练、部署权限 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **数据与文件**：图像分辨率建议控制在 `8K` 以内；视频文件最大支持 `2GB`（公网 URL）；ZIP 包最大 `2GB`；单个文件上传上限 `300MB`（API）。
- **计费**：按训练消耗的 [Token](../concepts/token.md) 总数计费，公式为 `Token 总数 × 训练单价`。CosyVoice 单价为 `0.2 元/千 Tokens`，Qwen 系列从 `0.003 元/千 Tokens`（qwen3-0.6b）到 `0.35 元/千 Tokens`（qwen3.7-plus）不等 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **产物特性**：微调产物为独立模型（新 `model_name`），非基础模型下的配置项。例如 CosyVoice 调优后仅支持 `voice="default"`，不再具备声音复刻能力；万相微调模型调用时需包含触发词（如 `s86b5p`）以激活 LoRA 风格。
- **安全合规**：SFT 是强化模型安全对齐的有效手段，可用于训练模型主动拒绝高危请求并引导正面价值观，但需使用高质量、覆盖多维度风险的训练数据 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


