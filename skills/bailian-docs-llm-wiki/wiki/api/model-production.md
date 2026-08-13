# model production

`model production` 指在百炼平台将训练/微调完成的模型部署为可稳定、可计量、可扩缩的在线推理服务的能力，核心支撑 TPM 预留（容量保障）与通用 PTU v2 部署两类生产模式。当前仅 TPM 预留场景提供完整的全生命周期 OpenAPI 管理能力，包括创建、扩缩容、续订、溢出策略调整等；通用模型部署（如微调后模型上线）暂未开放对应 API 文档 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)。开发者需通过 DashScope OpenAPI 调用，认证方式、参数约束与区域限制均需严格遵循规范。

## 支持的模型与功能

- **支持模型（TPM 预留）**：华北2（北京）区域支持 `qwen-max`（即千问3.8-Max）、`qwen-plus-2026-05-26`（千问3.7-Plus-2026-05-26）、`qwen-flash-2026-04-16`（千问3.6-Flash-2026-04-16）、`glm-5.2`、`glm-5.1`、`deepseek-v4-flash`、`deepseek-v4-pro`、`kimi-k2.6`；新加坡区域不支持 `kimi-k2.6`，其余一致。
- **深度思考支持**：上述全部 9 款模型均支持 `thinking_output_tpm` 配额，启用方式详见 [深度思考模型](https://help.aliyun.com/zh/model-studio/deep-thinking)，具体步长与起跑值以控制台创建页实时展示为准。
- **功能覆盖**：提供创建（`POST /api/v1/deployments`）、单/列表查询（`GET /api/v1/deployments/{id}` / `GET /api/v1/deployments`）、扩缩容（`PUT /api/v1/deployments/{id}/scale`）、续订（`PUT /api/v1/deployments/{id}/renew`）、溢出策略修改（`PUT /api/v1/deployments/{id}/updateOverflowStrategy`）共六类 REST 接口，完整覆盖 TPM 预留部署生命周期管理 [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)。

> **注意**：文档 2《模型部署》仅声明“将微调或导入的模型部署为在线推理服务”，但未提供任何 API 细节、参数或示例；文档 3《模型调优》仅描述微调功能，与部署无直接接口关联。二者均无法支撑实际开发，当前唯一可用的生产级部署 API 文档是 [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)。

## 关键参数

- `plan`: 必填，固定为 `"ptu"`，标识 TPM 预留场景（后端统一映射为 `ptu_v2`）。
- `service_tier`: 可选，`"ptu_default"` 表示 TPM 预留（容量保障），`"ptu_fast"` 表示 PTU v2 通用部署（非预留）；创建 TPM 预留时建议显式指定 `"ptu_default"`。
- `deployed_model`: 路径参数，格式为 `{model_name}-ptu-{random_suffix}`，由后端自动生成，不可自定义；`suffix` 字段在创建请求中**禁止传入**。
- `ptu_capacity`: 必填对象，含三个独立维度（单位：kTPM = 1000 [Token](../concepts/token.md)s/分钟）：
  - `input_tpm`: 输入配额，须为模型指定 step 的整数倍；
  - `output_tpm`: 输出配额，须为模型指定 step 的整数倍；
  - `thinking_output_tpm`: 思考输出配额，仅对支持思考的模型有效，同样须为 step 整数倍。
- `charge_type`: 必填，`"pre_paid"`（预付费）或 `"post_paid"`（后付费）；预付费需额外提供 `pre_paid_info` 对象（含 `duration`, `auto_renewal`, `auto_renewal_duration`）。

## 使用方式

- **认证**：使用百炼 API Key，请求头必须包含 `Authorization: Bearer <api-key>`；API Key 与区域强绑定，不可跨区调用。
- **SDK 支持**：
  - DashScope 原生 SDK：Python、Java；
  - OpenAI 兼容 SDK：Python、Node.js、Java、Go，路径前缀为 `/compatible-mode/v1`。
- **域名与工作空间**：
  - 默认域名：`https://dashscope.aliyuncs.com`；
  - 工作空间专属域名：`[workspaceId].[region].maas.aliyuncs.com`（如 `cn-beijing`, `ap-southeast-1`）；
  - 如需指定工作空间，请求头添加 `X-DashScope-WorkSpace: <workspace-id>`。
- **状态流转**：创建后初始状态为 `"DEPLOYING"`，成功后变为 `"RUNNING"`；扩缩容时状态为 `"SCALING"`（预付费）或直接生效（后付费）；续订后状态为 `"WAIT_PRE_PAID_BILLING_TO_SCALING"`。

## 限制和注意事项

- **区域限制**：TPM 预留仅在华北2（北京）、新加坡、东京、法兰克福等已开通区域可用；模型可用性因区域而异（如 `kimi-k2.6` 不在新加坡提供）。
- **扩缩容约束**：`input_tpm`、`output_tpm`、`thinking_output_tpm` 必须同向调整（全部增大或全部减小），混合方向将返回 `400 InvalidParameter` 错误；仅 `plan="ptu"` 的部署支持扩缩容。
- **溢出策略影响**：`overflow_strategy="enable"` 时，超出 TPM 容量的流量将按量计费；`"disable"` 时直接限流，不产生费用但可能触发 `429 Throttling.AllocationQuota` 错误 [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)。
- **错误处理**：关键错误码包括 `404 ModelNotFound`（确认模型名拼写及区域支持）、`403 AccessDenied`（检查工作空间与模型授权）、`429 Throttling.AllocationQuota`（扩容或切换溢出策略）；所有错误响应均含 `request_id`，用于提工单排查 [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)。
- **文档缺失**：微调模型的部署能力（即文档 2 所述）当前无公开 API 规范，实际生产应优先采用 TPM 预留模式；文档 3《模型调优》与部署无接口耦合，仅涉及训练阶段。

## 来源文档

- [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)


