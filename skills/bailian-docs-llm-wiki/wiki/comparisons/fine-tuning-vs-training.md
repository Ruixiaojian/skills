# 模型微调与训练对比

百炼平台围绕"模型调优"提供两条信息脉络：一条是从**用户与场景**视角组织的 [fine tuning](../guides/fine-tuning.md)（模型调优）指南，覆盖文本、视觉、图像、视频、语音五大模态的训练方式选型与数据格式；另一条是从 **REST API 视角**组织的 [model training](../api/model-training.md) 参考，统一描述 `/api/v1/fine-tunes` 系列接口、超参语义与任务状态机。两份文档面向同一底层能力，但抽象层次不同：前者回答 *"我该选 CPT 还是 SFT，数据要写成什么样"*，后者回答 *"我要发哪个请求、传哪些字段、如何轮询结果"*。本页对比两者的覆盖范围、关键约束与适用场景，帮助开发者在文档检索、技术选型与排查中找到正确入口。

## 关键维度对比

| 维度 | [fine tuning](../guides/fine-tuning.md)（模型调优指南） | [model training](../api/model-training.md)（调优 API 参考） |
| --- | --- | --- |
| 文档定位 | 面向**业务/算法工程师**的调优方法论与数据准备 | 面向**后端/集成开发者**的 HTTP 接口参考 |
| 视角 | 按**模态 + 训练方式**组织（文本 CPT/SFT/DPO、VL SFT-LoRA、视频/图像 SFT-LoRA、CosyVoice efficient_sft） | 按**接口 + 字段**组织（统一 `POST /api/v1/fine-tunes` 主入口 + 文件管理 + 压缩） |
| 主入口 | 控制台 + OpenAI 兼容 `/api/v1/fine-tunes` | `https://dashscope.aliyuncs.com/api/v1/fine-tunes` REST 系列 |
| 训练方式覆盖 | CPT、SFT 全参、SFT 高效（LoRA）、DPO 全参、DPO 高效、efficient_sft（CosyVoice）、SFT-LoRA（万相） | `cpt` / `sft` / `efficient_sft` / `dpo_full` / `dpo_lora`（与左侧一一对应的 `training_type` 取值） |
| 输入定义 | 数据格式规范：ChatML、thinking、VL ZIP 结构、CPT 纯文本、CosyVoice `.wav + jsonl`、DPO chosen/rejected | `training_file_ids` 数组 + 可选 `validation_file_ids`；不传验证集时按 `split` / `max_split_val_dataset_sample` 自动切分（默认 80/20） |
| 输出形态 | 强调"产出的模型**不支持下载**"、视频/语音等仅 API 创建 | `output.finetuned_output` 即产出模型 ID；全参产物可走模型压缩 API 量化部署 |
| 超参描述 | 简述训练方式选型与典型用法、专属约束（如 `freeze_vit=true` 才按 Token 计费） | 字段级表格：`n_epochs`/`batch_size`/`max_length` 必填，LoRA `lora_rank`/`lora_alpha`/`lora_dropout`、混合训练 `data_augmentation`、Checkpoint `save_strategy` 等 |
| 任务状态机 | 不展开（关注训练方式选择） | `PENDING` / `QUEUING` / `RUNNING` / `CANCELING` / `SUCCEEDED` / `FAILED` / `CANCELED`，同账号同时仅一个任务运行 |
| 支持模型清单 | 给出文本各基础模型的 CPT/SFT/SFT 高效/DPO 全参/DPO 高效支持矩阵与训练单价 | 提示"不同模型默认超参不同"，依赖控制台/调优指南确认 |
| 多模态特性 | 千问 VL ZIP 结构、视频万相首帧/首尾帧基础模型、CosyVoice 单音色锁死 `voice=default` | 通用流程覆盖；视频/图像/CosyVoice 细节链接到独立 API 参考子页 |
| 计费视角 | 列出训练单价（千 Token）、混合训练数据会计入计费 Token、VL 必须 `freeze_vit=true` 才按 Token 计费 | 仅提示超参影响时长与费用，不列价格 |
| 文件管理 | 关注训练集格式与压缩包结构 | `POST /api/v1/files`（`purpose=fine-tune`）、单文件 ≤ 1 GB、有效文件总空间 ≤ 5 GB、总数 ≤ 100 个 |
| 地域限制 | 仅中国大陆版（北京地域），产出模型不支持下载 | 同样仅北京地域；API Key 归属错误会鉴权失败 |
| 文档来源 | `guides/fine-tuning.md`（汇总多篇控制台与方法论文档） | `api/model-training.md`（汇总 4 份原始 API 参考） |

## 适用场景建议

- **选型阶段 / 算法侧**：先看 [fine tuning](../guides/fine-tuning.md) 指南。它直接回答"业务问题适合 CPT 补知识、SFT 学做事，还是 DPO 偏好对齐"，并给出每个基础模型在不同训练方式下的支持矩阵与训练单价，便于做成本与效果的初步评估。
- **数据准备阶段**：仍以 fine tuning 指南为主。ChatML / thinking / VL ZIP / CPT 纯文本 / DPO chosen-rejected / CosyVoice `.wav + jsonl` 等格式规范、文件大小与命名约束都集中在这里；遗漏会直接导致 `BadRequest.*` 类错误。
- **接口集成阶段 / 后端侧**：切到 [model training](../api/model-training.md) 参考。所有 `POST /api/v1/fine-tunes` 字段、`training_type` 取值、`hyper_parameters` 子集（含 LoRA 参数必须与上次一致、`freeze_vit` 计费门槛、CosyVoice 8 个 LM/FM 参数）以及 `validation_file_ids` 自动切分规则都在这里。
- **任务编排与排查**：依赖 model training 的状态机描述（`PENDING → QUEUING → RUNNING → SUCCEEDED/FAILED/CANCELED`）与"同账号同时仅一个任务"的并发约束，配合 `GET /api/v1/fine-tunes/{job_id}` 轮询。
- **二次微调与部署**：fine tuning 指南说明"基于上一次调优产出的模型再训练"沿用基础模型规则；model training 参考则给出全参产物可投递到模型压缩 API（`POST /api/v1/fine-tunes/compress/jobs`）的下游路径。
- **多模态特化场景**：万相视频/图像、CosyVoice 语音合成的"仅 API 可发起、控制台不可用"等限制，fine tuning 指南做了汇总说明，但具体超参与字段差异仍需到 model training 参考及其链接的独立子页确认。

## 选择建议总结

- 把 fine tuning 当作**调优能力的目录与决策树**：先确定模态、训练方式、基础模型与数据格式。
- 把 model training 当作**调优能力的接口契约**：在确定方案后，逐字段对照请求体、超参与状态机实现集成。
- 两份文档对同一能力的描述应当一致，但当出现差异（例如"支持模型清单"在控制台、API 指南与综述间略有出入）时，按调优指南的明确提示——**以控制台实际可选项为准**。

## 被对比主题页

- [fine tuning](../guides/fine-tuning.md)
- [model training](../api/model-training.md)


