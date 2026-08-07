# model production

model production 是百炼平台中用于将基础模型转化为可交付、可服务的定制化模型的一整套能力，涵盖微调训练与在线部署两个核心阶段。开发者可通过 API 或控制台完成端到端模型生命周期管理。该能力依赖于 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 和 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 两组独立但协同的接口。

## 支持的模型/功能

- **支持的模型类型**：仅限百炼平台官方托管的基础模型（如 Qwen 系列、Baichuan 系列），不支持用户自定义架构或本地 PyTorch 模型直接上传。
- **核心功能**：
  - 微调训练（Fine-tuning）：支持监督微调（SFT）、指令微调，输入为 JSONL 格式标注数据；
  - [模型部署](../concepts/model-deployment.md)：将微调完成的模型（或通过 `import_model` 导入的兼容格式模型）发布为 HTTP 推理服务；
  - 版本管理：每个微调任务生成唯一 `fine_tuning_job_id`，部署时需显式指定该 ID 或对应产出模型 ID。

> **注意**：文档中未明确说明是否支持 LoRA 微调权重的独立部署；实际使用中，[模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 接口要求传入完整模型 ID（即微调后已合并权重的模型），不接受仅传 LoRA adapter 的配置 —— 此行为与部分开源框架实践不同，请以 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 中 `merge_weights: true` 默认策略为准。

## 关键参数

| 参数 | 说明 | 必填 | 示例 |
|------|------|------|------|
| `model` | 基础模型标识符（如 `qwen2-7b-chat`） | ✅ | `"qwen2-7b-chat"` |
| `training_file` | 微调数据集文件 ID（由 `/files` 上传后获得） | ✅（微调时） | `"file-abc123"` |
| `n_epochs` | 训练轮数，默认 3 | ❌ | `5` |
| `deployment_name` | 部署服务名称（全局唯一，长度 3–32 字符） | ✅（部署时） | `"my-ft-qwen"` |
| `model_id` | 待部署模型 ID（来自微调任务 `fine_tuned_model_id` 或导入模型 ID） | ✅（部署时） | `"ft-qwen2-7b-xyz789"` |

## 使用方式

1. **微调启动**：调用 `POST /v1/fine_tuning/jobs`，传入 `model` 和 `training_file` 等参数，获取 `fine_tuning_job_id`；
2. **轮询状态**：通过 `GET /v1/fine_tuning/jobs/{job_id}` 查询 `status`，待变为 `succeeded` 后提取 `fine_tuned_model_id`；
3. **部署服务**：调用 `POST /v1/deployments`，传入 `deployment_name` 和上一步所得 `model_id`；
4. **调用推理**：使用 `POST /v1/chat/completions`，`model` 参数填写部署名称（如 `"my-ft-qwen"`）。

完整流程示例见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 与 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 文档中的 curl 示例。

## 限制和注意事项

- 单次微调任务最大训练数据量：2 GB（JSONL 行数建议 ≤ 50 万）；
- 每个账号最多同时运行 3 个微调任务；
- 部署服务默认 SLA 为 99.5%，但冷启动延迟（首次请求）可能达 30–60 秒，建议预热；
- 微调任务失败后，其关联临时模型不会自动清理，需手动调用 `DELETE /v1/models/{model_id}` 清理；
- > **注意**：[模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 文档中提及“支持 GPU 类型选择”，但当前 API 实际不接受 `gpu_type` 参数 —— 该字段已废弃，资源规格由 `model_id` 对应模型自动匹配，无需指定。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


