# fine tuning

fine tuning（微调）是百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练大模型进行定制化训练，以提升其在特定任务、领域或风格上的表现。该能力覆盖文本生成、图像生成、视频生成、语音合成及多模态理解等全模态场景，支持 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化）和 RL（强化学习）等多种训练范式，兼顾效果、效率与成本。

## 支持的模型/功能

百炼平台支持多种模态和训练方式的微调能力，但不同模型支持的训练类型存在差异。文本生成模型（如 Qwen 系列）普遍支持 CPT、SFT（全参/高效）、DPO（全参/高效），而图像、视频、语音类模型则聚焦于 SFT 高效微调（`efficient_sft`）。例如，万相图像生成模型 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md) 仅支持 `wan2.7-image-pro` 和 `wan2.7-image`；视频生成模型 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md) 仅支持 `wan2.7-i2v`、`wan2.5-i2v-preview` 等指定型号；CosyVoice 语音模型 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md) 则限定为 `cosyvoice-v3-flash`。视觉理解（千问 VL）模型支持 SFT 全参与高效训练，但不支持 DPO 或 CPT [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

> **注意**：文档 4 和文档 7 的表格中均列出 Qwen3-14B 支持 `dpo_lora`，但文档 5 的“说明”部分明确指出 DPO（高效训练）不支持 `freeze_vit` 参数，且未提及其他 DPO 高效训练限制；而文档 4 的表格中 Qwen3-14B 对应 `dpo_lora` 列为 ✓，文档 7 的相同表格也为 ✓。然而，文档 5 在“不同训练方式支持的参数有所不同”小节中强调：“**DPO（高效训练）：支持除'是否冻结VIT'（freeze_vit）外的全部参数**”，暗示其功能完整。因此，此处以文档 5 的详细说明为准，即 DPO 高效训练功能可用，但 `freeze_vit` 参数不适用——这并非矛盾，而是参数支持范围的精确描述。

强化学习（RL）训练则面向更高级的推理优化，当前仅对特定大模型开放，需联系商务经理开通权限，且必须通过模型训练单元（MTU）计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 关键参数

微调任务的核心参数因训练方式和模型类型而异，但存在通用关键字段：

- **`training_type`**：必填，指定训练方法，如 `"sft"`、`"efficient_sft"`、`"dpo_full"`、`"cpt"` 或 `"gspo"`（RL）。图像/视频/语音模型固定为 `"efficient_sft"`。
- **`model`**：必填，基础模型 ID，如 `"qwen3-8b"`、`"wan2.7-image-pro"` 或 `"cosyvoice-v3-flash"`。
- **`hyper_parameters`**：必填，包含影响效果与成本的核心超参：
  - **学习率 (`learning_rate`)**：文本 SFT 推荐 `1e-4`（高效）或 `1e-5`（全参）；图像生成推荐 `3e-5`；视频生成推荐 `2e-5`；RL 推荐 `2e-6`。
  - **训练轮次/步数**：文本 SFT 用 `n_epochs`（推荐 1–5），图像/视频用 `max_steps`（图像推荐 ≥800）或 `n_epochs`（视频推荐 50 起），RL 用 `batch_size`（如 64）。
  - **LoRA 参数**：`lora_rank`（秩值，推荐 8–32）、`lora_alpha`（缩放系数，推荐 16–32），仅 `efficient_sft` 及 DPO 高效训练使用。
  - **分辨率/尺寸控制**：图像/视频模型需设置 `max_pixels`（如 `"2k"` 或 `102400`），语音模型需设置 `lm_max_epoch`/`fm_max_epoch`。
  - **验证频率**：`eval_steps`（文本/图像）或 `eval_epochs`（视频）用于控制评估与 Checkpoint 保存间隔。

所有参数均需严格遵循各模型文档的取值范围与必选要求，否则任务将失败。

## 使用方式

微调流程统一为三步：上传数据 → 创建任务 → 部署模型。

1. **上传数据集**：通过 DashScope API 上传 `.jsonl`（文本）、`.zip`（图像/视频/语音）或 `.xlsx`（评测集）文件，获取 `file_id`。单个文件上限 300MB，总配额 100GB [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。图像/视频/语音数据包需符合特定目录结构（如 `user_data/data.jsonl` + `user_data/train/*.wav`）[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

2. **创建微调任务**：调用 `/api/v1/fine-tunes` 接口，传入 `model`、`training_type`、`training_datasets`（含 `file_id`）及 `hyper_parameters`。支持 OSS 挂载（需北京/新加坡地域）和混合训练 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。任务创建后状态为 `PENDING`，需轮询 `/api/v1/fine-tunes/{job_id}` 直至 `status` 变为 `SUCCEEDED`。

3. **部署与调用**：训练成功后，使用 `finetuned_output` 模型名调用 `/api/v1/deployments` 部署为在线服务。图像/视频模型部署时需在 `aigc_config` 中配置 `lora_prompt_default` 以固化特效 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)；语音模型部署后 `voice` 参数强制为 `"default"` [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 限制和注意事项

- **地域与权限限制**：绝大多数微调能力（除文本 SFT 外）仅限华北2（北京）地域，且必须使用该地域的 API Key [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。子账号需被授予模型调用、训练、部署的完整权限 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **计费模式**：文本/图像/视频微调按 Token 消耗计费；RL 训练强制使用 MTU 训练单元（预付费/后付费）；语音模型训练按 Token、部署按模型单元时长计费 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **数据与效果约束**：
  - 图像输入分辨率需 ≤1024px，单图 ≤10MB；视频输入时长、大小、格式有严格限制 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
  - CosyVoice 调优要求训练音频为同一发音人，且语种必须为基础模型已支持 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - 过拟合风险：若训练损失持续下降而验证损失上升，需减少 `n_epochs`、增大 `weight_decay` 或提高 `lora_dropout` [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **功能边界**：微调无法扩展基础模型能力，如 CosyVoice 调优不能新增语种支持，万相微调无法改变生成模式（如文生图不能变图生图）[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)


