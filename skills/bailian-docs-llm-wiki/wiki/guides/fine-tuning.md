# fine tuning

百炼平台的模型调优（fine tuning）覆盖**文本生成**、**视觉理解（千问 VL）**、**图像生成（万相）**、**视频生成（万相）**、**语音合成（CosyVoice）**五大模态，统一通过控制台或 OpenAI 兼容的 `/api/v1/fine-tunes` HTTP 接口发起。文本生成提供 **CPT / SFT / DPO** 三种递进式训练方式，多模态目前仅提供 **SFT-LoRA** 高效微调。**所有调优任务当前仅在中国大陆版（北京地域）可用，产出的模型不支持下载**。

## 适用场景与调优方法

- **文本生成**：CPT 用于"补知识"（领域适应，至少 5000 万 token 无标签语料）；SFT 用于"学做事"（ChatML 格式 1000+ 条问答对，含 thinking、VL 子变体）；DPO 用于"做得更好"（100+ 组 chosen/rejected 偏好对）。三者并不互斥，推荐顺序 `CPT（可选）→ SFT → DPO（可选）`，详见 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解（千问 VL）**：与 SFT 文本调优同流程，但 `system` 必须为数组格式 `[{"text":"..."}]`，训练数据需打包为 ZIP（≤ 2 GB），`data.jsonl` 必须位于压缩包根目录。VL 专属超参 `freeze_vit=true` 才能按 Token 计费。
- **视频生成（万相）**：仅支持 SFT-LoRA。`wan2.5-i2v-preview` / `wan2.2-i2v-flash` 用于图生视频-首帧，`wan2.2-kf2v-flash` 用于首尾帧。仅可通过 API 创建（[微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)）。
- **图像生成（万相）**：仅支持 SFT-LoRA，目前仅 `wan2.7-image-pro` 一个基础模型，覆盖文生图与图生图两种子任务（[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)）。
- **语音合成（CosyVoice）**：仅支持 `efficient_sft`，仅 `cosyvoice-v3-flash` 基础模型，**仅 API、控制台不可发起**；产出的是单音色独立模型，调用时 `voice` 锁死为 `"default"`，不支持指令控制（`instruction`），详见 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **安全合规强化**：零代码 SFT 用法的代表场景，使用安全合规训练集对 Qwen3-8B 等模型做对齐，参见 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 支持的基础模型

文本生成（`model_training-overview` / `fine-tuning-api-guide` 列表）：

| 模型代码 | CPT 全参 | SFT 全参 | SFT 高效 | DPO 全参 | DPO 高效 | 训练单价（千 Token） |
| --- | --- | --- | --- | --- | --- | --- |
| `qwen3.6-flash-2026-04-16` | × | 支持 | × | × | × | ¥0.05 |
| `qwen3.5-27b` | × | 支持 | 支持 | × | × | ¥0.05 |
| `qwen3.5-9b` | × | 支持 | 支持 | × | × | ¥0.02 |
| `qwen3.5-flash-2026-02-23` | × | 支持 | × | × | × | ¥0.05 |
| `qwen3-32b` | 支持 | 支持 | 支持 | 支持 | 支持 | ¥0.04 |
| `qwen3-30b-a3b-instruct-2507` | 支持 | 支持 | 支持 | × | × | ¥0.03 |
| `qwen3-14b` | × | 支持 | 支持 | 支持 | 支持 | ¥0.03 |
| `qwen3-8b` | × | 支持 | 支持 | 支持 | 支持 | ¥0.006 |
| `qwen3-1.7b` | 支持 | 支持 | 支持 | 支持 | 支持 | ¥0.0045 |
| `qwen3-0.6b` | 支持 | 支持 | 支持 | 支持 | 支持 | ¥0.003 |
| `qwen2.5-72b-instruct` | 支持 | 支持 | 支持 | 支持 | 支持 | ¥0.15 |
| `qwen2.5-32b-instruct` | 支持 | 支持 | 支持 | 支持 | 支持 | ¥0.03 |
| `qwen2.5-14b-instruct` | 支持 | 支持 | 支持 | 支持 | 支持 | ¥0.03 |
| `qwen2.5-7b-instruct` | 支持 | 支持 | 支持 | 支持 | 支持 | ¥0.006 |
| `qwen-plus-character-2025-11-06` | × | 支持 | 支持 | 支持 | 支持 | ¥0.15 |

