# model production

`model production` 指在百炼平台将模型投入生产环境的完整流程，涵盖模型微调、部署（含 TPM 预留）、扩缩容、续订及策略配置等全生命周期操作。该能力面向需要稳定、可预测吞吐与低延迟响应的生产级场景，核心支撑为 DashScope OpenAPI 接口体系。开发者需结合模型能力、计费模式与区域可用性进行规划。

## 支持的模型/功能

- **TPM 预留部署**：支持 9 款模型，包括 `qwen-max`（千问3.8-Max）、`qwen-plus`（千问3.7-Plus-2026-05-26）、`qwen-flash`（千问3.6-Flash-2026-04-16）、`glm-5.2`、`glm-5.1`、`deepseek-v4-flash`、`deepseek-v4-pro`、`kimi-k2.6` 及 `qwen-3.7-max-2026-05-20`。华北2（北京）全量支持；新加坡区域不支持 `kimi-k2.6` [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)。
- **思考输出配额**：上述全部 9 款模型均支持独立配置 `thinking_output_tpm`，用于控制深度思考阶段的输出吞吐，启用方式详见[深度思考模型](https://help.aliyun.com/zh/model-studio/deep-thinking)。
- **模型调优**：支持对基础模型进行监督微调（Supervised Fine-tuning），生成定制化模型版本 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)。
- **模型部署**：支持将微调产出或直接导入的模型部署为在线推理服务，提供标准 REST 接口与流式响应能力 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)。

> **注意**：文档 1 中明确指出 `ptu_default` 与 `ptu_fast` 是不同部署场景（容量保障 vs 通用 PTU v2），而非“默认/快速”版本关系；而文档 3 的标题“模型部署”未区分部署类型，实际生产中必须根据 SLA 要求选择 TPM 预留（`service_tier=ptu_default`）或通用部署，二者 API 行为与计费逻辑存在本质差异。

## 关键参数

- `plan`: 必填，固定为 `"ptu"`，标识 TPM 预留场景。
- `service_tier`: 推荐显式指定为 `"ptu_default"`，确保使用容量保障型部署；`"ptu_fast"` 对应 PTU v2 通用部署，不提供 TPM 级别保障 [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)。
- `ptu_capacity`: 必填对象，含三个整数字段：
  - `input_tpm`: 输入 Token 每分钟配额（kTPM），须为模型步长（step）的整数倍；
  - `output_tpm`: 输出 Token 每分钟配额（kTPM），同上；
  - `thinking_output_tpm`: 思考输出配额（仅思考模型支持），同上。
- `charge_type`: `"pre_paid"`（预付费）或 `"post_paid"`（后付费）；预付费需额外提供 `pre_paid_info`（含 `duration`, `auto_renewal`, `auto_renewal_duration`）。
- `deployed_model`: 路径参数，格式为 `{model_name}-ptu-{随机后缀}`，由后端生成，不可自定义。

## 使用方式

1. **认证**：使用百炼 API Key，请求头携带 `Authorization: Bearer <api-key>`；API Key 与区域强绑定，不可跨区调用。
2. **创建部署**：`POST /api/v1/deployments`，传入 `model_name`, `plan="ptu"`, `service_tier="ptu_default"`, `charge_type`, `ptu_capacity` 等；创建后状态为 `DEPLOYING`，完成为 `RUNNING`。
3. **查询**：
   - 单个部署：`GET /api/v1/deployments/{deployed_model}`
   - 列表分页：`GET /api/v1/deployments?page_no=1&page_size=10`
4. **扩缩容**：`PUT /api/v1/deployments/{deployed_model}/scale`，传新 `ptu_capacity`；注意：`input_tpm`/`output_tpm`/`thinking_output_tpm` 必须同向调整（全增或全减），否则报错；预付费扩缩容为异步，状态先变 `SCALING`，完成后回 `RUNNING`。
5. **续订**（仅预付费）：`PUT /api/v1/deployments/{deployed_model}/renew`，传 `pre_paid_info`；续订后状态为 `WAIT_PRE_PAID_BILLING_TO_SCALING`。
6. **溢出策略**：`PUT /api/v1/deployments/{deployed_model}/updateOverflowStrategy`，`overflow_strategy` 取 `"enable"`（超限流量按量计费）或 `"disable"`（超限直接限流）。

## 限制和注意事项

- **区域限制**：Kimi-K2.6 仅在华北2（北京）可用，新加坡区域不支持；所有 TPM 预留模型均不支持弗吉尼亚区域（仅 workspace-dedicated 域名支持 us-east-1）。
- **扩缩容约束**：仅 `plan=ptu`（内部 ptu_v2）的部署支持扩缩容；混合方向（如增 input_tpm 但减 output_tpm）会返回 400 错误。
- **续订时效**：22:00 后提交的续订请求，到期时间顺延至 N+2 日 00:00。
- **错误处理**：429 限流错误中，`Throttling.AllocationQuota` 明确表示 TPM 容量超额，此时应扩容或切换 `overflow_strategy=disable` 以避免额外费用 [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)。
- **SDK 支持**：DashScope 原生 SDK（Python/Java）与 OpenAI 兼容 SDK（Python/Node.js/Java/Go）均支持，后者需使用 `/compatible-mode/v1` 路径前缀。
- **命名约定**：官方 API 不含 `auto_renewal_cycle` 字段，续费仅依赖 `duration`、`auto_renewal` 和 `auto_renewal_duration` 三字段；`suffix` 参数在 TPM 预留创建中禁止传入，由后端生成。

## 来源文档

- [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


