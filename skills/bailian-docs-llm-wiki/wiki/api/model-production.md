# model production

model production 是百炼平台中用于将训练/微调完成的模型转化为可调用在线服务的核心能力，涵盖模型部署与微调作业管理两大功能模块。它面向开发者提供标准化 API 接口，支持从训练到上线的端到端流程。所有操作均需通过 RESTful API 完成，不提供控制台可视化部署入口。

## 支持的模型/功能

- **模型部署**：支持将已完成微调（fine-tuning）或通过 [模型导入](../../raw/model-api-reference/model-production/import-models-api.md) 的模型发布为 HTTP 可调用的在线推理服务；  
- **模型调优**：支持基于基础模型启动微调任务，使用用户私有数据优化模型行为，详见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)；  
- **模型生命周期管理**：包括创建、查询、删除部署实例及微调作业，但**不支持**对已部署服务进行热更新或参数动态调整。

> **注意**：[模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 文档未明确说明是否支持导入模型的直接部署，而 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 中提及“微调后模型可自动进入部署就绪状态”，二者逻辑衔接存在隐含假设，建议以部署 API 实际响应为准。

## 关键参数

| 参数 | 说明 | 必填 | 示例 |
|------|------|------|------|
| `model` | 模型标识符（如 `qwen2-7b-chat` 或微调生成的 `ft-xxx` ID） | 是 | `"ft-abc123"` |
| `name` | 部署服务名称（全局唯一，仅限字母、数字、连字符） | 是 | `"my-qwen-finetuned"` |
| `scale_type` | 扩缩容类型：`auto`（自动）或 `manual` | 否，默认 `auto` | `"manual"` |
| `instance_count` | 手动扩缩时指定实例数（`scale_type=manual` 时必填） | 条件必填 | `2` |

## 使用方式

1. **启动微调**：调用 `POST /fine_tuning_jobs` 创建微调任务（参考 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)）；  
2. **等待完成**：轮询 `GET /fine_tuning_jobs/{id}` 直至 `status == "succeeded"`，获取输出模型 ID；  
3. **部署模型**：使用该模型 ID 调用 `POST /deployments` 创建服务（参考 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)）；  
4. **调用服务**：通过返回的 `endpoint` 发送 `POST /v1/chat/completions` 请求（需携带 `Authorization: Bearer <api_key>`）。

## 限制和注意事项

- 单个账号最多同时运行 5 个活跃部署（`status == "running"`），超出需先删除闲置部署；  
- 微调作业最长运行时限为 72 小时，超时自动终止且不计费；  
- 部署服务默认启用自动扩缩容，但最小实例数固定为 1，不可设为 0（即无法完全暂停）；  
- > **注意**：两篇原始文档均未提及 GPU 类型选择能力，实际部署时实例规格由模型大小自动匹配，开发者无法显式指定 `gpus_per_instance` 等参数——该行为与部分旧版 SDK 文档描述冲突，以当前 API 响应为准。

## 来源文档

- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)


