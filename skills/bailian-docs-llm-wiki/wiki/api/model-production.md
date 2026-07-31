# model production

model production 是百炼平台中用于将基础模型转化为可交付业务价值的关键流程，涵盖模型微调、部署及生命周期管理。开发者可通过 API 或控制台完成端到端的模型定制与服务化。该能力聚焦于生产就绪性，强调稳定性、可观测性和资源可控性。

## 支持的模型/功能

- 支持对百炼托管的基础模型（如 Qwen 系列）进行监督微调（Supervised Fine-tuning），生成专属版本；
- 支持将微调完成的模型或通过 [模型导入](../../raw/model-api-reference/model-production/import-models-api.md) 接入的第三方[模型部署](../concepts/model-deployment.md)为 HTTP 推理服务；
- 提供部署实例的弹性扩缩容、流量灰度、版本回滚等生产级运维能力。

## 关键参数

- `model_id`：微调任务或部署任务所关联的模型唯一标识（格式如 `qwen2-7b-chat-finetuned-xxx`）；
- `training_type`：微调类型，当前仅支持 `supervised_fine_tuning`（见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)）；
- `instance_type`：部署实例规格，如 `gpu.g1.2xlarge`，需与模型显存需求匹配；
- `replicas`：部署副本数，最小值为 1，最大值受项目配额限制。

> **注意**：文档中未明确说明 `training_type` 是否支持 `reward_modeling` 或 `dpo`，但 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 当前仅列出 `supervised_fine_tuning`，其他类型暂不可用。

## 使用方式

1. **微调模型**：调用 `/v1/fine_tuning_jobs` 创建微调任务，指定训练数据集、超参和 `base_model_id`；
2. **验证与导出**：任务完成后，通过 `/v1/fine_tuning_jobs/{job_id}` 获取产出模型 ID；
3. **部署服务**：使用该模型 ID 调用 `/v1/deployments` 创建部署，配置 `instance_type` 和 `replicas`；
4. **调用推理**：部署成功后，通过 `/v1/deployments/{deployment_id}/chat/completions` 发起在线请求。

完整流程示例详见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 中的“快速开始”章节。

## 限制和注意事项

- 微调任务最长运行时间为 72 小时，超时自动终止；
- 单次部署最多支持 10 个副本，超出需提工单申请配额扩容；
- 部署状态为 `running` 后方可接收请求；若状态为 `failed`，需检查日志并修正 `instance_type` 或模型兼容性问题；
- 微调产出模型仅可在同一项目内直接部署，跨项目使用需先执行模型导出与导入（参见 [模型导入](../../raw/model-api-reference/model-production/import-models-api.md)）。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


