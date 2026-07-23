# fine tuning

微调（Fine-tuning）是阿里云百炼平台提供的核心模型优化能力，通过在基础模型上注入领域知识、业务指令或人类偏好，显著提升模型在特定任务上的准确性、安全性与风格一致性。它适用于文本生成、图像生成、视频生成及语音合成等[多模态](../concepts/multi-modal.md)场景，支持高效微调（LoRA）与全参训练两种模式，兼顾效果与成本。

## 支持的模型与功能

百炼平台支持对多种模态模型进行微调，覆盖文本、视觉、语音和视频生成任务。所有微调任务均需在**华北2（北京）地域**执行，并使用该地域的 API Key [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **文本生成**：支持 Qwen 系列大语言模型（如 `qwen3-8b`、`qwen2.5-7b-instruct`）的 SFT、CPT 和 DPO 训练；支持千问 VL 视觉理解模型的[多模态](../concepts/multi-modal.md) SFT [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **图像生成**：仅支持万相系列模型（`wan2.7-image-pro`、`wan2.7-image`），采用 SFT-LoRA 方式，适用于文生图与图生图任务 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成**：支持 `wan2.7-i2v`、`wan2.2-kf2v-flash` 等万相视频模型，同样基于 SFT-LoRA，支持首帧/首尾帧驱动的特效定制。
- **语音合成**：仅支持 `cosyvoice-v3-flash` 模型的 SFT 高效微调，用于高还原度专属音色定制，**控制台暂不支持，必须通过 API 发起** [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

> **注意**：文档 4 中称“阿里云百炼推荐您如果**模型支持全参训练，请优先选择全参训练**，因为全参训练效果比高效训练效果要好”，但文档 1、2、6 明确限定图像、视频、语音微调**仅支持 `efficient_sft`**（即 LoRA），且未提供全参训练选项。因此，对于非文本类模型，高效训练是唯一可用方式，不存在“优先选择”问题。

## 关键参数

不同模态模型的超参数命名与语义存在差异，开发者需按任务类型严格匹配：

| 参数名 | 文本模型（SFT） | 图像模型（wan） | 视频模型（wan） | 语音模型（CosyVoice） | 说明 |
|--------|----------------|-----------------|------------------|------------------------|------|
| `training_type` | `sft`, `efficient_sft`, `dpo_lora` | 固定为 `efficient_sft` | 固定为 `efficient_sft` | 固定为 `efficient_sft` | 必填，指定训练方法 |
| `learning_rate` | 默认 `3e-4`（高效训练）或 `1e-5`（全参） | `3e-5`（文生图）、`2e-5`（图生视频） | `2e-5` | 不直接暴露，由 `lm_max_epoch`/`fm_max_epoch` 间接影响 | 学习率过高易发散，过低收敛慢 |
| `max_steps` / `n_epochs` | `n_epochs`（循环次数），默认 `3` | `max_steps`（总步数），如 `800` | `n_epochs`（轮次），如 `50` | `lm_max_epoch` & `fm_max_epoch`（双网络轮次） | 控制训练强度的核心参数；图像用步数，其余多用轮次 |
| `batch_size` | 默认 `16` | 未显式暴露（由系统自动适配） | `1`（wan2.7-i2v）或 `4`（其他） | `lm_batch_size` / `fm_batch_size`（如 `1000`/`2000`） | 批次大小直接影响内存占用与训练稳定性 |
| `lora_rank` | 默认 `8` | `32`（必须为 2 的幂） | `32` | 不适用（CosyVoice 使用专用 LM/FM 架构） | LoRA 低秩矩阵维度，值越大拟合能力越强，但易过拟合 |
| `lora_alpha` | 默认 `16` | 未提及 | `32` | 不适用 | LoRA 缩放因子，控制修正项权重 |

所有模型均需配置 `model`（基础模型 ID）和 `training_datasets`（数据源）。图像/视频模型还需指定 `generation_type`（`t2i`/`i2i`/`i2v`）或 `max_pixels`（分辨率上限）；语音模型则强制要求 `wav_fn` 字段路径以 `train/` 开头。

## 使用方式

微调流程统一为四步：**准备数据 → 上传文件 → 创建任务 → 部署调用**，但各模态入口与细节不同：

- **控制台操作**：适用于文本与视觉理解模型。进入[模型调优](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager)页面，选择模型、训练方式（SFT/CPT/DPO）、上传数据集（ZIP 或 OSS 路径），配置超参后启动 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **API 操作**：通用方式，**语音模型强制要求**。先调用 `/api/v1/files` 上传 ZIP 数据包（`purpose="fine-tune"`），获取 `file_id`；再调用 `/api/v1/fine-tunes` 提交训练任务，`training_datasets` 中引用该 `file_id` [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **部署与调用**：训练成功（`status=SUCCEEDED`）后，调用 `/api/v1/deployments` 部署模型，获得 `deployed_model` 名称；调用时需将 `model` 字段设为该名称，并遵循对应模态的输入格式（如图像微调需含触发词 `s86b5p`，语音微调固定 `voice="default"`）。

> **注意**：文档 2 中视频微调部署请求包含 `aigc_config` 字段（如 `lora_prompt_default`），而文档 1 图像微调部署请求无此字段；文档 5 的通用 API 文档也未要求该字段。这表明 `aigc_config` 是视频模型特有的部署配置，开发者需按模型类型查阅对应指南。

## 限制和注意事项

- **地域与权限**：所有微调服务仅限华北2（北京）地域，子账号需被授予 `AliyunBailianFullAccess` 或精细化的 `dashscope:CreateFineTuneJob` 等权限 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **数据规范**：
  - 文本/视觉数据必须为 ZIP 包，根目录含 `data.jsonl`，图片尺寸 ≤1024px；
  - 语音数据 ZIP 内 `data.jsonl` 的 `wav_fn` 必须以 `train/` 开头；
  - 视频微调数据集需严格按 `i2v` 或 `kf2v` 格式组织，不可混用。
- **成本与耗时**：
  - 计费按训练 [Token](../concepts/token.md) 总量 × 单价（如文本 `¥0.006/千Token`，语音 `¥0.2/千Token`）；
  - 图像微调约 77 分钟（2K, 300 步），视频微调需“数小时”，语音微调最小化超参约 37 分钟 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **效果边界**：
  - 微调无法扩展基础模型能力（如 CosyVoice 不能通过微调支持新语种）；
  - 过度增加 `n_epochs` 或 `lora_rank` 可能导致基础能力“遗忘”或过拟合；
  - 安全合规微调需高质量拒答样本，单纯 [Prompt 工程](../concepts/prompt-engineering.md)无法替代参数层面的对齐 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)


