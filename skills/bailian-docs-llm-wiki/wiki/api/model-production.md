# model production

`model production` 指在百炼平台将模型投入生产环境的完整流程，涵盖模型微调（fine-tuning）、部署（deployment）及容量保障型部署（TPM 预留）三大核心能力。开发者可通过 OpenAPI 或控制台完成端到端操作，其中 TPM 预留是面向高 SLA 场景的专用部署模式，提供确定性吞吐保障。本文档聚焦生产就绪的关键技术要素，不覆盖训练/评估等离线环节。

## 支持的模型与功能

- **TPM 预留部署**：仅支持指定列表模型，华北2（北京）区域包括：`qwen-max`（即千问3.8-Max）、`qwen-plus-2026-05-26`、`qwen-flash-2026-04-16`、`glm-5.2`、`glm-5.1`、`deepseek-v4-flash`、`deepseek-v4-pro`、`kimi-k2.6` 及 `qwen-max-2026-05-20`（对应千问3.7-Max-2026-05-20）。新加坡区域不支持 `kimi-k2.6` [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)。  
- **思考输出配额**：上述全部 9 款模型均支持独立配置 `thinking_output_tpm`，需配合深度思考模型启用方式使用，详见[深度思考模型](https://help.aliyun.com/zh/model-studio/deep-thinking)。  
- **微调与部署分离**：模型调优（fine-tuning）生成可部署的定制模型，再通过部署 API 发布为服务；二者为正交能力，调优结果可多次部署 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)。  
- **通用部署能力**：除 TPM 预留外，平台还支持标准模型部署（含微调后模型），其 API 文档见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)。

> **注意**：文档1中列出的模型名（如 `qwen-max`）为 API 调用时必需的 `model_name` 字段值，与控制台显示的“千问3.8-Max”等别名不完全一致，必须严格按 API 文档取值，否则返回 `ModelNotFound` 错误。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `plan` | string | 是 | 固定为 `"ptu"`，标识 TPM 预留场景 |
| `service_tier` | string | 否 | `"ptu_default"`（TPM 预留，容量保障）或 `"ptu_fast"`（PTU v2 通用部署）；创建 TPM 预留时显式传 `"ptu_default"` |
| `charge_type` | string | 是 | `"pre_paid"`（预付费）或 `"post_paid"`（后付费） |
| `ptu_capacity` | object | 是 | 容量配置对象，含 `input_tpm`、`output_tpm`、`thinking_output_tpm`（仅思考模型），单位为 kTPM（1000 [Token](../concepts/token.md)s/分钟），取值须为模型步长整数倍 |
| `pre_paid_info.duration` | integer | 条件必填 | 预付费时长（天），合法值：1~30、60、90、120、365 |
| `pre_paid_info.auto_renewal` | boolean | 是 | 是否自动续费 |
| `pre_paid_info.auto_renewal_duration` | integer | 条件必填 | `auto_renewal=true` 时必填，续费周期（天） |

- `deployed_model`（部署服务 ID）格式为 `{model_name}-ptu-{随机后缀}`，由后端生成，不可自定义；创建时不传 `suffix` 字段 [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)。  
- 扩缩容时 `ptu_capacity` 的三个维度必须同向调整（全增或全减），混合方向将报错。

## 使用方式

1. **认证**：使用百炼 API Key，请求头携带 `Authorization: Bearer <api-key>`；API Key 与区域强绑定，不可跨区调用。  
2. **Endpoint**：  
   - 全局域名：`https://dashscope.aliyuncs.com`  
   - Workspace 专属域名：`https://{WorkspaceId}.{region}.maas.aliyuncs.com`（支持 `cn-beijing`, `ap-southeast-1`, `ap-northeast-1`, `eu-central-1`）  
   - OpenAI 兼容路径前缀：`/compatible-mode/v1`（需 SDK 支持）  
3. **核心流程**：  
   - 创建：`POST /api/v1/deployments`，传入完整配置，状态从 `DEPLOYING` 过渡至 `RUNNING`  
   - 查询：`GET /api/v1/deployments/{deployed_model}`（单个）或 `GET /api/v1/deployments`（分页列表）  
   - 扩缩容：`PUT /api/v1/deployments/{deployed_model}/scale`，传新 `ptu_capacity`；预付费需等待 `WAIT_PRE_PAID_BILLING_TO_SCALING` → `RUNNING`  
   - 续订：`PUT /api/v1/deployments/{deployed_model}/renew`，仅预付费部署支持  
   - 溢出策略：`PUT /api/v1/deployments/{deployed_model}/updateOverflowStrategy`，`enable`（溢出计费）或 `disable`（直接限流）  

> **注意**：文档1明确指出，官方 API 不含 `auto_renewal_cycle` 字段，续费逻辑仅依赖 `duration`、`auto_renewal` 和 `auto_renewal_duration` 三字段，任何引用 `auto_renewal_cycle` 的示例均为过时信息 [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)。

## 限制和注意事项

- **区域限制**：Kimi-K2.6 仅在华北2（北京）可用，新加坡区域不支持。  
- **扩缩容约束**：仅 `plan=ptu`（内部映射为 `ptu_v2`）的部署支持扩缩容；`SCALING` 状态期间禁止重复调用扩缩容接口。  
- **溢出策略影响**：`overflow_strategy=enable` 时，超出 PTU 容量的流量将按量计费并计入账单；`disable` 时直接返回 HTTP 429 `Throttling.AllocationQuota` 错误，需客户端重试或降级。  
- **错误处理**：常见错误码包括 `InvalidParameter`（参数校验失败）、`ModelNotFound`（模型名拼写错误或不在支持列表）、`Throttling.AllocationQuota`（TPM 超额限流）；所有错误响应均含 `request_id`，用于工单排查 [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)。  
- **微调模型部署**：微调产出的模型需先通过 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) API 部署，暂不支持直接作为 `model_name` 传入 TPM 预留创建接口。

## 来源文档

- [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


