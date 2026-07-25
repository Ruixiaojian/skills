# fine tuning

fine tuning（微调）是百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练大模型进行定制化训练，从而在特定任务、领域或风格上显著提升模型表现。它适用于文本生成、视觉理解、语音合成、图像生成和视频生成等多种模态，支持监督微调（SFT）、继续预训练（CPT）和直接偏好优化（DPO）三种范式，且默认采用 LoRA 等高效训练技术以平衡效果与成本。

## 支持的模型/功能

百炼平台支持多模态、多任务的 fine tuning，覆盖主流业务场景：

- **文本生成**：支持 Qwen3 系列（如 `qwen3-8b`, `qwen3-32b`）、Qwen2.5 系列及千问-Plus-Character 等数十个模型，可执行 SFT、CPT 和 DPO [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **视觉理解（VL）**：支持 `qwen3-vl-8b-instruct` 等 VL 模型，支持图文多模态 SFT 训练，需遵循 ChatML 格式并正确组织图片/视频文件 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **图像生成**：仅支持万相（Wan）系列模型，包括 `wan2.7-image-pro` 和 `wan2.7-image`，采用 SFT-LoRA 方式，适用于文生图（t2i）与图生图（i2i）两种模式 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成**：支持 `wan2.7-i2v`、`wan2.2-kf2v-flash` 等万相视频模型，同样基于 SFT-LoRA，分为“基于首帧”和“基于首尾帧”两类任务 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成**：当前仅支持 `cosyvoice-v3-flash` 模型的 SFT 高效微调，用于同一发音人的高还原度音色定制，**不支持 CPT/DPO**，且**控制台暂不提供该能力**，必须通过 API 调用 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

> **注意**：文档 7 中表格显示 `qwen3.7-plus-2026-05-26` 支持 SFT 全参训练，但文档 1 明确指出其“调优后部署请联系商务经理”，表明该模型虽在列表中，但实际调优流程受限，非标准自助服务。开发者应优先选用已明确标注“支持”的通用型号（如 `qwen3-8b`）。

## 关键参数

不同模态和训练方式的关键参数存在差异，但核心超参具有共性：

- **通用必填参数**：
  - `model`：基础模型 ID（如 `qwen3-8b`, `wan2.7-image-pro`, `cosyvoice-v3-flash`），必须与所选训练方式兼容。
  - `training_type`：取值为 `sft`、`efficient_sft`、`cpt` 或 `dpo_full` 等，决定训练范式；图像/视频/语音微调统一使用 `efficient_sft`。
  - `hyper_parameters`：包含学习率、轮次/步数、批次大小等，具体字段因模型而异。

- **文本/SFT 类参数**（见 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)）：
  - `n_epochs`（循环次数）：推荐小数据集（<10k 样本）设为 3–5，大数据集设为 1–2。
  - `learning_rate`：高效训练推荐 `1e-4` 量级，全参训练推荐 `1e-5` 量级。
  - `batch_size`：通常设为 16 或 32，需与显存匹配。
  - `lora_rank`：LoRA 秩值，影响拟合能力与速度，推荐设为模型支持的最大值（如 32 或 64）。

- **图像/视频类参数**（见 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md) 和 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)）：
  - `max_steps`（图像）或 `n_epochs`（视频）：控制训练时长，图像建议 ≥500 步，视频建议总步数 ≥800。
  - `generation_type`（图像）：必须指定 `"t2i"` 或 `"i2i"`。
  - `max_pixels` / `val_img_size`（图像）或 `max_pixels`（视频）：控制分辨率上限，单位为像素总数（如 `"2k"` 表示 2048×2048=4194304 像素）。
  - `lora_rank` & `lora_alpha`（视频）：LoRA 核心参数，推荐值均为 `32`。

- **语音类参数**（见 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)）：
  - `lm_max_epoch` & `fm_max_epoch`：分别控制语言模型和流匹配模型的训练轮次，生产推荐值为 `60` 和 `100`。
  - `lm_batch_size` & `fm_batch_size`：批次大小，推荐值为 `1000` 和 `2000`。

## 使用方式

fine tuning 的标准流程为：准备数据 → 上传文件 → 创建任务 → 查询状态 → 部署模型 → 调用服务。

- **数据准备**：
  - 文本/SFT：使用 ChatML 格式 `data.jsonl`，每行一个 JSON 对象，含 `messages` 数组（含 `system`/`user`/`assistant` 角色）；图片/视频需与 `data.jsonl` 同包，路径在 `content` 字段中声明 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
  - 图像/视频：下载官方训练集模板（如 `wan-image-t2i-training-dataset.zip`），按要求组织图片与 JSONL 文件 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
  - 语音：严格按 `user_data/data.jsonl` + `user_data/train/*.wav` 目录结构打包 ZIP，`wav_fn` 字段必须带 `train/` 前缀 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **API 调用**：
  - 上传：`POST /api/v1/files`，`purpose="fine-tune"`，返回 `file_id`。
  - 创建任务：`POST /api/v1/fine-tunes`，传入 `model`、`training_file_ids` 或 `training_datasets`、`hyper_parameters`。
  - 查询状态：`GET /api/v1/fine-tunes/{job_id}`，轮询至 `status == "SUCCEEDED"`。
  - 部署：`POST /api/v1/deployments`，传入 `model_name`（即 `finetuned_output`）。
  - 调用：使用新部署的 `deployed_model` 名称，调用对应模态的推理 API（如 `/services/aigc/image-generation/generation`）。

- **控制台操作**：
  - 文本/SFT/CPT/DPO 可全程在 [模型调优](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager) 页面可视化完成，支持参数配置、日志查看与损失曲线监控 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
  - 图像/视频/语音微调**不支持控制台创建**，必须使用 API。

## 限制和注意事项

- **地域与权限限制**：所有 fine tuning 功能（除部分文本模型外）**仅限华北2（北京）地域**，且必须使用该地域的 API Key；RAM 子账号需额外授予 `AliyunBailianFullAccess` 或精细化权限（模型调用、训练、部署）[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **数据与格式限制**：
  - ZIP 包最大 2 GB，文件名仅支持 ASCII 字符（a-z, A-Z, 0-9, `_`, `-`）；`data.jsonl` 必须位于 ZIP 根目录 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
  - 图像单张尺寸 ≤1024px，语音 WAV 采样率 ≥16 kHz，视频抽帧逻辑复杂，[Token](../concepts/token.md) 估算需参考官方代码 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

- **计费与资源**：
  - 训练费用按消耗 [Token](../concepts/token.md) 数计费（单价见文档 7），语音训练公式为 `(lm_max_epoch+fm_max_epoch)×25×总秒数` [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - 平台同一时刻**仅运行一个训练任务**，新任务将排队 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - 微调产物为独立模型（非音色 ID），语音模型调用时 `voice` 参数必须固定为 `"default"` [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **效果与调试**：
  - 过拟合表现为 `Training Loss` 下降而 `Validation Loss` 上升，此时应减少 `n_epochs` 或 `lora_rank`；欠拟合则相反 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。
  - 图像/视频微调后，**必须使用触发词（如 `s86b5p`）激活 LoRA 效果**，否则无法复现训练风格 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)


