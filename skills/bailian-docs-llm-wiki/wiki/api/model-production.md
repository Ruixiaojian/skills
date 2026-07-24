# model production

model production 是百炼平台中用于将基础模型转化为可交付、可服务的定制化模型的一整套能力，涵盖微调训练与在线部署两个核心阶段。开发者可通过 API 或控制台完成模型的定制化训练与服务化发布。该流程依赖于统一的模型生命周期管理机制，确保训练与部署环节的参数一致性与版本可追溯性。

## 支持的模型/功能

- **微调训练**：支持对百炼托管的基础模型（如 Qwen 系列）进行监督微调（Supervised Fine-tuning），适配下游任务（如分类、摘要、指令遵循）。详见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)。
- **模型部署**：支持将微调完成的模型或通过 `import_model` 接口导入的第三方模型（需符合 ONNX 或百炼自定义格式）部署为 HTTP 可调用的在线推理服务。详见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)。
- **功能边界**：当前不支持强化学习微调（RLHF）、多模态模型微调，也不支持跨架构迁移（如将 Llama 模型微调后部署为 Qwen 格式服务）。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `model_id` | 微调或部署所基于的基础模型 ID（必须为百炼平台已注册模型） | `qwen2-7b-chat` |
| `training_job_id` | 微调任务唯一标识，部署时需显式引用该 ID 以保证模型版本一致 | `ftjob_abc123` |
| `instance_type` | 部署实例规格，影响并发与延迟；仅限白名单规格（如 `ecs.gn7i-c8g1.2xlarge`） | `ecs.gn7i-c8g1.2xlarge` |
| `max_concurrency` | 单实例最大并发请求数，超出将触发自动扩缩容（需开启弹性伸缩） | `10` |

> **注意**：文档 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 中提及 `learning_rate` 为必填参数，但实际 API 已默认提供启发式推荐值；若显式传入非推荐范围（如 `1e-2`），将导致训练失败——该细节在 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 的“前置条件”章节未同步更新，以本节为准。

## 使用方式

1. **微调启动**：调用 `POST /api/v1/fine_tuning_jobs`，传入训练数据集 ID、`model_id` 和超参配置；
2. **状态轮询**：通过 `GET /api/v1/fine_tuning_jobs/{job_id}` 查询 `status` 字段（`succeeded` 表示就绪）；
3. **部署发布**：调用 `POST /api/v1/deployments`，指定 `base_model_id` 和 `training_job_id`（若基于微调模型），或 `imported_model_id`（若为导入模型）；
4. **调用服务**：部署成功后，使用返回的 `endpoint_url` 发起 `POST /v1/chat/completions` 请求（兼容 OpenAI 格式）。

## 限制和注意事项

- 微调任务最长运行时间为 72 小时，超时自动终止且不退还算力配额；
- 单个账号最多同时运行 5 个微调任务、10 个部署实例；
- 部署服务默认启用 TLS 1.2+ 加密，但**不支持自定义域名绑定**（该能力计划于 Q3 上线，当前仅支持平台分配的 `*.bailian.aliyuncs.com` 域名）；
- 所有微调产出模型仅保留 90 天，过期后不可再部署（除非重新训练）——该策略在 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 中未明确说明，但已在 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 的“模型版本有效性”小节注明。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


