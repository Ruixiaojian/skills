# fine tuning

fine tuning（微调）是百炼平台提供的核心模型优化能力，允许开发者基于预训练大模型，在特定任务、领域或风格上进行针对性适配。它不改变基座模型架构，而是通过增量学习注入业务知识、对齐人类偏好或强化安全合规能力，适用于文本生成、多模态理解、图像/视频生成及语音合成等多种场景。微调结果为独立部署的新模型，可直接通过 API 调用。

## 支持的模型与功能

百炼平台支持多种调优方式，覆盖不同模态和业务需求：

- **文本生成**：支持 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化），涵盖 Qwen3 系列（如 `qwen3-8b`、`qwen3-32b`）、Qwen2.5 系列及千问-Plus-Character 等数十种模型 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。  
- **多模态理解（千问 VL）**：支持图片/视频输入的 SFT 微调，需使用 zip 包格式（含 `data.jsonl` 与图像文件），适用于视觉问答、图文推理等场景 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。  
- **图像生成（万相）**：仅支持 `wan2.7-image-pro` 和 `wan2.7-image` 模型，采用 SFT-LoRA 高效微调，用于定制人物形象、IP 风格或特效（如“末日废土红黑机甲”）[原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。  
- **视频生成（万相）**：支持 `wan2.7-i2v`、`wan2.2-kf2v-flash` 等图生视频模型，同样基于 SFT-LoRA，可训练“金钱雨”“时尚杂志”等运动特效 [原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。  
- **语音合成（CosyVoice）**：仅支持 `cosyvoice-v3-flash` 模型的 `efficient_sft` 微调，面向同一发音人多条录音的高还原度音色定制，产物为单音色独立模型 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
- **强化学习（RL）**：支持 `qwen3.5-9b` 等 MoE/非 MoE 模型，通过 Rollout-Reward 循环实现自主策略优化，适用于数学推理、Agent [工具调用](../concepts/tool-use.md)等复杂决策任务 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档中提及的 `qwen3.7-plus-2026-05-26` 等部分新模型在控制台部署时需联系商务经理，而 CosyVoice 微调当前**仅支持 API 方式**，控制台暂未开放 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 关键参数

不同调优方式的关键参数差异显著，需按场景严格配置：

- **通用超参（SFT/DPO/CPT）**：`n_epochs`（循环次数，必填）、`batch_size`（批次大小，必填）、`learning_rate`（学习率，推荐 SFT 高效训练用 `1e-4` 量级）、`max_length`（序列长度，必填）。`lr_scheduler_type` 推荐 `cosine` 或 `inverse_sqrt`；`lora_rank` 应设为模型支持的最大值以提升效果 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。  
- **图像/视频生成（万相）**：`generation_type`（`t2i` 或 `i2i`）、`max_pixels`（训练图最大分辨率，文生图推荐 `"2k"`）、`val_img_size`（验证图分辨率）、`lora_rank`（必须为 2 的幂次，如 `32`）[原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。  
- **视频生成（万相）**：`n_epochs`（推荐 `50`，但需结合数据量动态调整）、`max_pixels`（整型，如 `wan2.7-i2v` 推荐 `102400`）、`lora_alpha`（与 `lora_rank` 配合，推荐 `32`）[原文标题](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。  
- **CosyVoice**：`lm_max_epoch`（语言模型轮次，生产推荐 `60`）、`fm_max_epoch`（流匹配模型轮次，生产推荐 `100`）、`lm_batch_size`/`fm_batch_size`（分别推荐 `1000`/`2000`），所有 `lm_*` 和 `fm_*` 字段均为必填 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
- **强化学习（RL）**：`algorithm`（如 `gspo`）、`batch_size`（如 `64`）、`kl_loss_coef`（KL 散度系数，如 `0.002`）、`resources.mtu_capacity`（必需指定 MTU 数量，如 `24`）[原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 使用方式

微调流程统一为“上传数据 → 创建任务 → 查询状态 → 部署模型”，但入口和细节因方式而异：

- **控制台操作**：适用于文本/SFT/DPO/CPT 及千问 VL 多模态微调。在[模型调优](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager)页面创建任务，支持数据集选择、OSS 挂载、混合训练及可视化日志监控 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。  
- **API/命令行**：全场景支持，尤其适用于图像/视频/语音生成及 RL 训练。需先调用 `/api/v1/files` 上传 `.zip` 或 `.jsonl` 文件获取 `file_id`，再以 `POST /api/v1/fine-tunes` 提交任务，传入 `model`、`training_file_ids`（或 `training_datasets`）、`training_type` 及 `hyper_parameters` [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。  
- **特殊流程**：  
  - 图像/视频微调需下载官方训练集模板（如 `wan-image-t2i-training-dataset.zip`），按规范组织数据 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。  
  - CosyVoice 必须打包为 `user_data/` 目录结构（含 `data.jsonl` 和 `train/` 音频子目录）的 `.zip` 文件 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
  - RL 训练需下载 Demo 包（如 `agentic-rl-example.zip`），配置函数组件（Rollout/Reward）并指定 MTU 资源 [原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 限制和注意事项

- **地域与权限**：所有微调服务（除文本 SFT/DPO/CPT 全地域支持外）均**仅限华北2（北京）地域**，且需使用该地域的 API Key；RAM 子账号必须被授予模型调用、训练、部署权限 [原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。  
- **数据格式与大小**：  
  - 文本 SFT 使用 `jsonl` 格式，单文件 ≤ 200 MB；多模态 SFT 使用 `.zip` 包，内含 `data.jsonl` 和图片/视频，单张图 ≤ 10 MB、宽高 ≤ 1024 px [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。  
  - CosyVoice 音频仅支持 `.wav`，采样率 ≥ 16 kHz，单条时长 1–30 秒，总时长建议 1–10 小时 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
- **计费与资源**：  
  - 文本/多模态微调按 [Token](../concepts/token.md) 计费（单价见模型列表），RL 训练**强制使用 MTU 训练单元**（不支持 [Token](../concepts/token.md) 计费）[原文标题](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。  
  - CosyVoice 训练费用 = `(lm_max_epoch + fm_max_epoch) × 25 × 总秒数 × 0.2 元/千 Tokens`，部署费用按模型单元时长计费 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
- **模型产物与调用**：微调后产出 `finetuned_output`（新模型名），需单独部署为 `deployed_model` 后方可调用；图像/视频/语音微调产物**不可切换音色或风格参数**（如 `voice="default"` 锁死），其能力边界由基础模型决定 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

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


