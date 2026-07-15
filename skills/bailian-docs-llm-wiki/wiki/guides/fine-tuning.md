# fine tuning

fine tuning（微调）是阿里云百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练大模型进行定制化训练，从而在特定任务、领域或风格上显著提升效果。它适用于图像生成、视频生成、文本生成、语音合成等多种模态，支持高效微调（LoRA）与全参微调两种模式，兼顾效果与成本。微调后的模型可独立部署为在线服务，直接用于生产环境。

## 支持的模型/功能

百炼平台支持多模态、多场景的 fine tuning，覆盖主流业务需求：

- **图像生成**：支持 `wan2.7-image-pro` 和 `wan2.7-image` 模型，通过 SFT-LoRA 微调实现人物形象、IP 风格、特效（如“末日废土红黑机甲”）的稳定复现 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成**：支持 `wan2.7-i2v`、`wan2.5-i2v-preview`、`wan2.2-i2v-flash`（首帧驱动）及 `wan2.2-kf2v-flash`（首尾帧驱动）等模型，用于定制动作、转场与特效（如“金钱雨”“时尚杂志”） [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **文本生成**：覆盖 Qwen 系列全量模型（如 `qwen3-8b`、`qwen3-32b`、`qwen2.5-72b-instruct`），支持 SFT、CPT、DPO 三种训练方式，适用于角色扮演、客服流程、安全合规强化等场景 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **语音合成**：仅支持 `cosyvoice-v3-flash` 模型的 SFT 高效微调，面向同一发音人多小时录音的高还原度音色定制，产物为独立部署的单音色模型 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **视觉理解（VL）**：支持 `qwen3-vl-8b-instruct` 等千问 VL 系列模型的 SFT 微调，支持图文多模态输入训练 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

> **注意**：文档 1 和文档 2 均明确限定“仅在华北2（北京）地域可用”，但文档 3、4、5 未强调地域限制；实际使用中，所有 fine tuning 功能均强制要求使用北京地域 API Key，该约束具有一致性，无需额外标注矛盾。

## 关键参数

不同模态和训练方式的关键参数存在差异，开发者需按场景选择：

- **通用超参**（文本/视觉/语音共用）：
  - `learning_rate`：高效训练推荐 `1e-4` 量级，全参训练推荐 `1e-5` 量级；过高易震荡，过低收敛慢。
  - `n_epochs` / `max_steps`：控制训练轮次或步数。文本 SFT 推荐 `3~5` 轮（数据 <10k 条）；图像/视频任务常用固定步数（如 `800` 步）；CosyVoice 则拆分为 `lm_max_epoch`（语言模型）与 `fm_max_epoch`（流匹配模型）[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - `lora_rank`：LoRA 秩值，影响表达能力与过拟合风险。图像微调默认 `32`；文本微调推荐设为模型支持的最大值；CosyVoice 推荐 `lm_rank=60`、`fm_rank=100`。
  - `batch_size`：文本训练常用 `16` 或 `32`；图像/视频因显存限制常设为 `1`；CosyVoice 使用 `lm_batch_size=1000`、`fm_batch_size=2000`。

- **模态特有参数**：
  - 图像生成：`generation_type`（`t2i` 或 `i2i`）、`max_pixels`（最大像素数）、`val_img_size`。
  - 视频生成：`split`（训练/验证集划分比例）、`eval_epochs`（验证周期）、`resolution`（输出分辨率）。
  - 语音合成：`lm_step`/`fm_step`（Checkpoint 保存步长）、`lm_num`/`fm_num`（保留 Checkpoint 数量）。
  - 安全合规微调：`lr_scheduler_type` 推荐 `cosine`，配合 `eval_steps=10` 可更早捕捉过拟合信号 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 使用方式

fine tuning 分为数据准备、任务创建、状态监控、部署调用四步，支持控制台与 API 两种入口：

- **数据准备**：
  - 文本/视觉：使用 ChatML 格式 `data.jsonl`，`messages` 字段含 `system`/`user`/`assistant` 多轮对话；图片/视频文件名需全局唯一，ZIP 包内 `data.jsonl` 必须位于根目录 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
  - 语音：`data.jsonl` 每行含 `wav_fn`（相对路径，如 `train/100001.wav`）与 `text`（纯文本，禁用 SSML/LaTeX）[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - 上传统一调用 `/api/v1/files` 接口，`purpose="fine-tune"`，返回 `file_id`。

- **任务创建**：
  - API 方式：POST `/api/v1/fine-tunes`，传入 `model`、`training_datasets`（含 `file_id` 或 OSS 挂载配置）、`training_type`（如 `efficient_sft`）、`hyper_parameters`。
  - 控制台方式：在[模型调优](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager)页面选择模型、训练方式、数据集，配置超参后提交。

- **状态监控**：
  - 轮询 `/api/v1/fine-tunes/{job_id}` 获取 `status`（`PENDING` → `RUNNING` → `SUCCEEDED`）。
  - CosyVoice 任务可能进入 `QUEUING`（平台单任务队列），需预留排队时间 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **部署与调用**：
  - 部署：POST `/api/v1/deployments`，传入 `model_name`（即 `finetuned_output`），`plan="lora"`（LoRA 模型）。
  - 调用：图像/视频使用异步 API（`X-DashScope-Async: enable`），获取 `task_id` 后轮询 `/api/v1/tasks/{task_id}`；文本/语音使用同步 API，直接返回结果。

## 限制和注意事项

- **地域与权限**：所有 fine tuning 功能**仅限华北2（北京）地域**，必须使用该地域 API Key；RAM 子账号需授予 `AliyunBailianFullAccess` 或最小化权限策略（含 `dashscope:CreateFineTuneJob`、`dashscope:DeployModel` 等）[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **数据与成本**：
  - 训练费用按 [Token](../concepts/token.md) 计费（文本/视觉）或按公式 `Tokens = (lm_max_epoch + fm_max_epoch) × 25 × 总时长(秒)`（语音）；单价从 ¥0.003/千 [Token](../concepts/token.md)（Qwen3-0.6B）到 ¥0.15/千 [Token](../concepts/token.md)（Qwen2.5-72B）不等 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
  - 单个 ZIP 文件 ≤ 2 GB；文本数据必须为 `data.jsonl`；图片单张 ≤ 1024×1024 px & ≤10 MB；语音 WAV 采样率 ≥16 kHz [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **效果与工程权衡**：
  - LoRA 训练快、成本低，适合快速验证；全参训练效果更优但耗时长、费用高 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
  - 安全合规微调需高质量拒答样本（如诱导网贷、历史错误表述），且评测必须使用**未见于训练集的新数据**，否则分数虚高 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。
  - CosyVoice 产物为单音色模型，`voice` 参数固定为 `default`，不再支持声音复刻或设计 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)