视觉理解（千问 VL）：`qwen3-vl-8b-instruct`、`qwen3-vl-8b-thinking`、`qwen3-vl-4b-instruct`、`qwen2.5-vl-72b-instruct`、`qwen2.5-vl-32b-instruct`、`qwen2.5-vl-7b-instruct`，目前**仅支持 SFT 全参与 SFT 高效**两种方式。

> **注意**：[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)、[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)、[使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md) 三篇文档的"支持模型"清单略有差异（例如控制台文档未列出 Qwen3.6-Flash / Qwen3.5-Flash），**请以控制台实际可选项为准**。自定义模型（基于上一次调优产出的模型再训练）的支持方式与对应预置模型相同。

## 调优数据格式

- **SFT ChatML**：每行一条 JSON，`messages` 数组依次包含 `system` / `user` / `assistant`。**所有 `assistant` 行都会被训练**，不支持 OpenAI 的 `name` / `weight` 参数；可选 `loss_weight ∈ [0,1]`（邀测参数）。
- **SFT thinking**：只对**最后一条** `assistant` 输出进行训练，思考内容需写成 `<think>\n...\n</think>\n\n回答`，中间轮的 `assistant` 不能带 `<think>` 标签。
- **SFT VL**：`system` `content` 必须是数组 `[{"text":"..."}]`；`user` / `assistant` `content` 支持文本、图像（`image`）、视频（`video` 字符串或图片帧列表）。图片单张 ≤ 1024×1024 / 10 MB；视频与图片帧模式仅 qwen3.5 及之后的 VL 模型支持。压缩包要求：ZIP ≤ 2 GB、`data.jsonl` 在根目录、文件名全局唯一且仅允许 ASCII 字母/数字/`_`/`-`。
- **DPO ChatML**：`messages` + `chosen` + `rejected`。`chosen` 支持 `loss_weight`。
- **CPT 纯文本**：每行 `{"text": "..."}`。
- **CosyVoice**：`.wav` + `data.jsonl` 同一发音人，混入多发音人会显著降低还原度。
- **万相图像 / 视频**：以训练目标场景的 ZIP 形式上传到 `purpose="fine-tune"`，详见对应模型的 finetune-guide 文档。

## 使用方式

### 控制台流程（八步）

依据 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)：

1. 选择调优方式（CPT / SFT / DPO）；
2. 选择基础模型与训练模式（全参 / 高效）；
3. 配置训练数据（支持自动按 9:1 切分验证集，或上传独立验证集）；
4. 配置参数快照（`save_total_limit` + Checkpoint 间隔，仅 SFT 支持）；
5. 开始训练，可在"指标"页查看 Training Loss / Validation Loss / Validation Token Accuracy；
6. 训练完成后发布 Checkpoint 至**我的模型**；
7. 在"我的模型"中进行**模型部署**；
8. 通过**模型评测**功能评估调优效果。

### API 流程

按 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)：

1. `POST /api/v1/files`（`purpose="fine-tune"`）上传训练集 / 验证集，拿到 `file_id`；
2. `POST /api/v1/fine-tunes` 创建训练任务，必填 `model`、`training_file_ids`、`hyper_parameters`（其中 `n_epochs`、`batch_size`、`max_length` 影响费用，**必填**），可选 `validation_file_ids`、`training_type`（`cpt` / `sft` / `efficient_sft` / `dpo_full` / `dpo_lora`）、`job_name`、`model_name`；
3. 返回的 `finetuned_output` / `job_id` 用于查询任务、列出 Checkpoint、发布与部署。

万相图像 / 视频与 CosyVoice 的 API 调用步骤一致，但 `training_type` 固定为 `efficient_sft`（或对应模型专属取值），且 hyperparameters 不同，请阅读对应模型的 finetune-guide。

> **注意**：通过 API 创建的训练任务**只支持按 Token 计费**，不支持模型训练单元（预付费 / 后付费）。若需使用训练单元，请改用控制台。

