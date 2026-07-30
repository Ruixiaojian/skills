# fine tuning

fine tuning（微调）是百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练大模型进行定制化训练，从而提升其在特定业务场景、垂直领域或风格偏好下的表现。它不改变基座模型的底层架构，而是通过参数更新（全参或高效LoRA方式）注入领域知识、对齐人类偏好或固化特定输出模式。微调适用于文本生成、视觉理解、语音合成、图像生成、视频生成等多种模态，且支持从轻量级模型到超大规模模型的全栈覆盖。

## 支持的模型/功能

百炼平台支持多种调优方式与模型类型，覆盖文本、视觉、语音、[多模态](../concepts/multi-modal.md)等主流任务：

- **文本生成**：支持 Qwen 系列（如 `qwen3-8b`, `qwen3.5-9b`, `qwen3-32b`）、千问VL系列（如 `qwen3-vl-8b-instruct`）的 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化）[原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。其中 SFT 高效训练（`efficient_sft`）为默认推荐方式，兼顾效果与成本。
  
- **图像生成**：仅支持万相（Wan）系列模型，包括 `wan2.7-image-pro` 和 `wan2.7-image`，采用 SFT-LoRA 方式进行文生图（t2i）或图生图（i2i）微调 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **视频生成**：支持 `wan2.7-i2v`、`wan2.5-i2v-preview`、`wan2.2-i2v-flash`（首帧驱动）及 `wan2.2-kf2v-flash`（首尾帧驱动），同样基于 SFT-LoRA 微调 [原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **语音合成**：当前仅支持 `cosyvoice-v3-flash` 模型的 SFT 高效微调（`efficient_sft`），用于同一发音人的高还原度音色定制，**控制台暂不支持，必须使用 API** [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **强化学习（RL）**：面向 Agent 场景，支持 `qwen3.5-9b`、`qwen3.6-flash-2026-04-16` 等 MoE 模型，需通过模型训练单元（MTU）计费，不支持按 [Token](../concepts/token.md) 计费 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 4 和文档 5 均列出 `qwen3.7-plus-2026-05-26` 支持 SFT，但文档 4 明确标注“调优后部署请联系商务经理”，而文档 5 未作此限制。实际使用前请以控制台实时选项或商务确认为准。

## 关键参数

不同调优方式和模型类型的关键参数存在差异，开发者需根据任务目标谨慎配置：

- **通用超参**（文本/SFT）：
  - `learning_rate`：SFT 高效训练推荐 `1e-4` 量级，全参训练推荐 `1e-5`；语音微调中 LM/FM 网络需分别设置 `lm_learning_rate`/`fm_learning_rate`（虽未在原始文档显式列出，但属必填逻辑）。
  - `n_epochs` / `max_steps`：控制训练深度。图像微调使用 `max_steps`（如 `800`），视频微调使用 `n_epochs`（如 `50`），文本微调两者皆可（文档 5 推荐 `n_epochs=3`，文档 6 示例用 `n_epochs=3`）。
  - `batch_size`：影响内存占用与收敛稳定性。图像微调未显式暴露该参数；视频微调中 `wan2.7-i2v` 推荐 `1`，`wan2.2-kf2v-flash` 推荐 `4`；文本微调推荐 `16` 或 `32`。
  - `lora_rank`：LoRA 低秩矩阵维数，决定可训练参数量。图像微调默认 `32`，文本微调控制台默认 `8`，语音微调则解耦为 `lm_rank`/`fm_rank`（文档 8 未显式定义，但 `lm_batch_size`/`fm_batch_size` 暗示其存在）。

- **模态特有参数**：
  - 图像/视频：`max_pixels`（训练图片/视频最大像素总数）、`val_img_size`（验证图分辨率）、`generation_type`（`"t2i"` 或 `"i2i"`）。
  - 视频：`eval_epochs`（验证间隔）、`max_split_val_dataset_sample`（自动验证集最大样本数）。
  - 语音：`lm_max_epoch`（语言模型训练轮次）、`fm_max_epoch`（流匹配模型训练轮次），二者共同决定最终音色还原度与韵律表现。

## 使用方式

微调流程遵循“准备数据 → 上传 → 创建任务 → 查询状态 → 部署 → 调用”标准链路，支持控制台可视化操作与 API/CLI 编程式调用两种路径：

- **控制台方式**：适用于快速验证与非技术用户。进入[模型调优](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager)页面，选择模型、训练方式（SFT/CPT/DPO）、上传 ZIP 数据集（含 `data.jsonl` 及媒体文件），配置超参后提交。详细指引见 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

- **API/CLI 方式**：适用于自动化集成与生产环境。需先调用 `/api/v1/files` 上传 ZIP 文件获取 `file_id`，再调用 `/api/v1/fine-tunes` 提交训练任务。图像/视频微调使用 `training_datasets` 字段，语音微调使用 `training_file_ids` 字段，文本微调两者均支持。完整示例见 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md) 和 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **特殊流程**：
  - **强化学习**：需额外完成 RL 服务授权（开通 FC/SLS/OpenTelemetry）、下载 SDK Demo 包、编写 Rollout/Reward 函数，并通过 `AgenticRL.run()` 提交任务，不复用标准 `/fine-tunes` 接口 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
  - **语音微调**：必须使用 API，且训练产物为独立模型（`voice="default"` 锁死），无法切换音色 ID [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 限制和注意事项

- **地域与权限**：所有微调功能（除 RL 外）均**仅限华北2（北京）地域**，且必须使用该地域的 API Key。RAM 子账号需被授予模型调用、训练、部署的完整权限 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **数据格式与约束**：
  - 文本 SFT 必须使用 ChatML 格式 JSONL，`messages` 字段内 `system/user/assistant` 角色严格嵌套；视觉理解需将 `image`/`video` 作为 `content` 数组元素；语音微调要求 `data.jsonl` 中 `wav_fn` 必须以 `train/` 开头 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
  - ZIP 包大小上限为 2 GB，`data.jsonl` 必须位于根目录，图片单张不超过 10 MB 且宽高均 >10 像素 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

- **计费与资源**：
  - 文本/图像/视频微调按训练消耗 [Token](../concepts/token.md) 计费；语音微调按 `(lm_max_epoch + fm_max_epoch) × 25 × 总秒数` 估算 [Token](../concepts/token.md)；RL 训练强制使用 MTU 训练单元（IV 型单价 41 元/小时），不支持 Token 计费 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
  - 语音微调产物部署后按模型单元时长计费，且**不支持指令控制**，仅支持 SSML/LaTeX 请求级控制 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **效果与风险**：
  - 过高的 `lora_rank` 或 `n_epochs` 可能导致过拟合或基础能力“遗忘”，尤其在语音微调中会损害长文本稳定性 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - 训练数据质量直接决定微调效果：图像微调需高质量风格一致图集，语音微调需同一发音人、低噪、无错读音频，安全合规微调需覆盖多维度风险的高质量问答对 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


