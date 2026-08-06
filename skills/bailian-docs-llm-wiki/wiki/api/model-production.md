# model production

`model production` 是百炼平台中用于将模型投入实际应用的核心能力集合，涵盖从微调训练到在线服务部署的完整生命周期。开发者可通过 API 或控制台完成模型定制与发布，适用于业务场景适配与规模化推理需求。该能力依赖于底层模型服务基础设施，需配合对应权限与资源配额使用。

## 支持的模型/功能

- **微调训练（Fine-tuning）**：支持对百炼托管的基础大模型（如 Qwen 系列）进行监督微调，适配垂直领域任务；训练数据需为 JSONL 格式，支持 LoRA 等轻量适配方法。  
- **模型部署（Deployment）**：支持将微调完成的模型或通过 [模型导入](../../raw/model-api-reference/model-production/import-models-api.md) 接入的第三方模型，发布为 HTTP 可调用的在线推理服务。  
- **版本管理与灰度发布**：每个部署可维护多版本，支持按流量比例灰度切流，详见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 文档。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `model_id` | 微调任务或部署所引用的模型唯一标识（如 `qwen2-7b-chat-hf` 或微调生成的 `ft-xxx`） | `ft-abc123` |
| `instance_type` | 部署实例规格，影响并发与延迟；必须与模型显存需求匹配 | `gpu-a10-2x` |
| `max_concurrency` | 单实例最大并发请求数，超限触发排队或拒绝 | `10` |
| `training_type`（仅微调） | 指定微调方式，当前仅支持 `lora` | `lora` |

> **注意**：文档 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 中提及“支持全参数微调”，但实际 API 已下线该能力，仅保留 LoRA；请以 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 中的 `instance_type` 兼容性列表为准，避免因规格不匹配导致部署失败。

## 使用方式

1. **微调流程**：提交训练数据 → 调用 `/fine_tuning_jobs` 创建任务 → 监听 `status=completed` → 获取输出模型 ID  
2. **部署流程**：调用 `/deployments` 创建部署 → 指定 `model_id` 和 `instance_type` → 等待 `status=ready` → 使用返回的 `endpoint_url` 发起推理请求  
3. 所有操作均需携带 `Authorization: Bearer <token>`，且 `project_id` 必须在请求头中显式声明。

## 限制和注意事项

- 微调任务最长运行时间为 72 小时，超时自动终止；训练数据大小上限为 500 MB。  
- 单个部署默认最多 5 个活跃版本；历史版本保留 30 天后自动清理。  
- 部署实例启动后不可变更 `instance_type`，如需升级需重建部署；详情见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)。  
- 微调输出模型仅可在同一项目内直接部署，跨项目使用需先执行模型导出与导入操作。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


