# fine tuning

fine tuning 是阿里云百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练模型进行定制化训练，以显著提升其在特定业务场景、垂直领域或风格任务上的表现。该能力覆盖文本生成、视觉理解（文生图/图生图/图生视频）、语音合成等多模态模型，支持监督微调（SFT）、持续预训练（CPT）、直接偏好优化（DPO）及强化学习（RL）等多种范式，兼顾效果、效率与成本。

## 支持的模型/功能

百炼平台支持多种模型类型和调优方式，覆盖主流应用场景：

- **文本生成模型**：支持 Qwen 系列（如 `qwen3-8b`, `qwen3.5-9b`, `qwen3-32b`）及千问 VL 多模态模型（如 `qwen3-vl-8b-instruct`），提供 CPT、SFT（全参/高效 LoRA）、DPO 三种训练方式 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。其中 SFT 高效训练（`efficient_sft`）是默认推荐方式，适用于绝大多数业务微调需求。
  
- **图像生成模型**：万相系列（`wan2.7-image-pro`, `wan2.7-image`）支持 SFT-LoRA 微调，用于定制 IP 形象、特定艺术风格或画面效果 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。该功能仅限华北2（北京）地域，且需使用对应地域的 API Key。

- **视频生成模型**：万相图生视频模型（`wan2.7-i2v`, `wan2.2-kf2v-flash` 等）同样采用 SFT-LoRA 方式，可训练“金钱雨”、“时尚杂志”等专属特效 [原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。与图像生成一致，该能力也严格限定于北京地域。

- **语音合成模型**：CosyVoice（`cosyvoice-v3-flash`）支持 SFT 高效微调，面向同一发音人的高还原度音色定制，但**控制台暂不支持，仅可通过 API 发起** [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **强化学习（RL）**：支持 Qwen3.5-9B 等 MoE 和非 MoE 模型，通过 Rollout + Reward 循环实现自主策略优化，适用于数学推理、Agent 工具调用等复杂任务 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。> **注意**：RL 训练**仅支持通过模型训练单元（MTU）计费**，不支持按 Token 计费方式，且需完成阿里云 OpenTelemetry、函数计算（FC）和日志服务（SLS）三项服务授权。

## 关键参数

不同调优方式和模型类型对应的关键超参数存在差异，开发者需根据任务目标谨慎配置：

- **通用核心参数**：
  - `learning_rate`：学习率是影响收敛稳定性的最关键参数。文本 SFT 推荐值为 `1e-4`（高效训练）或 `1e-5`（全参训练）；图像/视频微调中，`wan2.7-image-pro` 推荐 `3e-5`，`wan2.7-i2v` 推荐 `2e-5`。
  - `n_epochs` / `max_steps`：控制训练总轮次或步数。文本 SFT 建议 `3~5` 轮（小数据集）或 `1~2` 轮（大数据集）；图像微调推荐 `max_steps=800`；视频微调则以 `n_epochs=50` 为起点，实际步数由 `batch_size` 和数据量决定。
  - `batch_size`：批次大小直接影响显存占用和训练稳定性。图像微调中 `wan2.7-i2v` 必须设为 `1`，而 `wan2.2-kf2v-flash` 可设为 `4`；文本 SFT 通常使用 `16` 或 `32`。

- **LoRA 专用参数**（`efficient_sft`）：
  - `lora_rank`：低秩矩阵维数，决定可训练参数量。图像/视频微调中普遍设为 `32`；文本微调控制台默认为 `8`，API 文档建议设为模型支持的最大值以获得更好效果。
  - `lora_alpha`：权重缩放系数，常与 `lora_rank` 同值（如 `32`），用于平衡原始权重与 LoRA 修正项。

- **CosyVoice 专用参数**：采用解耦的 LM（语言模型）与 FM（流匹配模型）双网络架构，需分别配置 `lm_max_epoch`（推荐 `60`）、`fm_max_epoch`（推荐 `100`）等 8 个字段，不可省略 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **RL 专用参数**：`algorithm="gspo"`、`batch_size=64`、`kl_loss_coef=0.002` 等均为 GSPO 算法必需超参，且必须与所选基座模型（如 `qwen3.5-9b`）严格匹配。

## 使用方式

fine tuning 可通过控制台可视化操作或 API/CLI 编程方式完成，两者流程高度一致：

1. **准备数据集**：按指定格式构造训练数据。文本 SFT 使用 `jsonl` 格式，每行含 `messages` 字段（ChatML 结构）；图像/视频微调需打包为 `.zip`，内含 `data.jsonl` 和对应图片/视频文件；CosyVoice 则要求 `wav_fn` 和 `text` 字段严格匹配 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。

2. **上传数据**：通过 `POST /api/v1/files` 接口上传文件，获取唯一 `file_id`。单个文件上限为 `300MB`，总配额为 `100GB` [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

3. **创建训练任务**：调用 `POST /api/v1/fine-tunes`，传入 `model`、`training_file_ids`（或 `training_datasets`）、`training_type`（如 `"efficient_sft"`）及 `hyper_parameters`。图像/视频微调使用 `training_file_ids` 字段，而文本微调推荐使用更灵活的 `training_datasets` 数组 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

4. **查询与部署**：轮询 `GET /api/v1/fine-tunes/{job_id}` 直至 `status="SUCCEEDED"`，提取 `finetuned_output`；再调用 `POST /api/v1/deployments` 部署该模型，等待 `status="RUNNING"` 后即可通过标准 API 调用。

## 限制和注意事项

- **地域与权限限制**：图像生成、视频生成、CosyVoice 微调及 DPO/CPT 训练均**仅支持华北2（北京）地域**，且必须使用该地域的 API Key。子账号需被授予模型调用、训练和部署的完整权限 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **数据与资源限制**：图像输入分辨率上限为 `8K`，单张图片不超过 `10MB`；视频文件上传上限为 `2GB`（北京地域）；文本训练数据单文件上限 `200MB`；所有有效文件总数上限 `10000` 个 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

- **模型与功能限制**：CosyVoice 调优产物为单音色独立模型，`voice` 参数固定为 `"default"`，不再支持声音复刻或设计功能；其语种支持完全继承自基础模型，无法通过训练扩展 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **计费与成本**：文本/图像/视频微调按训练消耗的 Token 总数计费；CosyVoice 训练费用为 `0.2 元/千 Tokens`，部署费用则按模型单元时长计费；RL 训练必须使用 MTU 计费，不支持 Token 计费 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

- **效果与调试**：训练过程中需监控 `Training Loss` 与 `Validation Loss` 曲线。若训练损失下降而验证损失上升，表明过拟合，应减少 `n_epochs` 或增大 `weight_decay`；若两者均平稳，则视为良好拟合，可结束训练 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


