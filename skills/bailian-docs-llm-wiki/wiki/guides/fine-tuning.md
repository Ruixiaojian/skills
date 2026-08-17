# fine tuning

fine tuning 是阿里云百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练模型进行定制化训练，以提升其在特定业务场景、领域知识或安全合规等维度的表现。该能力覆盖文本生成、视觉理解、视频生成、语音合成等多种模态，支持 SFT（监督微调）、DPO（直接偏好优化）、CPT（持续预训练）及 RL（强化学习）等多种训练范式，兼顾效果与成本效率。

## 支持的模型与功能

百炼平台支持[多模态](../concepts/multi-modal.md)、多阶段的 fine tuning 能力：

- **文本生成**：支持 Qwen 系列全量模型（如 `qwen3-8b`, `qwen3-32b`）及千问 VL [多模态](../concepts/multi-modal.md)模型（如 `qwen3-vl-8b-instruct`）的 SFT、DPO 和 CPT 训练。其中 SFT 高效训练（`efficient_sft`）采用 LoRA 技术，显著降低显存与时间开销；DPO 用于对齐人类偏好；CPT 适用于注入海量领域知识 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
  
- **图像生成**：万相系列模型（`wan2.7-image-pro`, `wan2.7-image`）支持 SFT-LoRA 微调，适用于文生图（t2i）和图生图（i2i）两种模式，可定制 IP 形象、艺术风格等 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **视频生成**：万相视频模型（`wan2.7-i2v`, `wan2.2-kf2v-flash`）支持基于首帧或首尾帧的 SFT-LoRA 微调，用于稳定复现特定特效（如“金钱雨”“时尚杂志”） [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **语音合成**：CosyVoice 模型（`cosyvoice-v3-flash`）仅支持 `efficient_sft` 方式，面向同一发音人的高还原度音色定制，产物为独立部署的单音色模型，不支持声音复刻或指令控制 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **强化学习（RL）**：支持 Qwen3.5-9B 等 MoE/非 MoE 模型，通过 Rollout + Reward 函数实现端到端策略优化，适用于数学推理、Agent 工具调用等需自主探索的场景 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 4 和文档 7 的表格中均列出 `qwen3.7-plus-2026-05-26` 支持 SFT 全参训练，但文档 4 明确标注“调优后部署请联系商务经理”，而文档 7 未提此限制。实际使用前必须确认该模型是否已开放自助部署能力，否则可能无法完成完整流程。

## 关键参数

不同训练方式与模型类型对应的关键超参存在差异，开发者需按场景选择：

- **通用必填参数**（API 调用）：
  - `model`：基础模型 ID（如 `qwen3-8b`, `wan2.7-image-pro`），必须与训练方式兼容；
  - `training_type`：取值为 `sft`, `efficient_sft`, `dpo_full`, `dpo_lora`, `cpt` 或 `rl`；
  - `training_datasets`：数据源列表，支持 `file_id`（上传 ZIP/JSONL）或 `oss_mount`（挂载 OSS）；
  - `hyper_parameters`：核心训练配置，具体字段依模型和训练类型而异。

- **SFT/DPO 文本训练常用参数**：
  - `n_epochs`（循环次数）：推荐小数据集（<10k 条）设为 3–5，大数据集设为 1–2；
  - `batch_size`：Qwen3 系列推荐 16 或 32；视频模型 `wan2.7-i2v` 推荐为 1 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)；
  - `learning_rate`：高效训练推荐 `1e-4` 量级，全参训练推荐 `1e-5` 量级；
  - `lora_rank`：LoRA 低秩矩阵维数，推荐设为模型支持的最大值（如 32），数值越大拟合能力越强但训练越慢；
  - `eval_steps`：验证间隔步数，控制 Checkpoint 保存频率与验证损失监控粒度。

