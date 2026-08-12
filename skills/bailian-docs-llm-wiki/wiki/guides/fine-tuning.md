# fine tuning

fine tuning（微调）是百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练模型进行定制化训练，从而提升其在特定任务、领域或风格上的表现。该能力覆盖文本、图像、视频、语音等多种模态，支持 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化）、RL（强化学习）等多种训练范式，且默认采用 LoRA 等高效微调技术以平衡效果与成本。所有微调任务均需在华北2（北京）地域执行，并依赖 DashScope API Key 与相应 RAM 权限。

## 支持的模型/功能

百炼平台支持多模态、多阶段的 fine tuning，具体能力按模型类型和训练方式划分：

- **文本生成模型**：支持全参训练与 LoRA 高效训练（`sft` / `efficient_sft`），覆盖 Qwen3 系列（如 `qwen3-8b`, `qwen3.5-9b`）、Qwen2.5 系列及千问-Plus-Character 等数十种模型；同时支持 CPT（注入领域知识）和 DPO（对齐人类偏好）[原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解模型（千问VL）**：支持 `efficient_sft` 微调，适用于图片/视频理解场景，要求训练数据为 zip 包（含 `data.jsonl` 和对应图片文件），且单图宽高均不超过 1024 px [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **图像生成模型（万相）**：仅支持 SFT-LoRA 微调，适用模型为 `wan2.7-image-pro` 和 `wan2.7-image`，需指定 `generation_type: "t2i"`（文生图）或 `"i2i"`（图生图）[原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成模型（万相）**：支持 `wan2.7-i2v`、`wan2.5-i2v-preview`、`wan2.2-i2v-flash`（首帧）及 `wan2.2-kf2v-flash`（首尾帧）等模型，训练方式同为 `efficient_sft` [原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成模型（CosyVoice）**：当前仅支持 `cosyvoice-v3-flash` 的 `efficient_sft` 微调，用于同一发音人的高还原度音色定制，不支持 CPT/DPO [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **强化学习（RL）**：支持 `qwen3.5-9b` 等 MoE/非 MoE 模型，需通过 SDK 提交任务并配置 Rollout/Reward 函数，**仅支持 MTU 训练单元计费**，不支持 [Token](../concepts/token.md) 计费 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 4 与文档 8 均列出 `qwen3.7-plus-2026-05-26` 支持 SFT 全参训练，但文档 4 明确标注“调优后部署请联系商务经理”，而文档 8 未提此限制；实际使用前应以控制台实时配置为准，避免因权限或资源未开通导致部署失败。

## 关键参数

不同模态和训练方式的关键参数存在显著差异，开发者需严格按场景选用：

- **通用超参（文本/SFT）**：`n_epochs`（必填，推荐 1–5）、`learning_rate`（SFT 高效训练推荐 `1e-4` 量级，全参训练推荐 `1e-5`）、`batch_size`（推荐 16/32）、`max_length`（建议设为模型最大支持值）[原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **LoRA 专用参数**：`lora_rank`（秩值，推荐设为模型支持的最大值）、`lora_alpha`（缩放系数，常与 `lora_rank` 相同）、`lora_dropout`（推荐 0.1）；`freeze_vit` 仅对千问VL模型有效，设为 `true` 可启用 [Token](../concepts/token.md) 计费 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **图像/视频生成参数**：`max_pixels`（训练图最大分辨率，如 `"2k"`）、`val_img_size`（验证图分辨率）、`max_token_length`（如 `"2k"`），三者建议保持一致；`generation_type` 必须显式指定为 `"t2i"` 或 `"i2i"` [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成特有参数**：`batch_size` 因模型而异（`wan2.7-i2v` 推荐 1，`wan2.2-kf2v-flash` 推荐 4）、`max_pixels` 为整数（如 `102400`），且 `eval_epochs` 需 ≥ `n_epochs/10` [原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成参数**：解耦为 LM（影响韵律）与 FM（影响音色）两套参数，如 `lm_max_epoch=60`、`fm_max_epoch=100`，`*_batch_size` 为千级大数值（如 `1000`）[原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 使用方式

fine tuning 通过 API 或控制台两种方式执行，流程高度标准化：

1. **准备数据集**：按模态要求构造数据。文本 SFT 使用 `jsonl`（ChatML 格式），图像/视频 SFT 使用 `zip`（含 `data.jsonl` + 图片/视频文件），语音 SFT 使用 `zip`（含 `data.jsonl` + `.wav` 文件）。所有数据必须上传至百炼平台获取 `file_id`，或通过 OSS 挂载（需授权）[原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
2. **创建微调任务**：调用 `/api/v1/fine-tunes` 接口，传入 `model`、`training_datasets`（含 `file_id` 或 `oss_mount` 配置）、`training_type`（如 `"efficient_sft"`）及 `hyper_parameters`。注意：图像/视频任务需在 `hyper_parameters` 中指定 `generation_type`，语音任务需完整填写 `lm_*`/`fm_*` 八个字段 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
3. **查询任务状态**：轮询 `/api/v1/fine-tunes/{job_id}` 直至 `status` 变为 `"SUCCEEDED"`，此时 `finetuned_output` 即为新模型名称。
4. **部署模型**：调用 `/api/v1/deployments`，传入 `model_name`（即 `finetuned_output`）及 `plan: "lora"`。图像/视频模型部署时需额外配置 `aigc_config`（如 `use_input_prompt: false`），语音模型部署则需指定模型单元模板 [原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

> **注意**：CosyVoice 模型调优**仅支持 API 方式**，控制台暂不提供入口 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)；而 RL 训练必须使用离线 SDK 并完成 FC/SLS/OpenTelemetry 三项服务授权，无法通过简单 API 调用完成 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 限制和注意事项

- **地域与权限**：所有 fine tuning 任务**仅限华北2（北京）地域**，且子账号需被授予模型调用、训练、部署权限 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **数据限制**：文本 `jsonl` 单文件 ≤ 200 MB；图像 SFT 要求单图宽高 ≤ 1024 px、大小 ≤ 10 MB；视频 SFT 要求首帧/首尾帧视频文件 ≤ 2 GB（URL 上传）或 ≤ 100 MB（本地上传）；语音 SFT 要求 `.wav` 采样率 ≥ 16 kHz、单条时长 1–30 秒 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **计费模式**：文本/图像/视频 SFT 默认按 [Token](../concepts/token.md) 计费；RL 训练**强制使用 MTU 训练单元**（预付费/后付费），不支持 Token 计费；CosyVoice 同时产生训练费（0.2 元/千 Tokens）与部署费（按模型单元时长）[原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
- **产物特性**：微调产物为独立模型（非基础模型下的音色 ID 或 LoRA [插件](../concepts/plugin.md)），调用时需使用 `finetuned_output` 名称；CosyVoice 产物固定 `voice="default"`，不可切换音色；万相微调模型部署后需在 `aigc_config` 中设置 `use_input_prompt: false` 以启用 LoRA 特效 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **调试建议**：若训练中出现过拟合（Training Loss ↓, Validation Loss ↑），应减少 `n_epochs`、增大 `weight_decay` 或提高 `lora_dropout`；若欠拟合（两者均未收敛），可增加 `n_epochs` 或 `lora_rank` [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)


