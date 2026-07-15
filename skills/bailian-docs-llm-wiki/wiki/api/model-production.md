# model production

`model production` 是百炼平台中用于将模型投入实际应用的核心能力集合，涵盖从微调训练到在线服务部署的完整生命周期。开发者可通过 API 管理微调任务与部署实例，实现模型的定制化与规模化交付。该能力依赖于统一的模型标识（`model_id`）和资源隔离机制，适用于业务场景下的迭代演进。

## 支持的模型与功能

- **微调训练**：支持基于 Base Model（如 Qwen 系列）启动监督微调（SFT）任务，输入格式为标准 JSONL，支持 LoRA 等轻量适配方式 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)  
- **模型部署**：支持将微调完成的模型或通过 `import_model` 导入的第三方模型部署为 HTTP 推理服务，提供自动扩缩容、版本灰度、流量切分等生产级能力 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)  
- **功能边界**：当前不支持直接对已部署服务执行热更新或参数重载；模型版本变更需通过新建部署或蓝绿切换实现。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `model_id` | 唯一模型标识，微调任务输出或导入后生成 | `ft-qwen2-7b-20240501-123456` |
| `deployment_name` | 部署实例名称，全局唯一且不可修改 | `prod-chat-v2` |
| `instance_type` | 推理实例规格，影响并发与延迟 | `gpu.2xlarge`（仅限部署） |
| `training_type` | 微调类型，当前仅支持 `sft` | `sft`（仅限微调） |

> **注意**：文档中未明确 `instance_type` 的可选枚举值范围，实际使用请以 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 中最新 `GET /v1/deployments/instance-types` 接口返回为准；部分旧文档示例仍列出已下线的 `cpu.small` 类型，属过时信息。

## 使用方式

1. **微调流程**：  
   - 调用 `POST /v1/fine_tuning/jobs` 提交训练任务，指定 `base_model_id`、训练数据集 ID 及超参  
   - 监听 `status` 字段（`queued` → `running` → `succeeded`），成功后获取输出 `model_id`  

2. **部署流程**：  
   - 调用 `POST /v1/deployments`，传入上一步得到的 `model_id` 及 `deployment_name`  
   - 部署就绪后，通过 `endpoint_url` 发起推理请求（如 `POST https://<endpoint>/v1/chat/completions`）  

完整交互链路详见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 与 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 的 API 规范。

## 限制和注意事项

- 单个微调任务最大训练时长为 72 小时，超时将被强制终止  
- 每个 `deployment_name` 在同一 Region 下全局唯一，重名请求返回 `409 Conflict`  
- 微调任务不支持跨 Region 复制；部署实例必须与模型所在 Region 一致  
- 模型部署后，其底层 `model_id` 不可变更——若需替换模型，须新建部署或删除重建  
- 免费试用额度仅覆盖微调计算资源，部署实例按实际 GPU 小时计费

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


