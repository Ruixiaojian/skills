# model production

model production 是百炼平台中用于将基础模型转化为可交付、可服务化模型的关键流程，涵盖微调训练与在线部署两个核心阶段。开发者可通过 API 或控制台完成模型定制与服务发布，整个流程支持端到端的生命周期管理。该能力依赖于 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 和 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 两套独立但协同的 API。

## 支持的模型/功能

- 支持对百炼托管的基础模型（如 Qwen 系列）进行监督微调（Supervised Fine-tuning），不支持 RLHF 或持续预训练；
- 支持将微调完成的模型或通过 `import_model` 导入的第三方模型（需符合 ONNX/Triton 格式要求）部署为 HTTP 推理服务；
- 提供异步任务管理：微调任务（`fine_tuning_job`）与部署实例（`deployment`）均为独立资源，支持状态轮询与日志获取。

> **注意**：文档 1 中“通过微调训练定制专属模型”未明确限定仅支持监督微调；而文档 2 的实际 API 实现和错误码说明（见 `deployments-api.md` 的 `400 Bad Request` 响应示例）明确拒绝非 SFT 类型的训练产物。因此，当前仅 SFT 模型可进入部署流程，其他微调方式暂不受支持。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `base_model` | 微调所用的基础模型 ID | `qwen2-7b-chat` | [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) |
| `training_file` | 训练数据集文件 ID（需已上传至百炼对象存储） | `ft-dataset-abc123` | [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) |
| `model_id` | 部署时指定的模型唯一标识（微调成功后生成的 `fine_tuned_model_id` 或导入模型 ID） | `ft-qwen2-7b-chat-xyz789` | [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) |
| `instance_type` | 推理实例规格（如 `gpu.2xlarge`、`cpu.medium`） | `gpu.2xlarge` | [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) |

## 使用方式

1. **微调启动**：调用 `POST /v1/fine_tuning_jobs`，传入 `base_model`、`training_file` 及超参（如 `epoch`、`learning_rate`）；
2. **等待完成**：轮询 `GET /v1/fine_tuning_jobs/{job_id}`，直到 `status == "succeeded"`，提取返回中的 `fine_tuned_model_id`；
3. **部署服务**：调用 `POST /v1/deployments`，以 `fine_tuned_model_id` 作为 `model_id`，指定 `instance_type` 与 `scaling_config`；
4. **调用推理**：部署成功后，使用返回的 `endpoint_url` 发送 `POST /v1/chat/completions` 请求（兼容 OpenAI 格式）。

## 限制和注意事项

- 单次微调任务最大训练时长为 72 小时，超时自动终止且不退款；
- 同一 `model_id` 最多允许 5 个并发部署实例（按 `deployment_name` 区分），超出需先删除旧实例；
- 微调输出模型不可直接用于多模态推理——即使基础模型支持视觉输入，SFT 流程默认冻结非文本模态权重，此行为在 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 中未声明，但在实际 API 响应中会返回 `multimodal_enabled: false` 字段；
- 部署实例启动后不可变更 `instance_type`，如需调整，必须删除重建。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


