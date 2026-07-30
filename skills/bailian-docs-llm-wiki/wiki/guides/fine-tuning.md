# fine tuning

fine tuning（微调）是百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练大模型进行定制化训练，从而提升其在特定业务场景、领域知识或风格表达上的表现。它适用于文本生成、视觉理解、语音合成、图像/视频生成等多种模态，支持 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化）及 RL（强化学习）等多种训练范式。所有微调任务均需在华北2（北京）地域执行，并依赖 DashScope API Key 和相应 RAM 权限。

## 支持的模型与功能

百炼平台支持[多模态](../concepts/multi-modal.md)、多粒度的微调能力：

- **文本生成模型**：覆盖 Qwen 系列（如 `qwen3-8b`、`qwen3.5-9b`、`qwen3-vl-8b-instruct`）及千问 Plus/Flash 等变体，支持 CPT、SFT（全参/LoRA）、DPO（全参/LoRA）三种方式 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉生成模型**：图像生成（文生图/图生图）支持 `wan2.7-image-pro`、`wan2.7-image`；视频生成（图生视频）支持 `wan2.7-i2v`、`wan2.2-kf2v-flash` 等，均采用 SFT-LoRA 高效微调 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **语音合成模型**：仅支持 `cosyvoice-v3-flash` 的 SFT 高效微调（`efficient_sft`），用于同一发音人的高还原度音色定制，**控制台暂不支持，必须通过 API 发起** [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **强化学习（RL）训练**：面向 Agent 场景（如工具调用、数学推理），支持 `qwen3.5-9b` 等 MoE/非 MoE 模型，需通过 MTU 训练单元计费，不支持 [Token](../concepts/token.md) 计费 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 4 与文档 5 均列出 SFT 支持模型，但文档 4 明确标注 `Qwen3.7-Plus-2026-05-26` 调优后部署需联系商务经理，而文档 5 未提及此限制；实际使用前应以最新控制台可选模型为准，避免因版本变更导致部署失败。

## 关键参数

不同训练类型和模型对应的核心超参存在显著差异：

- **通用 SFT 参数（API/控制台）**：`learning_rate`（推荐 LoRA 为 `1e-4` 量级，全参为 `1e-5`）、`n_epochs`（数据 <10k 条建议 3–5 轮）、`batch_size`（默认值因模型而异，常见为 16/32）、`eval_steps`（默认 50）、`lora_rank`（LoRA 秩，默认 8，图像/视频任务常设为 32）[原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **图像/视频生成专用参数**：`max_pixels`（训练图最大像素总数，如 `"2k"` 表示 2048×2048）、`val_img_size`（验证图分辨率）、`generation_type`（`"t2i"` 或 `"i2i"`）、`lora_alpha`（视频任务中与 `lora_rank` 同时设置，推荐 32）。
- **CosyVoice 专用参数**：解耦为 LM（语言模型）与 FM（流匹配模型）两组，关键字段包括 `lm_max_epoch`（推荐 60）、`fm_max_epoch`（推荐 100）、`lm_batch_size`（推荐 1000）、`fm_batch_size`（推荐 2000），直接影响音色还原度与韵律表现。
- **RL 训练参数**：`algorithm`（如 `"gspo"`）、`batch_size`（如 64）、`kl_loss_coef`（KL 散度系数，如 `0.002`）、`n_rollouts`（每样本采样次数，如 8），需严格匹配基座模型规格。

## 使用方式

微调流程统一为四步：准备数据 → 上传文件 → 创建任务 → 部署调用。

1. **数据准备**：
   - 文本 SFT：使用 ChatML 格式 JSONL 文件（`{"messages": [...]}`），`data.jsonl` 必须位于 ZIP 包根目录；视觉/语音任务需按指定目录结构打包（如 `user_data/data.jsonl` + `user_data/train/*.wav`）。
   - 图像/视频：ZIP 包内图片尺寸 ≤1024px，格式支持 JPG/PNG/WEBP；视频需满足时长与大小限制（如 `qwen3.5` 系列视频 ≤2GB）。
   - CosyVoice：音频为 WAV 格式，采样率 ≥16kHz，总时长建议 1–10 小时，单条 2–30 秒。

2. **上传文件**：
   ```bash
   curl -X POST 'https://dashscope.aliyuncs.com/api/v1/files' \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -F 'files=@train_data.zip' \
     -F 'purpose="fine-tune"'
   ```
   返回 `file_id` 用于后续任务创建。

3. **创建任务**：
   - 文本/视觉：通过 `/api/v1/fine-tunes` 提交，指定 `model`、`training_datasets`（含 `file_id`）、`training_type`（如 `"efficient_sft"`）及 `hyper_parameters`。
   - CosyVoice：仅支持 API，且 `training_file_ids` 仅接受单个 ID，`hyper_parameters` 必填全部 8 个 LM/FM 字段。
   - RL：需先部署 Rollout/Reward 函数，再通过 `AgenticRL.run()` 提交，依赖 MTU 资源配置。

4. **部署与调用**：
   - 查询任务状态直至 `status` 为 `SUCCEEDED`，获取 `finetuned_output`。
   - 调用 `/api/v1/deployments` 部署，`plan` 设为 `"lora"`（LoRA 模型）或 `"full"`（全参模型）。
   - 部署成功（`status` 为 `RUNNING`）后，使用 `deployed_model` 名称调用对应服务（如图像生成需带 `X-DashScope-Async: enable` 头）。

## 限制和注意事项

- **地域与权限**：所有微调任务**仅限华北2（北京）地域**，且子账号需显式授予模型调用、训练、部署权限 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **计费模式**：
  - 文本/视觉微调：按训练消耗 [Token](../concepts/token.md) 数计费（单价见模型文档），[Token](../concepts/token.md) 数 = 数据 Token 总数 × 循环次数。
  - CosyVoice：训练费 0.2 元/千 Token，部署费按模型单元时长计费。
  - RL 训练：**强制使用 MTU 训练单元（预付费/后付费）**，不支持 Token 计费。
- **数据与格式约束**：
  - 图像分辨率上限为 8K，但超过 4K 仅支持 JPG/PNG；视频帧列表模式要求 `qwen3.5+` VL 模型。
  - CosyVoice 训练数据必须为**同一发音人**，混合多人会导致音色失真；`text` 字段禁止含 SSML/LaTeX 标签。
- **能力边界**：
  - 微调无法扩展基础模型能力（如 CosyVoice 不支持新语种，万相模型无法新增特效类型）。
  - LoRA 微调产物为轻量级适配器，部署后模型名固定（如 `xxx-ft-xxxx`），不可切换音色或风格。
- **调试建议**：首次训练推荐使用精简数据集快速验证链路；关注 `Training Loss` 与 `Validation Loss` 曲线判断欠拟合/过拟合；RL 训练需紧盯 `critic/rewards/mean` 指标趋势。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


