# model production

`model production` 是百炼平台中用于将模型投入实际应用的核心能力集合，涵盖从微调训练到在线服务部署的完整生命周期。开发者可通过 API 或控制台完成模型定制与发布，适用于私有化模型迭代与业务集成场景。该能力依赖于底层计算资源调度与模型服务框架协同工作。

## 支持的模型/功能

- **微调训练（Fine-tuning）**：支持基于基础大模型（如 Qwen 系列）进行监督微调，适配垂直领域任务（如客服问答、金融报告生成）。  
- **模型部署（Deployment）**：支持将微调完成的模型或通过 `import_model` 导入的第三方模型，一键发布为 HTTP 可调用的在线推理服务。  
- **版本管理**：每个微调任务和部署实例均自动关联唯一 ID 与版本号，便于灰度发布与回滚。  
> **注意**：文档中未明确说明是否支持 LoRA 微调以外的参数高效方法；实际使用请参考 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 中的 `training_type` 参数定义。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `model_id` | 基础模型标识符（如 `qwen2-7b-instruct`）或已微调模型 ID | `"qwen2-7b-instruct"` |
| `training_type` | 微调类型，当前仅支持 `"full"` 和 `"lora"`（见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)） | `"lora"` |
| `endpoint_name` | 部署后服务的唯一域名前缀，全局唯一 | `"my-qa-service"` |
| `instance_type` | 推理实例规格，影响并发与延迟（详见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)） | `"ecs.gn7i-c16g1.4xlarge"` |

## 使用方式

1. **发起微调任务**：调用 `POST /api/v1/fine_tuning_jobs`，传入训练数据集 URL、`model_id` 和 `training_type`；任务状态轮询 `GET /api/v1/fine_tuning_jobs/{job_id}`。  
2. **部署模型**：微调成功后，获取输出的 `fine_tuned_model_id`，调用 `POST /api/v1/deployments` 提交部署请求。  
3. **调用服务**：部署成功后，通过返回的 `endpoint_url` 发送 `POST /v1/chat/completions` 请求（兼容 OpenAI 格式）。

## 限制和注意事项

- 单次微调任务最大训练时长为 72 小时，超时自动终止；数据集大小上限为 10 GB（[模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)）。  
- 每个账号默认最多同时运行 5 个部署实例，超出需提工单扩容（[模型部署](../../raw/model-api-reference/model-production/deployments-api.md)）。  
- 微调任务不支持跨区域迁移；部署实例一旦创建，其 `instance_type` 不可变更，需重建部署。  
> **注意**：两篇原始文档均未提及模型格式兼容性要求（如是否支持 GGUF、AWQ 等量化格式），实际导入前请确认模型已按百炼规范转换并验证加载。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


