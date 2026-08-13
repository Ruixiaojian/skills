# fine tuning

fine tuning 是阿里云百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练模型进行定制化训练，以提升其在特定任务、领域或风格上的表现。该能力覆盖文本生成、[多模态](../concepts/multimodal.md)理解（图像/视频）、语音合成等主流模态，支持监督微调（SFT）、持续预训练（CPT）、直接偏好优化（DPO）及强化学习（RL）等多种范式，兼顾效果与成本效率。

## 支持的模型与功能

百炼平台支持[多模态](../concepts/multimodal.md)、多阶段的 fine tuning 能力：

- **文本生成模型**：支持 Qwen 系列（如 `qwen3-8b`, `qwen3-32b`）、千问 VL 系列（如 `qwen3-vl-8b-instruct`）等数十种模型，涵盖 CPT（补知识）、SFT（学做事）、DPO（做得更好）三种递进式训练方式 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
  
- **图像生成模型**：仅限华北2（北京）地域，支持 `wan2.7-image-pro` 和 `wan2.7-image`，采用 SFT-LoRA 高效微调，适用于文生图（t2i）和图生图（i2i）两类生成模式 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **视频生成模型**：同样限于华北2（北京）地域，支持 `wan2.7-i2v`、`wan2.2-kf2v-flash` 等模型，按“基于首帧”或“基于首尾帧”两种范式进行 LoRA 微调 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **语音合成模型**：仅通过 API 支持 `cosyvoice-v3-flash` 的 SFT 高效微调，面向同一发音人多小时录音的高还原度音色定制，不支持控制台操作 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **强化学习（RL）**：需联系商务经理开通，支持 `qwen3.5-9b` 等 MoE 或非 MoE 模型，依赖函数计算（FC）部署 Rollout/Reward 函数，按模型训练单元（MTU）计费，不支持 [Token](../concepts/token.md) 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 5 和文档 6 中关于“SFT 全参训练支持 Qwen3.5-27B”的描述与文档 1 中“图像生成仅支持 SFT-LoRA”存在隐含冲突——图像/视频生成类模型（wan 系列）**不支持全参训练**，其 `training_type` 固定为 `"efficient_sft"`，且参数中无 `n_epochs` 字段，而使用 `max_steps` 控制训练长度。此差异源于模态专用架构限制，非文档错误。

## 关键参数

不同训练方式与模态的关键超参存在显著差异，开发者需严格匹配：

- **通用 SFT/DPO 参数（文本）**：`n_epochs`（必填，循环次数）、`batch_size`（必填）、`learning_rate`（推荐默认值）、`max_length`（序列长度）、`eval_steps`（验证步数）。LoRA 模式下还需配置 `lora_rank`（默认 8）、`lora_alpha`（默认 16）等 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

- **图像生成（wan）参数**：`max_steps`（总步数，≥500）、`eval_steps`（验证间隔）、`generation_type`（`"t2i"` 或 `"i2i"`）、`max_pixels` / `val_img_size` / `max_token_length`（三者建议一致，如 `"2k"`）、`lora_rank`（必须为 2 的幂，如 32）[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **视频生成（wan）参数**：`n_epochs`（推荐 50，小数据集需更高）、`batch_size`（模型强约束，如 `wan2.7-i2v` 必须为 1）、`max_pixels`（整型像素总数，非字符串）、`lora_rank` 与 `lora_alpha`（均默认 32）[微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **语音合成（CosyVoice）参数**：解耦为 LM（语言模型）与 FM（流匹配模型）两套参数，如 `lm_max_epoch=60`、`fm_max_epoch=100`、`lm_batch_size=1000`、`fm_batch_size=2000`，全部字段均为必填 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **强化学习（RL）参数**：`algorithm="gspo"`、`batch_size=64`、`learning_rate=2e-6`、`kl_loss_coef=0.002`，且必须指定 `resources`（MTU 规格与数量）[强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 使用方式

fine tuning 流程统一为“上传数据 → 创建任务 → 查询状态 → 部署模型”，但入口与细节因模态而异：

- **API/CLI 方式（通用）**：所有模态均支持。首先调用 `/api/v1/files` 上传 `.zip`（[多模态](../concepts/multimodal.md)）或 `.jsonl`（文本）数据集，获取 `file_id`；再调用 `/api/v1/fine-tunes` 提交任务，传入 `model`、`training_datasets`（含 `file_id`）及 `hyper_parameters`；最后轮询 `/api/v1/fine-tunes/{job_id}` 直至 `status="SUCCEEDED"`，提取 `finetuned_output` [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

- **控制台方式（文本/多模态）**：适用于 SFT/CPT/DPO 文本训练及千问 VL 多模态训练。在[模型调优](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager)页面创建任务，可视化配置模型、超参、数据集（支持自动切分验证集），并一键启动 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

- **特殊模态限制**：
  - CosyVoice 语音调优**仅支持 API**，控制台不可见 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - RL 训练需先完成 FC/SLS/OpenTelemetry 授权，并使用离线 SDK 打包函数，无法通过简单 API 提交 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

训练完成后，均需调用 `/api/v1/deployments` 部署 `finetuned_output` 为在线服务，再通过标准推理 API 调用（如 `qwen3-8b-ft-xxx`）。

## 限制和注意事项

- **地域与权限**：图像/视频生成、CosyVoice、DPO/CPT 及 OSS 挂载均**仅限华北2（北京）地域**；子账号需显式授予 `dashscope:FineTune*`、`dashscope:Deploy*` 等权限 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **数据格式强约束**：
  - 文本 SFT/DPO 必须为 `.jsonl`，每行含 `messages` 数组（ChatML 格式）；DPO 额外要求 `chosen`/`rejected` 字段 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
  - 图像/视频训练需 `.zip` 包含 `data.jsonl` + 原始媒体文件，图片分辨率≤1024px，单图≤10MB [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
  - CosyVoice 数据包必须为 `user_data/data.jsonl` + `user_data/train/*.wav` 结构，`text` 字段禁止含 SSML/LaTeX [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **计费与资源**：
  - 文本/图像/视频调优按 **[Token](../concepts/token.md) 消耗计费**（训练数据 [Token](../concepts/token.md) × 循环次数 × 单价）；RL 训练**强制使用 MTU 训练单元**，不支持 Token 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
  - CosyVoice 调优费用 = （LM + FM 轮次）× 25 × 总音频秒数 × 0.2元/千Token，部署另计模型单元时长费 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **模型产物特性**：
  - LoRA 微调产物为轻量级适配器，部署后 `plan="lora"`；全参微调产物为完整模型快照 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
  - CosyVoice 调优产物为**单音色独立模型**，`voice` 参数固定为 `"default"`，不再支持声音复刻或设计 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


