# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：TPM 预留（保障专属容量）与快速模式（提升单请求输出速度）。二者定位不同，可独立使用或组合使用——TPM 预留解决“容量确定性”问题，快速模式解决“响应实时性”问题。开发者需根据业务 SLA（如是否容忍限流、是否要求首 token 延迟 <200ms）选择合适方案。

## 支持的模型/功能

- **TPM 预留**：为指定模型锁定专属 TPM（[Token](../concepts/token.md)s Per Minute）吞吐量，确保高峰期调用不被公共池限流影响。支持千问、GLM、DeepSeek、Kimi 等主流模型，覆盖华北2（北京）和新加坡地域。具体支持列表详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档中的「支持的模型」表格。
  
- **快速模式（Fast mode）**：当前为 preview 阶段，仅支持 `glm-5.2-fast-preview` 模型（北京/新加坡双地域），通过优化推理调度与内存复用，将 TPS 提升至标准 API 的 1.5~2 倍（典型值 80~100 TPS），适用于 AI 编程助手、Agent 多步推理等对输出速度敏感的场景。详细支持模型与计费单价见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 文档。

> **注意**：两篇原始文档对模型支持范围存在明显差异——TPM 预留文档列出十余个模型（含 Qwen3.7-Max、DeepSeek-v4-Pro 等），而快速模式文档仅明确支持 `glm-5.2-fast-preview`。快速模式暂未开放其他模型的 fast 变体，不可自行拼接如 `qwen3.6-flash-2026-04-16-fast-preview` 等 model ID，否则将返回 404 错误。

## 关键参数

| 参数 | TPM 预留 | 快速模式 |
|------|----------|----------|
| **核心指标** | 输入/输出 kTPM（1 kTPM = 1,000 tokens/min） | TPS（[Token](../concepts/token.md)s Per Second），实测 80~100 |
| **容量保障** | 刚性兑付：预留容量内 100% 服务可用，不受公共限流影响 | 无专属容量保障；超出 TPM 额度时请求排队，不立即限流（但排队超时仍返回 429） |
| **溢出策略** | 创建时可选：<br>• 自动溢出（默认）→ 超额请求降级为按量计费<br>• 仅预留容量 → 超额直接返回 429 | 无显式溢出策略；依赖底层排队机制，排队时长受全局负载影响 |
| **缓存折扣** | 支持（如 GLM-5.2 缓存命中部分按 25% 折算输入容量） | 支持（`glm-5.2-fast-preview` 缓存命中单价为 4 元/百万 token） |
| **长输入阶梯系数** | 部分模型支持（如 GLM-5.1 在 \[32K,200K\] 区间输入系数 1.33） | 文档未提及阶梯系数，实际按标准输入长度计费 |

## 使用方式

- **TPM 预留**：创建成功后获取专属 `model` code（如 `qwen3.7-plus-2026-05-26-tpm-xxxxx`），在 API 请求中替换标准 model ID 即可生效。接入域名与标准 API 一致（`https://dashscope.aliyuncs.com/...`）。示例见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的 Python/curl 调用片段。

- **快速模式**：直接使用 `glm-5.2-fast-preview` 作为 model ID，并**必须使用专属域名**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（北京）或对应新加坡地域域名。标准 dashscope 域名不支持快速模式。示例见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 文档。

> **注意**：快速模式要求显式指定 workspace_id 并使用 maas.aliyuncs.com 域名，若错误使用 dashscope.aliyuncs.com 域名调用 `glm-5.2-fast-preview`，将返回 404 或 400 错误，而非降级到标准模式。

## 限制和注意事项

- **TPM 预留**
  - 预留实例状态变化有延迟窗口：服务到期后 2 小时内仍可调用，2~14 小时内实例已停止但可续费，14 小时后彻底删除且不可恢复。
  - 扩缩容操作期间服务不中断，但归零（输入/输出 TPM 设为 0）会触发 1.5 倍违约金结算。
  - 首次大流量突增时存在短暂预热期（秒级），期间可能出现延迟波动，建议客户端实现重试或排队机制。

- **快速模式**
  - 当前为 preview 阶段，API 行为、模型能力、支持地域可能随时调整，不承诺向后兼容。
  - 流式响应中新增 `reasoning_content` 字段（用于思考过程），需客户端适配解析逻辑；非流式响应中该字段与 `content` 同时返回。
  - 不支持与 TPM 预留叠加使用：`glm-5.2-fast-preview` 无法绑定 TPM 预留，其调用走独立资源池，按 token 计费且无专属容量保障。

- **共性限制**
  - 两种模式均不改变模型本身的能力边界（如上下文长度、多模态支持），仅优化推理执行路径。
  - 缓存命中率高度依赖请求内容重复性，实际效果需以线上监控数据为准，不可仅依赖理论折扣系数估算成本。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


