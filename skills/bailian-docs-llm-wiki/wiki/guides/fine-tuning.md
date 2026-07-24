# fine tuning

fine tuning 是阿里云百炼平台提供的核心模型优化能力，支持通过监督微调（SFT）、持续预训练（CPT）和直接偏好优化（DPO）等方式，在特定业务、行业或安全合规场景下提升模型效果。它采用 LoRA 等高效训练技术，在华北2（北京）地域提供服务，适用于文本、图像、视频及语音等多种模态模型。

## 支持的模型/功能

百炼平台支持[多模态](../concepts/multi-modal.md)模型的 fine tuning，覆盖文本生成、视觉理解、图像生成、视频生成和语音合成五大类：

- **文本生成**：支持 Qwen3 系列（如 `qwen3-8b`, `qwen3-14b`）、Qwen2.5 系列及 `qwen-plus-character-2025-11-06` 等模型，支持 SFT、CPT、DPO 三种训练方式，其中高效训练（`efficient_sft`）为默认推荐方案 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解（千问VL）**：支持 `qwen3-vl-8b-instruct` 等 VL 模型的 SFT 和 DPO 训练，需遵循 ChatML 格式并使用数组格式 `content` 传入 system 消息 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **图像生成**：仅支持万相系列模型（`wan2.7-image-pro`, `wan2.7-image`），采用 SFT-LoRA 方式，适用于文生图（t2i）和图生图（i2i）两种模式，且必须在华北2（北京）地域使用 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成**：支持 `wan2.7-i2v`、`wan2.5-i2v-preview`、`wan2.2-i2v-flash`（首帧）及 `wan2.2-kf2v-flash`（首尾帧）等模型，同样基于 SFT-LoRA，地域限制同图像生成 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成**：仅支持 `cosyvoice-v3-flash` 模型的 SFT 高效微调（`efficient_sft`），用于同一发音人的高还原度音色定制，**控制台暂不支持，仅可通过 API 发起** [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

> **注意**：文档 1 和文档 2 均明确要求“仅在华北2（北京）地域可用”，而文档 3 的“模型调优简介”也标注“本文档仅适用于华北2（北京）地域”，三者一致；但文档 7 的 CosyVoice 文档虽未在“适用范围”章节重复强调，却在“调优规格”中单独注明“仅支持华北2（北京）地域”，因此所有 fine tuning 功能均受地域严格限制。

## 关键参数

不同模态的 fine tuning 使用不同超参体系，但核心参数存在共性：

- **通用必选参数**：
  - `model`：基础模型 ID（如 `qwen3-8b`, `wan2.7-image-pro`, `cosyvoice-v3-flash`），必须与支持列表匹配。
  - `training_type`：训练方法，常见值为 `sft`（全参）、`efficient_sft`（LoRA）、`cpt`、`dpo_full`、`dpo_lora`。
  - `training_datasets`：数据源配置，支持 `file_id`（上传 ZIP）或 `oss_mount`（OSS 挂载）两种方式；图像/视频/语音任务中 `training_file_ids` 字段已弃用，统一使用 `training_datasets` [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

- **LoRA 专用参数**（适用于 `efficient_sft`）：
  - `lora_rank`：低秩矩阵维数，必须为 2 的幂（如 16、32、64），影响拟合能力与训练速度；图像生成推荐 32，文本生成默认 8 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
  - `lora_alpha`：LoRA 权重缩放系数，通常与 `lora_rank` 相等（如 32），控制修正项强度 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **训练规模控制参数**：
  - `n_epochs`（文本/语音）或 `max_steps`（图像/视频）：决定训练总轮次或步数。图像生成建议 `max_steps ≥ 500`；视频生成推荐 `n_epochs=50`（小数据集）或按 `steps ≥ 800` 推算；语音合成则拆分为 `lm_max_epoch` 和 `fm_max_epoch`，生产推荐 `60` 和 `100` [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
  - `batch_size`：批次大小，图像生成推荐 `1`（wan2.7-i2v）或 `4`（wan2.2-kf2v-flash），文本生成推荐 `16`，语音合成 LM/FM 分别为 `1000`/`2000` [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **学习率与正则化**：
  - `learning_rate`：高效训练推荐 `1e-4` 量级（如 `3e-5` 图像、`2e-5` 视频、`3e-4` 文本），全参训练推荐 `1e-5` 量级 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
  - `weight_decay`：权重衰减系数，图像生成默认 `0.02`，文本生成默认 `0.01` [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

## 使用方式

fine tuning 流程标准化为四步：准备数据 → 上传文件 → 创建任务 → 部署调用。

1. **准备数据集**：
   - **文本/语音**：ZIP 包内根目录必须含 `data.jsonl`，格式为 ChatML（SFT/DPO）或纯文本（CPT）；语音还需 `train/` 目录存放 `.wav` 文件 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
   - **图像/视频**：ZIP 包内 `data.jsonl` 引用图片/视频文件名（不带路径），文件名全局唯一；图像单张 ≤1024px，视频支持路径或帧列表模式 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

2. **上传文件**：
   ```bash
   curl -X POST 'https://dashscope.aliyuncs.com/api/v1/files' \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -F 'files=@./dataset.zip' \
     -F 'purpose=fine-tune'
   ```
   返回 `file_id` 用于后续任务创建。

3. **创建并监控任务**：
   - 提交 `fine-tunes` 请求，传入 `file_id` 和超参；
   - 轮询 `GET /api/v1/fine-tunes/{job_id}` 直至 `status=SUCCEEDED`；
   - 语音合成任务需额外注意：平台同一时刻仅运行一个训练任务，新任务将进入 `QUEUING` 状态 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

4. **部署与调用**：
   - 成功后获取 `finetuned_output`（新模型名），调用 `POST /api/v1/deployments` 部署；
   - 部署状态变为 `RUNNING` 后即可调用，图像/视频模型需异步（`X-DashScope-Async: enable`），语音模型调用时 `voice` 固定为 `default` [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

## 限制和注意事项

- **地域与权限**：所有 fine tuning 功能**仅限华北2（北京）地域**，且子账号需显式授予模型调用、训练、部署权限 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **数据与存储**：ZIP 包最大 2GB（文本/视觉）或 300MB（API 上传），文件名仅支持 ASCII 字符；有效文件总数上限 10000 个，总空间 100GB [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **模型产物特性**：
  - 图像/视频 LoRA 模型调用时需在 [prompt](prompt.md) 中加入触发词（如 `s86b5p`）以激活风格 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)；
  - CosyVoice 调优产物为单音色独立模型，**不支持声音复刻、声音设计或指令控制**，仅支持 SSML/LaTeX [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)；
  - 所有调优产物均为新模型 ID，不可叠加微调（即不能以微调后模型为 base 再次 fine tune）。
- **计费与成本**：训练费用按 [Token](../concepts/token.md) 计费（公式：`Token 总数 × 循环次数 × 单价`），图像/视频 [Token](../concepts/token.md) 计算复杂，需参考内部缩放逻辑；语音合成单价为 0.2 元/千 [Token](../concepts/token.md)s，部署费用另计 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


