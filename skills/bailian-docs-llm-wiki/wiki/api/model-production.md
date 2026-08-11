# model production

`model production` 指在百炼平台将模型投入生产环境的完整流程，涵盖模型微调、部署（含 TPM 预留）、扩缩容、续订及策略配置等全生命周期操作。该能力面向需要稳定、可预测吞吐与低延迟响应的生产级场景，核心支撑为 DashScope OpenAPI 接口体系。开发者需结合模型能力、计费模式与区域可用性进行规划。

## 支持的模型/功能

- **TPM 预留部署**：支持 9 款模型（如 `qwen-max`、`glm-5.2`、`deepseek-v4-pro`、`kimi-k2.6` 等），其中华北2（北京）全量支持；新加坡区域不支持 `kimi-k2.6`。所有支持模型均具备思考输出配额（`thinking_output_tpm`）能力 [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)。
- **微调训练**：支持基于自有数据对基础模型进行监督微调，生成专属版本 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)。
- **模型部署**：支持将微调产出或直接导入的模型发布为在线推理服务 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)。

> **注意**：文档1明确指出 `ptu_default` 与 `ptu_fast` 是不同部署场景（容量保障 vs 通用PTU v2），而非同一模型的“默认/快速”版本；而文档3未说明其是否覆盖 TPM 预留场景。实际生产中，TPM 预留必须使用 `plan=ptu` + `service_tier=ptu_default`，不可混用 `ptu_fast`。

## 关键参数

- `plan`: 必填，固定为 `ptu`（TPM 预留场景）。
- `service_tier`: 推荐显式指定为 `ptu_default`，避免误用 `ptu_fast`（[TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)）。
- `deployed_model`: 路径参数，格式为 `{model_name}-ptu-{随机后缀}`，由后端生成，不可自定义。
- `ptu_capacity`: 必填对象，含三个独立维度（单位：kTPM）：
  - `input_tpm`: 输入 [Token](../concepts/token.md)/分钟配额；
  - `output_tpm`: 输出 [Token](../concepts/token.md)/分钟配额；
  - `thinking_output_tpm`: 思考输出配额（仅思考模型支持）；
  > **注意**：各维度起始值与步长因模型而异，以控制台创建页实时展示为准，非文档硬编码值。
- `charge_type`: `pre_paid`（预付费）或 `post_paid`（后付费）；预付费需额外提供 `pre_paid_info`（含 `duration`, `auto_renewal`, `auto_renewal_duration`）。

## 使用方式

1. **认证**：使用百炼 API Key，请求头携带 `Authorization: Bearer <api-key>`；API Key 与区域强绑定，不可跨区调用。
2. **创建部署**：调用 `POST /api/v1/deployments`，传入 `model_name`、`plan="ptu"`、`service_tier="ptu_default"`、`ptu_capacity` 及计费信息。`suffix` 字段**不可传**，由后端生成 `deployed_model`。
3. **查询状态**：
   - 单个部署：`GET /api/v1/deployments/{deployed_model}`
   - 列表分页：`GET /api/v1/deployments?page_no=1&page_size=10`
4. **扩缩容**：`PUT /api/v1/deployments/{deployed_model}/scale`，新 `ptu_capacity` 中各维度须同向调整（全增或全减）。
5. **续订（仅预付费）**：`PUT /api/v1/deployments/{deployed_model}/renew`，传入新的 `pre_paid_info`；续订后状态为 `WAIT_PRE_PAID_BILLING_TO_SCALING`，需等待账单处理完成。
6. **溢出策略**：`PUT /api/v1/deployments/{deployed_model}/updateOverflowStrategy`，`overflow_strategy` 取 `"enable"`（溢出至公共池按量计费）或 `"disable"`（直接限流）。

SDK 支持：DashScope 原生 SDK（Python/Java）及 OpenAI 兼容 SDK（Python/Node.js/Java/Go），后者路径前缀为 `/compatible-mode/v1`。

## 限制和注意事项

- **区域限制**：Kimi-K2.6 仅在华北2（北京）可用，其他区域不支持。
- **扩缩容约束**：仅 `plan=ptu` 的部署支持扩缩容；预付费扩缩容为异步操作，状态为 `SCALING` 期间禁止重复调用。
- **续订时效**：22:00 后提交的续订请求，到期时间顺延至 N+2 日 00:00。
- **错误处理**：HTTP 429 错误码 `Throttling.AllocationQuota` 表示 TPM 容量超额，应扩容或禁用溢出策略（[TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)）。
- **命名规范**：`deployed_model` 后缀长度不固定，由后端生成，勿依赖固定位数（如8位）做解析。

## 来源文档

- [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


