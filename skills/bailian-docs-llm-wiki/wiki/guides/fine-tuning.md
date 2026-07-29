# fine tuning

fine tuning 是阿里云百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练大模型进行定制化训练，从而提升其在特定业务场景、领域知识或风格表达上的表现。该能力覆盖文本生成、视觉理解、语音合成、图像生成、视频生成及强化学习等多种模态与范式，支持高效微调（LoRA）、全参微调、持续预训练（CPT）、直接偏好优化（DPO）和强化学习（RL）等多种技术路径。所有 fine tuning 任务当前均仅限华北2（北京）地域使用，且需配置对应地域的 API Key [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

## 支持的模型/功能

百炼平台支持多模态、多范式的 fine tuning，具体能力按模型类型划分：

- **文本生成模型**：支持 Qwen 系列（如 `qwen3-8b`, `qwen3.5-9b`, `qwen3-32b`）、千问VL系列（如 `qwen3-vl-8b-instruct`）等，提供 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化）三种训练方式，其中 SFT 高效训练（`efficient_sft`）为默认推荐方案 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **图像生成模型**：支持万相系列（如 `wan2.7-image-pro`, `wan2.7-image`），采用 SFT-LoRA 高效微调，适用于文生图（t2i）和图生图（i2i）两种模式，可定制特定 IP 形象、艺术风格或画面特效 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成模型**：支持万相图生视频系列（如 `wan2.7-i2v`, `wan2.2-kf2v-flash`），同样采用 SFT-LoRA，支持基于首帧或首尾帧的微调，用于稳定复现特定运动特效（如“金钱雨”、“时尚杂志”） [原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成模型**：支持 CosyVoice 系列（仅 `cosyvoice-v3-flash`），通过 SFT 高效微调实现同一发音人的高还原度专属音色定制，产物为独立部署的单音色模型 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **强化学习（RL）**：支持 Qwen3.5-9B 等基座模型，通过“生成-评分-优化”循环进行策略自主探索，适用于数学推理、Agent 工具调用等需深度推理的场景，**必须使用模型训练单元（MTU）计费** [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 4 和文档 5 中关于“SFT 全参训练（sft）”与“SFT 高效训练（efficient_sft）”的支持列表存在不一致。例如，文档 4 显示 `qwen3.5-9b` 同时支持二者，而文档 5 的表格中 `qwen3.5-9b` 行在“SFT全参训练（sft）”列为“支持”，但在“SFT高效训练（efficient_sft）”列为空白。根据文档 1、2、6、8 的实操示例及文档 7 的明确推荐，`efficient_sft` 是图像、视频、语音及多数文本模型的主流且推荐方式，应以实际 API 接口和控制台可选项为准。

## 关键参数

不同训练方式的核心超参数差异显著，开发者需根据任务类型选择：

- **通用 SFT 参数（文本/视觉/语音）**：
  - `learning_rate`：高效训练推荐 `1e-4` 量级（如 `3e-4`），全参训练推荐 `1e-5` 量级；过高易导致发散，过低收敛缓慢。
  - `n_epochs` / `max_steps`：控制训练轮次或总步数。文本 SFT 默认 `3` 轮；图像微调（文档 1）使用 `max_steps=800`；视频微调（文档 2）使用 `n_epochs=50`；语音微调（文档 8）则解耦为 `lm_max_epoch` 和 `fm_max_epoch`。
  - `batch_size`：影响显存占用与收敛稳定性。文本推荐 `16` 或 `32`；图像微调中 `t2i` 模式建议 `1k` token；视频微调中 `wan2.7-i2v` 推荐 `batch_size=1`；语音微调中 `lm_batch_size=1000`。
  - `lora_rank`：LoRA 低秩矩阵维数，决定微调参数量。图像微调（文档 1）设为 `32`；文本微调（文档 5）默认 `8`；语音微调（文档 8）无此参数，因其采用专用 LM/FM 架构。

- **模态特有参数**：
  - 图像/视频：`max_pixels`（训练图片/视频最大像素总数）、`val_img_size`（验证图分辨率）、`generation_type`（`t2i` 或 `i2i`）等，直接影响输入尺寸与输出质量。
  - 视觉理解（VL）：`resized_width`/`resized_height` 可在 data.jsonl 中为每张图/视频帧指定缩放目标。
  - 强化学习（RL）：`algorithm`（如 `gspo`）、`kl_loss_coef`（KL 散度系数）、`n_rollouts`（每样本采样次数）等，构成 RL 特有的算法栈。

## 使用方式

fine tuning 流程标准化为四步：准备数据 → 上传文件 → 创建任务 → 部署调用。

1. **准备数据集**：
   - 文本 SFT：使用 ChatML 格式 JSONL 文件，每行含 `messages` 数组（含 `system`/`user`/`assistant` 角色），`assistant` 输出即为监督信号 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
   - 图像/视频：ZIP 压缩包，内含 `data.jsonl`（定义 [prompt](prompt.md)/image/video 路径）及对应媒体文件；图像单张不超过 `10MB`，分辨率建议控制在 `8K` 内。
   - 语音：ZIP 包含 `data.jsonl`（字段 `wav_fn` 和 `text`）及 `train/` 目录下的 `.wav` 文件，采样率 ≥ `16kHz`，单条时长 `2-30` 秒。
   - 强化学习：JSONL 格式，每行含 `messages`（用户问题）和 `rollout_extra`（参考答案），用于 Reward 函数评分。

2. **上传文件**：
   - 通过 `/api/v1/files` 接口上传 ZIP 或 JSONL 文件，`purpose="fine-tune"`，获取 `file_id`。
   - 支持 OSS 挂载（需指定 `region`/`bucket`/`file_path`），但图像/视频 ZIP 不支持，仅支持解压后的原始文件结构。

3. **创建训练任务**：
   - 调用 `/api/v1/fine-tunes`，传入 `model`、`training_datasets`（含 `file_id` 或 OSS 配置）、`training_type`（如 `efficient_sft`）及 `hyper_parameters`。
   - 任务状态初始为 `PENDING`，需轮询 `/api/v1/fine-tunes/{job_id}` 直至 `status="SUCCEEDED"`。

4. **部署与调用**：
   - 成功后，`finetuned_output` 即为新模型名，需调用 `/api/v1/deployments` 部署为在线服务。
   - 部署状态变为 `RUNNING` 后，即可用 `deployed_model` 名称调用对应 API（如 `/services/aigc/image-generation/generation`）。

## 限制和注意事项

- **地域与权限**：所有 fine tuning 功能**仅限华北2（北京）地域**，且必须使用该地域的 API Key。子账号需被授予模型调用、训练、部署的完整权限 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **数据与文件**：ZIP 包最大 `2GB`，单个文件上传上限 `300MB`；图像分辨率需满足宽高比 ≤ `200:1`，最小尺寸 > `10px`；语音训练数据必须为同一发音人。
- **计费模式**：
  - 文本/图像/视频/语音微调：按训练消耗 [Token](../concepts/token.md) 总数计费，公式为 `Token总数 × 单价`。
  - 强化学习：**强制使用模型训练单元（MTU）计费**，不支持 [Token](../concepts/token.md) 计费，需预先购买或开通后付费 MTU [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
- **产物特性**：微调产物是独立模型（如 `xxxx-ft-...`），非基础模型的音色 ID 或插件；CosyVoice 微调后 `voice` 参数固定为 `default`，不可切换音色。
- **效果预期**：fine tuning 旨在提升特定场景表现，**无法扩展基础模型能力边界**（如 CosyVoice 无法通过微调支持新语种，Qwen VL 无法通过微调支持新视频格式）。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


