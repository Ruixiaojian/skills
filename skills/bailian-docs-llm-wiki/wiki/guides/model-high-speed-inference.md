# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：TPM 预留（保障专属容量）与快速模式（提升单请求输出速度）。二者定位不同，可独立使用或组合使用——TPM 预留解决「容量确定性」问题，快速模式解决「响应时延敏感性」问题。开发者需根据业务 SLA（如是否容忍限流、是否要求首字节延迟 <200ms）选择合适方案。

## 支持的模型/功能

- **TPM 预留**：为指定模型锁定专属 TPM 容量，支持千问、GLM、DeepSeek、Kimi 等主流模型（含多版本），覆盖华北2（北京）和新加坡地域。详情见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **快速模式**：当前仅支持 `glm-5.2-fast-preview` 模型（北京/新加坡双地域），处于 preview 阶段，提供 1.5~2 倍于标准 API 的 TPS（达 80~100 TPS），适用于 AI 编程助手、Agent 多步推理等对输出速度敏感的场景。详情见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。
- > **注意**：文档 1 中列出的 `千问3.7-Max-2026-05-20` 等模型虽支持 TPM 预留，但**不支持快速模式**；文档 2 明确限定快速模式仅适配 `glm-5.2-fast-preview`。二者模型支持范围无交集，不可混用。

## 关键参数

| 能力 | 核心参数 | 说明 |
|------|----------|------|
| TPM 预留 | `input_tpm` / `output_tpm`（单位：kTPM） | 必填，分别控制输入/输出方向的每分钟 token 吞吐上限；起步值与步长因模型而异，以控制台实时展示为准。详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。 |
| TPM 预留 | `overflow_strategy` | 可选 `"auto_fallback"`（默认，超限自动降级为按量计费）或 `"reject"`（超限返回 HTTP 429）。 |
| 快速模式 | `model` 参数值 | 必须设为 `glm-5.2-fast-preview`，且需使用专属域名 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（北京）或对应新加坡域名。 |
| 快速模式 | `stream` | 推荐启用流式响应（`stream=true`），以获得更低的端到端延迟；流式返回中 `reasoning_content` 和 `content` 字段分离推送。 |

## 使用方式

- **TPM 预留**：创建成功后，系统生成专属模型 code（如 `qwen3.7-plus-2026-05-26-tpm-abc123`），**必须将 API 请求中的 `model` 参数替换为此 code**，否则仍走公共资源池。调用域名与标准 API 一致（`https://dashscope.aliyuncs.com/...`）。示例见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **快速模式**：无需变更 `model` 参数以外的任何配置，仅需：
  1. 使用专属接入域名（非 `dashscope.aliyuncs.com`）；
  2. 将 `model` 设为 `glm-5.2-fast-preview`；
  3. （推荐）启用 `stream=true` 并处理 `reasoning_content` 字段。
- > **注意**：快速模式**不支持 TPM 预留的专属 model code**。若同时需要容量保障与高速输出，需先为 `glm-5.2` 创建 TPM 预留（获得如 `glm-5.2-tpm-xyz789` 的 code），再在快速模式域名下调用 `glm-5.2-fast-preview` —— 二者资源池物理隔离，TPM 预留额度**不覆盖**快速模式调用。

## 限制和注意事项

- **TPM 预留**：
  - 预留实例到期后 2 小时内仍可调用，之后进入“已停止”状态（14 小时内可续费），超 14 小时自动删除且不可恢复；
  - 缩容/退订需支付违约金（已用部分按 1.5 倍系数结算）；
  - 首次调用量激增时存在短暂预热期，可能引发延迟波动，建议客户端实现重试或排队机制。
- **快速模式**：
  - 当前为 preview 阶段，模型 ID、性能指标、计费策略可能调整，不建议用于生产环境长期依赖；
  - 不支持缓存（文档 2 中 `缓存命中` 列显示为 `4元`，实为固定单价，非折扣）；
  - 错误码体系与标准 API 不完全一致，需单独查阅 [错误码](https://help.aliyun.com/zh/model-studio/error-code)。
- **共性限制**：
  - 两种能力均不改变模型本身的能力边界（如上下文长度、推理逻辑）；
  - TPM 预留的“专属容量”仅保障吞吐量，不承诺 P99 延迟；快速模式提升 TPS，但不保证单请求最低延迟。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


