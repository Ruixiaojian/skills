# model production

`model production` 是百炼平台中用于将模型投入实际应用的核心能力集合，涵盖从微调训练到在线服务部署的完整生命周期。开发者可通过 API 或控制台完成模型定制与发布，支持快速迭代和灰度发布。该能力依赖于底层计算资源调度与版本化管理机制。

## 支持的模型/功能

- **微调训练（Fine-tuning）**：支持基于预训练大模型（如 Qwen 系列）进行监督微调，适配特定任务（如客服对话、金融问答）。训练数据需为 JSONL 格式，每条样本包含 `messages` 字段（[模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)）。
- **模型部署（Deployment）**：支持将微调完成的模型或通过 `import_model` 接口导入的第三方模型（如 Hugging Face 格式）部署为 HTTP 可调用的在线推理服务，提供自动扩缩容与健康检查（[模型部署](../../raw/model-api-reference/model-production/deployments-api.md)）。
- **版本管理**：每个微调任务生成唯一 `fine_tuning_job_id`，对应产出模型版本；部署时需显式指定 `model_version_id`，确保可追溯性。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_model` | 微调所基于的基座模型 ID | `"qwen2-7b"` |
| `training_file_id` | 训练数据文件 ID（需先通过 `/files/upload` 上传） | `"file_abc123"` |
| `deployment_name` | 部署服务唯一标识符，全局唯一且不可修改 | `"prod-faq-v2"` |
| `instance_type` | 推理实例规格，影响并发与延迟 | `"gpu.2xlarge"` |

> **注意**：文档 1 中未明确 `base_model` 的可选值范围，而文档 2 的 `/deployments` 接口文档（见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)）补充了 `qwen2-7b`、`qwen2-57b` 和 `llama3-8b` 三类已验证支持型号，建议以该文档为准。

## 使用方式

1. **微调流程**：  
   - 上传训练数据 → 创建微调任务（`POST /fine_tuning/jobs`）→ 轮询 `status` 直至 `succeeded` → 获取产出 `model_version_id`  
2. **部署流程**：  
   - 调用 `POST /deployments`，传入 `model_version_id`、`deployment_name` 与 `instance_type` → 等待 `status: "ready"` → 使用 `endpoint_url` 发起推理请求  

所有操作均需携带 `Authorization: Bearer <api_key>`，且请求体必须为 `application/json`。

## 限制和注意事项

- 单次微调任务最大训练时长为 72 小时，超时自动终止；若需更长训练周期，须拆分为多阶段微调（[模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)）。
- 每个部署服务默认最大并发请求数为 100，超出后返回 `429 Too Many Requests`；可通过工单申请提升配额。
- 微调任务一旦提交不可取消或修改参数；部署服务删除后，关联模型版本仍保留在仓库中，但无法再被部署（除非重新创建同名 deployment）。
- > **注意**：文档 1 声称“支持任意开源模型微调”，但文档 2 明确限定仅支持平台预置基座模型（见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)），自定义基座模型暂不支持部署，此为关键兼容性约束。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


