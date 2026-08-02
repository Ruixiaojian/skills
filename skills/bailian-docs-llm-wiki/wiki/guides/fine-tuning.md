# fine tuning

fine tuning（微调）是百炼平台提供的核心模型优化能力，允许开发者基于预训练大模型，使用自有领域数据进行定制化训练，从而提升模型在特定任务、风格或安全合规等维度的表现。它不改变基础模型架构，而是通过参数更新（全参或LoRA高效方式）注入业务知识、对齐人类偏好或强化特定能力。所有微调任务均需在华北2（北京）地域执行，并依赖 DashScope API Key 与相应 RAM 权限。

## 支持的模型与功能

百炼支持多模态、多任务的微调能力，覆盖文本生成、视觉理解、语音合成及视频生成四大类，且不同模态对应不同的训练方法与数据格式要求。

- **文本生成模型**：支持 SFT（监督微调）、CPT（持续预训练）和 DPO（直接偏好优化）三种方式，适用于 Qwen 系列（如 `qwen3-8b`、`qwen3.5-9b`）及千问 VL 多模态模型（如 `qwen3-vl-8b-instruct`）。SFT 用于教会模型执行特定指令（如客服流程、工具调用），DPO 用于优化输出质量（如拒有害建议、答更简洁），CPT 用于注入海量领域知识（如金融术语、法律条文）[原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
  
- **图像生成模型**：仅支持 `efficient_sft` 方式，当前适配 `wan2.7-image-pro` 和 `wan2.7-image`，用于定制 IP 形象、特定画风（如“末日废土红黑机甲”）或图生图特效 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **视频生成模型**：仅支持 `efficient_sft`，适配 `wan2.7-i2v`（首帧驱动）、`wan2.2-kf2v-flash`（首尾帧驱动）等，用于固化特定运动特效（如“金钱雨”）[原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **语音合成模型**：仅支持 `efficient_sft`，当前唯一支持模型为 `cosyvoice-v3-flash`，用于同一发音人多小时录音的高还原度音色定制，产物为独立部署的单音色模型 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **强化学习（RL）训练**：面向 Agent 场景，支持 `qwen3.5-9b` 等 MoE/非 MoE 模型，通过“生成-评分-优化”循环自主探索最优策略，需专用模型训练单元（MTU）计费，不支持 Token 计费 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 6 和文档 8 的模型支持矩阵存在不一致——文档 6 声明 `qwen3.7-plus-2026-05-26` 仅支持 SFT，而文档 8 的表格中该模型同样标记为仅支持 SFT；但文档 6 中 `Qwen3-VL-8B-Thinking` 明确支持 SFT，而文档 8 的 VL 表格中未列出该型号。实际以控制台实时显示为准，API 调用前请务必在控制台确认目标模型对 `training_type` 的支持情况。

## 关键参数

不同训练方式与模型类型对应的超参数差异显著，开发者需按场景谨慎配置：

- **通用必填参数**：`model`（基础模型 ID）、`training_type`（如 `sft`、`efficient_sft`、`dpo_lora`）、`training_datasets`（数据源列表）。`hyper_parameters` 中部分字段为强制填写，例如文本 SFT 必须提供 `n_epochs`、`batch_size`、`max_length`；图像/视频微调则需 `max_pixels`、`val_img_size`、`generation_type` 等分辨率与模式参数。

- **学习率（learning_rate）**：是影响收敛与效果的核心。推荐值因训练方式而异：SFT 高效训练常用 `1e-4` 量级，全参训练为 `1e-5` 量级，CPT 同样为 `1e-5`；而 CosyVoice 语音微调固定为 `2e-5`，图像生成微调推荐 `3e-5`。过高易导致震荡，过低则收敛缓慢。

- **LoRA 相关参数**：当 `training_type` 为 `efficient_sft` 或 `dpo_lora` 时生效，包括 `lora_rank`（秩值，推荐 8–64，值越大拟合越强但训练越慢）、`lora_alpha`（缩放系数，常与 `lora_rank` 相同）、`lora_dropout`（防过拟合，推荐 0.1）。图像生成文档明确要求 `lora_rank` 必须为 2 的幂次（如 32）。

- **训练规模控制**：`n_epochs`（轮次）与 `max_steps`（步数）决定训练强度。图像生成使用 `max_steps`（如 800），视频生成使用 `n_epochs`（如 50），文本 SFT 两者皆可，但需注意 `steps = n_epochs × ⌈dataset_size / batch_size⌉`。文档 2 特别指出：50 epochs 仅适用于约 2 条的小数据集，50–60 条数据时应训练 3000–5000 steps。

- **验证与保存**：`eval_steps`（每 N 步验证）或 `eval_epochs`（每 N 轮验证）用于监控训练过程；`save_total_limit` 控制 Checkpoint 保留数量（默认 10），避免磁盘空间耗尽。

## 使用方式

微调流程统一为三阶段：**准备数据 → 创建任务 → 部署调用**，支持控制台可视化操作与 API 编程两种路径。

- **数据准备**：必须严格遵循格式规范。文本 SFT 使用 `jsonl`（ChatML messages 结构），图像/视频 SFT 使用 `zip` 包（含 `data.jsonl` 与媒体文件），语音 SFT 要求 `wav` 音频 + `data.jsonl`（`wav_fn` 必须带 `train/` 前缀）。所有数据上传均通过 `/api/v1/files` 接口，`purpose="fine-tune"` 是必需参数 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

- **创建任务**：调用 `/api/v1/fine-tunes` 提交。关键区别在于：
  - 图像/视频微调使用 `training_datasets` 数组（含 `file_id` 或 `oss_mount`）；
  - 语音微调使用 `training_file_ids` 字段（仅支持单个 `file_id`）；
  - 文本微调支持混合数据源（`file_id` + `oss_mount`），且可同时指定 `validation_datasets`。
  任务创建后返回 `job_id` 与 `finetuned_output`（新模型名），状态初始为 `PENDING`。

- **状态查询与部署**：轮询 `/api/v1/fine-tunes/{job_id}` 直至 `status="SUCCEEDED"`；随后调用 `/api/v1/deployments` 部署模型，传入 `model_name`（即 `finetuned_output`）。图像/视频微调部署时需指定 `"plan": "lora"`；语音微调部署后 `voice` 参数必须固定为 `"default"`；视频微调部署还需在 `aigc_config` 中配置 `lora_prompt_default` 以固化特效提示词。

## 限制和注意事项

- **地域与权限限制**：所有微调功能（除部分文本 SFT 外）**仅限华北2（北京）地域**。子账号需显式授予 `dashscope:FineTune*`、`dashscope:Deploy*` 等权限，否则任务提交失败 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **数据与资源限制**：单个上传文件上限 300MB（API）或 200MB（文本 jsonl）；OSS 挂载仅支持 `cn-beijing` 和 `ap-southeast-1` 地域；RL 训练**强制使用 MTU 计费**，不支持 Token 计费；CosyVoice 微调产物无法切换音色或使用指令控制，仅支持 SSML/LaTeX 请求级控制。

- **效果与成本权衡**：高效训练（LoRA）速度快、成本低，适合快速验证；全参训练效果更优但耗时长、费用高。文档 7 明确建议：“如果模型支持全参训练，请优先选择全参训练，因为全参训练效果比高效训练效果要好，性价比更高”。但文档 9 的安全微调案例却选用 LoRA（`lora_rank=8`），因其在 15–30 分钟内即可达成 98% Pass 率，凸显了场景适配性。

- **训练失败诊断**：若 `Training Loss` 持续下降而 `Validation Loss` 上升，表明过拟合，应减少 `n_epochs`、增大 `weight_decay` 或提高 `lora_dropout`；若两者均停滞，则可能欠拟合，需增加 `n_epochs` 或 `lora_rank`。训练日志与损失曲线是调优的关键依据。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)


