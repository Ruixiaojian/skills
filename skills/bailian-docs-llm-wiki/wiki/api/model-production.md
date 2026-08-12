# model production

`model production` 指将训练/微调完成的模型部署为可稳定提供在线推理服务的生产环境实例，涵盖模型部署、TPM 预留容量保障、扩缩容与生命周期管理等核心能力。该能力面向需要确定性吞吐、低延迟响应及资源隔离保障的高价值业务场景，支持预付费与后付费两种计费模式。所有操作均通过 DashScope OpenAPI 完成，需使用百炼 API Key 进行区域绑定认证。

## 支持的模型与功能

- **支持模型**：当前 TPM 预留部署仅支持以下 9 款模型（华北2 区域全量支持）：`qwen-max`（即千问3.8-Max）、`qwen-plus-2026-05-26`（千问3.7-Plus-2026-05-26）、`qwen-flash-2026-04-16`（千问3.6-Flash-2026-04-16）、`glm-5.2`、`glm-5.1`、`deepseek-v4-flash`、`deepseek-v4-pro`、`kimi-k2.6`，以及 `qwen-max-2026-05-20`（千问3.7-Max-2026-05-20）。新加坡区域不支持 `kimi-k2.6` [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)。
- **深度思考支持**：上述全部 9 款模型均支持独立配置 `thinking_output_tpm` 配额，启用方式详见[深度思考模型](https://help.aliyun.com/zh/model-studio/deep-thinking)（该能力依赖模型自身架构，非通用功能）。
- **部署类型区分**：通过 `service_tier` 参数区分部署形态：`ptu_default` 表示 TPM 预留（容量保障型），`ptu_fast` 表示 PTU v2 通用部署（弹性共享型），二者非版本迭代关系，而是不同 SLA 场景 [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)。
- **基础能力**：支持模型部署（含微调或导入模型）、TPM 容量预留、实时扩缩容、预付费续订、溢出策略动态切换等全生命周期管理 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)。

> **注意**：文档 3（模型调优）仅说明“通过微调训练定制专属模型”，但未明确微调模型是否可直接用于 TPM 预留部署。根据文档 2 明确列出的支持模型清单及创建接口要求（`model_name` 必须为白名单值），**微调产出的自定义模型暂不支持 TPM 预留部署**，仅支持通用部署（`service_tier=ptu_fast`）或标准 API 调用。此为关键限制，需开发者确认模型来源是否在 TPM 白名单内。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_name` | String | ✅ | 基础模型名，**必须为 TPM 预留支持列表中的精确名称**（如 `qwen-max`），不支持自定义微调模型 ID |
| `plan` | String | ✅ | 固定为 `ptu`，标识 TPM 预留场景 |
| `service_tier` | String | ⚠️ | `ptu_default`（容量保障）或 `ptu_fast`（通用部署），默认 `ptu_fast`；TPM 预留必须显式传 `ptu_default` |
| `charge_type` | String | ✅ | `pre_paid`（预付费）或 `post_paid`（后付费） |
| `ptu_capacity` | Object | ✅ | 吞吐配额对象，含 `input_tpm`、`output_tpm`、`thinking_output_tpm`（仅思考模型支持），单位为 kTPM（1000 [Token](../concepts/token.md)s/分钟），取值须为模型步长整数倍 |
| `pre_paid_info` | Object | 条件必填 | `charge_type=pre_paid` 时必填，含 `duration`（1~30/60/90/120/365 天）、`auto_renewal`（Boolean）、`auto_renewal_duration`（`auto_renewal=true` 时必填） |

- `deployed_model`（部署服务 ID）由后端自动生成，格式为 `{model_name}-ptu-{随机后缀}`，**创建时不传 `suffix` 字段**，避免重名冲突。
- 所有 API 请求头必须包含 `Authorization: Bearer <api-key>` 和 `Content-Type: application/json`；流式调用需加 `X-DashScope-SSE: enable`；异步批处理需加 `X-DashScope-Async: enable`。

## 使用方式

1. **创建部署**：调用 `POST /api/v1/deployments`，传入完整请求体（含 `model_name`, `plan="ptu"`, `service_tier="ptu_default"`, `charge_type`, `ptu_capacity` 等）。成功后返回 `deployed_model` 及初始状态 `DEPLOYING`。
2. **查询状态**：
   - 单个部署：`GET /api/v1/deployments/{deployed_model}`
   - 列表分页：`GET /api/v1/deployments?page_no=1&page_size=10`
3. **扩缩容**：`PUT /api/v1/deployments/{deployed_model}/scale`，传入新 `ptu_capacity`。**注意**：`input_tpm`/`output_tpm`/`thinking_output_tpm` 必须同向调整（全增或全减），混合方向报错；预付费扩缩容为异步，状态先变 `SCALING`，完成后变 `RUNNING`。
4. **续订**：`PUT /api/v1/deployments/{deployed_model}/renew`，仅适用于 `charge_type=pre_paid`，传 `pre_paid_info`。续订后状态为 `WAIT_PRE_PAID_BILLING_TO_SCALING`。
5. **修改溢出策略**：`PUT /api/v1/deployments/{deployed_model}/updateOverflowStrategy`，传 `{"overflow_strategy": "enable" \| "disable"}`。`enable` 时超额流量按量计费；`disable` 时直接限流。

SDK 支持：DashScope 原生 SDK（Python/Java）及 OpenAI 兼容 SDK（Python/Node.js/Java/Go），后者路径前缀为 `/compatible-mode/v1` [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)。

## 限制和注意事项

- **区域与密钥绑定**：API Key 与区域强绑定（如 `cn-beijing`），不可跨区调用；workspace-dedicated 域名格式为 `[workspaceId].[region].maas.aliyuncs.com`。
- **模型限制**：仅文档 2 明确列出的 9 款模型支持 TPM 预留；微调模型（见[模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)）不在支持列表内，不可用于 `service_tier=ptu_default`。
- **扩缩容约束**：仅 `plan=ptu`（内部 ptu_v2）部署支持扩缩容；`SCALING` 状态期间禁止重复调用扩缩容接口。
- **续订时效**：22:00 后提交的续订请求，到期时间顺延至 N+2 日 00:00。
- **错误处理**：重点关注 `429 Throttling.AllocationQuota`（TPM 超额走公共池限流），此时应扩容 `ptu_capacity` 或设 `overflow_strategy=disable`；`404 ModelNotFound` 需核对 `model_name` 是否拼写正确且在白名单中。
- **命名规范**：`deployed_model` 为路径参数，不可自行构造；控制台无溢出策略配置入口，必须通过 OpenAPI 调用 `updateOverflowStrategy`。

## 来源文档

- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)


