# fine tuning

fine tuning 是百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练大模型进行定制化训练，从而提升其在特定任务、领域或风格上的表现。该能力覆盖文本、图像、视频、语音等多模态模型，支持监督微调（SFT）、持续预训练（CPT）、直接偏好优化（DPO）和强化学习（RL）等多种范式，适用于安全合规加固、IP形象生成、专属音色定制等生产级场景。所有 fine tuning 任务当前均仅支持华北2（北京）地域。

## 支持的模型/功能

百炼平台支持多类模型的 fine tuning，按模态与训练目标划分如下：

- **文本生成模型**：支持 Qwen 系列（如 `qwen3-8b`, `qwen3.5-9b`, `qwen3-32b`）及千问VL系列（如 `qwen3-vl-8b-instruct`），训练方式包括 CPT、SFT（全参/LoRA）、DPO（全参/LoRA）。详见 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
  
- **图像生成模型**：仅支持万相（Wan）系列，包括 `wan2.7-image-pro` 和 `wan2.7-image`，采用 SFT-LoRA 高效微调，适用于文生图（t2i）与图生图（i2i）两类生成模式 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **视频生成模型**：支持 `wan2.7-i2v`、`wan2.5-i2v-preview`、`wan2.2-i2v-flash`（首帧驱动）及 `wan2.2-kf2v-flash`（首尾帧驱动），同样基于 SFT-LoRA，用于定制“金钱雨”“时尚杂志”等动态特效 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **语音合成模型**：当前仅支持 `cosyvoice-v3-flash` 的 SFT 高效微调（`efficient_sft`），面向同一发音人的高还原度音色定制，不支持 CPT 或 DPO [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **强化学习（RL）训练**：面向 Agent 场景（如工具调用、数学推理），需通过函数计算（FC）部署 Rollout/Reward 函数，支持 `qwen3.5-9b` 等非 MoE 模型及 `qwen3.6-flash-2026-04-16` 等 MoE 模型，**必须使用模型训练单元（MTU）计费**，不支持 [Token](../concepts/token.md) 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 4 中表格显示 `Qwen3.7-Plus-2026-05-26` 支持 SFT 全参训练，但文档 1–2、5–6 均未提及该模型的任何 fine tuning 实践；且文档 4 明确标注“调优后部署请联系商务经理”，表明其 SFT 支持尚处受限阶段，实际可用性以控制台或最新 API 文档为准。

## 关键参数

不同 fine tuning 类型的关键参数差异显著，开发者需严格匹配模型类型与超参语义：

- **图像/视频生成（SFT-LoRA）**：核心参数为 `max_steps`（总步数，≥500）、`eval_steps`（验证间隔）、`learning_rate`（默认 `3e-5`）、`lora_rank`（LoRA 维数，须为 2 的幂，如 32）、`generation_type`（`"t2i"` 或 `"i2i"`）、`max_pixels`/`val_img_size`（分辨率，如 `"2k"`）。视频模型额外使用 `n_epochs`、`batch_size`（如 `wan2.7-i2v` 推荐 `batch_size=1`）和 `max_pixels`（整型像素总数，如 `102400`）[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **文本生成（SFT LoRA）**：关键参数包括 `batch_size`（如 `16`）、`learning_rate`（如 `3e-4`）、`eval_steps`（如 `10`）、`lr_scheduler_type`（如 `"cosine"`）、`lora_rank`（如 `16` 或 `32`）。零代码控制台默认值可直接使用，但需根据损失曲线动态调整：若验证损失上升则减小 `n_epochs` 或 `lora_rank`，若持续下降则可增大 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

- **语音合成（CosyVoice SFT）**：采用双网络解耦设计，参数前缀区分 LM（语言模型，影响韵律）与 FM（流匹配模型，影响音色），如 `lm_max_epoch=60`、`fm_max_epoch=100`、`lm_batch_size=1000`、`fm_batch_size=2000`。`*_step` 与 `*_num` 共同决定 Checkpoint 保存策略，最终产物为 `checkpoint-{LM轮次}{FM轮次}` 命名的组合 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **强化学习（RL）**：必需超参包括 `algorithm="gspo"`、`batch_size=64`、`n_rollouts=8`、`kl_loss_coef=0.002`、`learning_rate=2e-6`、`max_length=8192`。所有 11 项超参均为 `qwen3.5-9b` 非 MoE 模型的推荐起点，首次训练不应修改 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 使用方式

fine tuning 流程统一为四步：准备数据 → 上传文件 → 创建任务 → 部署调用，但具体操作路径因方式而异：

- **API 方式（推荐自动化）**：适用于所有类型。先通过 `/api/v1/files` 上传 `.zip` 数据集（`purpose="fine-tune"`），获取 `file_id`；再调用 `/api/v1/fine-tunes` 提交任务，传入 `model`、`training_file_ids` 及 `hyper_parameters`；轮询 `/api/v1/fine-tunes/{job_id}` 直至 `status="SUCCEEDED"`；最后用 `finetuned_output` 调用 `/api/v1/deployments` 部署，并通过对应服务 API（如 `/services/aigc/image-generation/generation`）调用 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **零代码控制台（适合快速验证）**：仅支持文本生成模型（如 Qwen3-8B）的 SFT。在[模型调优](https://bailian.console.aliyun.com/#/efm/model_manager)页面选择“SFT微调训练”，指定模型、数据集（已上传至[数据管理](https://bailian.console.aliyun.com/#/efm/model_data)）、训练方式（高效训练/LoRA），配置超参后一键启动。训练完成后，在[模型部署](https://bailian.console.aliyun.com/#/efm/model_deploy)页面选择该模型部署 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

- **RL 训练（专用 SDK）**：必须使用 DashScope Python SDK。下载 Demo 包（含 `submit_job.py`），配置 `DASHSCOPE_API_KEY` 及 FC 环境变量，运行 `python submit_job.py` 即可自动完成函数部署、数据上传与任务提交。训练状态需在控制台“模型调优”页签中查看轨迹、指标与日志 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 限制和注意事项

- **地域与权限限制**：所有 fine tuning 任务（图像、视频、语音、文本、RL）均**仅支持华北2（北京）地域**，且必须使用该地域的 API Key。子账号需显式授予模型调用、训练、部署权限 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **数据与格式约束**：
  - 图像训练：分辨率建议 ≤ `8K`（7680×4320），宽高比 ≤ `200:1`，单图 ≤ `20MB`（公网URL）或 `10MB`（本地/ Base64）[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
  - 语音训练：音频必须为 `.wav` 格式、采样率 ≥16 kHz、单条时长 1–30 秒；`data.jsonl` 中 `wav_fn` 必须以 `train/` 开头，`text` 字段禁止包含 SSML/LaTeX/指令等标记语言 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - RL 训练：数据为 JSONL 格式，每行含 `messages`（用户问题）和 `rollout_extra`（参考答案等业务字段），`rollout_extra` 会透传至 Reward 函数用于评分 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

- **计费与资源**：
  - 文本/图像/视频/语音 SFT：按训练消耗的 [Token](../concepts/token.md) 总数计费（公式：[Token](../concepts/token.md) 总数 × 循环次数 × 单价），单价因模型而异（如 `qwen3-8b` ¥0.006/千Token，`cosyvoice-v3-flash` ¥0.2/千Token）[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
  - RL 训练：**仅支持模型训练单元（MTU）计费**，不支持 Token 计费；需提前购买或开通 IV 型 MTU（¥41.00/小时/实例），最小计费粒度为 1 分钟 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

- **能力边界**：
  - CosyVoice 调优产物为单音色独立模型，`voice` 参数强制为 `"default"`，不可切换音色，也不支持声音复刻/设计功能 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - 所有 fine tuning 均**无法扩展基础模型的原生能力**，如语种支持（CosyVoice 不支持保加利亚语）、视频音频理解（Qwen-VL 不解析视频音频流）等 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)


