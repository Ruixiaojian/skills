# fine tuning

fine tuning 是阿里云百炼平台提供的核心模型优化能力，通过在基础模型上注入领域知识、业务逻辑或人类偏好，显著提升模型在特定任务上的效果、安全性与一致性。它支持多种训练范式（SFT、DPO、CPT、RL）和多模态模型（文本、图像、视频、语音），适用于从安全合规加固到专属音色定制的广泛场景。所有 fine tuning 任务均需在华北2（北京）地域执行，并依赖 DashScope API Key 和相应 RAM 权限。

## 支持的模型/功能

百炼平台支持面向不同模态和目标的 fine tuning：

- **文本生成模型**：支持 SFT（监督微调）、DPO（直接偏好优化）、CPT（持续预训练）三种方式，覆盖 Qwen3 系列（如 `qwen3-8b`, `qwen3-14b`, `qwen3-32b`）、Qwen2.5 系列及千问-Plus-Character 等数十种模型。其中 SFT 和 DPO 支持高效训练（LoRA）与全参训练两种模式，CPT 仅支持全参训练 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
  
- **视觉理解模型（千问VL）**：支持 SFT 高效训练（`efficient_sft`），适用于图片和视频理解任务，但不支持 DPO 或 CPT [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

- **图像生成模型（万相）**：支持 SFT-LoRA 微调，适用于 `wan2.7-image-pro` 和 `wan2.7-image`，支持文生图（t2i）与图生图（i2i）两种生成模式 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **视频生成模型（万相）**：支持 SFT-LoRA 微调，适用于 `wan2.7-i2v`、`wan2.5-i2v-preview`、`wan2.2-i2v-flash`（首帧驱动）及 `wan2.2-kf2v-flash`（首尾帧驱动） [原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **语音合成模型（CosyVoice）**：**仅支持 SFT 高效微调（`efficient_sft`）**，且当前仅可通过 API 发起，控制台暂不支持 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **强化学习（RL）训练**：支持 GSPO 算法，适用于数学推理、Agent 工具调用等需自主策略探索的场景，需使用专用模型训练单元（MTU）计费，不支持按 [Token](../concepts/token.md) 计费 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 4 和文档 8 的模型支持矩阵存在不一致：文档 4 表明 `qwen3.5-flash-2026-02-23` 仅支持 SFT 全参训练，而文档 8 明确列出其支持 `efficient_sft`。以文档 8 的 API 支持列表为准，因其为最新接口规范。

## 关键参数

不同训练类型和模型对超参数的支持范围不同，以下为通用关键参数及其推荐值：

- **`training_type`**：必填。取值包括 `sft`、`efficient_sft`、`dpo_full`、`dpo_lora`、`cpt`。视频和语音模型固定为 `efficient_sft`；RL 训练使用独立接口，不在此字段中指定。

- **`n_epochs` / `max_steps`**：控制训练时长的核心参数。SFT 文本模型推荐 `n_epochs=3~5`（小数据集）或 `1~2`（大数据集）；图像生成模型推荐 `max_steps=800`；视频生成模型默认 `n_epochs=50`（但实际建议根据数据量动态调整至 3000–5000 steps）[原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **`learning_rate`**：学习率。SFT 文本模型高效训练推荐 `1e-4` 量级（如 `3e-4`），全参训练推荐 `1e-5` 量级（如 `2e-5`）；图像生成模型推荐 `3e-5`；视频生成模型统一为 `2e-5`。

- **LoRA 参数**（仅 `efficient_sft`）：
  - `lora_rank`：低秩矩阵维数，推荐 `32`（图像/视频）或 `8~16`（文本）；
  - `lora_alpha`：缩放系数，推荐与 `lora_rank` 相同（如 `32`）；
  - `lora_dropout`：推荐 `0.1`。

- **其他关键参数**：
  - `batch_size`：需严格匹配模型推荐值（如 `wan2.7-i2v` 必须为 `1`，`wan2.2-kf2v-flash` 必须为 `4`）[原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)；
  - `max_length`（文本）或 `max_pixels`（图像/视频）：必须设置，影响数据截断与分辨率；
  - `eval_steps` / `eval_epochs`：验证间隔，必须满足 `≥ n_epochs/10`（视频）或 `≥ 0`（图像）。

## 使用方式

fine tuning 可通过控制台可视化操作或 API/CLI 编程方式完成，流程统一为三步：**准备数据 → 创建任务 → 部署模型**。

1. **准备数据集**：
   - 文本 SFT/DPO：使用 `.jsonl` 文件，遵循 ChatML 格式（`messages` 数组），每行一条样本 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)；
   - 图像/视频：打包为 `.zip`，内含 `data.jsonl`（定义样本路径与 [prompt](prompt.md)）及对应图片/视频文件；
   - CosyVoice：`.zip` 内含 `data.jsonl`（`wav_fn` + `text`）及 `train/` 目录下的 `.wav` 文件；
   - RL：`.jsonl` 文件含 `messages` 和 `rollout_extra` 字段，需配合自定义 Rollout/Reward 函数 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

2. **创建训练任务**：
   - 控制台：进入[模型调优](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager)页面，选择模型、训练方式、数据集及超参数后提交；
   - API：先调用 `/api/v1/files` 上传数据获取 `file_id`，再调用 `/api/v1/fine-tunes` 提交任务，传入 `model`、`training_file_ids`（或 `training_datasets`）、`training_type` 和 `hyper_parameters` [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

3. **部署与调用**：
   - 查询任务状态直至 `status=SUCCEEDED`；
   - 调用 `/api/v1/deployments` 接口部署 `finetuned_output` 模型；
   - 部署成功（`status=RUNNING`）后，使用 `deployed_model` 名称调用，参数与基础模型一致（如图像生成仍需传 `input` 和 `prompt`）。

## 限制和注意事项

- **地域与权限**：所有 fine tuning 任务**仅支持华北2（北京）地域**，且必须使用该地域的 API Key；RAM 子账号需显式授予 `dashscope:FineTune*`、`dashscope:Deploy*` 等权限 [原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **计费模式**：
  - 文本/图像/视频 SFT/DPO/CPT：按训练消耗 [Token](../concepts/token.md) 计费，公式为 `Token 总数 × 循环次数 × 单价`；
  - RL 训练：**仅支持模型训练单元（MTU）计费**，不支持 [Token](../concepts/token.md) 计费 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)；
  - CosyVoice：训练按 Token 计费（0.2 元/千 Tokens），部署按模型单元时长计费。

- **数据与资源限制**：
  - 单个训练文件最大 300 MB（文本/视频）或 200 MB（图像）；
  - 视频训练要求最少 4 帧、最多 8000 帧（依模型而定）；
  - CosyVoice 要求训练音频总时长 1–10 小时，且必须为同一发音人。

- **关键注意事项**：
  - CosyVoice 调优产物为单音色独立模型，`voice` 参数强制为 `default`，不再支持声音复刻或设计 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)；
  - RL 训练需提前完成函数计算（FC）、日志服务（SLS）等云服务授权；
  - 控制台创建的任务仅支持 Token 计费；若需 MTU 计费（如 RL），必须使用 API。

## 来源文档

- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


