# model production

`model production` 指在百炼平台将模型投入生产环境的完整流程，涵盖模型微调（fine-tuning）、部署（deployment）及容量保障型部署（TPM 预留）三大核心环节。开发者可通过 OpenAPI 或控制台完成端到端管理，其中 TPM 预留是面向高 SLA 场景的关键能力，提供确定性吞吐与容量保障。本文档聚焦生产态模型的可编程管理接口与约束。

## 支持的模型与功能

- **TPM 预留部署**：支持 9 款模型，包括 `qwen-max`、`qwen-plus`、`qwen-flash`、`glm-5.2`、`glm-5.1`、`deepseek-v4-flash`、`deepseek-v4-pro`、`kimi-k2.6` 及其带时间后缀的版本（如 `qwen-3.7-max-2026-05-20`）。华北2（北京）全量支持；新加坡区域不支持 `kimi-k2.6`。  
- **思考输出配额**：上述全部 9 款模型均支持独立配置 `thinking_output_tpm`，启用方式详见 [深度思考模型](https://help.aliyun.com/zh/model-studio/deep-thinking) —— 此能力仅适用于思考模型家族，非通用特性。  
- **微调与部署联动**：模型调优（fine-tuning）产出的定制模型，可通过部署 API 发布为在线服务；该流程由 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 和 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 两份文档分别定义。  
> **注意**：文档 1 明确指出 `ptu_default` 与 `ptu_fast` 是不同部署场景（容量保障 vs 通用 PTU v2），而非“默认/快速”版本关系；而文档 3 的标题“模型部署”未区分部署类型，实际使用中需以文档 1 的 `plan=ptu` + `service_tier=ptu_default` 为准实现 TPM 预留。

## 关键参数

- `plan`: 必填，固定为 `"ptu"`（TPM 预留场景），后端统一映射为 `ptu_v2` 内部处理逻辑。  
- `service_tier`: 推荐显式指定 `"ptu_default"`，明确标识 TPM 预留（容量保障）；`"ptu_fast"` 对应 PTU v2 通用部署，**不适用本节所述容量保障能力**。  
- `ptu_capacity`: 对象类型，必填，含三个独立维度（单位：kTPM = 1000 [Token](../concepts/token.md)s/分钟）：  
  - `input_tpm`: 输入配额，须为模型最小步长整数倍；  
  - `output_tpm`: 输出配额，须为模型最小步长整数倍；  
  - `thinking_output_tpm`: 思考输出配额，仅思考模型支持，须为模型步长整数倍。  
- `charge_type`: `"pre_paid"`（预付费）或 `"post_paid"`（后付费）；预付费需额外传 `pre_paid_info`（含 `duration`, `auto_renewal`, `auto_renewal_duration`）。  
- `deployed_model`: 路径参数，格式为 `{model_name}-ptu-{随机后缀}`，由后端生成，**创建时不可传 `suffix`**（文档 1 明确说明）。

## 使用方式

- **认证**：使用百炼 API Key，请求头必须携带 `Authorization: Bearer <api-key>`；API Key 与区域强绑定，不可跨区调用。  
- **SDK 支持**：DashScope 原生 SDK（Python/Java）与 OpenAI 兼容 SDK（Python/Node.js/Java/Go）均可用；OpenAI 兼容路径前缀为 `/compatible-mode/v1`。  
- **核心接口**（均基于 `https://dashscope.aliyuncs.com/api/v1/` 或 workspace-dedicated 域名）：  
  - 创建：`POST /deployments`（[TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)）  
  - 查询：`GET /deployments/{deployed_model}`（单个）或 `GET /deployments`（列表分页）  
  - 扩缩容：`PUT /deployments/{deployed_model}/scale`（仅 `plan=ptu` 部署支持；扩缩容方向须一致：同增或同减）  
  - 续订：`PUT /deployments/{deployed_model}/renew`（仅预付费部署；状态变为 `WAIT_PRE_PAID_BILLING_TO_SCALING` 后需等待账单处理）  
  - 溢出策略：`PUT /deployments/{deployed_model}/updateOverflowStrategy`（`enable`：溢出至公共池按量计费；`disable`：直接限流）  

## 限制和注意事项

- **区域与模型约束**：`kimi-k2.6` 仅在华北2（北京）可用，新加坡区域无此模型；所有 TPM 预留模型均需从文档 1 列出的 9 款中选择，拼写错误将返回 `ModelNotFound`（404）。  
- **扩缩容异步性**：预付费扩缩容为异步操作，接口返回 `SCALING` 状态后，**禁止在该状态下重复发起扩缩容请求**，否则可能触发冲突错误（409）。  
- **续订时效规则**：22:00 后提交的续订请求，到期时间顺延至 N+2 天 00:00，非即时生效。  
- **溢出策略成本影响**：`overflow_strategy=enable` 时，超出 PTU 容量的流量将产生额外按量费用；`disable` 时虽无额外费用，但请求将被直接拒绝，影响可用性。  
- **错误码处理**：重点关注 `429 Throttling.AllocationQuota`（TPM 容量超额），应对方案为扩容 `ptu_capacity` 或切换 `overflow_strategy`；详见 [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md) 中的错误码章节。  
> **注意**：文档 2（模型调优）和文档 3（模型部署）内容高度简略，仅提供标题与一句话说明，**无具体参数、接口或约束细节**；实际开发中，TPM 预留的完整行为边界、字段定义与错误处理必须严格遵循 [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)。

## 来源文档

- [TPM 预留 DashScope OpenAPI 接口文档](../../raw/model-api-reference/model-production/tpm-reserved-openapi.md)
- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