- **图像/视频生成专用参数**：
  - `generation_type`：`"t2i"` 或 `"i2i"`（图像生成）；`"i2v"` 或 `"kf2v"`（视频生成）；
  - `max_pixels` / `val_img_size` / `max_token_length`：三者建议保持一致（如 `"2k"`），控制分辨率与 [Token](../concepts/token.md) 处理上限；
  - `max_pixels`（视频）：单位为像素总数（宽×高），`wan2.7-i2v` 推荐 `102400`（≈320×320）[微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **RL 训练特有参数**：
  - `algorithm`：当前仅支持 `"gspo"`；
  - `batch_size`：Qwen3.5-9B 推荐 `64`；
  - `kl_loss_coef`：KL 散度损失系数，推荐 `0.002`；
  - `resources`：必须指定 MTU 规格（如 `"MTU4"`）与数量（如 `24`），RL 不支持按 [Token](../concepts/token.md) 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 使用方式

fine tuning 可通过控制台可视化操作或 API/CLI 编程方式完成，两者流程一致但适用场景不同：

- **控制台方式**（推荐入门与调试）：
  1. 进入[模型调优](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager)页面，点击“创建训练任务”；
  2. 选择模型、训练方法（SFT/DPO/CPT）、训练模式（高效/全参）；
  3. 在“超参配置”中设置 `n_epochs`, `learning_rate`, `lora_rank` 等（界面实时显示默认值）；
  4. 在“数据配置”中选择已上传的数据集或挂载 OSS；
  5. 在“训练资源配置”中选择“按 [Token](../concepts/token.md) 计费”（共享资源）或联系商务开通 MTU（RL 必需）；
  6. 提交后轮询任务状态，待 `status` 变为 `SUCCEEDED` 后，在“我的模型”中导出并部署。

- **API/CLI 方式**（推荐自动化与生产集成）：
  1. **上传数据**：使用 `/api/v1/files` 接口上传 ZIP/JSONL 文件，获取 `file_id`；
  2. **创建任务**：调用 `/api/v1/fine-tunes`，传入 `model`, `training_file_ids`, `hyper_parameters` 等；
     ```bash
     curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
       --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
       --data '{
         "model": "qwen3-8b",
         "training_datasets": [{"data_source_type":"file_id","file_id":"<id>"}],
         "training_type": "efficient_sft",
         "hyper_parameters": {"n_epochs":3,"learning_rate":"3e-4"}
       }'
     ```
  3. **轮询状态**：用返回的 `job_id` 查询 `/api/v1/fine-tunes/{job_id}`，直至 `status` 为 `SUCCEEDED`；
  4. **部署模型**：调用 `/api/v1/deployments`，传入 `finetuned_output` 作为 `model_name`。

> **注意**：CosyVoice 模型调优**仅支持 API 方式**，控制台暂不提供入口 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)；而 RL 训练必须使用 SDK（`dashscope.finetune.reinforcement`）提交，不可直接用 REST API [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 限制和注意事项

- **地域与权限限制**：除 RL 和 CosyVoice 外，多数 fine tuning 功能仅在华北2（北京）地域可用，且需使用该地域的 API Key；RAM 子账号必须被授予 `AliyunDashScopeFullAccess` 或等效权限 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **数据格式与大小**：
  - 文本 SFT/DPO：JSONL 格式，单文件 ≤ 200 MB；
  - 图像/视频 SFT：ZIP 包含 `data.jsonl` + 原图/视频，图片宽高 ≤ 1024 px，单图 ≤ 10 MB [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)；
  - CosyVoice：ZIP 包含 `user_data/data.jsonl` + `train/*.wav`，音频采样率 ≥ 16 kHz，单条时长 1–30 秒 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **计费与资源**：
  - SFT/DPO/CPT 按训练消耗 Token 计费，单价因模型而异（如 `qwen3-8b` 为 ¥0.006/千 Token）；
  - RL 训练强制使用 MTU（模型训练单元），按小时计费，IV 型单元后付费单价 ¥41.00/小时/实例 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)；
  - CosyVoice 训练费用 = `(lm_max_epoch + fm_max_epoch) × 25 × 总秒数 × ¥0.2/千 Token` [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **模型产物与调用**：
  - 微调后模型需单独部署（`/api/v1/deployments`），调用时使用 `finetuned_output` 名称，而非原始模型名；
  - CosyVoice 调优产物固定 `voice="default"`，不支持切换音色或指令控制；
  - 视频生成微调模型部署时需配置 `aigc_config.lora_prompt_default` 以固化特效提示词 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **效果调优建议**：
  - 若训练损失下降但验证损失上升（过拟合），应减少 `n_epochs`、增大 `weight_decay` 或减小 `lora_rank`；
  - 若两者均停滞（欠拟合），可增加 `n_epochs`、提高 `learning_rate` 或增大 `lora_rank`；
  - 安全合规类 SFT（如拒绝有害请求）建议使用高质量、覆盖多风险维度的指令数据，并通过独立评测集量化 `Pass`/`Warn`/`Fail` 比例 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


