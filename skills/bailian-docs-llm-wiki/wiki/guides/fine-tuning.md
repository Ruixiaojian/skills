# fine tuning

fine tuning（微调）是百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练大模型进行定制化训练，从而提升其在特定业务场景、领域知识或安全合规要求下的表现。该能力覆盖文本生成、视觉理解、语音合成和视频生成等多种模态，并支持 SFT、DPO、CPT、RL 等多种训练范式。所有微调任务均需在华北2（北京）地域执行，且依赖 DashScope API Key 与相应 RAM 权限。

## 支持的模型与功能

百炼平台支持多模态、多阶段的 fine tuning，具体能力按模型类型划分：

- **文本生成模型**：支持 Qwen3 系列（如 `qwen3-8b`, `qwen3.5-9b`）、Qwen2.5 系列及千问-Plus-Character 等数十种模型，提供 CPT（持续预训练）、SFT（监督微调）、DPO（直接偏好优化）三种训练方式，其中 SFT 和 DPO 均支持全参训练与 LoRA 高效训练 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解模型（千问VL）**：支持 `qwen3-vl-8b-instruct` 等 VL 模型的 SFT 和 DPO 训练，输入支持图像、视频帧列表及视频文件路径等多种格式，需严格遵循 ChatML 数据结构与压缩包目录规范 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **图像生成模型（万相）**：仅支持 `wan2.7-image-pro` 和 `wan2.7-image`，采用 SFT-LoRA 方式，分文生图（t2i）与图生图（i2i）两种模式，需上传 ZIP 格式训练集并指定 `generation_type` 参数 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成模型（万相）**：支持 `wan2.7-i2v`、`wan2.2-kf2v-flash` 等模型，同样基于 SFT-LoRA，区分“基于首帧”与“基于首尾帧”两类任务，超参中 `batch_size` 和 `max_pixels` 因模型而异，不可混用 [原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成模型（CosyVoice）**：当前仅支持 `cosyvoice-v3-flash` 的 SFT 高效微调，目标为同一发音人的高还原度音色定制，产物为独立部署的单音色模型，不支持语种扩展或指令控制 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **强化学习（RL）训练**：面向 Agent 场景，支持 `qwen3.5-9b` 等非 MoE 模型及 `qwen3.6-flash-2026-04-16` 等 MoE 模型，需通过 MTU 训练单元计费，不支持 [Token](../concepts/token.md) 计费 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 4 与文档 5 在“训练方式推荐”上存在矛盾。文档 4 明确指出“阿里云百炼推荐您如果**模型支持全参训练，请优先选择全参训练**，因为全参训练效果比高效训练效果要好，性价比更高”；而文档 8 的实操案例却默认选用高效训练（LoRA），并强调其“速度快、成本低”“更具性价比”。实际选型应依据业务目标权衡：生产环境追求效果上限时优先全参训练；快速验证或资源受限时可选 LoRA。

## 关键参数

不同训练类型的关键参数差异显著，开发者需按任务类型准确配置：

- **通用超参（文本/SFT/DPO）**：`learning_rate`（SFT 推荐 `3e-4`，DPO 推荐 `1e-5`）、`n_epochs`（数据量 < 10k 时设 3~5）、`batch_size`（通常 16 或 32）、`eval_steps`（默认 50）、`lora_rank`（LoRA 秩，默认 8，图像生成中为 32）、`max_length`（默认 8192）[原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **图像生成专用参数**：`generation_type`（必填 `"t2i"` 或 `"i2i"`）、`max_pixels`（文生图 `"2k"`，图生图 `"1k"`）、`val_img_size`（同 `max_pixels`）、`max_token_length`（同 `max_pixels`）[原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成专用参数**：`batch_size`（`wan2.7-i2v` 必须为 1，`wan2.2-kf2v-flash` 推荐为 4）、`max_pixels`（整数，如 `102400`，非字符串）、`n_epochs`（需结合数据量换算总步数 ≥ 800）[原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **CosyVoice 专用参数**：分为 LM（语言模型）与 FM（流匹配模型）两套子参数，如 `lm_max_epoch=60`、`fm_max_epoch=100`、`lm_batch_size=1000`、`fm_batch_size=2000`，二者不可互换 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **RL 训练专用参数**：`algorithm="gspo"`、`batch_size=64`、`kl_loss_coef=0.002`、`learning_rate=2e-6`、`n_rollouts=8`，全部为 qwen3.5-9b 的必填项，MoE 模型参数需另行确认 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 使用方式

fine tuning 通过 API 或控制台两种方式执行，流程高度标准化：

1. **准备数据集**：按模态要求组织数据。文本 SFT 使用 ChatML 格式 JSONL（`{"messages":[...]}`），图像/视频需打包 ZIP 并确保 `data.jsonl` 在根目录，语音需 `wav_fn` 路径以 `train/` 开头 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
2. **上传文件**：调用 `/api/v1/files` 接口上传 ZIP 或 JSONL 文件，获取 `file_id`；OSS 挂载方式需指定 `region`、`bucket` 和 `file_path`，且不支持 ZIP [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
3. **创建训练任务**：POST `/api/v1/fine-tunes`，传入 `model`、`training_datasets`（含 `file_id` 或 OSS 配置）、`training_type`（如 `"efficient_sft"`）及 `hyper_parameters`。CosyVoice 和 RL 任务使用 `training_file_ids` 字段而非 `training_datasets` [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
4. **查询与部署**：轮询 `/api/v1/fine-tunes/{job_id}` 直至 `status="SUCCEEDED"`，提取 `finetuned_output`；再 POST `/api/v1/deployments` 部署，轮询 `/api/v1/deployments/{deployed_model}` 至 `status="RUNNING"`。
5. **调用模型**：使用 `deployed_model` 名称调用对应服务接口（如 `/services/aigc/image-generation/generation`），注意图像生成需异步调用并解析 `task_id`。

## 限制和注意事项

- **地域与权限强制约束**：所有 fine tuning 任务（含图像、视频、语音、文本、RL）**仅支持华北2（北京）地域**，且必须使用该地域的 API Key；RAM 子账号需显式授予模型调用、训练、部署权限 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **文件与数据限制**：ZIP 包最大 2 GB，单文件上传上限 300 MB；图像分辨率建议 ≤ 8K，视频文件 URL 需包含 `Content-Length` 和 `Content-Type` 响应头；CosyVoice 训练音频采样率 ≥ 16 kHz，单条时长 1~30 秒 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **计费模式差异**：API 方式仅支持 [Token](../concepts/token.md) 计费；RL 训练**强制使用 MTU 训练单元**（预付费或后付费），不支持 [Token](../concepts/token.md) 计费；CosyVoice 训练费用 = `(lm_max_epoch + fm_max_epoch) × 25 × 总秒数 × 0.2 元/千 Tokens` [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
- **产物与能力边界**：微调产物为新模型 ID（如 `xxxx-ft-...`），非基础模型下的配置项；CosyVoice 调优后 `voice` 参数锁死为 `default`，不再支持声音复刻；万相微调后仍需触发词（如 `s86b5p`）才能激活 LoRA 效果 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **训练失败排查**：任务状态为 `FAILED` 时，优先查看日志页签末尾报错；RL 任务失败需检查 FC 函数部署、DashScope SDK 版本及 `FC_PYPI_LIB` 环境变量是否匹配 whl 文件名 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)

