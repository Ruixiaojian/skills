# model production

`model production` 是百炼平台中用于将模型投入实际应用的核心能力集合，涵盖从微调训练到在线服务部署的完整生命周期。开发者可通过统一 API 管理模型版本、启动训练任务及发布高可用推理端点。该能力面向生产环境设计，强调可重复性、可观测性和资源隔离。

## 支持的模型与功能

- 支持基于百炼基础模型（如 Qwen 系列）的**全参数微调**和**LoRA 微调**  
- 支持导入已训练的 Hugging Face 格式模型（需满足 `torch_dtype: bfloat16` 且含 `config.json` 和 `pytorch_model.bin`）  
- 提供模型版本管理、自动快照保存及跨环境（dev/staging/prod）部署能力  
- 可通过 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 创建带弹性扩缩容的 RESTful 推理服务，或通过 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 启动分布式训练任务  

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 基础模型 ID（如 `qwen2-7b`）或已上传的自定义模型 ID |
| `training_type` | string | 是 | 取值：`full` 或 `lora`；注意 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 中明确要求 LoRA 必须指定 `lora_rank` 和 `lora_alpha` |
| `deployment_config.min_replicas` | integer | 否 | 最小实例数，默认为 `1`；若设为 `0`，需启用冷启动策略（见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)） |
| `dataset_id` | string | 条件必填 | 微调时必需；部署时可为空（用于部署已有模型） |

> **注意**：文档 1 中未说明 `lora_target_modules` 的默认值，但实际 API 要求显式指定（如 `["q_proj","v_proj"]`），该行为与 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 中的示例代码一致，建议始终显式配置。

## 使用方式

1. **微调模型**：调用 `POST /api/v1/fine_tuning_jobs`，传入 `model_id`、`dataset_id` 和 `training_type` 等参数，获取 `job_id`  
2. **查询状态**：轮询 `GET /api/v1/fine_tuning_jobs/{job_id}`，待 `status == "succeeded"` 后获取产出模型 ID（`fine_tuned_model_id`）  
3. **部署服务**：调用 `POST /api/v1/deployments`，传入 `fine_tuned_model_id` 或自有模型 ID，指定 `deployment_config`  
4. **调用推理**：使用返回的 `endpoint_url` 发送 `POST` 请求，格式同标准 `/v1/chat/completions` 接口  

## 限制和注意事项

- 单次微调任务最长运行 72 小时，超时自动终止；超过 50GB 的数据集需提前申请配额  
- 部署服务的并发请求上限默认为 100 QPS，可通过工单提升至 1000 QPS  
- 模型权重文件总大小不可超过 20GB（含 tokenizer 和 config）；LoRA 适配器权重单独限制为 500MB  
- > **注意**：[模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 文档中提及支持 `GPU_TYPE: T4`，但当前生产环境仅开放 `A10` 和 `V100`，T4 尚未上线，该描述已过时。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


