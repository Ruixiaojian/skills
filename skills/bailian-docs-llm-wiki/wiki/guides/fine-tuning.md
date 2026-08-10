# fine tuning

fine tuning 是阿里云百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练模型进行定制化训练，以提升其在特定业务场景、领域知识或安全合规要求下的表现。该能力覆盖文本生成、[多模态](../concepts/multi-modal.md)理解、图像/视频生成及语音合成等多种模型类型，支持 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化）及 RL（强化学习）等多种范式，兼顾效果、效率与成本。

## 支持的模型与功能

百炼平台支持多种模态和任务类型的 fine tuning，但不同模型支持的训练方式存在差异。文本生成模型（如 Qwen 系列）全面支持 CPT、SFT（含高效 LoRA 训练 `efficient_sft`）和 DPO；视觉理解模型（Qwen-VL 系列）支持 SFT 和 DPO；图像生成（万相 `wan2.7-image-*`）和视频生成（万相 `wan2.7-i2v` 等）仅支持 SFT-LoRA 高效微调；语音合成模型（CosyVoice）当前仅支持 `efficient_sft` [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。强化学习（RL）训练则需联系商务经理开通，且仅支持指定 MoE 或非 MoE 的千问大模型 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。所有 fine tuning 任务均**仅限华北2（北京）地域**，且需使用该地域的 API Key [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

> **注意**：文档 4 和文档 6 的表格中均列出 `qwen3.5-9b` 支持 `efficient_sft`，但文档 9 的“全参训练与高效训练”章节明确指出“如果模型支持全参训练，请优先选择全参训练，因为全参训练效果比高效训练效果要好”，且未说明 `qwen3.5-9b` 不支持全参。这与文档 4 表格中 `qwen3.5-9b` 对应 `efficient_sft` 列为“支持”、`sft` 列也为“支持”的表述一致，但文档 9 的推荐逻辑暗示两者可并存。此处以表格为准，即 `qwen3.5-9b` 同时支持 `sft`（全参）和 `efficient_sft`（高效），开发者可根据效果与成本权衡选择。

## 关键参数

fine tuning 的关键参数因模型和训练方式而异，但核心超参具有共性：
- **`learning_rate`（学习率）**：控制权重更新幅度。文本 SFT 推荐 `1e-4`（高效）或 `1e-5`（全参）量级；图像/视频生成模型推荐 `3e-5` 或 `2e-5`；RL 训练推荐 `2e-6`。过高易导致发散，过低收敛缓慢。
- **`n_epochs` / `max_steps`**：决定训练深度。文本 SFT 推荐 `3~5` 轮（小数据集）或 `1~2` 轮（大数据集）；图像生成推荐 `800` 步；视频生成推荐 `50` 轮（对应约 800+ 步）；CosyVoice 语音模型需分别设置 `lm_max_epoch=60` 和 `fm_max_epoch=100`。
- **`batch_size`**：影响内存占用与收敛稳定性。文本 SFT 常用 `16` 或 `32`；视频生成模型 `wan2.7-i2v` 推荐 `1`，`wan2.2-kf2v-flash` 推荐 `4`；CosyVoice LM 网络推荐 `1000`，FM 网络推荐 `2000`。
- **LoRA 相关参数**：`lora_rank`（秩，如 `32` 或 `8`）、`lora_alpha`（缩放系数，如 `32` 或 `16`）和 `lora_dropout`（丢弃率，如 `0.1`）共同控制适配器的容量与泛化能力。
- **验证与保存**：`eval_steps`（如 `200`）或 `eval_epochs`（如 `20`）控制评估频率；`save_total_limit`（如 `10`）限制 Checkpoint 数量，避免存储浪费。

## 使用方式

fine tuning 全流程包含数据准备、上传、任务创建、状态监控与模型部署四步：
1. **准备数据**：文本 SFT 使用 `jsonl` 格式，遵循 ChatML 多轮结构；图像/视频 SFT 使用 `.zip` 包，内含 `data.jsonl` 和对应媒体文件；语音 SFT 要求 `.wav` 音频与 `data.jsonl` 映射；RL 训练需提供 `messages` + `rollout_extra` 的 JSONL 数据 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
2. **上传数据**：通过 `POST /api/v1/files` 接口上传，`purpose="fine-tune"`，获取 `file_id`。单文件上限 `300MB`，总配额 `100GB`。
3. **创建任务**：调用 `POST /api/v1/fine-tunes`，指定 `model`、`training_datasets`（含 `file_id` 或 OSS 挂载路径）、`training_type`（如 `"efficient_sft"`）及 `hyper_parameters`。OSS 挂载需提前授权，且仅支持北京和新加坡地域。
4. **监控与部署**：轮询 `GET /api/v1/fine-tunes/{job_id}` 直至 `status="SUCCEEDED"`，提取 `finetuned_output`；再调用 `POST /api/v1/deployments` 部署，`plan="lora"` 用于 LoRA 模型。图像/视频模型部署时需在 `aigc_config` 中配置 `lora_prompt_default` 以启用 LoRA 效果。

## 限制和注意事项

- **地域与权限**：所有 fine tuning 功能均强制要求华北2（北京）地域及对应 API Key，子账号需显式授予模型调用、训练、部署权限。
- **数据与资源**：图像输入单张宽高 ≤ `1024px`，视频输入最大 `2GB`；文本训练数据单文件 ≤ `200MB`；API 上传总文件数上限 `10000` 个。
- **计费模式**：文本/图像/视频 SFT 默认按 [Token](../concepts/token.md) 计费；RL 训练**仅支持模型训练单元（MTU）计费**，不支持 [Token](../concepts/token.md) 计费 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)；CosyVoice 训练费用 = `(lm_max_epoch + fm_max_epoch) × 25 × 总秒数 × 0.2元/千Token`。
- **模型产物**：LoRA 微调产物为独立模型 ID（如 `xxxx-ft-...`），调用时必须使用该 ID；CosyVoice 调优产物锁定 `voice="default"`，无法切换音色。
- **效果调优**：若训练损失下降而验证损失上升，表明过拟合，应减少 `n_epochs`、增大 `weight_decay` 或启用数据增强；若损失平稳，则视为良好拟合，可结束训练。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)


