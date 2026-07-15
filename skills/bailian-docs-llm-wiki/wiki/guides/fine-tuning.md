# fine tuning

fine tuning 是阿里云百炼平台提供的模型定制化能力，允许开发者基于自有数据对预训练模型进行增量训练，以提升其在特定任务、领域或风格上的表现。该能力覆盖文本生成、视觉理解、图像/视频生成及语音合成等多模态模型，支持 SFT（监督微调）、CPT（持续预训练）和 DPO（直接偏好优化）等多种训练范式。所有 fine tuning 任务当前均仅支持华北2（北京）地域，且需使用该地域的 API Key [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

## 支持的模型与功能

- **文本生成**：支持 Qwen 系列全量模型（如 `qwen3-8b`, `qwen2.5-7b-instruct`）及千问-VL 视觉语言模型，提供 CPT、SFT（含高效 LoRA 和全参）、DPO 三种训练方式。具体支持矩阵详见 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **图像生成**：仅支持万相系列模型（`wan2.7-image-pro`, `wan2.7-image`），采用 SFT-LoRA 高效微调，适用于文生图（t2i）和图生图（i2i）场景 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成**：支持万相图生视频模型（`wan2.7-i2v`, `wan2.2-kf2v-flash` 等），同样基于 SFT-LoRA，支持基于首帧或首尾帧的特效/动作定制 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成**：仅支持 `cosyvoice-v3-flash` 模型，通过 SFT-LoRA 进行单发音人音色定制，产物为独立部署的专属音色模型，不支持多音色切换 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

> **注意**：文档 4 中称“阿里云百炼推荐您如果**模型支持全参训练，请优先选择全参训练**”，但文档 1、2、7 均明确限定图像、视频、语音类模型**仅支持 `efficient_sft`（LoRA）**，且文档 3 的支持矩阵中，`wan*` 和 `cosyvoice*` 系列未列出任何全参训练选项。因此，对非文本生成模型，全参训练不可用，该推荐不适用。

## 关键参数

- **通用超参**：`learning_rate`（文本推荐 1e-4~1e-5，图像/视频/语音需按文档示例设置）、`n_epochs` 或 `max_steps`（控制训练轮次/步数）、`batch_size`、`lora_rank`（LoRA 秩，默认 8~32）、`lora_alpha`（LoRA 缩放因子）。
- **模型特有参数**：
  - 图像生成：`generation_type`（`t2i` 或 `i2i`）、`max_pixels`、`val_img_size`；
  - 视频生成：`split`（训练/验证集划分比例）、`eval_epochs`；
  - 语音合成：`lm_max_epoch`/`fm_max_epoch`（语言模型/流匹配模型轮次）、`lm_batch_size`/`fm_batch_size`；
  - 文本生成：`max_length`（序列长度）、`warmup_ratio`（学习率预热比例）。
- **数据源参数**：支持 `file_id`（上传 ZIP）和 `oss_mount`（OSS 挂载）两种方式；OSS 挂载要求数据集为解压状态，且 `data.jsonl` 必须位于根目录 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

## 使用方式

1. **准备数据集**：按指定格式（如 ChatML JSONL）组织训练数据，ZIP 打包（最大 2GB），确保 `data.jsonl` 在根目录，图片/音频文件名全局唯一。
2. **上传文件**：调用 `/api/v1/files` 接口上传，获取 `file_id`。
3. **创建任务**：调用 `/api/v1/fine-tunes`，传入 `model`、`training_datasets`（含 `file_id`）、`training_type`（如 `efficient_sft`）及 `hyper_parameters`。
4. **轮询状态**：用 `job_id` 调用 `/api/v1/fine-tunes/{job_id}`，等待 `status` 变为 `SUCCEEDED`。
5. **部署模型**：调用 `/api/v1/deployments`，传入 `finetuned_output` 作为 `model_name`，获取 `deployed_model`。
6. **调用服务**：使用 `deployed_model` 名称发起推理请求（图像/视频需异步，文本可同步）。

## 限制和注意事项

- **地域与权限**：所有 fine tuning 服务仅限华北2（北京）地域，子账号需显式授予模型调用、训练、部署权限 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **数据要求**：SFT 至少需 1000+ 条高质量样本；CPT 需 1000 万+ Token 无标签文本；DPO 需 100+ 组正负样本对。
- **计费**：按训练消耗 Token 数计费（单价因模型而异，如 `qwen3-8b` 为 ¥0.006/千 Token，`cosyvoice-v3-flash` 为 ¥0.2/千 Token），部署后另计模型单元费用。
- **工程成本**：fine tuning 是“最后手段”，应优先尝试 Prompt 工程和插件调用；其迭代周期长、成本高，需谨慎评估 ROI [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **能力边界**：调优无法扩展基础模型能力（如语种、指令控制、多音色），仅能优化其在已有能力范围内的表现 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


