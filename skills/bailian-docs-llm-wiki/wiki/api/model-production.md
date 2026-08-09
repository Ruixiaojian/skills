# model production

`model production` 是百炼平台中用于将模型投入实际使用的完整流程，涵盖模型微调、部署及服务化等关键环节。它为开发者提供从训练到上线的一站式能力，支持快速迭代与规模化推理。该能力基于 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 和 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 两大核心 API 组成。

## 支持的模型/功能

- 支持对百炼托管的基础大模型（如 Qwen 系列）进行监督微调（SFT）；
- 支持导入已训练好的 Hugging Face 格式模型（需满足平台兼容性要求）；
- 提供微调任务管理、版本控制、评估指标输出（如 loss、accuracy）；
- 支持将微调完成或导入的模型一键部署为 HTTP 接口服务，并可配置自动扩缩容策略。

> **注意**：文档 1 中未明确说明是否支持 RLHF 微调，而当前平台实际仅支持 SFT；请以 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 中定义的 `training_type: "sft"` 为准，RLHF 功能暂未开放。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 基础模型 ID（如 `qwen2-7b-chat`），需在 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 中指定 |
| `training_dataset_id` | string | 是 | 训练数据集 ID（格式为 `dataset-xxx`） |
| `max_steps` / `num_epochs` | integer | 二选一 | 控制训练时长，避免过拟合 |
| `deployment_config` | object | 否（部署时必填） | 包含 `instance_type`（如 `gpu.2xlarge`）、`replicas`、`autoscaling_enabled` 等字段，详见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) |

## 使用方式

1. **微调模型**：调用 `/v1/fine_tuning_jobs` 创建任务，传入 `model_id` 和训练数据集；
2. **监控与验证**：通过 `GET /v1/fine_tuning_jobs/{job_id}` 查询状态与评估结果；
3. **部署服务**：微调成功后，使用其生成的 `fine_tuned_model_id` 调用 `/v1/deployments` 创建在线服务；
4. **调用推理**：部署成功后，通过返回的 `endpoint_url` 发送 POST 请求，格式同标准 `/v1/chat/completions`。

## 限制和注意事项

- 单次微调任务最长运行时间为 72 小时，超时将自动终止；
- 每个微调模型最多保留 5 个历史版本，旧版本需手动清理；
- 部署实例类型受账号配额限制，GPU 实例需提前申请配额；
- > **注意**：[模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 文档中提及“支持热更新模型”，但当前版本仅支持重建部署（即删除旧 deployment 并创建新 deployment），热更新尚未上线，请勿依赖该描述。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


