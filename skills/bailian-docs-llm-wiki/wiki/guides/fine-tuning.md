# fine tuning

fine tuning（微调）是百炼平台提供的核心模型优化能力，允许开发者基于预训练大模型，使用自有领域数据进行定制化训练，从而提升模型在特定任务、风格或安全合规等维度的表现。它不改变基础模型架构，而是通过参数增量更新（如LoRA）或全量更新方式，将业务知识、表达习惯和价值观对齐目标注入模型。微调适用于图像生成、视频生成、文本生成、语音合成及多模态理解等多种模态，支持SFT、DPO、CPT等多种训练范式。

## 支持的模型/功能

百炼平台支持跨模态的微调能力，不同模态对应不同的模型系列与训练方式：

- **文本生成**：支持Qwen3系列（如`qwen3-8b`, `qwen3-32b`）、Qwen2.5系列及千问-Plus-Character等模型，涵盖SFT（监督微调）、DPO（直接偏好优化）和CPT（持续预训练）三种方式。其中高效训练（`efficient_sft`）为LoRA实现，推荐用于快速验证与成本敏感场景；全参训练适用于效果优先的生产环境 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
  
- **图像生成**：仅支持万相系列模型（`wan2.7-image-pro`, `wan2.7-image`），采用SFT-LoRA高效微调，适用于文生图（t2i）与图生图（i2i）两种模式，需在华北2（北京）地域使用 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **视频生成**：支持`wan2.7-i2v`、`wan2.2-kf2v-flash`等万相视频模型，同样采用SFT-LoRA，分为“基于首帧”和“基于首尾帧”两类训练模式，地域限制同图像生成 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **语音合成**：当前仅支持`cosyvoice-v3-flash`模型的SFT高效微调，面向同一发音人的高还原度音色定制，**不支持控制台操作，必须通过API发起** [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **强化学习（RL）**：提供端到端的Agentic RL训练框架，支持`qwen3.5-9b`等模型，通过Rollout+Reward函数闭环优化Agent策略，但需联系商务经理开通权限，并依赖专属模型训练单元（MTU）计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档4与文档6中关于Qwen3.7-Plus-2026-05-26模型的部署说明存在矛盾——文档4称“调优后部署请联系商务经理”，而文档6未提及此限制。实际部署前请以最新控制台提示或商务确认为准。

## 关键参数

微调任务的核心超参数因模型类型与训练方式而异，以下为通用性最强的必填项与典型取值：

- `model`：基础模型ID（如`qwen3-8b`, `wan2.7-image-pro`, `cosyvoice-v3-flash`），必须与所选训练方式兼容。
- `training_type`：训练方法，常见值包括`efficient_sft`（推荐LoRA）、`sft`（全参）、`dpo_lora`、`cpt`；语音合成固定为`efficient_sft`。
- `hyper_parameters`：核心配置对象，关键字段如下：
  - `learning_rate`：学习率。文本SFT推荐`1e-4`（LoRA）或`1e-5`（全参）；图像生成推荐`3e-5`；语音合成LM/FM网络分别独立设置。
  - `n_epochs` 或 `max_steps`：训练轮次或总步数。文本SFT建议`3~5`轮（数据<10k条）；图像生成要求`≥500`步；视频生成推荐`50`轮（小数据集）或按`steps ≥ 800`换算。
  - `batch_size`：批次大小。文本SFT常用`16`或`32`；图像生成`t2i`模式为`1`，`i2i`模式为`4`；语音合成LM/FM网络分别为`1000`/`2000`。
  - `lora_rank`：LoRA低秩矩阵维数，影响参数量与拟合能力，取值须为2的幂（如`8`, `16`, `32`），图像生成默认`32`。
  - `eval_steps` 或 `eval_epochs`：验证间隔，用于监控收敛性，文本SFT推荐`50`步，图像生成推荐`200`步。
  - `split`：训练集自动划分比例（如`0.9`表示90%训练/10%验证），当未指定`validation_datasets`时生效。

其他参数（如`max_length`, `lr_scheduler_type`, `weight_decay`）需根据具体模型在控制台查看默认值，文档7明确指出“**并非所有模型都支持所有参数的调节，请以控制台显示为准**”。

## 使用方式

微调流程统一为三阶段：**数据准备 → 任务提交 → 部署调用**，支持API与控制台双路径（语音合成除外）：

1. **数据准备**：
   - 文本SFT/DPO/CPT：使用JSONL格式，遵循ChatML messages结构，单文件≤200MB [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
   - 图像/视频SFT：打包为ZIP，内含`data.jsonl`与图片/视频文件，`data.jsonl`中`content`字段需包含`image`或`video`引用。
   - 语音合成：ZIP内含`user_data/data.jsonl`（指定`wav_fn`与`text`）及`train/`目录下的WAV音频（采样率≥16kHz，单条1–30秒）。

2. **任务提交**：
   - 先调用`POST /api/v1/files`上传数据，获取`file_id`。
   - 再调用`POST /api/v1/fine-tunes`创建任务，传入`model`、`training_file_ids`（或`training_datasets`）、`training_type`及`hyper_parameters`。
   - 控制台用户可在[模型调优](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager)页面图形化配置，支持OSS挂载与混合训练。

3. **部署调用**：
   - 任务状态变为`SUCCEEDED`后，调用`POST /api/v1/deployments`部署模型，指定`model_name`（即`finetuned_output`）与`plan`（如`lora`）。
   - 部署成功（`status: RUNNING`）后，即可用新模型ID调用推理API，图像/视频[模型部署](../concepts/model-deployment.md)时需额外配置`aigc_config`中的`lora_prompt_default`以固化特效提示词。

## 限制和注意事项

- **地域与权限**：绝大多数微调功能（图像、视频、文本SFT/DPO/CPT）**仅限华北2（北京）地域**，且需使用该地域的API Key；子账号需被授予模型调用、训练、部署的RAM权限。
- **计费模式**：文本/图像/视频微调默认按[Token](../concepts/token.md)用量计费；强化学习（RL）**强制使用模型训练单元（MTU）计费，不支持[Token](../concepts/token.md)计费**；语音合成训练按[Token](../concepts/token.md)计费（0.2元/千Token），部署按模型单元时长计费。
- **数据与模型约束**：
  - 图像训练：单张图片宽高均≤1024px，单张≤10MB；视频训练：首帧/首尾帧分辨率需匹配模型要求（如`wan2.7-i2v`推荐`1k`）。
  - CosyVoice调优：**严格限定同一发音人**，混合多发音人会导致音色还原度下降；训练语种不可超出基础模型支持范围。
  - RL训练：需完成阿里云OpenTelemetry、函数计算（FC）、日志服务（SLS）三项服务授权，且依赖离线SDK包（`.whl`）部署Rollout/Reward函数。
- **工程实践建议**：
  - 避免过拟合：若训练损失持续下降而验证损失上升，应减少`n_epochs`、增大`weight_decay`或启用数据增强。
  - 参数调试：文档7强调“**请前往控制台选择相同的模型和训练方式查看实际默认值**”，切勿直接套用文档示例值。
  - 安全合规：SFT是强化模型安全底线的有效手段，但需配合高质量、覆盖多风险维度的训练数据 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


