# fine tuning

fine tuning 是阿里云百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练模型进行定制化训练，以提升其在特定业务场景、领域知识或安全合规要求下的表现。该能力覆盖文本生成、多模态理解、图像/视频生成及语音合成等多种模态，支持 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化）及 RL（强化学习）等多种训练范式，且多数场景默认采用 LoRA 等高效微调方式以平衡效果与成本。

## 支持的模型与功能

百炼平台支持对多种官方模型进行 fine tuning，覆盖文本、视觉、语音和视频等模态。不同模态支持的训练方式存在差异：

- **文本生成模型**：全面支持 SFT（全参/LoRA）、CPT 和 DPO，适用于客服流程、代码生成、法律文书、安全合规强化等场景。例如，[0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md) 文档展示了如何使用 SFT 提升 Qwen3-8B 在政治、历史、社会等高风险领域的拒绝能力和正面引导能力。
  
- **多模态理解（千问 VL）**：支持 SFT 全参与高效训练，用于图片/视频理解任务，如图文问答、工具调用+图像分析等，但不支持 DPO 或 CPT [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。

- **图像生成模型（万相）**：仅支持 `efficient_sft` 方式，适用于文生图（t2i）与图生图（i2i）两类任务，目标是稳定复现特定 IP 形象或画面风格（如“末日废土红黑机甲”），详见 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **视频生成模型（万相）**：同样仅支持 `efficient_sft`，覆盖图生视频（基于首帧或首尾帧），用于定制特定运动特效（如“金钱雨”），其超参体系与图像模型不同，需按模型类型配置 `batch_size`、`n_epochs` 和 `max_pixels` 等参数 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **语音合成模型（CosyVoice）**：仅支持 `efficient_sft`，面向同一发音人的高还原度音色定制，产出为独立部署的单音色模型，调用时 `voice` 参数固定为 `default`，不支持声音复刻或指令控制 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **强化学习（RL）**：作为高级调优路径，适用于数学推理、Agent 工具调用稳定性等需自主探索最优策略的场景，需通过模型训练单元（MTU）计费，不支持 [Token](../concepts/token.md) 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 5 与文档 8 的模型支持矩阵存在不一致——文档 5 表明 `qwen3.7-plus-2026-05-26` 仅支持 SFT，而文档 8 同一表格中将其列为支持 `sft` 但不支持 `efficient_sft`；实际 API 调用中该模型 `training_type` 仅接受 `"sft"`，不可设为 `"efficient_sft"`。请以 API 文档为准，避免参数错误。

## 关键参数

fine tuning 的效果高度依赖超参数配置，不同训练方式与模型类型的关键参数差异显著：

- **通用核心参数**：
  - `learning_rate`：控制权重更新强度。SFT 推荐值因训练方式而异：高效训练（LoRA）常用 `1e-4` 量级，全参训练则为 `1e-5` 量级；视频模型推荐 `2e-5`；语音模型 LM/FM 网络分别设为 `lm_learning_rate`/`fm_learning_rate`（未显式暴露，由 `lm_max_epoch` 等隐式决定）。
  - `n_epochs` / `max_steps`：训练轮次或总步数。文本 SFT 常设 `3~5` 轮（小数据集）或 `1~2` 轮（大数据集）；图像模型推荐 `max_steps ≥ 500`；视频模型建议总步数 `≥ 800`；语音模型需分别设置 `lm_max_epoch=60` 与 `fm_max_epoch=100` 才能获得生产级效果。
  - `batch_size`：影响内存占用与收敛稳定性。文本模型推荐 `16` 或 `32`；视频模型严格按模型指定（如 `wan2.7-i2v` 必须为 `1`）；语音模型 `lm_batch_size=1000`、`fm_batch_size=2000`。

- **LoRA 特有参数**：
  - `lora_rank`：低秩矩阵维数，决定可训练参数量。图像模型推荐 `32`；控制台默认 `8`，但文档明确建议“设置为模型支持的最大值”以提升效果。
  - `lora_alpha`：缩放系数，控制 LoRA 更新对原始权重的影响程度。视频模型与控制台均默认 `32`。

- **数据与验证参数**：
  - `split`：训练集自动划分验证集比例，默认 `0.9`（即 90% 训练，10% 验证）。
  - `eval_steps` / `eval_epochs`：验证频率。文本/图像模型常用 `50` 步或 `20` 轮；视频模型要求 `eval_epochs ≥ n_epochs/10`。

- **其他关键参数**：
  - `max_length`（文本）：单条数据最大 token 长度，SFT 会丢弃超长样本，DPO 则自动截断。
  - `max_pixels`（图像/视频）：训练时图片/视频分辨率上限（像素总数），如图像模型 `"2k"`（2048×2048），视频模型 `wan2.7-i2v` 推荐 `102400`（约 320×320）。
  - `generation_type`（图像）：必须显式指定 `"t2i"` 或 `"i2i"`，否则训练失败。

## 使用方式

fine tuning 流程标准化为四步：准备数据 → 上传文件 → 创建任务 → 部署模型。

1. **准备数据**：
   - 文本 SFT/DPO/CPT 使用 `jsonl` 格式，遵循 ChatML 多轮结构（含 `system`/`user`/`assistant` 角色），支持深度思考与工具调用扩展 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
   - 图像/视频 SFT 使用 `zip` 包，内含 `data.jsonl`（定义 [prompt](prompt.md) 与 image/video 路径）及对应媒体文件；语音 SFT 要求 `wav` 音频 + `data.jsonl`（含 `wav_fn` 与 `text` 字段）。
   - 数据需满足地域限制：所有微调任务（除 RL 外）仅支持华北2（北京）地域。

2. **上传文件**：
   - 通过 `/api/v1/files` 接口上传，`purpose="fine-tune"`，返回唯一 `file_id`。
   - 单文件上限 300 MB（API）或 200 MB（控制台），总配额 100 GB。

3. **创建任务**：
   - 调用 `/api/v1/fine-tunes`，传入 `model`、`training_datasets`（含 `file_id` 或 OSS 挂载配置）、`training_type` 及 `hyper_parameters`。
   - 控制台用户可在 [模型调优](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager) 页面可视化配置，支持数据集选择、混合训练、自动切分验证集等功能 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

4. **部署与调用**：
   - 任务状态变为 `SUCCEEDED` 后，使用 `/api/v1/deployments` 部署 `finetuned_output` 模型。
   - 图像/视频模型部署时需指定 `"plan": "lora"`；语音模型部署后 `voice` 参数锁定为 `"default"`；文本模型部署后可直接用 `deployed_model` 替代原模型 ID 调用。

## 限制和注意事项

- **地域与权限限制**：所有 fine tuning 功能（除 RL 外）仅限华北2（北京）地域；子账号需额外授予模型调用、训练、部署权限，且 RL 训练需单独完成 OpenTelemetry、函数计算、日志服务三项授权 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

- **数据与格式限制**：
  - 图像训练要求单张图片宽高 ≤ 1024 px、大小 ≤ 10 MB；视频训练要求首帧/首尾帧图像符合相同限制 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
  - CosyVoice 训练数据必须为同一发音人，混合多发音人将导致音色还原度下降 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **计费与资源限制**：
  - RL 训练强制使用模型训练单元（MTU），不支持 [Token](../concepts/token.md) 计费；其余 fine tuning 默认按 [Token](../concepts/token.md) 计费，费用 = 训练消耗 Token 数 × 单价（如 `qwen3-8b` 为 ¥0.006/千 Token）。
  - API 创建的任务仅支持 Token 计费；若需 MTU 资源，必须通过控制台创建 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

- **模型与功能边界**：
  - 微调无法扩展基础模型能力：CosyVoice 调优不能新增语种支持；万相微调不能改变生成模式（如 t2i 模型无法转为 i2i）；文本模型微调后仍受原始上下文长度限制。
  - 部署后的模型产物不可变更：CosyVoice 调优产物为单音色模型，无法切换 `voice`；万相微调模型部署后需使用专属 `deployed_model` 名称调用，不可混用原模型 ID。

- **调试与监控**：
  - 训练过程需监控 `Training Loss` 与 `Validation Loss` 曲线：若前者持续下降而后者上升，表明过拟合，应减少 `n_epochs` 或增大 `weight_decay`；若两者均平稳，则训练充分 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
  - 任务状态轮询接口为 `/api/v1/fine-tunes/{job_id}`，成功状态为 `SUCCEEDED`；部署状态查询为 `/api/v1/deployments/{deployed_model}`，成功状态为 `RUNNING`。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)


