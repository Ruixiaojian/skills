# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：TPM 预留（保障专属容量）与快速模式（提升单请求输出速度）。二者定位不同，可独立使用或组合使用——TPM 预留解决**稳定性与确定性**问题（避免公共池限流），快速模式解决**响应速度**问题（提升 TPS 与首 token 延迟）。开发者应根据业务 SLA 要求（如是否容忍限流、是否敏感于输出延迟）选择合适方案。

## 支持的模型/功能

- **TPM 预留**：为指定模型锁定专属输入/输出吞吐量（单位：kTPM），确保高峰期调用不受公共资源限流影响。支持千问、GLM、DeepSeek、Kimi 等主流模型，覆盖华北2（北京）和新加坡地域。具体支持列表详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档中的「支持的模型」表格。
  
- **快速模式（Fast mode）**：当前仅支持 `glm-5.2-fast-preview` 模型（北京/新加坡双地域），通过优化调度与计算流水线，将 TPS 提升至标准 API 的 1.5~2 倍（达 80~100 TPS），适用于 AI 编程助手、Agent 多步推理等对输出速度敏感的场景。该能力处于 preview 阶段，规格可能调整，详情见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。

> **注意**：TPM 预留文档中列出的 `glm-5.2` 是标准模型，而快速模式文档明确指出仅 `glm-5.2-fast-preview` 支持快速模式。二者为不同 model code，不可混用；标准 `glm-5.2` 即使配置了 TPM 预留，也不会自动获得快速模式的 TPS 提升。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `model` | 必须替换为专属 model code（TPM 预留）或 `-fast-preview` 后缀模型 ID（快速模式）。两者互斥，不可同时使用同一请求。 | [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)、[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) |
| 输入/输出 TPM（kTPM） | TPM 预留需显式配置输入与输出吞吐量额度，单位为千 token/分钟；额度决定容量保障上限。 | [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) |
| 溢出策略 | TPM 预留创建时可选：`自动溢出至按量计费`（默认，服务不中断）或 `仅使用预留容量`（超出返回 429）。 | [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) |
| 接入域名 | 快速模式必须使用专属域名 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，标准 API 或 TPM 预留仍使用 `dashscope.aliyuncs.com`。 | [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) |

## 使用方式

- **TPM 预留**：在百炼控制台创建实例后，获取专属 model code，并在 API 请求中将其赋值给 `model` 字段（[示例代码](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)）。无需修改 endpoint 或其他参数，但需注意预热期可能有短暂延迟波动。
  
- **快速模式**：直接使用 `glm-5.2-fast-preview` 作为 `model` 参数，并切换至 `maas.aliyuncs.com` 域名（[调用示例](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)）。不支持流式 `reasoning_content` 以外的字段定制，且暂不支持 TPM 预留绑定（即快速模式请求不计入 TPM 预留用量，也不受其保障）。

> **注意**：快速模式文档未提及缓存命中率对计费的影响，但 TPM 预留文档明确说明 `glm-5.2` 支持 25% 缓存折扣（仅影响输入容量消耗）。由于 `glm-5.2-fast-preview` 是独立模型 ID，其缓存策略以 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 文档中“缓存命中”列为准（当前为 4 元/百万 token），二者计费逻辑不互通。

## 限制和注意事项

- **地域隔离**：TPM 预留与快速模式均按地域独立配置，北京与新加坡的预留实例、模型 code、域名不可跨地域复用。
  
- **生命周期管理**：TPM 预留按自然日计费（非 24 小时），到期后 2 小时内仍可调用，14 小时后彻底删除且 model code 失效；快速模式无预付费周期，按 token 实时计费，无到期概念。
  
- **组合使用限制**：当前不支持为 `glm-5.2-fast-preview` 创建 TPM 预留；亦不支持在快速模式请求中使用 TPM 预留生成的 model code。二者为正交能力，需按场景单独选型。
  
- **preview 风险**：快速模式处于预览阶段，接口行为、模型性能、支持地域及计费规则可能变更，生产环境使用前请关注 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 文档更新。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


