# fine tuning

fine tuning 是阿里云百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练模型进行定制化训练，以提升其在特定任务、领域或风格上的表现。该能力覆盖文本生成、[多模态](../concepts/multi-modal.md)理解（图像/视频）、语音合成等多种模态，并支持监督微调（SFT）、持续预训练（CPT）、直接偏好优化（DPO）及强化学习（RL）等多种训练范式。所有 fine tuning 任务均需在华北2（北京）地域执行，并依赖 DashScope API Key 进行身份认证与资源调度。

## 支持的模型与功能

百炼平台支持多种模型类型的 fine tuning，具体能力因模态和模型而异：

- **文本生成模型**：支持 SFT（全参/LoRA）、CPT、DPO 三种方式。Qwen3 系列（如 `qwen3-8b`, `qwen3-14b`）、Qwen2.5 系列及千问-Plus-Character 等均支持高效训练（`efficient_sft`），部分大模型（如 `qwen3-32b`）还支持全参训练与 DPO [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
  
- **[多模态](../concepts/multi-modal.md)模型（千问VL）**：支持 SFT 和 DPO，但仅限于 `qwen3-vl-*` 和 `qwen2.5-vl-*` 系列，且不支持 CPT [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

- **图像生成模型（万相）**：仅支持 SFT-LoRA 微调，适用模型为 `wan2.7-image-pro` 和 `wan2.7-image`，且必须在华北2（北京）地域使用 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **视频生成模型（万相）**：支持图生视频（首帧/首尾帧）的 SFT-LoRA 微调，模型包括 `wan2.7-i2v`、`wan2.5-i2v-preview`、`wan2.2-i2v-flash` 及 `wan2.2-kf2v-flash` [原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **语音合成模型（CosyVoice）**：当前仅支持 `cosyvoice-v3-flash` 的 SFT 高效微调（`efficient_sft`），控制台暂不支持，必须通过 API 发起 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **强化学习（RL）**：支持 Qwen3.5-9B、Qwen3.6-flash 等 MoE 模型，但需联系商务经理开通权限，且**仅支持模型训练单元（MTU）计费，不支持按 [Token](../concepts/token.md) 计费** [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 4 和文档 6 中关于 `qwen3.7-plus-2026-05-26` 的部署说明存在矛盾——文档 4 称“调优后部署请联系商务经理”，而文档 6 的支持矩阵中将其列为 SFT 全参训练“支持”，未提部署限制。实际部署前请务必确认该模型的商用许可状态。

## 关键参数

不同训练方式和模型类型对应的关键超参数差异较大，以下为通用核心参数及其典型取值：

| 参数 | 类型 | 必填 | 说明 | 推荐值/范围 |
|------|------|------|------|-------------|
| `training_type` | string | 是 | 训练方法标识 | `sft`, `efficient_sft`, `cpt`, `dpo_full`, `dpo_lora` |
| `model` | string | 是 | 基础模型 ID | 如 `qwen3-8b`, `wan2.7-image-pro`, `cosyvoice-v3-flash` |
| `n_epochs` / `max_steps` | int | 是 | 训练轮次或总步数 | 文本 SFT：3–5；图像/视频：依数据量设 ≥500；CosyVoice：LM=60, FM=100 |
| `learning_rate` | float | 是 | 学习率 | LoRA：`1e-4` 量级；全参：`1e-5` 量级；CosyVoice：默认 `2e-5` |
| `batch_size` | int | 是 | 单次训练样本数 | 文本：16/32；万相图像：1；万相视频：1–4；CosyVoice：LM=1000, FM=2000 |
| `lora_rank` | int | 是（LoRA） | LoRA 低秩矩阵维数 | 必须为 2 的幂（16/32/64），图像/视频推荐 32 |
| `lora_alpha` | int | 否（LoRA） | LoRA 权重缩放系数 | 通常与 `lora_rank` 相同（如 32） |
| `eval_steps` / `eval_epochs` | int | 是 | 验证间隔步数/轮数 | 文本：50；万相图像：200；万相视频：20；CosyVoice：LM=5, FM=10 |

其他重要参数包括 `max_length`（文本序列长度）、`max_pixels`（图像/视频分辨率上限）、`val_img_size`（验证图尺寸）、`lm_max_epoch`/`fm_max_epoch`（CosyVoice 子网络轮次）等，具体约束请参考各模型文档。

## 使用方式

fine tuning 任务可通过控制台或 API 两种方式发起，二者流程一致，但 API 提供更高灵活性：

1. **准备数据集**：按训练方式要求构造数据文件。SFT 文本需为 `jsonl` 格式（ChatML 结构）；SFT 图像/视频需为 `.zip` 包（含 `data.jsonl` + 原始媒体文件）；CosyVoice 需为 `.zip`（含 `data.jsonl` + `.wav` 文件）；RL 需为 `jsonl`（含 `messages` 和 `rollout_extra` 字段）[原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。

2. **上传数据**：调用 `/api/v1/files` 接口上传文件，获取 `file_id`。单文件上限 300MB，总配额 100GB [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

3. **创建训练任务**：调用 `/api/v1/fine-tunes`，传入 `model`、`training_datasets`（含 `file_id` 或 OSS 挂载配置）、`hyper_parameters` 等。CosyVoice 任务仅支持 `training_file_ids` 字段，不支持 `training_datasets` [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

4. **查询与监控**：轮询 `/api/v1/fine-tunes/{job_id}` 直至 `status` 变为 `SUCCEEDED`。训练耗时因模型与数据量而异：万相图像约 77 分钟（300 步），CosyVoice 生产级训练需数小时 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

5. **部署与调用**：训练成功后，使用 `finetuned_output` 作为 `model_name` 调用 `/api/v1/deployments` 部署为在线服务。部署成功后（`status: RUNNING`），即可用标准推理 API 调用新模型。

## 限制和注意事项

- **地域与权限**：所有 fine tuning 任务**仅支持华北2（北京）地域**，且必须使用该地域的 API Key。RAM 子账号需显式授予模型调用、训练、部署权限 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **计费模式**：
  - 文本/[多模态](../concepts/multi-modal.md)/图像/视频微调：按训练消耗 [Token](../concepts/token.md) 数计费（单价见文档 4）。
  - CosyVoice：训练按 [Token](../concepts/token.md) 计费（¥0.2/千 Tokens），部署按模型单元时长计费。
  - RL 训练：**强制使用模型训练单元（MTU）计费，不支持 Token 计费** [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

- **数据与格式限制**：
  - 图像输入：单张宽高 ≤1024px，大小 ≤10MB；视频输入：时长 2秒–2小时，大小 ≤2GB（URL 方式）。
  - SFT `jsonl` 文件单个上限 200MB；CosyVoice `data.jsonl` 中 `wav_fn` 必须以 `train/` 开头。
  - RL 数据必须包含 `messages` 和 `rollout_extra` 字段，且 `rollout_extra` 会透传至 Reward 函数用于评分 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

- **工程实践建议**：
  - 初次训练建议先用小数据集（如 150 条音频、几百条文本）验证流程，再扩展规模。
  - 训练中若出现过拟合（Training Loss ↓，Validation Loss ↑），应减少 `n_epochs`、增大 `weight_decay` 或提高 `lora_dropout`。
  - CosyVoice 调优产物为单音色独立模型，`voice` 参数固定为 `default`，不再支持声音复刻或设计 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **安全合规**：SFT 可用于强化模型安全能力（如拒绝敏感请求），但需确保训练数据符合中国法律法规及阿里云算法安全规范 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)


