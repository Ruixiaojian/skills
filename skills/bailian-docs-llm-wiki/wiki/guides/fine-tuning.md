# fine tuning

fine tuning（微调）是阿里云百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练大模型进行定制化训练，以提升其在特定任务、领域或风格上的表现。它适用于当 Prompt 工程、[插件](../concepts/plugin.md)调用等轻量级优化手段无法满足业务精度、一致性或可控性要求的场景。微调支持多种训练范式（SFT、CPT、DPO、RL），并覆盖文本、图像、视频、语音等[多模态](../concepts/multimodal.md)模型。

## 支持的模型/功能

百炼平台支持多种微调方式与模型类型，具体能力取决于模型本身和地域限制。所有微调功能当前**仅在华北2（北京）地域可用**，且必须使用该地域的 API Key [原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **文本生成模型**：支持 SFT（全参/LoRA）、CPT、DPO 三种训练方式。Qwen 系列（如 `qwen3-8b`, `qwen3.5-9b`）及千问 VL 系列（如 `qwen3-vl-8b-instruct`）均提供高效训练（`efficient_sft`）选项 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉生成模型**：万相（Wan）系列支持 SFT-LoRA 微调，包括图生图（`wan2.7-image-pro`）、文生图（`wan2.7-image`）及图生视频（`wan2.7-i2v`, `wan2.2-kf2v-flash`）等 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **语音合成模型**：CosyVoice (`cosyvoice-v3-flash`) 仅支持 `efficient_sft` 方式，用于同一发音人的高还原度音色定制 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **强化学习（RL）**：支持通过 Reward 信号驱动策略优化，适用于数学推理、Agent 工具调用等需自主探索的场景，但需联系商务经理开通 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 4 和文档 7 的模型支持矩阵存在不一致。文档 4 明确列出 `qwen3.5-9b` 支持 `efficient_sft`，而文档 7 的表格中该模型对应 `efficient_sft` 列为空白。应以控制台实时显示或文档 4 为准，实际调用前请务必在控制台确认模型支持的 `training_type`。

## 关键参数

不同模型和训练方式的关键参数差异较大，但核心超参具有通用含义：

- **`training_type`**：必填，指定训练方法。常用值包括 `sft`（全参微调）、`efficient_sft`（LoRA 高效微调）、`cpt`、`dpo_full`、`dpo_lora`。CosyVoice 和万相视频模型强制使用 `efficient_sft` [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **`model`**：必填，基础模型 ID（如 `wan2.7-i2v`, `qwen3-8b`, `cosyvoice-v3-flash`）。
- **`hyper_parameters`**：
  - **学习率 (`learning_rate`)**：控制权重更新幅度。推荐值因模型而异：文本 SFT 通常为 `1e-4`（LoRA）或 `1e-5`（全参）；万相图像生成为 `3e-5`；万相视频生成为 `2e-5`；CosyVoice 无此字段。
  - **批次大小 (`batch_size`)**：影响显存占用和收敛速度。万相视频模型 `wan2.7-i2v` 推荐 `1`，而 `wan2.2-kf2v-flash` 推荐 `4`；文本模型 `qwen3-8b` 推荐 `16`。
  - **训练轮次/步数**：文本 SFT 用 `n_epochs`（如 `3`），图像生成用 `max_steps`（如 `800`），CosyVoice 用 `lm_max_epoch`/`fm_max_epoch`（如 `60`/`100`）。
  - **LoRA 参数**：`lora_rank`（秩，如 `32`）和 `lora_alpha`（缩放系数，如 `32`）决定低秩适配器的容量与强度。
- **`training_datasets` / `training_file_ids`**：指定训练数据来源。支持 `file_id`（上传的 zip/jsonl 文件）和 `oss_mount`（OSS 挂载）两种方式，后者不支持 zip 压缩包 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

## 使用方式

微调流程标准化为三步：上传数据 → 创建任务 → 部署模型。

1. **上传数据集**：将符合格式要求的数据（如 `data.jsonl` 或 `train_data.zip`）通过 `/api/v1/files` 接口上传，获取 `file_id`。单个文件上限为 300MB，总空间配额为 100GB [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
2. **创建微调任务**：调用 `/api/v1/fine-tunes` 接口，传入 `model`、`training_file_ids` 和 `hyper_parameters`。任务创建后返回 `job_id` 和 `finetuned_output`（新模型名）。任务状态初始为 `PENDING`，需轮询查询直至变为 `SUCCEEDED`。
3. **部署与调用**：训练成功后，使用 `finetuned_output` 作为 `model_name` 调用 `/api/v1/deployments` 接口部署为在线服务。部署完成后状态为 `RUNNING`，即可通过标准 API 调用该专属模型。

对于零代码需求，控制台提供可视化向导，支持数据选择、超参配置和一键训练 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

## 限制和注意事项

- **地域与权限**：所有微调操作必须在华北2（北京）地域进行，并确保子账号已授予 `model:Train`, `model:Deploy`, `model:Invoke` 等必要权限 [原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **数据格式**：SFT 文本数据必须为 `jsonl` 格式，遵循 ChatML messages 结构；[多模态](../concepts/multimodal.md)（图像/视频）数据需打包为 zip，内含 `data.jsonl` 和对应媒体文件；CosyVoice 数据需严格按 `user_data/` 目录结构组织 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **计费模式**：文本/图像/视频微调按训练消耗的 [Token](../concepts/token.md) 总数计费；CosyVoice 微调费用 = `(lm_max_epoch + fm_max_epoch) × 25 × 总秒数 × 0.2 元/千 Tokens`；RL 训练必须使用模型训练单元（MTU），不支持 [Token](../concepts/token.md) 计费 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
- **能力边界**：微调无法扩展基础模型的固有能力，例如 CosyVoice 微调不能新增语种支持，万相视频微调无法改变其支持的输入帧数范围 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 来源文档

- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


