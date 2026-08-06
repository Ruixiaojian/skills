# fine tuning

fine tuning（微调）是百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练大模型进行定制化训练，以提升其在特定任务、领域或风格上的表现。该能力覆盖文本生成、[多模态](../concepts/multimodal.md)理解、图像/视频生成及语音合成等多种模态，支持高效微调（LoRA）、全参微调、持续预训练（CPT）和直接偏好优化（DPO）等多种范式，适用于从安全合规强化到IP形象定制的广泛场景。

## 支持的模型与功能

百炼平台支持多类模型的 fine tuning，具体能力因模型类型而异：

- **文本生成模型**：支持 SFT（监督微调）、CPT（持续预训练）和 DPO（直接偏好优化），覆盖 Qwen3 系列（如 `qwen3-8b`、`qwen3-14b`）、Qwen2.5 系列及千问-Plus-Character 等模型。其中 SFT 高效训练（`efficient_sft`）为默认推荐方式，兼顾效果与成本 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **[多模态](../concepts/multimodal.md)理解模型（千问VL）**：支持 SFT 全参与高效训练，适用于图片/视频理解任务，需注意视觉主干网络（VIT）冻结参数 `freeze_vit` 仅在高效训练中生效，且影响计费模式 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **图像生成模型（万相）**：仅支持 SFT-LoRA 高效微调，适用模型包括 `wan2.7-image-pro` 和 `wan2.7-image`，部署后需使用 `plan: "lora"` 参数 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成模型（万相）**：支持图生视频（i2v）与首尾帧生成（kf2v）两类模型的 SFT-LoRA 微调，如 `wan2.7-i2v`、`wan2.2-kf2v-flash`，但不支持 CPT 或 DPO [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成模型（CosyVoice）**：当前仅支持 `cosyvoice-v3-flash` 的 SFT 高效微调（`efficient_sft`），且**仅可通过 API 发起，控制台暂不支持**；调优产物为单音色独立模型，`voice` 参数固定为 `default` [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **强化学习（RL）训练**：面向 Agent 场景，支持 `qwen3.5-9b` 等 MoE/非MoE 模型，需通过模型训练单元（MTU）计费，不支持按 [Token](../concepts/token.md) 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 4 与文档 8 中关于 `qwen3.7-plus-2026-05-26` 的支持状态存在矛盾——文档 4 标注“SFT全参训练（sft）支持”，而文档 8 同一模型下明确标注“×”（不支持）。依据文档 8 的 API 接口说明及实际调用约束，应以文档 8 为准：该模型**不支持 SFT 全参训练**，仅支持高效训练（`efficient_sft`）。

## 关键参数

不同训练方式的核心超参数差异显著，开发者需根据任务目标选择：

- **通用必填参数**：
  - `model`：基础模型 ID（如 `qwen3-8b`、`wan2.7-image-pro`），必须与所选训练方式兼容。
  - `training_type`：指定训练方法，取值包括 `sft`、`efficient_sft`、`cpt`、`dpo_full`、`dpo_lora`；CosyVoice 固定为 `efficient_sft`。
  - `n_epochs`（文本）或 `max_steps`（图像/视频）：控制训练深度。文本 SFT 推荐 `n_epochs=3~5`（小数据集）或 `1~2`（大数据集）；图像微调要求 `max_steps ≥ 500`；视频微调建议总步数 ≥ 800 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **LoRA 相关参数**（高效训练专用）：
  - `lora_rank`：低秩矩阵维数，决定可训练参数量，取值须为 2 的幂（如 8、16、32）。图像微调推荐 `32`，文本微调默认 `8`，增大可提升拟合能力但增加训练时间。
  - `lora_alpha`：权重缩放系数，通常与 `lora_rank` 等值设置（如 `32`），控制 LoRA 更新对原始权重的影响强度。

- **学习率与调度**：
  - `learning_rate`：文本 SFT 高效训练推荐 `1e-4` 量级，全参训练为 `1e-5`；图像微调默认 `3e-5`；视频微调为 `2e-5`；RL 训练为 `2e-6`。
  - `lr_scheduler_type`：推荐 `linear` 或 `inverse_sqrt`；`cosine` 适用于长周期训练，但 `cosine_with_restarts` 经实测无效，不推荐使用 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

- **数据与验证**：
  - `split`：自动划分验证集比例（如 `0.9` 表示 90% 训练/10% 验证），仅当未指定 `validation_datasets` 时生效。
  - `eval_steps`（文本/图像）或 `eval_epochs`（视频）：验证频率，用于监控过拟合。文本默认 `50`，图像推荐 `200`，视频推荐 `20`。

## 使用方式

fine tuning 通过 API 或控制台两种途径执行，流程高度一致：

1. **准备与上传数据集**：
   - 文本 SFT/DPO/CPT 使用 `jsonl` 格式，遵循 ChatML messages 结构；[多模态](../concepts/multimodal.md) SFT（图片/视频）需打包为 `.zip`，内含 `data.jsonl` 及对应媒体文件 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
   - 通过 `/api/v1/files` 接口上传，获取 `file_id`；OSS 挂载方式需提前授权，且仅支持北京/新加坡地域 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

2. **创建训练任务**：
   - 构造 `/api/v1/fine-tunes` 请求体，填入 `model`、`training_datasets`（含 `file_id` 或 OSS 路径）、`training_type` 及 `hyper_parameters`。
   - CosyVoice 等特定模型有专属字段（如 `lm_max_epoch`、`fm_max_epoch`），必须严格按文档填写 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

3. **监控与查询**：
   - 使用返回的 `job_id` 轮询 `/api/v1/fine-tunes/{job_id}`，直至 `status` 变为 `SUCCEEDED`。
   - RL 训练需额外关注 Reward 曲线，而图像/视频微调耗时较长（数小时），需耐心等待 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

4. **部署与调用**：
   - 成功后，`finetuned_output` 即为新模型名称，需通过 `/api/v1/deployments` 部署。
   - 图像/视频微调部署必须指定 `"plan": "lora"`；文本模型部署无此限制，但 LoRA 模型需确保推理时加载正确适配器 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

## 限制和注意事项

- **地域与权限限制**：所有 fine tuning 功能（除部分文本 SFT 外）均**仅限华北2（北京）地域**；子账号需显式授予模型调用、训练、部署权限，且 RL 训练需额外开通 OpenTelemetry、函数计算（FC）和日志服务（SLS）授权 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **数据与格式约束**：
  - 图像输入分辨率上限为 `8K`，但推荐控制在 `4K` 内以避免超时；单张图片 ≤ 10 MB，`.zip` 数据包 ≤ 300 MB [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
  - CosyVoice 训练音频必须为 `.wav` 格式、采样率 ≥ 16 kHz，且**所有样本必须来自同一发音人**；混入多发音人将导致音色还原度下降 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **计费与资源**：
  - 文本/多模态微调按 [Token](../concepts/token.md) 计费，公式为 `训练数据 Token 总数 × 循环次数 × 单价`；RL 训练强制使用模型训练单元（MTU），不支持 [Token](../concepts/token.md) 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
  - CosyVoice 训练费用 = `(lm_max_epoch + fm_max_epoch) × 25 × 总时长(秒) × 0.2元/千Tokens`，部署费用按模型单元时长单独计算 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **模型能力边界**：
  - fine tuning **无法扩展基础模型的能力**：CosyVoice 调优不能新增语种支持；万相微调不能改变生成模式（如文生图模型无法通过微调支持图生图）；千问VL 微调不能启用未开放的思考模式 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - 安全合规微调需谨慎设计数据集，避免诱导性样本污染模型；评测必须使用**全新、未参与训练的独立数据集**，否则结果不可信 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


