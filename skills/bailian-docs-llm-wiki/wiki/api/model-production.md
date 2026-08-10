# model production

model production 是百炼平台中用于将基础模型转化为可交付、可服务化模型的关键流程，涵盖微调训练与在线部署两个核心阶段。开发者可通过 API 或控制台完成模型定制与服务发布，整个流程支持端到端的版本管理与生命周期控制。该能力面向需要私有化适配或高性能推理场景的开发者。

## 支持的模型/功能

- 支持对百炼官方提供的基础大模型（如 Qwen 系列）进行监督微调（Supervised Fine-tuning），不支持 RLHF 或强化学习路径 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)  
- 支持部署已微调完成的模型（`fine_tuned_model_id`）或通过 `import_model` 导入的第三方模型（需符合 ONNX/Triton 格式规范） [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)  
- 提供部署实例规格选择（CPU/GPU）、自动扩缩容配置及 HTTPS 端点暴露能力  

> **注意**：文档 1 中未明确说明是否支持 LoRA 微调，但实际 API 已支持 `lora_target_modules` 参数；该细节在 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 中缺失，建议以最新 OpenAPI Schema 为准。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `base_model` | string | 必填，基础模型 ID（如 `qwen2-7b-chat`），仅限平台白名单模型 |
| `training_file` | string | 微调数据集 OSS 路径（JSONL 格式），需满足指令对齐格式要求 |
| `instance_type` | string | 部署时指定，如 `gpu.p4.2xlarge` 或 `cpu.c5.2xlarge`，详见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) |
| `max_tokens` | integer | 推理最大输出长度，默认 2048，不可超过模型原生上下文窗口 |

## 使用方式

1. **微调启动**：调用 `POST /v1/fine_tuning/jobs`，传入 `base_model`、`training_file` 及超参（`epochs`, `learning_rate` 等）  
2. **状态轮询**：通过 `GET /v1/fine_tuning/jobs/{job_id}` 获取 `status: succeeded` 后获取 `fine_tuned_model_id`  
3. **部署发布**：调用 `POST /v1/deployments`，传入 `model_id`（即上步所得 ID）、`instance_type` 和 `replicas`  
4. **调用服务**：使用返回的 `endpoint_url` + `Authorization: Bearer <api_key>` 发起 `/v1/chat/completions` 请求  

## 限制和注意事项

- 单次微调任务最长运行时间 72 小时，超时自动终止且不退款  
- 部署实例最小副本数为 1，暂停（scale to zero）功能暂不支持  
- 微调数据集大小上限 100 MB，单条样本 `input` + `output` 总长度不得超过 8192 token  
- > **注意**：文档 2 声称“支持导入任意 Hugging Face 模型”，但实际仅支持已通过百炼兼容性验证的模型列表（见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 附录 A），未验证模型导入将返回 `400 UnsupportedModelFormat` 错误

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