## 关键超参与训练配置

| 参数 | 推荐值 | 作用 |
| --- | --- | --- |
| `n_epochs`（循环次数）| 数据 <10k 取 3~5；>10k 取 1~2 | 训练遍数，直接影响时长与费用 |
| `batch_size`（批次大小）| 默认（一般 16/32）| 每多少条数据更新一次参数 |
| `max_length`（序列长度）| 模型支持的最大值 | SFT 超长样本直接丢弃；DPO 截断 |
| `learning_rate` | 高效 1e-4 级；全参 1e-5 级；CPT 1e-5 级 | 参数修正强度，过大不稳定，过小不见效 |
| `lr_scheduler_type` | `linear` 或 `inverse_sqrt` | 支持 8 种策略，`polynomial`、`cosine_with_restarts` 不推荐 |
| `warmup_ratio` | 默认 | 预热阶段比例；`constant` 策略下无效 |
| `weight_decay` | 默认 | L2 正则化强度 |
| `lora_alpha` / `lora_dropout` / `lora_rank` | 默认；`lora_rank` 取最大值 | LoRA 高效训练专属 |
| `freeze_vit` | 仅 VL 模型可用 | 设为 `true` 才能按 Token 计费 |
| `data_augmentation` / `augmentation_ratio` / `augmentation_types` | 视场景启用 | 自动数据增强（如 `dialogue_CN`、`general_purpose_CN`、`NLP`）|
| `save_strategy` / `save_total_limit` | 默认 | Checkpoint 保存策略与数量上限 |
| `split` | 默认 0.9 | 自动切分训练集 / 验证集的比例 |

阿里云建议**优先选择全参训练**（与高效训练同价但效果更好）；选择 LoRA 时 `lora_rank` 取模型支持的最大值。

## 计费

- **训练费用** = `(训练 Token 总数 + 混合训练 Token 总数) × 循环次数 × 训练单价`，最小计费单位 1 Token。
- **CosyVoice** 训练费用按音频时长换算 Token：`(lm_max_epoch + fm_max_epoch) × 25 × 训练集总秒数`，单价 ¥0.2 / 千 Token。
- **部署费用**单独计算（按模型单元使用时长），调优产出的模型部署后才能调用。模型评测不额外收费。
- 控制台底部"预估训练费用 → 计算详情"可看到 Token 数、循环次数与训练单价。

## 限制与注意事项

- **地域**：所有调优功能仅在中国大陆版（北京地域）开放，且必须使用北京地域的 API Key。RAM 子账号需要授予"模型调优-操作 / 模型部署-操作 / 模型评测-操作"以及业务空间下对**特定模型**的训练权限。
- **不可下载本地**：在百炼调优的模型不支持导出，仅能在百炼平台部署后调用；导出的 Checkpoint 存储于云存储，不开放下载。Checkpoint 有保存时长，超时自动清理，需及时发布。
- **耗时与门槛**：CPT 数据集最少 5000 万 Token，SFT 至少 1000 条，DPO 至少 100 组；模型调优通常作为"最后的手段"，优先尝试 Prompt 工程、Function Calling、RAG。
- **过拟合判断**：若 Training Loss 持续下降而 Validation Loss 上升，应增加数据多样性 / 减小学习率 / 增大权重衰减 / 提高 LoRA dropout；欠拟合则反向调整。
- **DPO / CosyVoice 等专项限制**：DPO 模型自定义训练后仅 `sft` / `efficient_sft` / `dpo_*` 可继续；CosyVoice 调优产物锁死 `voice="default"`、不能调用 `instruction`，且训练数据语种必须为基础模型已支持的语种。
- **自定义模型回训**：仅 `efficient_sft`（LoRA）产出可作为后续 `sft_efficient` 的基模型；全参产出可作为更多训练方式的基模型。是否能基于他人的自定义模型回训以**我的模型**页面的实际显示为准。
- **不支持调优自家上传的模型**：可通过"我的模型（北京）→ 模型导入"上传 safetensor 格式的开源千问模型并部署使用，但不再进入调优流程。

## 来源文档

- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)


