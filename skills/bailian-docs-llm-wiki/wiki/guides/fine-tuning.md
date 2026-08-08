# fine tuning

fine tuning（微调）是百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练大模型进行定制化训练，以提升其在特定任务、领域或风格上的表现。该能力覆盖文本生成、多模态理解、图像/视频生成、语音合成等多种模态，并支持监督微调（SFT）、持续预训练（CPT）、直接偏好优化（DPO）及强化学习（RL）等多种训练范式。所有微调任务均需在华北2（北京）地域执行，并依赖 DashScope API Key 及相应 RAM 权限。

## 支持的模型与功能

百炼平台支持多模态、多阶段的 fine tuning，不同模型和任务类型对应不同的训练方式与能力边界：

- **文本与多模态模型**：支持 SFT、CPT、DPO 三种训练方式，覆盖 Qwen 系列（如 `qwen3-8b`、`qwen3-vl-8b-instruct`）及千问-Plus-Character 等模型。其中 SFT 用于教会模型执行特定任务（如客服流程、工具调用），CPT 用于注入领域知识（如金融术语、法律判例），DPO 用于对齐人类偏好（如拒有害建议、答干脆利落）[原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。  
- **图像生成模型**：仅支持 `wan2.7-image-pro` 和 `wan2.7-image`，采用 SFT-LoRA 高效微调，适用于文生图（t2i）与图生图（i2i）两种模式，需严格使用北京地域 API Key [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。  
- **视频生成模型**：支持 `wan2.7-i2v`、`wan2.5-i2v-preview`、`wan2.2-i2v-flash`（首帧）及 `wan2.2-kf2v-flash`（首尾帧），同样基于 SFT-LoRA，但超参结构（如 `n_epochs`、`max_pixels`）与图像模型不同 [原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。  
- **语音合成模型**：仅支持 `cosyvoice-v3-flash` 的 SFT 高效微调，目标为同一发音人的高还原度音色定制，产物为独立部署的单音色模型，不支持切换 voice 或新增语种 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
- **强化学习（RL）**：面向高级推理场景（如数学解题、Agent 工具调用），需通过模型训练单元（MTU）计费，不支持 [Token](../concepts/token.md) 计费；当前仅对 `qwen3.5-9b` 等指定模型开放，且需商务经理授权 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 5 与文档 7 均声明“阿里云百炼推荐您如果模型支持全参训练，请优先选择全参训练”，但文档 6 的支持矩阵明确显示多数 Qwen3 系列模型（如 `qwen3.5-9b`、`qwen3-14b`）仅支持 `efficient_sft`（高效训练），不支持 `sft`（全参训练）。因此，**全参训练并非普遍可用，实际支持情况应以控制台实时选项或文档 6/7 的支持矩阵为准**。

## 关键参数

不同训练方式与模型类型的关键参数存在显著差异，开发者需按场景选用：

- **通用超参（文本/SFT）**：`n_epochs`（循环次数，数据量 < 10k 推荐 3–5 次）、`learning_rate`（SFT 高效训练推荐 `1e-4` 量级）、`batch_size`（通常 16 或 32）、`max_length`（序列长度，设为模型支持最大值）、`lora_rank`（LoRA 秩值，影响拟合能力与速度，推荐设为模型支持的最大值）[原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。  
- **图像/视频专用参数**：图像生成中 `max_pixels`、`val_img_size`、`max_token_length` 需保持一致（如文生图设为 `"2k"`）；视频生成中 `max_pixels` 为整型（如 `wan2.7-i2v` 推荐 `102400`），且 `n_epochs` 与 `batch_size` 强耦合（总步数 = `n_epochs × ⌈数据集大小 / batch_size⌉`，建议 ≥ 800 步）[原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。  
- **语音合成专用参数**：CosyVoice 使用解耦的 LM（影响韵律）与 FM（影响音色）双网络超参，如 `lm_max_epoch=60`、`fm_max_epoch=100`，且 `*_step` 控制 Checkpoint 保存间隔，`*_num` 控制保留上限 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
- **RL 专用参数**：必须配置 `algorithm="gspo"`、`batch_size=64`、`kl_loss_coef=0.002`、`learning_rate=2e-6` 等 GSPO 算法必需项，且 `resources` 中需明确 `mtu_spec_code` 与 `mtu_capacity` [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 使用方式

fine tuning 可通过控制台可视化操作或 API/CLI 编程方式完成，二者流程一致但权限与计费模式有别：

- **控制台方式**：适用于快速验证，支持 SFT/CPT/DPO，提供向导式配置（选择模型、上传数据集、设置超参、启动训练）。训练完成后自动导出 Checkpoint 至“我的模型”，并支持一键部署。**注意：CosyVoice 和 RL 训练暂不支持控制台创建，必须使用 API** [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。  
- **API/CLI 方式**：适用于自动化流水线，所有模型均支持。核心步骤为：① 上传数据集（`POST /api/v1/files`，`purpose="fine-tune"`）；② 创建训练任务（`POST /api/v1/fine-tunes`，指定 `model`、`training_file_ids` 或 `training_datasets`、`training_type` 及 `hyper_parameters`）；③ 轮询任务状态（`GET /api/v1/fine-tunes/{job_id}` 直至 `status="SUCCEEDED"`）；④ 部署模型（`POST /api/v1/deployments`）。**重要：API 创建的任务仅支持 [Token](../concepts/token.md) 计费，RL 训练必须使用 MTU 计费，故 RL 任务只能通过控制台（已授权）或 SDK 提交** [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。  
- **数据格式要求**：SFT 文本需 `jsonl` 格式，遵循 ChatML messages 结构（含 `system`/`user`/`assistant` 角色）；图像/视频 SFT 需 `.zip` 包含 `data.jsonl` 与媒体文件；CosyVoice 需 `.zip` 包含 `data.jsonl`（含 `wav_fn` 与 `text` 字段）及 `train/` 目录下的 `.wav` 文件 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。

## 限制和注意事项

- **地域与权限限制**：所有 fine tuning 任务（除 RL 外）均**仅支持华北2（北京）地域**，且必须使用该地域的 API Key；RAM 子账号需被授予模型调用、训练、部署权限 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。  
- **数据与资源限制**：文本训练单文件 ≤ 300MB，总存储配额 100GB；图像单张 ≤ 10MB、宽高 ≤ 1024px；视频单个 ≤ 2GB（URL 传入）；CosyVoice 训练音频总时长建议 1–10 小时 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。  
- **功能边界**：微调无法扩展基础模型能力——CosyVoice 调优不能新增语种或指令控制；图像/视频微调无法改变生成模式（如 t2i 不能转 i2i）；RL 训练必须使用 MTU 计费，不支持 [Token](../concepts/token.md) 计费 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
- **效果调试提示**：若训练损失下降而验证损失上升（过拟合），应减少 `n_epochs`、增大 `weight_decay` 或降低 `lora_rank`；若两者均平稳，则训练充分，可终止 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


