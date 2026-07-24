# model high speed inference

百炼平台提供两种面向高吞吐、低延迟推理场景的加速能力：**TPM 预留**（保障专属容量）和**快速模式（Fast mode）**（提升单请求输出速度）。二者定位不同：TPM 预留解决「容量确定性」问题，适用于流量可预估、不可接受限流的生产核心链路；快速模式解决「响应实时性」问题，适用于对 TPS 和首 token 延迟敏感的交互式场景（如编程助手、Agent 多步调用）。两者可独立使用，也可组合——例如在 TPM 预留的专属模型 code 上启用 `*-fast-preview` 变体（需模型支持）。

## 支持的模型/功能

- **TPM 预留**：为指定模型锁定专属输入/输出吞吐量（单位：kTPM），确保业务高峰期不受公共资源限流影响。支持模型详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档中“支持的模型”表格，覆盖千问、GLM、DeepSeek、Kimi 等主流模型的多个版本，按地域（华北2/新加坡）分列定价与容量参数。
  
- **快速模式（Fast mode）**：当前为 preview 阶段，仅支持 `glm-5.2-fast-preview` 模型变体，通过优化调度与计算流水线，将 TPS 提升至标准 API 的 1.5~2 倍（达 80~100 TPS），并引入请求排队机制缓解瞬时超载。详细支持列表与计费单价见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 文档。

> **注意**：两篇文档对 `glm-5.2` 的缓存折扣描述存在差异。[TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 明确其缓存折扣为 0.25（命中部分按 25% 折算容量），而 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 表格中标注“缓存命中”为 4 元（疑似指缓存命中单价，非折扣率）。实际缓存行为以控制台最新说明或 API 返回的 `usage.prompt_tokens_details.cached_tokens` 字段为准。

## 关键参数

| 参数 | TPM 预留 | 快速模式 |
|------|----------|-----------|
| **核心指标** | 输入TPM / 输出TPM（kTPM） | TPS（目标 80~100）、首 token 延迟（隐含优化） |
| **计费单位** | 预付费（按天，kTPM）+ 溢出按量（token） | 纯按 token 计费（输入/输出单价明确） |
| **容量保障** | 刚性兑付：预留额度内绝对优先、零限流 | 无容量保障：超限请求进入排队队列，不返回 429 |
| **缓存策略** | 支持长输入阶梯系数与缓存折扣（如 glm-5.2 折扣 0.25） | 支持缓存（文档标注“缓存命中”单价，但未说明折扣逻辑） |
| **模型标识** | 专属 model code（由系统生成，形如 `qwen3.7-max-20260520-tpm-xxxxx`） | 固定 model ID（如 `glm-5.2-fast-preview`） |

## 使用方式

- **TPM 预留**：创建后获取专属 model code，并在 API 请求中替换 `model` 参数。接入域名与标准 API 一致（如 `https://dashscope.aliyuncs.com/...`）。示例见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的 Python/curl 调用片段。**注意**：实例需处于“运行中”状态，且首次大流量请求前存在短暂预热期，建议实现客户端重试机制。

- **快速模式**：直接使用 `*-fast-preview` 模型 ID（如 `glm-5.2-fast-preview`），**必须使用专属 workspace 域名**（格式：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/...`），不可使用通用 dashscope 域名。流式响应中新增 `reasoning_content` 字段，需按 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 文档示例解析。

## 限制和注意事项

- **TPM 预留限制**：
  - 仅支持控制台开放的模型列表，新模型上线后需等待控制台同步才可创建预留；
  - 输入/输出 TPM 可独立调整，但归零操作会产生 1.5 倍违约金（已用部分）；
  - 服务到期后 14 小时内未续费，实例将被删除且 model code 不可恢复。

- **快速模式限制**：
  - 当前仅 `glm-5.2-fast-preview` 单一模型可用，其他模型暂不支持；
  - preview 阶段能力可能变更，不承诺 SLA，不建议用于关键生产环境；
  - 排队机制不保证最大等待时长，极端负载下延迟仍可能升高。

- **共性注意事项**：
  - 两种能力均需业务空间（Workspace）已开通对应地域的模型服务；
  - 缓存效果高度依赖请求内容重复度，实际命中率需通过监控（如 `usage.prompt_tokens_details.cached_tokens`）验证；
  - TPM 预留与快速模式**不可叠加作用于同一 model ID**：`*-fast-preview` 变体本身不支持 TPM 预留，若需容量保障，应先为基线模型（如 `glm-5.2`）创建 TPM 预留，再在其专属 code 后缀追加 `-fast-preview`（需确认控制台是否支持该组合，当前文档未明确）。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


