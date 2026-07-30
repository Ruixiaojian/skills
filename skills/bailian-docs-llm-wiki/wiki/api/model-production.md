# model production

`model production` 是百炼平台中用于将模型投入实际应用的核心能力集合，涵盖模型微调、部署与服务化全流程。开发者可通过统一 API 管理模型从训练到上线的生命周期。该能力面向已通过模型接入审核的用户开放，需配合 `model` 权限策略使用。

## 支持的模型/功能

- **微调（Fine-tuning）**：支持基于 Base 模型（如 Qwen 系列）进行监督微调，适配特定任务（如客服问答、摘要生成）。仅限平台白名单内的基础模型，不支持自定义架构模型。  
- **部署（Deployment）**：支持将微调完成的模型或通过 [模型导入](../../raw/model-api-reference/model-production/import-models-api.md) 接入的模型，发布为 HTTP 可调用的在线推理服务。  
- **版本管理**：每个微调任务和部署实例均自动绑定唯一 ID 与版本号，支持灰度发布与回滚（详见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)）。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 基础模型 ID（如 `qwen2-7b`）或微调任务 ID（如 `ft-xxx`） |
| `training_file` | string | 微调必填 | 训练数据集 OSS 路径，格式为 JSONL，每行含 `messages` 字段 |
| `deployment_name` | string | 部署必填 | 全局唯一标识符，长度 3–32 字符，仅支持小写字母、数字与连字符 |
| `instance_type` | string | 否 | 默认 `gpu.2xlarge`；可选 `gpu.4xlarge` 或 `cpu.large`（CPU 实例仅支持部分轻量模型） |

> **注意**：文档 1 中未明确 `training_file` 格式要求，但 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 明确要求 JSONL 且必须含 `messages` 字段；而旧版文档曾允许 `prompt/completion` 格式，该格式已废弃，请以 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 为准。

## 使用方式

1. **微调流程**：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/fine_tunes \
     -H "Authorization: Bearer $API_KEY" \
     -d '{"model_id":"qwen2-7b","training_file":"oss://bucket/train.jsonl"}'
   ```

2. **部署流程**（需微调任务状态为 `succeeded`）：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/deployments \
     -H "Authorization: Bearer $API_KEY" \
     -d '{"model_id":"ft-abc123","deployment_name":"my-qa-bot"}'
   ```

3. **调用部署服务**：  
   使用返回的 `endpoint` 和 `api_key`，按标准 `/v1/chat/completions` 协议发起请求（兼容 OpenAI 格式）。

## 限制和注意事项

- 单个账号最多同时运行 5 个微调任务、10 个部署实例；超出需申请配额提升。  
- 微调任务最长运行时间 72 小时，超时自动终止且不退还 token；部署实例默认保留 90 天，过期后自动下线。  
- 所有微调数据在训练完成后自动清理，平台不持久化原始训练文件（参见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)）。  
- 部署服务不支持动态加载新权重；更新模型需新建部署或使用 `update_deployment` 接口替换 `model_id`（详见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)）。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


