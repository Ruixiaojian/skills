# model production

model production 是百炼平台中用于将基础模型转化为可交付、可服务的定制化模型的一整套能力，涵盖微调训练与在线部署两个核心阶段。开发者可通过 API 或控制台完成端到端模型生命周期管理。该流程依赖于统一的模型标识（`model_id`）和版本化资源管理。

## 支持的模型/功能

- **微调训练**：支持对百炼托管的基础模型（如 Qwen 系列）进行监督微调（Supervised Fine-tuning），适配特定任务数据集；详见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)。
- **[模型部署](../concepts/model-deployment.md)**：支持将微调完成的模型或通过 `import_model` 导入的第三方模型（需符合 ONNX/Triton 格式要求）部署为 HTTP 接口服务；详见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)。
- **版本管理**：所有微调作业产出及部署实例均绑定唯一 `version_id`，支持灰度发布与回滚。

## 关键参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `model_id` | 模型唯一标识符，格式为 `org-id/model-name` | `my-org/qwen2-7b-chat-ft-v1` |
| `training_job_id` / `deployment_id` | 微调作业或部署实例 ID，全局唯一 | `ft-job-abc123`, `dep-xyz789` |
| `instance_type` | 部署时指定的 GPU 规格（仅限部署阶段） | `gpu-a10-2` |
| `max_batch_size` | 推理服务最大批处理尺寸（部署参数） | `8` |

> **注意**：文档中未明确 `instance_type` 是否支持 CPU 实例；当前 API 实际仅接受 GPU 类型，CPU 部署暂不支持，请以 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 中的 `instance_type` 枚举值为准。

## 使用方式

1. **微调启动**：调用 `POST /v1/fine_tuning_jobs`，传入 `base_model_id`、训练数据 OSS 路径及超参配置；
2. **监控状态**：轮询 `GET /v1/fine_tuning_jobs/{job_id}` 获取 `status: succeeded` 后，获取产出 `model_id`；
3. **部署服务**：调用 `POST /v1/deployments`，传入上一步得到的 `model_id` 及 `instance_type` 等参数；
4. **调用推理**：使用返回的 `endpoint_url` 发送 `POST /v1/chat/completions` 请求（兼容 OpenAI 格式）。

## 限制和注意事项

- 单次微调作业最长运行时限为 72 小时，超时自动终止；
- 每个 `model_id` 最多保留 10 个历史版本（含微调产出与手动导入），超出后需显式清理旧版本；
- 部署实例默认启用自动扩缩容（min=1, max=5），但 `max_batch_size` 和 `max_concurrent_requests` 需在创建时固定，不支持运行时修改；
- 微调数据集必须为 JSONL 格式且字段名严格匹配 `messages`（Chat）或 `prompt`/`completion`（Completion）；具体约束见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


