# model production

`model production` 是百炼平台中用于将训练/微调后的模型投入实际推理服务的关键流程，涵盖模型微调、部署及生命周期管理。它面向开发者提供标准化 API 接口，支持从定制化训练到高可用服务的端到端交付。该能力依赖于底层模型服务基础设施，需配合 `model` 和 `endpoint` 资源协同使用。

## 支持的模型/功能

- **微调（Fine-tuning）**：支持基于 Base Model（如 Qwen 系列）启动监督微调任务，适配下游任务（如分类、指令遵循）。微调结果生成新版本模型 ID，可用于后续部署。
- **部署（Deployment）**：支持将微调完成的模型或直接导入的兼容格式模型（如 GGUF、Safetensors）发布为 HTTP 可调用的在线推理 endpoint。
- **版本管理**：每个微调任务产出唯一 `fine_tuning_job_id`，对应一个 `model_id`；每个部署绑定一个 `model_id` 与 `endpoint_id`，支持灰度发布与版本回滚。

> **注意**：文档中未明确说明是否支持 LoRA 微调权重的独立部署；当前 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 要求部署对象为完整模型快照，而非增量权重 —— 若需 LoRA 推理，请参考 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 中 `merge_lora` 参数行为。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 微调完成后的模型 ID（如 `ft-qwen2-7b-20240510-123456`），或已导入的模型 ID |
| `endpoint_name` | string | 是 | 部署服务的唯一标识符，需全局唯一，符合 DNS 子域名规范（小写字母/数字/连字符） |
| `instance_type` | string | 是 | 实例规格，如 `ecs.gn7i-c16g1.4xlarge`（GPU）或 `ecs.c7.large`（CPU），详见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 支持列表 |
| `max_concurrency` | integer | 否 | 每实例最大并发请求数，默认值由 `instance_type` 决定 |

## 使用方式

1. **启动微调**：调用 `/v1/fine_tuning/jobs` 创建任务，指定 `training_file_id`、`base_model` 和 `hyperparameters`；
2. **等待完成**：轮询 `GET /v1/fine_tuning/jobs/{job_id}` 直至 `status == "succeeded"`，提取返回中的 `fine_tuned_model` 字段作为 `model_id`；
3. **创建部署**：调用 `/v1/deployments`，传入上一步获得的 `model_id` 及所需 `instance_type` 等参数；
4. **调用推理**：使用返回的 `endpoint_url` 发送 `POST /v1/chat/completions` 请求（需携带 `Authorization: Bearer <api_key>`）。

完整流程示例见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 与 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 的 Quick Start 章节。

## 限制和注意事项

- 单个微调任务最长运行时间为 72 小时，超时自动终止；
- 每个 `model_id` 最多关联 5 个 active deployment，超出需先删除旧 deployment；
- 部署后模型不可修改；若需更新，须新建微调任务并部署新 `model_id`；
- 免费试用额度不覆盖 GPU 实例部署费用，生产环境部署需确保账户已开通计费权限。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


