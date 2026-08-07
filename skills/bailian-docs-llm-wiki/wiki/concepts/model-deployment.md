# 模型部署

模型部署是百炼平台将训练完成或预置的大模型发布为稳定、可调用、可计量的在线推理服务的核心能力。它将模型从静态资产转化为生产就绪的 API 端点，支持高并发、低延迟、可监控的业务集成。

## 在百炼平台的不同场景中，这个概念如何使用

模型部署在百炼中不是单一操作，而是适配多种模型来源与业务目标的**服务化枢纽**，主要分为三类典型路径：

- **预置模型即开即用部署**：直接选择千问（Qwen3-Max/Plus/Flash/VL/Omni）、DeepSeek、GLM、Kimi、CosyVoice 等官方托管模型，通过控制台或 API 一键部署为专属服务。适用于快速验证、POC 或标准化业务场景，支持 PTU（预置吞吐）、MU（模型单元）两种生产级计费模式。

- **微调模型部署**：将通过 `model production` 流程完成训练（SFT/DPO/CPT）并已合并权重的自定义模型（如 `ft-qwen3-8b-xyz123`），以完整模型 ID 形式部署。该路径强调“训练即交付”，部署后服务名即为推理时的 `model` 参数值，无需额外适配。

- **LoRA 微调模型轻量部署**：仅支持从 OSS 导入、满足 rank=8/16/32/64、未修改 chat_template 和 vocab 的 LoRA 权重包，必须使用 `plan: "lora"` 模式部署（**不支持 PTU/MU**）。此模式按 [Token](token.md) 实时计费，适合效果验证、A/B 测试或成本敏感型实验，但功能受限（无 PD 分离、无限流、无思考模式）。

> ⚠️ 注意：模型压缩（quantization）后的模型属于“自定义模型”范畴，可直接用于上述第二类部署；而基础模型（未微调）不可压缩，也不支持 LoRA 权重独立部署（仅支持导入后以 `lora` 模式部署）。

## 关键参数和配置

| 参数 | 适用场景 | 必填 | 说明 | 示例 |
|------|----------|------|------|------|
| `plan` | 全部部署 | ✅ | 计费与调度模式标识 | `"ptu"`（预置吞吐）、`"mu"`（模型单元）、`"lora"`（LoRA 按量） |
| `model_id` 或 `model_name` | 全部部署 | ✅ | 待部署模型标识：预置模型用标准 model code（如 `qwen3-flash-2025-07-28`）；微调模型用 `fine_tuned_model_id`；LoRA 模型用导入后的模型名 |
| `deployment_name` | 全部部署 | ✅ | 服务唯一标识符（3–32 字符），推理时作为 `model` 参数传入 | `"prod-qwen3-flash"` |
| `ptu_capacity` | `plan="ptu"` | ✅ | 输入/输出 TPM 额度（单位：token/分钟） | `{"input_tpm": 20000, "output_tpm": 2000}` |
| `deploy_spec` | `plan="mu"` | ✅ | 模型单元规格与数量，决定算力与并发能力 | `"MU2 x 4"` |
| `enable_thinking` | `plan="mu"` | ❌ | 是否启用思考模式（仅部分模型支持） | `true` |
| `max_context_length` | `plan="mu"` | ❌ | 最长上下文长度（需模型原生支持） | `128000` |
| `rpm_limit` / `tpm_limit` | `plan="mu"` | ❌ | 服务级请求/[Token](token.md) 速率限制 | `100`, `5000` |

> 💡 提示：  
> - LoRA 部署中 `capacity` 字段为占位符，必须填 `1`，无效；  
> - 所有部署创建成功即开始计费（含冷启动等待期）；  
> - 地域强约束：API 创建仅支持华北2（北京），新加坡地域需通过控制台操作；  
> - 推理时务必使用 `deployment_name`（而非原始模型名）作为 `model` 参数。

## 面向开发者，简洁实用

- ✅ **首选自动化**：用 `POST /api/v1/deployments` API 部署，配合轮询 `GET /api/v1/deployments/{id}` 状态，状态变为 `"RUNNING"` 后即可调用；
- ✅ **调试技巧**：首次调用前，建议用 `curl -X POST https://dashscope.aliyuncs.com/api/v1/chat/completions -H "Authorization: Bearer $DASHSCOPE_API_KEY" -d '{"model":"your-deployment-name","messages":[{"role":"user","content":"hello"}]}'` 快速验证；
- ✅ **成本控制**：PTU 模式开启「自动溢出」避免 429 错误；MU 模式通过 `rpm_limit`/`tpm_limit` 主动控流；LoRA 模式天然按需付费，适合灰度；
- ⚠️ **避坑提醒**：  
> - 不要混淆 `model_id`（训练产出/导入模型ID）与 `deployment_name`（服务名）；  
> - LoRA 模型不支持 `plan="ptu"` 或 `plan="mu"`，API 会返回 400；  
> - 部署后无法修改 `plan`、`model_id` 或核心规格，需删除重建；  
> - 冷启动延迟约 30–60 秒，高 SLA 业务建议预热（发送 dummy 请求）。

## 关联主题页

- [model deployment 1](../guides/model-deployment-1.md)
- [model production](../api/model-production.md)
- [fine tuning](../guides/fine-tuning.md)
- [model compression](../guides/model-compression.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


