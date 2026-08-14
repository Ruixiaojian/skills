# model production

`model production` 是百炼平台中模型从训练、部署到服务化运行的全生命周期管理能力集合，涵盖微调（Fine-tuning）、在线部署（Deployment）及 TPM 预留（TPM Reservation）等核心环节。开发者可通过 OpenAPI 或控制台完成模型定制、容量保障型服务发布与弹性扩缩容操作。该能力面向生产环境高可用、可计量、可治理的需求设计，不提供模型训练基础设施，仅支持基于百炼托管模型的微调与部署。

## 支持的模型/功能

- **微调（Fine-tuning）**：支持对百炼平台托管的基础大模型进行监督微调，生成专属适配业务场景的定制模型。具体能力详见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)。
- **部署类型**：
  - **通用部署（PTU v2）**：按需弹性伸缩，适用于流量波动大、成本敏感场景；
  - **TPM 预留部署（`service_tier=ptu_default`）**：预购固定 TPM（[Token](../concepts/token.md)s Per Minute）容量，保障推理吞吐下限，适用于 SLA 要求严格的生产服务。
- **当前支持的 TPM 预留模型（华北2 北京）**：`qwen-max`（即千问3.8-Max）、`qwen-plus-2026-05-26`、`qwen-flash-2026-04-16`、`glm-5.2`、`glm-5.1`、`deepseek-v4-flash`、`deepseek-v4-pro`、`kimi-k2.6`、`qwen-3.7-max-2026-05-20`。  
  > **注意**：新加坡区域不支持 `kimi-k2.6`，其余模型一致；所有 9 款模型均支持 `thinking_output_tpm` 配额，但该字段仅对深度思考模型家族生效，启用方式见[深度思考模型](https://help.aliyun.com/zh/model-studio/deep-thinking)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_name` | String | 是 | 基础模型名，如 `qwen-max`，须在[支持清单](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)中 |
| `plan` | String | 是 | 固定为 `ptu`（TPM 预留场景） |
| `service_tier` | String | 否 | `ptu_default`（TPM 预留）或 `ptu_fast`（PTU v2 通用，默认）；二者非版本关系，而是部署策略差异 |
| `charge_type` | String | 是 | `pre_paid`（预付费）或 `post_paid`（后付费） |
| `ptu_capacity` | Object | 是 | 容量配置对象，含 `input_tpm`、`output_tpm`、`thinking_output_tpm`（仅思考模型），单位为 kTPM（1000 TPM），取值须为模型指定 step 的整数倍 |
| `pre_paid_info` | Object | 条件必填 | `charge_type=pre_paid` 时必填，含 `duration`（1~30/60/90/120/365 天）、`auto_renewal`（布尔值）、`auto_renewal_duration`（`auto_renewal=true` 时必填） |

> **注意**：`suffix` 字段在 TPM 预留创建中**不可传入**，由后端自动生成 `deployed_model`（如 `qwen-max-ptu-a1b2c3d4`），长度不固定；若手动传入将导致 `InvalidParameter` 错误。

## 使用方式

1. **认证**：使用百炼 API Key，请求头携带 `Authorization: Bearer <api-key>`；API Key 与区域强绑定，不可跨区调用。
2. **Endpoint**：
   - DashScope 原生域名：`https://dashscope.aliyuncs.com`
   - Workspace 专属域名（需指定工作空间）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com`
   - OpenAI 兼容路径前缀：`/compatible-mode/v1`
3. **核心接口（TPM 预留）**：
   - 创建：`POST /api/v1/deployments`（状态流转：`DEPLOYING` → `RUNNING`）
   - 查询单个：`GET /api/v1/deployments/{deployed_model}`
   - 列表查询：`GET /api/v1/deployments?page_no=1&page_size=10`
   - 扩缩容：`PUT /api/v1/deployments/{deployed_model}/scale`（`input_tpm`/`output_tpm`/`thinking_output_tpm` 必须同向调整）
   - 续订：`PUT /api/v1/deployments/{deployed_model}/renew`（预付费专用，状态变为 `WAIT_PRE_PAID_BILLING_TO_SCALING`）
   - 修改溢出策略：`PUT /api/v1/deployments/{deployed_model}/updateOverflowStrategy`（`enable`：溢出至公共池按量计费；`disable`：直接限流）

完整接口定义与示例详见 [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)。

## 限制和注意事项

- **区域限制**：TPM 预留目前仅支持 `cn-beijing`（华北2）、`ap-southeast-1`（新加坡）、`ap-northeast-1`（东京）、`eu-central-1`（法兰克福）；弗吉尼亚区域暂不支持。
- **扩缩容约束**：
  - 仅 `plan=ptu` 的部署支持扩缩容；
  - 预付费扩缩容为异步操作，状态为 `SCALING` 期间禁止重复调用；
  - `input_tpm`、`output_tpm`、`thinking_output_tpm` 必须同步增减，混合方向（如 input 增、output 减）将返回 `InvalidParameter`。
- **续订时效**：22:00 后提交的续订请求，到期时间顺延至 N+2 日 00:00。
- **错误处理**：HTTP 429 `Throttling.AllocationQuota` 表示超出预留 TPM 容量且 `overflow_strategy=enable`，此时流量已溢出计费；若设为 `disable` 则直接限流，无额外费用但影响可用性。
- **模型部署一致性**：通用部署（`service_tier=ptu_fast`）与 TPM 预留（`service_tier=ptu_default`）共用同一套部署 API，但计费模型与容量保障机制不同；二者不可混用参数，例如 `ptu_capacity` 仅对 `ptu_default` 有效。相关概念对比详见 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)
- [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)


