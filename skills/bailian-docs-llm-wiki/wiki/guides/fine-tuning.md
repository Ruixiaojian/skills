# fine tuning

fine tuning 是阿里云百炼平台提供的核心模型优化能力，通过在基础模型上注入领域知识、业务逻辑或人类偏好，显著提升模型在特定场景下的准确性、安全性与响应效率。它支持多种训练范式（SFT、CPT、DPO、RL）和[多模态](../concepts/multi-modal.md)模型（文本、图像、视频、语音），适用于从安全合规强化到IP形象定制等广泛用例。所有 fine tuning 任务当前仅在华北2（北京）地域可用 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

## 支持的模型/功能

百炼平台支持覆盖文本、视觉、语音、视频四大模态的 fine tuning，具体能力如下：

- **文本生成**：支持 Qwen 系列全量模型（如 `qwen3-8b`, `qwen3-32b`）及千问 VL [多模态](../concepts/multi-modal.md)模型（如 `qwen3-vl-8b-instruct`）的 SFT、CPT、DPO 训练；其中 SFT 高效训练（`efficient_sft`）为默认推荐方式 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **图像生成**：仅支持万相（Wan）系列模型，包括 `wan2.7-image-pro` 和 `wan2.7-image`，采用 SFT-LoRA 方式，支持文生图（t2i）与图生图（i2i）两种模式 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成**：支持 `wan2.7-i2v`、`wan2.5-i2v-preview`、`wan2.2-i2v-flash`（首帧驱动）及 `wan2.2-kf2v-flash`（首尾帧驱动），同样基于 SFT-LoRA [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成**：仅支持 `cosyvoice-v3-flash` 模型的 SFT 调优，用于同一发音人的高还原度音色定制，不支持 CPT/DPO [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **强化学习（RL）**：面向 Agent 场景，支持 `qwen3.5-9b` 等指定 MoE/非-MoE 模型，需通过 MTU 训练单元计费，不支持 [Token](../concepts/token.md) 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 5 和文档 8 的模型支持矩阵存在矛盾。文档 5 声明 `qwen3.7-plus-2026-05-26` 仅支持 `efficient_sft`，而文档 8 同一表格中显示其支持 `sft`（全参训练）。实际以控制台实时选项为准，API 请求时若传入不支持的 `training_type` 将返回 400 错误。

## 关键参数

不同模态和训练方式的关键超参差异较大，开发者需按场景严格匹配：

- **通用参数（文本/SFT）**：`n_epochs`（必填，循环次数）、`batch_size`（必填）、`learning_rate`（推荐高效训练用 `1e-4` 量级，全参训练用 `1e-5` 量级）、`max_length`（序列长度，建议设为模型最大支持值）[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **图像/视频生成**：`generation_type`（`"t2i"` 或 `"i2i"`）、`max_pixels`（训练图最大分辨率，如 `"2k"`）、`val_img_size`（验证图分辨率）、`lora_rank`（LoRA 秩，必须为 2 的幂次，如 32）[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成（特殊）**：`n_epochs` 与 `batch_size` 共同决定总步数（steps = n_epochs × ⌈数据集大小 / batch_size⌉），且 `eval_epochs` 必须 ≥ `n_epochs/10`；`max_pixels` 为整型像素总数（如 `102400`），非字符串 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成（CosyVoice）**：采用解耦的 LM/FM 双网络，超参均以 `lm_*`/`fm_*` 前缀区分，如 `lm_max_epoch`（LM 训练轮次）、`fm_batch_size`（FM 批次大小），全部 8 个字段均为必填 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **强化学习（RL）**：核心为 `algorithm`（如 `"gspo"`）、`batch_size`、`kl_loss_coef`、`learning_rate`（通常极低，如 `2e-6`），且必须配置 `resources`（MTU 规格与数量）[强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 使用方式

fine tuning 通过标准 API 流程实现，共三步：上传数据 → 创建任务 → 部署模型。

1. **上传数据集**：使用 `/api/v1/files` 接口上传 `.jsonl`（文本）、`.zip`（图像/视频）或 `.wav`+`data.jsonl`（语音）文件，`purpose="fine-tune"` 为必需字段。单文件上限 300MB，总配额 100GB [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
2. **创建训练任务**：调用 `/api/v1/fine-tunes`，关键字段包括：
   - `model`：基础模型 ID（如 `"qwen3-8b"`）
   - `training_datasets`：含 `file_id` 或 `oss_mount` 配置的数据源列表
   - `training_type`：如 `"efficient_sft"`、`"dpo_lora"`、`"cpt"`
   - `hyper_parameters`：按模型类型填写对应参数
   > 注意：图像/视频任务需在 `hyper_parameters` 中显式指定 `generation_type`；语音任务需完整填写 `lm_*`/`fm_*` 全部 8 个字段。
3. **部署与调用**：任务状态变为 `SUCCEEDED` 后，用 `finetuned_output` 作为 `model_name` 调用 `/api/v1/deployments` 接口部署。部署成功（`status="RUNNING"`）后即可用新模型 ID 发起推理请求 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

## 限制和注意事项

- **地域与权限**：所有 fine tuning 功能仅限华北2（北京）地域，且子账号需显式授予模型调用、训练、部署权限 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **计费模式**：
  - 文本/图像/视频/语音：按训练消耗 [Token](../concepts/token.md) 数计费，单价因模型而异（如 `qwen3-8b` 为 ¥0.006/千[Token](../concepts/token.md)，`wan2.7-image-pro` 未公开单价）。
  - 强化学习：强制使用 MTU 训练单元（预付费/后付费），不支持 Token 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
- **数据规范**：
  - 文本 SFT：必须为 ChatML 格式的 `.jsonl`，每行含 `messages` 数组，`role` 限 `system`/`user`/`assistant` [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
  - 图像/视频：`.zip` 包内必须含根目录 `data.jsonl`，图片路径需以 `train/` 为前缀；单图宽高 ≤1024px，单文件 ≤10MB [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **训练约束**：
  - CosyVoice 调优产物为单音色模型，`voice` 参数固定为 `"default"`，不可切换音色或使用指令控制 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - RL 训练必须完成 OpenTelemetry、函数计算（FC）、日志服务（SLS）三项服务授权，且 SDK 版本需 ≥3.10 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)


