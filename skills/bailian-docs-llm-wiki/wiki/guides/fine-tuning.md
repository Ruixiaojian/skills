# fine tuning

fine tuning 是阿里云百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练大模型进行定制化训练，以提升其在特定业务场景、领域知识或安全合规要求下的表现。该能力覆盖文本生成、视觉理解、语音合成、图像生成、视频生成及强化学习等多种模态与任务类型，支持高效微调（LoRA）、全参微调、持续预训练（CPT）和直接偏好优化（DPO）等多种训练范式，适用于从快速验证到生产部署的全生命周期。

## 支持的模型与功能

百炼平台支持多模态、多任务的 fine tuning，不同模型类型对应不同的训练方式与适用场景：

- **文本生成模型**：支持 SFT（监督微调）、CPT（持续预训练）和 DPO（直接偏好优化），覆盖 Qwen3 系列、Qwen2.5 系列及千问-Plus-Character 等数十种模型。其中，SFT 用于教会模型执行特定任务（如客服流程、代码范式），CPT 用于注入领域知识（如金融术语、法律条文），DPO 用于对齐人类偏好（如拒有害建议、答干脆利落）[原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
  
- **视觉理解模型（千问VL）**：支持 SFT 和 DPO，需遵循 ChatML 格式并支持图像/视频嵌入；训练数据中 `system` 消息的 `content` 必须为数组格式（如 `[{"text":"..."}]`），且图片/视频文件名需全局唯一、位于 ZIP 包根目录下 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

- **图像生成模型（万相）**：仅支持 SFT-LoRA 高效微调，当前限华北2（北京）地域，适用模型包括 `wan2.7-image-pro` 和 `wan2.7-image`，支持文生图（t2i）与图生图（i2i）两种模式 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **视频生成模型（万相）**：同样限北京地域，支持 `wan2.7-i2v`、`wan2.5-i2v-preview`、`wan2.2-i2v-flash`（首帧驱动）及 `wan2.2-kf2v-flash`（首尾帧驱动）等模型，采用 SFT-LoRA 方式，需指定 `generation_type` 对应的超参（如 `n_epochs`、`batch_size`）[原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **语音合成模型（CosyVoice）**：仅支持 `cosyvoice-v3-flash` 的 `efficient_sft` 微调，面向同一发音人多小时录音的高还原度音色定制，产物为独立部署的单音色模型，调用时 `voice` 参数固定为 `default` [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **强化学习（RL）训练**：面向 Agent 场景（如工具调用、数学推理），需通过模型训练单元（MTU）计费，不支持按 [Token](../concepts/token.md) 计费；当前支持 `qwen3.5-9b` 等非 MoE 模型及 `qwen3.6-flash` 等 MoE 模型，需联系商务经理开通权限 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 4 与文档 5 均指出“推荐您以先 CPT（可选），后 SFT，再 DPO 的顺序使用模型调优”，但文档 3 的 RL 训练流程图明确将 RL 列为可选的最终环节（`CPT→SFT→DPO→RL`）。实际工程中，RL 通常在 SFT/DPO 后引入，用于端到端策略优化，而非替代 DPO。此处以 RL 文档为准，因其专述 RL 流程。

## 关键参数

不同训练方式与模型类型的关键参数存在显著差异，开发者需按场景选择：

- **通用超参（文本/SFT）**：`learning_rate`（SFT 推荐 `1e-4` 量级，CPT 推荐 `1e-5`）、`n_epochs`（数据 <10k 条时设 3~5，>10k 条时设 1~2）、`batch_size`（默认 16/32）、`lora_rank`（LoRA 秩，默认 8，图像/视频任务常设 32）、`eval_steps`（默认 50）[原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

- **图像/视频生成专用参数**：
  - 图像：`max_pixels`（如 `"2k"` 表示 2048×2048）、`val_img_size`（验证图分辨率）、`max_token_length`（如 `"2k"`）必须保持一致；`generation_type` 必填 `"t2i"` 或 `"i2i"` [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
  - 视频：`max_pixels` 为整数（如 `102400`），`n_epochs` 与 `batch_size` 强耦合（steps = n_epochs × ⌈数据集大小 / batch_size⌉），`eval_epochs` 需 ≥ `n_epochs/10` [原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **语音合成（CosyVoice）专用参数**：分为 LM（影响韵律）与 FM（影响音色）两套子参数，如 `lm_max_epoch=60`、`fm_max_epoch=100`，`*_step` 控制 Checkpoint 保存间隔，`*_num` 控制保留数量，组合后候选模型数为 `lm_num × fm_num` [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **强化学习（RL）专用参数**：`algorithm="gspo"`、`batch_size=64`、`kl_loss_coef=0.002`、`n_rollouts=8` 等 11 项必填超参，需严格匹配基座模型类型（如 `qwen3.5-9b` 非 MoE 模型）[原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 使用方式

fine tuning 通过 API、命令行或控制台三种方式发起，流程高度统一：上传数据 → 创建任务 → 查询状态 → 部署模型 → 调用服务。

- **数据上传**：所有方式均需先将训练数据（ZIP 或 JSONL）上传至百炼平台获取 `file_id`。ZIP 包需满足：`data.jsonl` 位于根目录、图片/音频文件名全局唯一、单文件 ≤300MB（API）或 2GB（控制台）[原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

- **任务创建**：
  - **API/CLI**：通过 `POST /api/v1/fine-tunes` 提交，需指定 `model`、`training_datasets`（含 `file_id`）、`training_type`（如 `"sft"`、`"efficient_sft"`）及 `hyper_parameters`。CosyVoice 等部分模型仅支持 API [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - **控制台**：在[模型调优](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager)页面可视化配置，支持实时摘要预览，但 CosyVoice、RL 等高级功能暂未开放控制台入口。

- **状态查询与日志**：通过 `GET /api/v1/fine-tunes/{job_id}` 轮询，`status` 为 `"SUCCEEDED"` 后提取 `finetuned_output`（新模型名）；RL 训练需额外通过 `AgenticRL.logs()` 查看 Reward 曲线 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

- **模型部署与调用**：
  - 部署：调用 `POST /api/v1/deployments`，传入 `model_name`（即 `finetuned_output`）及 `plan="lora"`（LoRA 模型）。
  - 调用：使用 `deployed_model` 名称发起推理请求。注意：图像生成模型仅支持异步调用，且响应中 `message.content` 无 `type` 字段 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

## 限制和注意事项

- **地域与权限限制**：图像/视频生成、CosyVoice 及部分 RL 功能**仅限华北2（北京）地域**；子账号需显式授予模型调用、训练、部署权限，且 RL 训练必须通过 MTU 计费（不支持 [Token](../concepts/token.md) 计费）[原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **数据与格式限制**：
  - 图像训练：单张图宽高均 >10px，长宽比 ≤200:1，推荐 ≤8K 分辨率；ZIP 包内图片尺寸 ≤1024px [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
  - 语音训练：音频必须为 `.wav` 格式、采样率 ≥16kHz、单条时长 1~30 秒；`data.jsonl` 中 `wav_fn` 必须带 `train/` 前缀，`text` 为纯文本（禁用 SSML/LaTeX）[原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - RL 训练：数据量至少大于 `batch_size`，起步几十条即可验证；Demo 默认使用精简数据集 `calc_train_min.jsonl` 以避免资源浪费 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

- **计费与成本**：
  - 文本/SFT：按训练 [Token](../concepts/token.md) 总数计费，单价因模型而异（如 `qwen3-8b` ¥0.006/千Token）；高效训练（LoRA）与全参训练单价相同，但 LoRA 更快更省 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
  - CosyVoice：训练费 ¥0.2/千Tokens，部署费按模型单元时长计费；最小化超参（`lm_max_epoch=4`）实测耗时约 37 分钟，推荐超参成本约为其 20 倍 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - RL：按 MTU 单元计费（IV 型预付费 ¥19,914/月/实例），无 Token 计费选项 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

- **效果与风险**：
  - 过拟合风险：训练损失持续下降但验证损失上升时，需减少 `n_epochs` 或 `lora_rank`；欠拟合则反之 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。
  - 能力边界：调优无法扩展基础模型能力（如 CosyVoice 无法通过训练支持新语种；图像模型无法提升原生分辨率上限）[原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


