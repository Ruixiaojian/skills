# fine tuning

fine tuning（微调）是阿里云百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练大模型进行定制化训练，以提升其在特定业务场景、领域知识或安全合规要求下的表现。该能力覆盖文本生成、[多模态](../concepts/multi-modal.md)理解、图像生成、视频生成及语音合成等多种模态，支持高效微调（LoRA）、全参微调、持续预训练（CPT）和直接偏好优化（DPO）等多种训练范式，适用于从快速验证到生产部署的全生命周期需求。

## 支持的模型与功能

百炼平台支持跨模态的 fine tuning 能力，不同模态对应不同的模型系列与训练方式：

- **文本生成与[多模态](../concepts/multi-modal.md)理解**：支持 Qwen 系列（如 `qwen3-8b`, `qwen3-vl-8b-instruct`）的 SFT、CPT、DPO 训练，涵盖纯文本、图文、视频理解等场景 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。  
- **图像生成**：仅支持万相（WanX）系列模型（如 `wan2.7-image-pro`, `wan2.7-image`），采用 SFT-LoRA 高效微调，适用于文生图（t2i）与图生图（i2i）两种模式 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。  
- **视频生成**：支持万相图生视频模型（如 `wan2.7-i2v`, `wan2.2-kf2v-flash`），同样基于 SFT-LoRA，分为“基于首帧”和“基于首尾帧”两类训练范式 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。  
- **语音合成**：仅支持 CosyVoice 模型（`cosyvoice-v3-flash`），当前**仅通过 API 支持 SFT 高效微调**，控制台暂不提供入口 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
- **强化学习（RL）**：面向 Agent 场景，支持千问系列 MoE 与非 MoE 模型（如 `qwen3.5-9b`, `qwen3.6-flash-2026-04-16`），需通过模型训练单元（MTU）计费，不支持 [Token](../concepts/token.md) 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 1 和文档 2 均明确限定图像与视频微调**仅在华北2（北京）地域可用**；而文档 4 和文档 7 中的文本生成模型调优虽未显式声明地域限制，但其计费说明与权限配置均指向同一控制台逻辑，且文档 4 开篇即强调“本文档仅适用于华北2（北京）地域”，因此所有 fine tuning 功能均受地域约束，开发者须确保 API Key 与资源部署均位于北京地域。

## 关键参数

不同训练方式与模型类型对应的关键超参数存在显著差异，需按场景选择：

- **通用文本 SFT/DPO/CPT**：必填参数包括 `n_epochs`（循环次数）、`batch_size`（批次大小）、`max_length`（序列长度）；推荐 `learning_rate` 在高效训练中设为 `1e-4` 量级，全参训练中为 `1e-5` 量级；`lora_rank` 推荐设为模型支持的最大值以提升效果 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。  
- **图像生成（WanX）**：核心参数为 `generation_type`（`t2i` 或 `i2i`）、`max_pixels`/`val_img_size`/`max_token_length`（三者建议保持一致，如文生图用 `"2k"`，图生图用 `"1k"`）、`lora_rank`（必须为 2 的幂次，如 32）及 `eval_steps`（验证间隔）[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。  
- **视频生成（WanX）**：关键参数为 `n_epochs`（需结合数据量计算总步数 ≥ 800）、`batch_size`（依模型而异，如 `wan2.7-i2v` 推荐为 1）、`max_pixels`（整数，如 `102400` 表示 1024×100 分辨率上限）及 `lora_alpha`（与 `lora_rank` 协同控制 LoRA 权重缩放）[微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。  
- **语音合成（CosyVoice）**：采用双网络解耦设计，`lm_*` 参数（如 `lm_max_epoch=60`）主导韵律建模，`fm_*` 参数（如 `fm_max_epoch=100`）主导音色还原，二者均需显式指定且不可省略 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
- **强化学习（RL）**：算法级参数如 `algorithm="gspo"`、`kl_loss_coef=0.002`、`batch_size=64` 为必填项，且需配合 MTU 资源规格（如 `mtu_spec_code="MTU4"`）与数量（如 `mtu_capacity=24`）共同配置 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 使用方式

fine tuning 可通过控制台可视化操作或 API/CLI 编程方式完成，两者流程高度一致：

1. **准备数据集**：按模态要求构造合规数据。文本 SFT 使用 `jsonl`（ChatML 格式）；图像/视频 SFT 使用 `.zip` 包含 `data.jsonl` 与媒体文件；CosyVoice 使用 `.zip` 包含 `data.jsonl` 与 `.wav` 文件；RL 训练则需 `jsonl` 含 `messages` 与 `rollout_extra` 字段 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。  
2. **上传数据**：通过 `/api/v1/files` 接口上传，获取 `file_id`；或在控制台「数据管理」页面上传并发布 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。  
3. **创建训练任务**：调用 `/api/v1/fine-tunes` 接口，传入 `model`、`training_datasets`（或 `training_file_ids`）、`training_type`（如 `"efficient_sft"`）及 `hyper_parameters`；控制台用户在「模型调优」页面填写表单即可 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。  
4. **监控与查询**：轮询 `/api/v1/fine-tunes/{job_id}` 获取 `status`（`SUCCEEDED` 表示成功），关注 `finetuned_output`（新模型名）与 `usage`（[Token](../concepts/token.md) 消耗）[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。  
5. **部署与调用**：将 `finetuned_output` 作为 `model_name` 调用 `/api/v1/deployments` 部署为在线服务，状态变为 `RUNNING` 后即可按标准 API 调用 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

## 限制和注意事项

- **地域与权限**：所有 fine tuning 功能均**仅限华北2（北京）地域**，且子账号需被授予模型调用、训练、部署的完整权限 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。  
- **数据格式强约束**：图像 SFT 要求单张图片宽高 ≤ 1024 px、单张 ≤ 10 MB；视频 SFT 对时长（如 `qwen3.5` 系列为 2 秒至 2 小时）、格式（MP4/AVI 等）与大小（URL 传入时 ≤ 2 GB）有严格限制；CosyVoice 仅接受 `.wav` 格式音频 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。  
- **计费模式差异**：文本/图像/视频微调按 [Token](../concepts/token.md) 消耗计费；CosyVoice 微调含训练费（0.2 元/千 Tokens）与部署费（按模型单元时长）；RL 训练**强制使用 MTU 训练单元**，不支持 Token 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。  
- **功能边界明确**：CosyVoice 微调产物为单音色模型，`voice` 参数固定为 `default`，不支持声音复刻或设计；万相微调后无需提示词即可复现训练特效，但无法扩展基础模型不支持的语种或动作 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
- **训练失败诊断**：若训练损失下降而验证损失上升，表明过拟合，应减少 `n_epochs`、增大 `weight_decay` 或降低 `lora_rank`；反之若两者均平稳，则训练收敛良好 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


