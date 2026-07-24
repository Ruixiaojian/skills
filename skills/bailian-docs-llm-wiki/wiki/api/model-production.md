# model production

`model production` 是百炼平台中将训练/微调后的模型投入实际服务的关键阶段，涵盖模型部署、版本管理与在线推理能力。它不涉及模型训练本身，而是聚焦于已存在模型（微调产出或第三方导入）的上线与运维。开发者需先完成模型准备，再通过 API 或控制台触发生产流程。

## 支持的模型与功能

- 支持由 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 生成的微调模型；
- 支持通过模型导入流程上传的 Hugging Face 格式或 ONNX 模型；
- 提供模型版本管理、灰度发布、自动扩缩容及健康监控等生产级能力；
- > **注意**：文档 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 中提及“支持直接部署原始基础模型”，但该能力已于 v2.3 版本移除，仅允许部署已注册的微调模型或显式导入模型。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，来自微调任务输出或导入任务返回值 |
| `instance_type` | string | 是 | 推理实例规格（如 `gpu.a10.2xlarge`），详见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 文档 |
| `replicas` | integer | 否 | 初始副本数，默认为 1；支持后续动态调整 |
| `timeout` | integer | 否 | 单次推理超时（秒），范围 1–300 |

## 使用方式

1. 确保目标模型已完成微调或导入，并获取其 `model_id`（参见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 的响应结构）；
2. 调用 `POST /v1/deployments`，传入上述关键参数；
3. 部署成功后，平台返回 `deployment_id` 和可访问的 endpoint URL；
4. 通过该 endpoint 发起标准 `/v1/chat/completions` 或 `/v1/embeddings` 请求（协议兼容 OpenAI）。

## 限制和注意事项

- 单个账号最多同时运行 5 个 active deployment（含正在创建中的）；
- 部署实例类型必须与模型精度（FP16/INT8）及架构（如 Llama-3-8B）匹配，不匹配将导致启动失败；
- 模型文件体积上限为 20 GB；若超出，请先量化或裁剪；
- > **注意**：[模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 文档中描述的 `auto_scale` 字段在当前 API 版本（v1.2+）中已被弃用，应改用 `autoscaling_policy` 对象配置。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


