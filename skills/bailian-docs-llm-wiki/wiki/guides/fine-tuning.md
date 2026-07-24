# fine tuning

微调（Fine-tuning）是阿里云百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练模型进行定制化训练，以提升其在特定任务、风格或安全合规等维度的表现。该能力支持文本、图像、视频、语音等多种模态，采用高效微调（LoRA）为主的技术路径，在控制成本与训练时长的同时保障效果。所有微调任务当前均仅限华北2（北京）地域使用。

## 支持的模型/功能

百炼平台支持多模态模型的微调，覆盖文本生成、视觉理解、图像生成、视频生成和语音合成五大类：

- **文本生成**：支持 Qwen 系列大语言模型（如 `qwen3-8b`、`qwen3-14b`、`qwen2.5-7b-instruct` 等）的 SFT（监督微调）、CPT（持续预训练）和 DPO（直接偏好优化），详见 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解（千问VL）**：支持 `qwen3-vl-8b-instruct` 等 VL 模型的 SFT 微调，支持图像、视频输入及多模态对话格式 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **图像生成**：支持万相系列模型 `wan2.7-image-pro` 和 `wan2.7-image` 的 LoRA 微调，适用于文生图、图生图场景，可定制 IP 形象、艺术风格等 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成**：支持万相图生视频模型 `wan2.7-i2v`、`wan2.5-i2v-preview`、`wan2.2-i2v-flash`（首帧）及 `wan2.2-kf2v-flash`（首尾帧）的 SFT-LoRA 微调，用于稳定复现特定动作、特效或运镜 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成**：支持 `cosyvoice-v3-flash` 模型的 SFT 高效微调，面向同一发音人的高还原度音色定制，产出独立部署的专属音色模型 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

> **注意**：文档 3 中表格列出 `Qwen3.7-Plus-2026-05-26` 支持 SFT 全参训练，但文档 4 明确说明“Qwen3.7-Plus-2026-05-26 调优后部署请联系商务经理”，表明其生产可用性受限，实际开发者应优先选用已明确开放 API 或控制台支持的模型（如 `qwen3-8b`）。

## 关键参数

不同模态的微调任务使用差异化的超参数体系，但核心字段保持一致语义：

- **通用必填参数**：
  - `model`：基础模型 ID（如 `qwen3-8b`、`wan2.7-i2v`、`cosyvoice-v3-flash`），必须准确匹配 [支持的模型/功能](#支持的模型功能) 中所列型号。
  - `training_type`：训练方法，`efficient_sft`（LoRA）为最常用选项；`sft`（全参）、`cpt`、`dpo_full` 等需确认模型支持。
  - `training_file_ids` 或 `training_datasets`：训练数据集标识，通过 `files` 接口上传后获得 `file_id`，或通过 OSS 挂载指定路径。

- **核心超参数**：
  - `learning_rate`：学习率，文本模型推荐 `1e-4`（LoRA）或 `1e-5`（全参）；图像/视频模型推荐 `2e-5`～`3e-5`；语音模型无全局学习率，由子网络参数控制。
  - `n_epochs` / `max_steps`：训练轮次或总步数。图像生成用 `max_steps`（推荐 ≥800）；视频生成用 `n_epochs`（小数据集推荐 50）；语音模型用 `lm_max_epoch`/`fm_max_epoch`（推荐 60/100）。
  - `batch_size`：批次大小，直接影响显存占用与收敛速度。视频模型 `wan2.7-i2v` 必须设为 `1`，而 `wan2.2-kf2v-flash` 可设为 `4`；文本模型通常设为 `16`。
  - `lora_rank` 与 `lora_alpha`：LoRA 低秩矩阵维数与缩放系数，推荐值均为 `32`，取值须为 2 的幂（16/32/64）。
  - `max_pixels` / `max_length`：图像最大像素总数（如 `102400`）或文本最大 token 长度（如 `8192`），用于控制输入尺寸与内存消耗。

- **验证与保存**：
  - `eval_steps` / `eval_epochs`：验证间隔，文本模型推荐 `50` 步，视频模型推荐 `20` 轮。
  - `save_total_limit`：Checkpoint 保存上限，推荐 `10`，避免存储溢出。

## 使用方式

微调流程统一为四步：准备数据 → 上传文件 → 创建任务 → 部署调用。

1. **准备数据集**：严格遵循各模态格式要求。
   - 文本/SFT：ChatML 格式 `.jsonl`，每行含 `messages` 数组，`assistant` 输出为期望结果 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
   - 图像/视频：ZIP 包含 `data.jsonl`（根目录）及对应图片/视频文件，命名唯一，分辨率符合 `max_pixels` 要求 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
   - 语音：ZIP 包含 `user_data/data.jsonl`（含 `wav_fn` 和 `text` 字段）及 `train/*.wav` 音频，采样率 ≥16kHz [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

2. **上传文件**：调用 `/api/v1/files` 接口，`purpose="fine-tune"`，获取 `file_id`。

3. **创建任务**：调用 `/api/v1/fine-tunes`，传入 `model`、`training_file_ids`、`training_type` 及 `hyper_parameters`。任务状态初始为 `PENDING`，需轮询查询直至 `status="SUCCEEDED"`。

4. **部署与调用**：
   - 部署：使用 `finetuned_output` 作为 `model_name` 调用 `/api/v1/deployments`，等待 `status="RUNNING"`。
   - 调用：将 `deployed_model` 填入对应模态的推理 API（如 `/services/aigc/image-generation/generation`），**无需修改提示词结构，但需确保触发词（如 `s86b5p`）存在以激活 LoRA**。

## 限制和注意事项

- **地域与权限**：所有微调功能**仅限华北2（北京）地域**，且需使用该地域的 API Key；RAM 子账号必须被授予 `AliyunBailianFullAccess` 或等效的模型训练、部署权限。
- **数据与计费**：
  - 训练费用按消耗 [Token](../concepts/token.md) 计费，图像/视频 [Token](../concepts/token.md) 计算复杂，建议使用文档 3 提供的估算代码预估 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
  - CosyVoice 训练费用公式为 `(lm_max_epoch + fm_max_epoch) × 25 × 总秒数`，单价 0.2 元/千 [Token](../concepts/token.md) [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **技术限制**：
  - 视频/图像微调不支持自定义分辨率，必须使用文档中指定的 `max_pixels` 值（如 `wan2.7-i2v` 为 `102400`），否则训练失败。
  - CosyVoice 微调产物为单音色模型，`voice` 参数强制为 `default`，不支持声音复刻或切换音色 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **工程实践**：
  - 小规模数据（<100 条）建议优先尝试 LoRA（`efficient_sft`），成本低、速度快；大规模生产场景可评估全参训练效果 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
  - 安全合规类微调（如拒绝有害请求）需构建高质量正负样本，避免仅靠单条指令，推荐使用文档 6 中的多维度风险覆盖策略 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 来源文档

- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


