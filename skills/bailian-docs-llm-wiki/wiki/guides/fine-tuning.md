# fine tuning

fine tuning 是百炼平台提供的核心模型优化能力，允许开发者基于自有数据对预训练大模型进行定制化训练，从而提升其在特定业务场景、领域知识或安全合规要求下的表现。该能力覆盖文本生成、多模态理解、图像生成、视频生成及强化学习等多种任务类型，支持全参训练与 LoRA 等高效微调方式，并统一通过 `fine-tunes` API 接口管理生命周期。

## 支持的模型/功能

百炼平台支持多种调优方式与模型类型，按任务域划分如下：

- **文本生成**：支持 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化），覆盖 Qwen3 系列（如 `qwen3-8b`, `qwen3-32b`）、Qwen2.5 系列及千问-Plus-Character 等模型；其中 `efficient_sft`（LoRA）为默认推荐方式，兼顾效果与成本 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **视觉理解（千问 VL）**：支持 SFT/DPO，适用于图片/视频输入场景，需注意 `freeze_vit` 参数仅在设为 `true` 时支持按 [Token](../concepts/token.md) 计费 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **图像生成（万相）**：仅支持 `efficient_sft` 方式，当前可用模型为 `wan2.7-image-pro` 和 `wan2.7-image`，且**仅限华北2（北京）地域** [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成（万相）**：支持 `efficient_sft`，模型包括 `wan2.7-i2v`（首帧）、`wan2.2-kf2v-flash`（首尾帧）等，同样**仅限华北2（北京）地域** [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **强化学习（RL）**：采用 GSPO 算法，支持 `qwen3.5-9b` 等 MoE/非 MoE 模型，**必须使用模型训练单元（MTU）计费，不支持按 [Token](../concepts/token.md) 计费** [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 4 和文档 6 的表格中均列出 `Qwen3.7-Plus-2026-05-26` 支持 SFT，但文档 4 明确标注“调优后部署请联系商务经理”，而文档 6 未提此限制。实际使用前须确认该模型是否已开放部署权限，避免因权限缺失导致部署失败。

## 关键参数

不同训练方式与模型类型的关键超参存在差异，开发者应以控制台实时配置为准，以下为通用高频参数：

| 参数 | 类型 | 必填 | 说明 | 推荐值/约束 |
|------|------|------|------|-------------|
| `training_type` | string | 是 | 训练方法：`sft`/`efficient_sft`/`cpt`/`dpo_full`/`dpo_lora` | 图像/视频生成固定为 `efficient_sft` |
| `n_epochs` 或 `max_steps` | int | 是（二选一） | 训练轮数（SFT/CPT/DPO）或总步数（万相图像/视频） | SFT：数据量 <10k 用 3–5；万相图像：≥500 步 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md) |
| `learning_rate` | float | 是 | 权重更新步长 | SFT 全参：`1e-5`；SFT LoRA：`1e-4`；万相图像：`3e-5`；万相视频：`2e-5` |
| `batch_size` | int | 是 | 单次送入数据条数 | 文本 SFT：16/32；万相视频：`wan2.7-i2v` 用 1，`wan2.2-kf2v-flash` 用 4 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md) |
| `lora_rank` | int | 是（LoRA 场景） | 低秩矩阵维数，须为 2 的幂（16/32/64） | 万相图像：32；文本 LoRA：8–32（越大拟合越强，但易过拟合） |
| `max_length` 或 `max_token_length` | int/string | 是 | 单条数据最大 token 长度（文本）或分辨率上限（多模态） | 文本：8192；万相文生图：`"2k"`（2048×2048） [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md) |
| `eval_steps` 或 `eval_epochs` | int | 是 | 验证间隔步数/轮数 | SFT：50；万相图像：200；万相视频：20 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md) |

> **注意**：`max_pixels`（万相）与 `max_length`（文本）语义不同，前者控制图像缩放像素上限（如 `"2k"`=1024×1024），后者控制文本序列长度。混用将导致训练失败。

## 使用方式

全流程分为四步：上传数据 → 创建任务 → 查询状态 → 部署调用。

1. **上传数据集**  
   - 文本：JSONL 格式，遵循 ChatML 多轮结构（`messages` 数组含 `system`/`user`/`assistant` 角色），单文件 ≤200 MB [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。  
   - 多模态（图像/视频）：ZIP 包含 `data.jsonl` + 原始媒体文件，`data.jsonl` 中 `content` 字段引用图片名（如 `{"image": "a.jpg"}`），单图宽高 ≤1024 px [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。  
   - 调用 `/api/v1/files` 接口上传，获取 `file_id`。

2. **创建微调任务**  
   - 构造 POST `/api/v1/fine-tunes` 请求体，指定 `model`、`training_datasets`（含 `file_id`）、`training_type` 及 `hyper_parameters`。  
   - 支持 OSS 挂载（`data_source_type: oss_mount`），需提前授权百炼访问 Bucket [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

3. **查询任务状态**  
   - 轮询 `/api/v1/fine-tunes/{job_id}`，直至 `output.status == "SUCCEEDED"`。  
   - 图像/视频微调耗时较长（万相图像 2K/300 步约 77 分钟；万相视频需数小时），需耐心等待 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

4. **部署与调用**  
   - 成功后，用 `finetuned_output` 名称调用 `/api/v1/deployments` 部署为在线服务（`plan: "lora"`）。  
   - 部署状态变为 `RUNNING` 后，通过对应 AIGC 接口调用（如图像生成用 `/services/aigc/image-generation/generation`），注意万相模型**仅支持异步调用** [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

## 限制和注意事项

- **地域与权限**：图像/视频生成微调**仅限华北2（北京）地域**，且需为子账号授予模型调用、训练、部署权限 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。RL 训练强制要求 MTU 计费，不支持 [Token](../concepts/token.md) 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
- **文件限制**：单个上传文件 ≤300 MB（API）；ZIP 包内单图 ≤10 MB、宽高 ≤1024 px；视频文件 ≤2 GB（URL 传入） [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **数据格式**：SFT 文本必须为 JSONL，每行一个 `messages` 对象；多模态 ZIP 包中 `data.jsonl` 必须位于根目录，图片路径需与 ZIP 内实际文件名一致 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **训练失败排查**：若 `Training Loss` 下降而 `Validation Loss` 上升，表明过拟合，建议减少 `n_epochs`、增大 `weight_decay` 或启用数据增强；若两者均不下降，检查数据质量或增大 `learning_rate` [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **计费说明**：按训练消耗 Token 总数计费（`Token 总数 × 循环次数 × 单价`），单价依模型而异（如 `qwen3-8b` 为 ¥0.006/千 Token）；RL 训练按 MTU 实例小时计费 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)


