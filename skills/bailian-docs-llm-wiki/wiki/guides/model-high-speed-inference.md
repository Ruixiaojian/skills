# model high speed inference

百炼平台提供两种面向高吞吐、低延迟推理场景的加速能力：**TPM 预留（[Token](../concepts/token.md) Per Minute Reservation）** 和 **快速模式（Fast Mode）**。前者通过预分配专属容量保障确定性吞吐与稳定性，适用于流量可预估、不可接受限流的核心业务；后者通过底层调度与硬件优化提升单请求输出速度（TPS），适用于对响应实时性敏感的交互式场景（如编程助手、Agent 多步推理）。二者可独立使用，也可组合——例如在 TPM 预留的专属实例上启用 `*-fast-preview` 模型。

## 支持的模型/功能

- **TPM 预留**：为指定模型锁定专属输入/输出吞吐量（单位：kTPM），支持千问、GLM、DeepSeek、Kimi 等主流模型，覆盖华北2（北京）和新加坡地域。具体支持列表及价格详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档中的“支持的模型”表格。
  
- **快速模式**：当前仅支持 `glm-5.2-fast-preview` 模型（北京、新加坡双地域），处于 preview 阶段，提供 1.5~2 倍于标准 API 的 TPS（达 80~100 TPS），并引入排队机制缓解突发流量冲击。详细模型列表与计费单价见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 文档。

> **注意**：两套机制的模型支持范围不重叠。TPM 预留支持 Qwen3.6-Flash、DeepSeek-v4-Pro 等多款模型，而快速模式目前**仅支持 `glm-5.2-fast-preview`**。若需在快速模式下获得容量保障，必须先为该模型创建 TPM 预留，并将 `model` 参数设为预留生成的专属 code（如 `bailian-glm-5.2-fast-preview-xxxxx`），而非直接使用 `glm-5.2-fast-preview` —— 后者走公共资源池，不享受预留保障。此关键差异在 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 和 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 两份文档中均未明确交叉说明，开发者需自行组合配置。

## 关键参数

| 参数 | 适用场景 | 说明 |
|------|----------|------|
| `model` | 全局必填 | TPM 预留需替换为专属模型 code（如 `bailian-qwen37-max-xxxxx`）；快速模式需设为 `glm-5.2-fast-preview`（或其对应预留 code）。两者不可混用同一字符串。 |
| 输入/输出 TPM（kTPM） | TPM 预留 | 创建时按模型粒度分别设置，决定专属吞吐上限。阶梯系数、缓存折扣等影响实际容量消耗，详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中“长输入阶梯系数和缓存折扣”表格。 |
| 溢出策略 | TPM 预留 | “自动溢出”（默认）：超限请求降级为按量计费；“仅使用预留容量”：超限返回 HTTP 429。 |
| 接入域名 | 快速模式 | 必须使用 `https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1` 格式，`{workspace_id}` 和 `{region}` 需从控制台获取，标准 dashscope 域名不支持快速模式。 |

## 使用方式

- **TPM 预留**：在百炼控制台创建预留后，复制生成的专属 `model` code，替换 API 请求中的 `model` 字段即可生效。调用示例见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档末尾的 Python/curl 示例。注意：新预留实例存在短暂预热期，期间可能出现延迟波动，建议实现客户端重试逻辑。

- **快速模式**：无需额外配置，只需将 `model` 设为 `glm-5.2-fast-preview` 并使用专用域名调用。流式响应中 `reasoning_content` 与 `content` 字段分离推送，需按 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 文档示例解析。非流式调用返回结构亦含 `reasoning_content` 字段。

## 限制和注意事项

- **地域与模型绑定**：TPM 预留和快速模式均按地域隔离。北京地域的预留 code 不能在新加坡调用；`glm-5.2-fast-preview` 在两地价格不同，需按实际地域选择对应计费标准。
  
- **preview 风险**：快速模式为预览功能，接口行为、模型能力、可用性及计费规则可能随时调整，不建议用于生产环境的关键链路。正式 GA 后将同步更新文档。

- **容量计算复杂性**：TPM 预留的实际容量消耗受输入长度阶梯系数、缓存命中率影响显著。例如 GLM-5.1 在 `[32K, 200K]` 输入区间内，输入容量消耗系数为 1.33，需在容量计算器中准确填写平均输入长度，否则易导致预留不足。详情参见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中“长输入阶梯系数和缓存折扣”表格。

- **退订与 code 失效**：TPM 预留退订后专属 `model` code 立即失效，历史请求将回退至公共资源池。若需长期稳定接入，建议开启“到期自动续费”并监控用量趋势，避免因过期导致服务中断。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


