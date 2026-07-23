# model production

`model production` 是百炼平台中用于将训练/微调后的模型投入实际服务的关键流程，涵盖模型微调、部署及生命周期管理。它为开发者提供从定制化训练到高可用推理服务的端到端能力。该能力依托统一 API 接口，支持自动化编排与可观测性集成。

## 支持的模型与功能

- **微调（Fine-tuning）**：支持基于基础大模型（如 Qwen 系列）进行监督微调，适配垂类任务（如客服问答、合同解析）。  
- **部署（Deployment）**：支持将微调完成的模型或通过 [模型导入](../../raw/model-api-reference/model-production/import-models-api.md) 接入的第三方模型，发布为带弹性扩缩容、流量灰度和版本管理的在线推理服务。  
- **模型注册与版本控制**：每个微调任务产出唯一 `model_id`，可被多次部署为不同环境（staging/prod）的独立 `deployment_id`。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_model` | 微调所基于的基础模型 ID | `qwen2-7b-instruct` |
| `training_file` | 训练数据集对象 ID（需先通过文件上传 API 上传） | `file-abc123` |
| `deployment_name` | 部署服务名称，全局唯一且不可修改 | `prod-qa-service-v2` |
| `instance_type` | 推理实例规格（影响并发与延迟） | `ecs.gn7i-c8g1.2xlarge` |

> **注意**：文档 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 中提及的 `autoscale_min_instances` 默认值为 `1`，但最新 SDK v3.2+ 已调整为 `0`（支持冷启缩容），请以 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 的 OpenAPI Schema 为准。

## 使用方式

1. **微调模型**：调用 `POST /v1/fine_tuning/jobs`，传入 `base_model` 和 `training_file`；任务状态轮询 `GET /v1/fine_tuning/jobs/{job_id}`，成功后获取 `fine_tuned_model` 字段值（即新模型 ID）。  
2. **部署模型**：调用 `POST /v1/deployments`，指定上一步得到的 `model_id` 及 `instance_type` 等参数。  
3. **调用服务**：使用返回的 `deployment_id` 构造推理 endpoint（格式：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation?deployment_id={deployment_id}`），并按 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 规范传入请求体。

## 限制和注意事项

- 单次微调任务最长运行时间为 72 小时；超时自动终止，不产生费用。  
- 同一 `model_id` 最多可同时存在 5 个活跃部署（`status=active`），超出需先停用旧部署。  
- 微调数据集大小上限为 100 MB（压缩后），且仅支持 JSONL 格式，字段必须包含 `messages` 数组（遵循 OpenAI ChatML 协议）。  
- **重要**：微调任务一旦提交不可取消或修改；若需中止，请直接删除对应 job（调用 `DELETE /v1/fine_tuning/jobs/{job_id}`），但已产生的计算资源费用仍会计费至任务结束时刻。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


