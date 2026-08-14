# fine tuning

fine tuning（微调）是百炼平台提供的核心模型优化能力，允许开发者基于预训练大模型，使用自有业务数据定制化提升其在特定任务、领域或风格上的表现。它不改变基础模型架构，而是通过增量学习注入领域知识、对齐人类偏好或强化安全合规能力，适用于文本生成、图像/视频生成、语音合成等多模态场景。所有微调均需在华北2（北京）地域执行，并依赖 DashScope API Key 和相应 RAM 权限。

## 支持的模型与功能

百炼支持多种微调方式及对应模型，覆盖文本、视觉、语音和强化学习四大方向：

- **文本生成**：支持 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化）三种方式。全参训练与 LoRA 高效训练均可用，其中 `qwen3-32b`、`qwen3-14b` 等主流模型全面支持 `sft`、`efficient_sft`、`dpo_full`、`dpo_lora`；而 `qwen3.7-plus-2026-05-26` 仅支持 `efficient_sft` [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。  
- **视觉理解（千问VL）**：支持图片/视频输入的 SFT 微调，如 `qwen3-vl-8b-instruct`，但不支持 DPO 或 CPT [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。  
- **图像生成**：仅支持 `wan2.7-image-pro` 和 `wan2.7-image` 两款模型，采用 SFT-LoRA 方式，分文生图（t2i）与图生图（i2i）两种模式 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。  
- **视频生成**：支持 `wan2.7-i2v`、`wan2.5-i2v-preview`、`wan2.2-i2v-flash`（首帧）及 `wan2.2-kf2v-flash`（首尾帧），同样基于 SFT-LoRA [原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。  
- **语音合成**：仅支持 `cosyvoice-v3-flash` 模型的 SFT 微调，用于构建高还原度专属音色，产物为独立部署模型且 `voice` 参数固定为 `default` [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
- **强化学习（RL）**：面向 Agent 推理优化，支持 `qwen3.5-9b`、`qwen3.6-flash-2026-04-16` 等 MoE 模型，需通过 SDK 提交任务并依赖模型训练单元（MTU）计费，不支持 [Token](../concepts/token.md) 计费 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 5 与文档 8 的模型支持矩阵存在不一致——文档 5 声明 `qwen3.7-plus-2026-05-26` 仅支持 `efficient_sft`，而文档 8 的表格中该模型“SFT全参训练（sft）”列为“支持”。以文档 5 为准，该模型不支持全参 SFT 训练，仅支持高效微调。

## 关键参数

不同微调类型的关键参数差异显著，开发者需按场景严格配置：

- **通用超参（文本/SFT）**：`n_epochs`（循环次数，必填）、`batch_size`（批次大小，必填）、`learning_rate`（学习率，推荐高效训练用 `1e-4` 量级，全参训练用 `1e-5` 量级）、`max_length`（序列长度，建议设为模型最大支持值）。`lr_scheduler_type` 推荐 `linear` 或 `inverse_sqrt`，`cosine_with_restarts` 经实测无效，不推荐使用 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。  
- **LoRA 专用参数**：`lora_rank`（秩值，推荐设为模型支持的最大值以提升效果）、`lora_alpha`（缩放系数，常与 `lora_rank` 同值）、`lora_dropout`（丢弃率，默认 `0.1`）。  
- **图像/视频微调特有参数**：`generation_type`（`t2i`/`i2i`/`i2v`）、`max_pixels`（训练图最大像素数，如 `"2k"` 表示 2048×2048）、`val_img_size`（验证图分辨率）、`max_token_length`（如 `"2k"`）；视频微调还需 `max_pixels`（整型，如 `102400`）和 `batch_size`（模型强约束，如 `wan2.7-i2v` 必须为 `1`）[原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。  
- **语音微调特有参数**：分为 LM（语言模型，影响韵律）与 FM（流匹配模型，影响音色）两套参数，如 `lm_max_epoch=60`、`fm_max_epoch=100`，二者必须同时配置且不可省略 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
- **RL 微调特有参数**：`algorithm="gspo"`、`kl_loss_coef=0.002`、`batch_size=64`，且必须指定 `resources`（MTU 规格与数量）[原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 使用方式

微调流程统一为四步：准备数据 → 上传文件 → 创建任务 → 部署调用，但接口与细节因方式而异：

- **API 方式（推荐）**：适用于所有场景。先调用 `/api/v1/files` 上传 `.zip`（图像/视频/语音）或 `.jsonl`（文本）文件，获取 `file_id`；再调用 `/api/v1/fine-tunes` 提交任务，`training_datasets` 字段支持 `file_id` 或 `oss_mount`（OSS 挂载需授权，仅限北京/新加坡地域）[原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。图像生成任务示例中 `training_type` 固定为 `"efficient_sft"`，而文本任务可选 `"sft"` 或 `"efficient_sft"` [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。  
- **控制台方式**：仅支持文本生成（SFT/DPO/CPT）及部分视觉模型。在“模型调优”页面选择模型、训练方式、数据集及超参，一键提交。控制台自动处理数据切分（如 `split=0.9`）、Checkpoint 保存策略等，但不支持图像/视频/语音微调 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。  
- **RL 特殊流程**：需下载 SDK Demo 包，编写 Rollout/Reward 函数，运行 `python submit_job.py` 一步完成函数部署、数据上传与任务提交，全程依赖 MTU 资源 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。  
- **部署调用**：微调成功后（`status=SUCCEEDED`），调用 `/api/v1/deployments` 部署为在线服务。图像/视频模型部署时 `plan="lora"`；语音模型部署后 `voice` 参数强制为 `"default"`；文本模型部署后即可用 `deployed_model` 名称调用 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

## 限制和注意事项

- **地域与权限**：所有微调操作**仅限华北2（北京）地域**，且必须使用该地域的 API Key。RAM 子账号需显式授予 `dashscope:FineTune*`、`dashscope:Deploy*` 等权限 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。  
- **数据格式与大小**：文本 SFT/DPO 使用 `.jsonl`，单文件 ≤200 MB；图像/视频/语音需 `.zip` 打包，含 `data.jsonl` 及媒体文件；语音训练音频需 `.wav` 格式、≥16 kHz、单条 ≥1 秒 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。  
- **计费与资源**：微调按训练消耗 [Token](../concepts/token.md) 计费（单价见文档 5），RL 训练**强制使用 MTU 计费**，不支持 [Token](../concepts/token.md) 计费 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)；语音微调费用 = `(lm_max_epoch + fm_max_epoch) × 25 × 总秒数 × 0.2 元/千 Tokens` [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
- **模型产物与能力边界**：微调产物为新模型 ID（如 `xxxx-ft-...`），非基础模型的音色 ID 或风格[插件](../concepts/plugin.md)；语音微调后**不支持指令控制、声音复刻或新增语种**；图像微调后无需提示词即可复现训练风格，但无法扩展基础模型不支持的画质或分辨率 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
- **训练监控与调优**：关注 `Training Loss` 与 `Validation Loss` 曲线——若训练损失降而验证损失升，表明过拟合，应减少 `n_epochs` 或增大 `weight_decay`；若两者均平稳，说明训练充分 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)


