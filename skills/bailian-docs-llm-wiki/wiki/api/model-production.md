# model production

`model production` 是百炼平台中用于将训练/微调后的模型投入实际服务的关键流程，涵盖模型微调、部署及生命周期管理。它为开发者提供从定制化训练到高可用推理服务的端到端能力。该能力依托统一 API 接口，支持自动化编排与可观测性集成。

## 支持的模型与功能

- **微调（Fine-tuning）**：支持基于基础大模型（如 Qwen 系列）进行监督微调，适配垂类任务（如客服问答、合同解析）。  
- **部署（Deployment）**：支持将微调完成的模型或通过 [模型导入](../../raw/model-api-reference/model-production/import-models-api.md) 接入的第三方模型，发布为带弹性扩缩容、流量灰度和版本管理的在线推理服务。  
- **模型注册与版本控制**：每个微调作业产出唯一 `model_id`，可直接用于部署；部署时支持指定 `model_version` 实现多版本共存与回滚。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 微调作业成功后返回的模型唯一标识，见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 文档 |
| `instance_type` | string | 是 | 部署实例规格（如 `ecs.c7.large`），需匹配模型显存需求；不支持动态降配 |
| `replicas` | integer | 否 | 初始副本数，默认为 `1`；支持后续通过 `PATCH /deployments/{id}` 调整 |
| `traffic_split` | object | 否 | 灰度发布配置，格式为 `{ "v1": 80, "v2": 20 }`，单位为百分比 |

> **注意**：文档 2 中称“支持导入模型部署”，但当前 API 实际仅接受 `model_id`（即必须源自平台内微调或官方模型库），不支持任意本地模型文件直传。该差异已在 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 的 v2.3 版本注释中修正，旧版文档未同步更新。

## 使用方式

1. **启动微调**：调用 `POST /fine_tuning_jobs` 提交数据集与超参，轮询 `status` 字段直至变为 `succeeded`，提取响应中的 `model_id`。  
2. **创建部署**：使用上一步的 `model_id`，调用 `POST /deployments` 并指定 `instance_type` 与 `replicas`。  
3. **验证服务**：部署就绪（`status == "running"`）后，通过返回的 `endpoint` 发起 `POST /v1/chat/completions` 请求测试。

完整示例与错误码详见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 和 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 原文。

## 限制和注意事项

- 单次微调作业最长运行时限为 72 小时；超时自动终止，状态置为 `failed`。  
- 每个部署最多绑定 5 个不同 `model_version`（含主版本），超出需先删除旧版本。  
- 部署实例类型一旦创建不可变更，如需升级硬件，须重建部署。  
- 微调数据集最大体积为 10 GB（压缩后），且仅支持 `.jsonl` 格式，字段名必须为 `messages` 或 `prompt`/`completion` —— 具体约束请参考 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


