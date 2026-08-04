# fine tuning

fine tuning（微调）是阿里云百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练大模型进行定制化训练，以提升其在特定业务场景、领域知识或风格表达上的表现。该能力覆盖文本、图像、视频、语音等多模态模型，支持监督微调（SFT）、持续预训练（CPT）、直接偏好优化（DPO）及强化学习（RL）等多种范式，兼顾效果与成本效率。所有微调任务均需在华北2（北京）地域执行，并依赖 DashScope API Key 进行身份认证与资源调度。

## 支持的模型与功能

百炼平台支持对多种官方模型进行微调，具体能力因模型类型而异：

- **文本生成模型**：支持 Qwen 系列（如 `qwen3-8b`、`qwen3.5-9b`）、千问 VL 多模态模型（如 `qwen3-vl-8b-instruct`）的 SFT、CPT 和 DPO 训练。其中 SFT 高效训练（`efficient_sft`）采用 LoRA 技术，显著降低显存与时间开销；CPT 适用于注入海量领域知识；DPO 则用于对齐人类偏好 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
  
- **图像生成模型**：万相（Wan）系列支持 `wan2.7-image-pro` 和 `wan2.7-image` 的 SFT-LoRA 微调，适用于文生图（t2i）和图生图（i2i）两种模式，可定制 IP 形象、艺术风格等 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **视频生成模型**：万相视频模型（如 `wan2.7-i2v`、`wan2.2-kf2v-flash`）支持 SFT-LoRA 微调，用于稳定复现特定动作、特效或镜头语言，例如“金钱雨”或“时尚杂志”风格 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **语音合成模型**：CosyVoice (`cosyvoice-v3-flash`) 仅支持 SFT 高效微调，面向同一发音人的高还原度音色定制，产物为独立部署的单音色模型，不支持切换音色或新增语种 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **强化学习（RL）**：支持 `qwen3.5-9b` 等模型的 RL 训练，通过 Rollout + Reward 机制驱动模型自主探索最优策略，适用于数学推理、Agent 工具调用等需深度推理的场景 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 4 与文档 7 中关于 `qwen3.7-plus-2026-05-26` 的部署说明存在矛盾——文档 4 明确标注“调优后部署请联系商务经理”，而文档 7 的支持矩阵中未体现此限制。实际使用时应以控制台提示或商务确认为准。

## 关键参数

不同微调任务的关键超参数差异较大，需严格按模型类型配置：

- **通用文本 SFT**：必填 `n_epochs`（循环次数）、`batch_size`（批次大小）、`learning_rate`（学习率）和 `max_length`（序列长度）。推荐值依数据量而定：数据 < 10,000 条时设 `n_epochs=3~5`；`learning_rate` 高效训练用 `1e-4` 量级，全参训练用 `1e-5` 量级 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

- **图像/视频微调**：核心参数为 `max_pixels`（训练图像/视频最大像素总数）、`lora_rank`（LoRA 秩，推荐 32）、`lora_alpha`（缩放系数，推荐 32）。视频模型 `wan2.7-i2v` 推荐 `max_pixels=102400`，而 `wan2.2-kf2v-flash` 推荐 `262144` [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)；图像模型则使用 `"1k"` 或 `"2k"` 字符串表示分辨率上限 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **CosyVoice 语音微调**：参数解耦为 LM（语言模型）与 FM（流匹配模型）两组，全部必填。生产推荐值为 `lm_max_epoch=60`、`fm_max_epoch=100`，最小化验证值（`lm_max_epoch=4`, `fm_max_epoch=4`）仅用于流程验证，不可用于生产 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **强化学习（RL）**：必需 `algorithm`（如 `"gspo"`）、`batch_size`（如 64）、`learning_rate`（如 `2e-6`）、`kl_loss_coef`（KL 散度系数，如 `0.002`）等 GSPO 算法专属参数 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 使用方式

微调可通过控制台可视化操作或 API/命令行两种方式完成：

- **控制台流程**：进入[模型调优](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager)页面 → 创建训练任务 → 选择模型与训练方式（SFT/CPT/DPO）→ 配置超参 → 选择训练/验证数据集 → 设置计费方式（[Token](../concepts/token.md) 或 MTU）→ 开始训练。训练完成后，模型自动发布至“我的模型”，可一键部署 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

- **API 流程**：分三步调用 DashScope API：
  1. **上传数据**：`POST /api/v1/files` 上传 `.zip` 或 `.jsonl` 文件，获取 `file_id`；
  2. **创建任务**：`POST /api/v1/fine-tunes` 提交训练请求，传入 `model`、`training_file_ids` 及 `hyper_parameters`；
  3. **查询与部署**：轮询 `GET /api/v1/fine-tunes/{job_id}` 直至 `status=SUCCEEDED`，再调用 `/api/v1/deployments` 部署 `finetuned_output` 模型 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

> **注意**：CosyVoice 微调**仅支持 API 方式**，控制台暂不提供入口 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)；而 RL 训练**必须使用模型训练单元（MTU）计费**，不支持 [Token](../concepts/token.md) 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 限制和注意事项

- **地域与权限**：所有微调任务强制要求在华北2（北京）地域执行，且 API Key 必须为该地域生成。子账号需被授予 `AliyunBailianFullAccess` 或等效细粒度权限（模型调用、训练、部署） [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **数据格式与大小**：
  - 文本 SFT 数据为 `.jsonl`，单文件 ≤ 200 MB；图像/视频 SFT 数据为 `.zip` 包，内含 `data.jsonl` 与媒体文件，单包 ≤ 300 MB [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
  - CosyVoice 训练音频需为 `.wav` 格式，采样率 ≥ 16 kHz，单条时长 1–30 秒，总时长建议 1–10 小时 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **计费与资源**：
  - 文本/图像/视频微调按训练消耗 [Token](../concepts/token.md) 计费，单价依模型而异（如 `qwen3-8b` 为 ¥0.006/千 Token） [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
  - CosyVoice 训练费用 = `(lm_max_epoch + fm_max_epoch) × 25 × 总秒数 × ¥0.2/千 Token`，部署费用另计 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - RL 训练必须购买 MTU（模型训练单元），IV 型单元后付费单价 ¥41.00/小时 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

- **模型产物与调用**：微调产出为新模型 ID（如 `qwen3-8b-ft-xxx`），部署后需用该 ID 调用，而非原基础模型 ID。CosyVoice 产物固定 `voice="default"`，不可切换音色；万相视频模型部署时需配置 `aigc_config.use_input_prompt=false` 以启用 LoRA 默认提示 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

## 来源文档

- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


