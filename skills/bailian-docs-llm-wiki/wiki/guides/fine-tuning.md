# fine tuning

阿里云百炼平台的模型调优（Fine Tuning）功能支持对文本生成、视觉理解、视频生成和语音合成等多种模型进行微调，以提升模型在特定行业或业务场景下的表现。平台提供 SFT（监督微调）、CPT（继续预训练）、DPO（直接偏好优化）三种调优方式，以及全参训练和高效训练（LoRA）两种训练模式，覆盖从数据准备、训练、部署到评测的完整流程。

> **注意**：模型调优功能仅适用于中国大陆版（北京地域），需使用对应地域的 API Key。

## 支持的模型与调优方式

### 文本生成模型

百炼支持对 Qwen 系列文本生成模型进行 CPT、SFT、DPO 调优。主要支持的模型包括：

- **Qwen3 系列**：qwen3-32b、qwen3-14b、qwen3-8b、qwen3-1.7b、qwen3-0.6b 等，大部分支持 SFT 全参/高效训练和 DPO
- **Qwen3.5 系列**：qwen3.5-27b、qwen3.5-9b，支持 SFT 全参/高效训练
- **Qwen2.5 系列**：qwen2.5-72b-instruct 至 qwen2.5-7b-instruct，支持全部五种调优方式
- **视觉理解模型（Qwen-VL）**：qwen3-vl-8b-instruct、qwen2.5-vl-72b-instruct 等，支持 SFT 全参/高效训练

完整的支持矩阵详见 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

### 视频生成模型

视频生成模型支持 SFT-LoRA 高效微调，适用于定制特定动作、特效或风格：

- **图生视频-基于首帧**：wan2.5-i2v-preview、wan2.2-i2v-flash
- **图生视频-基于首尾帧**：wan2.2-kf2v-flash

详细操作流程见 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

### 语音合成模型

CosyVoice 语音合成模型支持 SFT 高效微调（`efficient_sft`），当前仅支持 `cosyvoice-v3-flash` 模型，且只能通过 API 方式发起调优任务。详见 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

> **注意**：CosyVoice 模型调优与声音复刻/声音设计是不同的功能，后者应使用专用接口。

## 调优方法对比

百炼提供的三种调优方式是递进的，推荐流程为 `CPT（可选）→ SFT → DPO（可选）`：

| 特性 | CPT（持续预训练） | SFT（监督微调） | DPO（直接偏好优化） |
|------|-------------------|------------------|----------------------|
| 核心目标 | 注入领域知识 | 学会遵循指令 | 对齐人类偏好 |
| 输入数据 | 1000万+ Token 无标签文本 | 1000+ 条高质量问答对 | 100+ 组正负样本对 |
| 学习方式 | 自监督（预测下一个词） | 监督（模仿标准答案） | 偏好学习（增大好答案概率） |

### 训练模式

| | 全参训练 | 高效训练（LoRA） |
|---|---------|-----------------|
| 适用场景 | 需学习新能力、追求最优效果 | 优化特定场景、对时间和成本敏感 |
| 训练时间 | 较长 | 较短 |

> 两种训练方式费用相同，如模型支持全参训练则优先选择全参训练，性价比更高。

## 关键参数

### 文本生成模型超参数

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| `batch_size` | 默认值（16/32） | 每次更新参数的数据步长 |
| `learning_rate` | 高效训练 1e-4；全参训练 1e-5 | 控制权重修正强度，过高易导致效果变差 |
| `n_epochs` | 数据 <10000 条设 3-5；>10000 条设 1-2 | 模型遍历训练次数 |
| `max_length` | 设为模型支持最大值 | 单条数据 token 最大长度，SFT 超出则丢弃 |
| `lora_rank` | 设为模型支持最大值 | LoRA 低秩矩阵秩，越大效果越好但训练略慢 |

### CosyVoice 模型超参数

CosyVoice 涉及 LM（语言模型）和 FM（流匹配模型）两个子网络，推荐首次使用以下配置：

- **LM**：`lm_max_epoch=60`、`lm_step=5`、`lm_num=3`、`lm_batch_size=1000`
- **FM**：`fm_max_epoch=100`、`fm_step=10`、`fm_num=3`、`fm_batch_size=2000`

## 数据格式

### SFT 训练数据（ChatML 格式）

```json
{"messages": [
  {"role": "system", "content": "系统输入"},
  {"role": "user", "content": "用户输入"},
  {"role": "assistant", "content": "期望的模型输出"}
]}
```

- **思考模型（Thinking）**：仅最后一个 assistant 输出添加 `<think>` 标签
- **视觉理解（VL）**：`content` 使用数组格式传入文本和图像/视频，压缩为 ZIP 上传
- **DPO 数据**：在 messages 基础上增加 `chosen` 和 `rejected` 字段
- **CPT 数据**：纯文本格式 `{"text": "文本内容"}`

### CosyVoice 训练数据

将 `.wav` 音频文件和 `data.jsonl` 打包为 ZIP，每行格式为：

```json
{"wav_fn": "train/100001.wav", "text": "对应文本"}
```

推荐训练音频总时长 1-10 小时，不少于 150 条样本。

## 使用方式

### 控制台

适用于文本生成模型调优，提供可视化界面完成训练配置、数据上传、任务创建和模型部署，详见 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

### API / 命令行

通过 HTTP 接口或 DashScope CLI 操作，完整流程包括：

1. **上传数据集**：`POST /api/v1/files`，获取 `file_id`
2. **创建调优任务**：`POST /api/v1/fine-tunes`，指定模型、训练方式和超参数
3. **查询任务状态**：`GET /api/v1/fine-tunes/{job_id}`，等待 `status` 变为 `SUCCEEDED`
4. **部署模型**：`POST /api/v1/deployments`，等待状态为 `RUNNING`
5. **调用模型**：使用 `deployed_model` 作为模型名称进行推理

> **注意**：通过 API 创建的训练任务仅支持按 Token 计费，暂不支持使用模型训练单元（预付费或后付费）。如需使用训练单元，请通过控制台创建任务。

## 计费

- **文本生成模型**：按 `（训练 Token 总数 + 混合训练 Token 总数）× 循环次数 × 训练单价` 计费，单价因模型而异（如 qwen3-8b 为 ¥0.006/千Token，qwen2.5-72b-instruct 为 ¥0.15/千Token）
- **CosyVoice 模型**：训练费用按 Token 计费（¥0.2/千Token），部署费用按模型单元使用时长计费
- **调优后模型**：需部署后才能使用，部署产生额外费用

## 限制和注意事项

- 模型调优功能**仅限中国大陆版（北京地域）**
- 子账号（RAM 用户）需额外授予训练和部署权限
- 建议在尝试 Prompt 工程和插件调用效果不佳后，再考虑模型调优——调优通常是改进模型表现的"最后手段"
- 文件上传限制：单文件最大 300MB，有效文件总空间 5GB，最多 100 个文件
- SFT 训练数据不支持 OpenAI 的 `name`、`weight` 参数
- SFT 中单条数据超过 `max_length` 会被**直接丢弃**；DPO 则会截断后继续训练

> **注意**：关于控制台支持的模型列表，不同文档中存在细微差异（例如 Qwen3.6-Flash 和 Qwen3.5-Flash 在部分文档中出现、在另一些文档中未列出）。请以控制台实际显示的可选模型为准。

## 来源文档

- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)

