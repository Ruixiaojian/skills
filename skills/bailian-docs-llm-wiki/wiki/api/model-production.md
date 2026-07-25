# model production

`model production` 是百炼平台中用于将训练/微调后的模型投入实际使用的功能模块，涵盖模型微调、部署及服务化全流程。它提供标准化 API 接口，支持从训练任务管理到在线推理服务的端到端控制。开发者可通过 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 和 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 两个核心子系统协同完成生产就绪。

## 支持的模型/功能

- **微调（Fine-tuning）**：支持基于百炼托管基座模型（如 Qwen 系列）启动监督微调任务，输入格式为 JSONL 格式指令数据集。
- **部署（Deployment）**：支持将以下两类[模型部署](../concepts/model-deployment.md)为 HTTP 可调用的在线服务：
  - 通过 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 完成的微调模型；
  - 已导入平台的自定义模型（需符合 ONNX 或 Hugging Face 格式规范，详见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)）。

> **注意**：文档 1 未明确说明是否支持导入模型的微调，而文档 2 明确将“导入的模型”列为部署来源之一；当前平台实际仅允许对百炼原生基座模型及其微调产物进行部署，导入模型暂不支持微调——该差异表明文档 1 的描述存在信息缺失，应以 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 中的部署约束为准。

## 关键参数

| 参数 | 说明 | 是否必需 | 示例 |
|------|------|----------|------|
| `model_id` | 微调任务中指定的基座模型 ID（如 `qwen2-7b-instruct`）或微调产出模型 ID（格式为 `ft-xxx`） | 是（部署时） | `ft-abc123` |
| `training_file` | 微调任务上传的数据集文件 ID（由 `/files/upload` 接口返回） | 是（微调创建时） | `file-xyz789` |
| `endpoint_name` | 部署后生成的唯一服务域名前缀（全局唯一，长度 3–32 字符，仅含小写字母、数字、短横线） | 是 | `my-qa-bot` |

## 使用方式

1. **启动微调**：调用 `POST /v1/fine_tuning/jobs`，传入 `model_id` 和 `training_file`，获取 `job_id`；
2. **轮询状态**：调用 `GET /v1/fine_tuning/jobs/{job_id}`，待状态变为 `succeeded` 后提取 `fine_tuned_model` 字段值；
3. **部署模型**：调用 `POST /v1/deployments`，传入 `model_id`（即上步所得 `fine_tuned_model`）与 `endpoint_name`；
4. **调用服务**：部署成功后，使用 `https://<endpoint_name>.api.bailian.aliyun.com/v1/chat/completions` 发起推理请求。

## 限制和注意事项

- 单个微调任务最大训练时长为 72 小时，超时自动终止；
- 每个账号最多同时运行 5 个微调任务，最多创建 20 个活跃部署（`status=active`）；
- 微调产出模型仅可在创建该任务的 Region 内部署，跨 Region 部署需重新微调或使用模型导出/导入流程；
- > **注意**：文档 1 未提及微调任务失败后的重试机制与错误码说明，而 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 明确列出 `422 Unprocessable Entity` 等常见响应码；建议开发者在集成时优先参考部署文档中的错误处理章节，并结合微调任务的 `error_code` 字段做容错。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


