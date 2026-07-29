# model production

`model production` 是百炼平台中用于将训练/微调完成的模型投入实际推理服务的关键流程，涵盖模型部署与微调作业管理两大核心能力。开发者可通过统一 API 接口完成从训练到上线的闭环操作。该模块不提供训练数据托管或自动超参搜索，仅聚焦于生产就绪模型的生命周期管理。

## 支持的模型/功能

- **模型部署**：支持将已微调（fine-tuned）或手动导入的模型发布为 HTTP 可调用的在线推理服务，具备自动扩缩容与健康检查能力 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)  
- **微调作业管理**：支持创建、查询、终止微调任务，可指定基础模型、训练数据集、超参配置等；微调完成后模型自动进入待部署状态 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)  
- **不支持**：零样本/少样本即时推理（需调用 `inference` 模块）、模型权重直接下载、跨区域模型复制

## 关键参数

| 参数 | 说明 | 必填 | 示例 |
|------|------|------|------|
| `model_id` | 微调后生成的唯一模型 ID（如 `ft-xxx`）或导入模型 ID | 是 | `ft-abc123` |
| `deployment_name` | 部署服务的唯一标识符，全局唯一 | 是 | `prod-qa-bot-v2` |
| `instance_type` | 推理实例规格（`gpu.t4.1x` / `gpu.a10.2x` 等） | 是 | `gpu.a10.2x` |
| `max_concurrency` | 单实例最大并发请求数（1–100） | 否，默认 10 | `50` |

> **注意**：文档 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 中提及 `instance_type` 支持 `cpu.small`，但当前 API 实际返回 `400 Unsupported instance type` 错误；该参数仅接受 GPU 规格，CPU 类型已下线，请以 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 中“部署兼容性说明”附录为准。

## 使用方式

1. **启动微调**：调用 `POST /v1/fine_tuning_jobs` 提交训练任务  
2. **等待完成**：轮询 `GET /v1/fine_tuning_jobs/{job_id}` 直至 `status == "succeeded"`，获取输出 `model_id`  
3. **部署模型**：调用 `POST /v1/deployments`，传入 `model_id` 与 `deployment_name` 等参数  
4. **调用服务**：使用返回的 `endpoint_url` 发起 `POST /v1/chat/completions` 请求（需携带 `Authorization: Bearer <token>`）

完整示例见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 的「快速开始」章节。

## 限制和注意事项

- 单个账号最多同时运行 5 个活跃部署（`status == "running"`），超出需先删除闲置部署  
- 微调作业最长运行时限为 72 小时，超时自动终止且不计费  
- 部署服务启动后不可修改 `instance_type` 或 `max_concurrency`，如需调整须先 `DELETE /v1/deployments/{name}` 再重建  
- 所有部署默认启用 TLS 1.2+，不支持 HTTP 明文访问  
- 模型 ID 一旦部署成功即绑定至该 deployment，不可复用至其他 deployment 名称

## 来源文档

- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)


