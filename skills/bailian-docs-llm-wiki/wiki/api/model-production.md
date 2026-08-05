# model production

`model production` 是百炼平台中用于将模型投入实际使用的完整流程，涵盖微调训练、部署上线及生命周期管理。它提供统一的 API 接口和 CLI 工具，支持从训练任务提交到服务端点发布的端到端操作。开发者可通过 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 和 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 两个核心模块协同完成生产化。

## 支持的模型/功能

- 支持基于百炼基础模型（如 Qwen 系列）启动监督微调（SFT）任务；
- 支持导入已训练的 Hugging Face 格式模型（需满足 `config.json` + `pytorch_model.bin` 或 `safetensors` 结构）；
- 提供推理服务部署能力，包括自动扩缩容、流量灰度、版本回滚；
- 支持通过 `model production` 命令行工具统一管理微调任务与部署实例。

> **注意**：文档 1 中仅提及“微调训练”，未说明是否支持 RLHF；而文档 2 明确限定部署对象为“微调或导入的模型”。当前 API 实际仅支持 SFT，RLHF 尚未开放，详见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 的 `training_type` 参数约束。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 基础模型 ID（如 `qwen2-7b-chat`）或已导入模型 ID |
| `training_type` | string | 是 | 固定为 `"sft"`，暂不支持 `"rlhf"` |
| `dataset_id` | string | 是（微调时） | 训练数据集 ID，需提前通过 `/datasets` 接口上传 |
| `endpoint_name` | string | 是（部署时） | 全局唯一服务名称，符合 DNS-1123 规范（小写字母/数字/-） |
| `instance_type` | string | 否 | 默认 `ecs.gn7i-c8g1.2xlarge`，可选 GPU 实例类型，详见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) |

## 使用方式

1. **微调训练**：  
   ```bash
   bl model production fine-tune create \
     --model-id qwen2-7b-chat \
     --dataset-id ds-abc123 \
     --training-type sft \
     --epochs 3
   ```
   任务提交后返回 `job_id`，可用 `bl model production fine-tune get --job-id <id>` 查询状态。

2. **部署服务**：  
   微调完成后，获取输出模型 ID（`output_model_id`），执行：
   ```bash
   bl model production deploy create \
     --model-id <output_model_id> \
     --endpoint-name my-qwen-service \
     --instance-type ecs.gn7i-c8g1.2xlarge
   ```
   成功后返回可调用的 `endpoint_url`（HTTPS 地址）。

3. 所有操作均支持通过 REST API 调用，具体路径与请求体结构请参考 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 和 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)。

## 限制和注意事项

- 单次微调任务最长运行时间：72 小时；超时自动终止；
- 每个 `endpoint_name` 在同一地域下全局唯一，重复创建将报错 `409 Conflict`；
- 部署服务默认启用 HTTPS，不支持自定义域名或证书；
- 微调任务失败时，日志仅保留 7 天；部署服务日志需通过 `bl model production deploy logs` 主动拉取；
- > **注意**：文档 1 未说明数据集格式要求，但实际仅支持 JSONL 格式且字段必须含 `"messages"`（OpenAI 格式）或 `"prompt"`/`"completion"`（旧版格式）；该约束在 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 的附录中有明确示例，建议优先遵循后者。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


