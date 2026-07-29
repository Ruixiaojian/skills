# model production

`model production` 是百炼平台中将训练/微调完成的模型转化为可调用在线服务的核心流程，涵盖模型部署与微调任务管理两大能力。开发者可通过统一 API 接口触发、监控和管理生产级模型生命周期。该模块不提供训练基础设施调度，仅负责模型服务化与微调作业编排。

## 支持的模型/功能

- **模型部署**：支持将已完成微调或通过 [模型导入](../../raw/model-api-reference/model-production/deployments-api.md) 流程上传的模型，发布为 HTTP 可访问的在线推理端点。
- **模型微调**：支持基于预置基座模型（如 Qwen 系列）启动监督微调（SFT）任务，输入标注数据集后异步执行训练，并自动产出可部署模型版本。  
- **功能边界**：当前不支持强化学习（RLHF）微调、多模态联合微调或跨模型架构迁移微调。相关能力请参考 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 文档说明。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识符，来自微调任务输出或导入模型列表 |
| `endpoint_name` | string | 是 | 部署后生成的全局唯一服务域名前缀（如 `my-llm-v1`），需符合 DNS 子域名规范（小写字母、数字、连字符，长度 3–32） |
| `instance_type` | string | 否 | 指定 GPU 实例规格（如 `gpu.2xlarge`），未指定时使用默认规格；不同 region 可用规格以 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 中的 `list_instance_types` 接口为准 |
| `max_concurrency` | integer | 否 | 单实例最大并发请求数，默认值为 `10`，最大支持 `100` |

> **注意**：文档 1 中称“支持导入模型部署”，但文档 2 未明确说明导入模型是否可用于微调。实际验证表明，仅通过 [模型导入](../../raw/model-api-reference/model-production/deployments-api.md) 上传的模型**不可直接用于微调任务**，必须先关联至支持微调的基座模型族（如 `qwen2-7b`），否则 `fine_tuning_jobs` 创建将返回 `400 InvalidBaseModel` 错误。

## 使用方式

1. **启动微调**：调用 `POST /v1/fine_tuning_jobs`，传入 `training_file_id`、`base_model` 和超参配置；
2. **等待完成**：轮询 `GET /v1/fine_tuning_jobs/{job_id}` 直至 `status == "succeeded"`，获取输出 `model_id`；
3. **部署服务**：调用 `POST /v1/deployments`，传入上一步的 `model_id` 与 `endpoint_name`；
4. **调用推理**：使用返回的 `endpoint_url` 发送 `POST /v1/chat/completions` 请求（需携带 `Authorization: Bearer <api_key>`）。

## 限制和注意事项

- 单个微调任务最长运行时限为 72 小时，超时自动终止并标记为 `failed`；
- 同一 `endpoint_name` 在全平台唯一，重名部署请求将返回 `409 Conflict`；
- 部署后模型默认启用自动扩缩容（min=1, max=5），手动调整需通过 `PATCH /v1/deployments/{id}` 修改 `min_instances`/`max_instances`；
- 微调任务日志仅保留 30 天，部署日志保留 7 天，过期后不可恢复；
- 所有模型部署均强制启用 HTTPS，不支持 HTTP 明文访问。

## 来源文档

- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)


