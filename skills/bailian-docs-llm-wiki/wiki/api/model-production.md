# model production

model production 是百炼平台中用于模型定制化与服务化的关键能力集合，涵盖模型微调、部署及生命周期管理。它面向开发者提供标准化 API 接口，支持从训练到上线的端到端流程。所有操作均通过 RESTful API 或 SDK 调用，需配合百炼平台认证体系使用。

## 支持的模型/功能

- **微调（Fine-tuning）**：支持基于预训练大语言模型（如 Qwen 系列）进行监督微调，适配下游任务（如指令遵循、领域问答）。输入为结构化 JSONL 格式数据集，支持 LoRA 等高效微调方法。  
- **部署（Deployment）**：支持将微调完成的模型或直接导入的兼容格式模型（如 GGUF、ONNX 导出模型）发布为高可用推理服务，自动分配 endpoint 并支持流量路由与扩缩容。  
- **模型版本管理**：每个微调任务生成唯一 `job_id`，对应产出模型可被多次部署；部署实例绑定 `model_id` 与 `version_id`，确保可追溯性。  
详见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 和 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 基座模型 ID（如 `qwen2.5-7b`），必须在 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 支持列表中 |
| `training_file` | string | 是（微调） | OSS 或 S3 URI，指向训练数据集（JSONL 格式） |
| `endpoint_name` | string | 是（部署） | 全局唯一标识符，长度 3–63 字符，仅含小写字母、数字和连字符 |
| `instance_type` | string | 否 | 默认 `gpu-a10`；部署时可选 `gpu-v100`、`cpu-small`（仅限测试） |

> **注意**：文档 2 中提及“支持导入 ONNX 模型”，但当前版本（v2.4+）实际仅支持 ONNX 的 *推理兼容验证*，不支持 ONNX 模型直接部署；完整支持计划见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 的“未来特性”章节（该内容已过时，以控制台 API 文档为准）。

## 使用方式

1. **微调流程**：  
   - POST `/api/v1/fine_tuning_jobs`，携带 `model`、`training_file` 等参数；  
   - 轮询 `GET /api/v1/fine_tuning_jobs/{job_id}` 直至 `status == "succeeded"`；  
   - 提取响应中的 `fine_tuned_model_id` 用于后续部署。

2. **部署流程**：  
   - POST `/api/v1/deployments`，传入 `model_id`（来自微调结果）、`endpoint_name`、`instance_type`；  
   - 部署成功后，`endpoint_url` 可立即用于 `POST /v1/chat/completions` 请求。

完整示例代码与错误码说明参见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)。

## 限制和注意事项

- 单次微调最大训练时长为 72 小时，超时任务自动终止且不计费；  
- 每个账号默认最多同时运行 3 个微调任务、5 个部署实例，配额可通过工单申请提升；  
- 微调数据集须经敏感信息过滤（如 PII），平台不承担未脱敏数据导致的合规风险；  
- 部署实例启动后需 2–5 分钟完成初始化，期间 `health_check` 返回 `503`，请实现重试逻辑。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


