# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：TPM 预留（保障专属容量）与快速模式（提升单请求输出速度）。二者定位不同——TPM 预留解决**容量确定性问题**（避免公共池限流），快速模式解决**单次响应时效性问题**（提升 TPS 与首 token 延迟）。开发者需根据业务 SLA（如是否容忍 429、是否要求 <500ms 首 token）选择组合使用。两者均通过替换 `model` 参数接入，无需修改 SDK 或协议。

## 支持的模型/功能

- **TPM 预留**：为指定模型锁定专属输入/输出吞吐量（单位：kTPM），支持千问、GLM、DeepSeek、Kimi 等主流模型，覆盖华北2（北京）和新加坡地域。详情见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **快速模式**：当前仅支持 `glm-5.2-fast-preview` 模型（北京、新加坡双地域），提供 1.5~2 倍于标准 API 的 TPS（达 80~100 TPS），适用于 AI 编程助手、Agent 多步推理等对输出速度敏感的场景。详情见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。
- > **注意**：两文档对 `glm-5.2` 的缓存折扣描述存在差异。[TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 明确其缓存折扣为 0.25；而 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 在计费表中单独列出“缓存命中”单价（4元/百万[Token](../concepts/token.md)），未说明是否复用相同缓存机制。实际调用时请以控制台最新参数或 `usage.prompt_tokens_details.cached_tokens` 字段为准。

## 关键参数

| 参数 | TPM 预留 | 快速模式 |
|------|----------|-----------|
| **核心标识** | 专属模型 code（如 `qwen3.7-max-2026-05-20-tpm-xxxxx`），由控制台生成 | 固定 model ID（`glm-5.2-fast-preview`） |
| **容量单位** | 输入/输出 kTPM（1 kTPM = 1,000 tokens/分钟） | 无独立容量单位，按 token 计费，但受全局 TPM 配额排队约束 |
| **溢出行为** | 可选：自动溢出至按量计费（默认）或返回 429 | 请求进入排队队列，不立即限流（[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)） |
| **缓存支持** | 支持（如 GLM-5.2 缓存命中部分按 25% 折算容量） | 支持（计费表中单独列出缓存命中单价） |
| **长输入阶梯** | 部分模型支持（如 GLM-5.1 在 [32K,200K] 区间输入系数 1.33） | 文档未提及阶梯系数，按标准 token 计费 |

## 使用方式

- **TPM 预留**：  
  1. 在百炼控制台创建预留实例，获取专属模型 code；  
  2. 将 API 请求中的 `model` 替换为该 code；  
  3. 调用域名与标准 API 一致（`https://dashscope.aliyuncs.com/...`）。示例见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的 Python/curl 代码片段。

- **快速模式**：  
  1. 使用 `glm-5.2-fast-preview` 作为 `model` 参数；  
  2. **必须使用专属域名**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（北京）或对应新加坡地域域名；  
  3. 支持流式响应，`reasoning_content` 与 `content` 分离推送。完整示例见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。

- > **注意**：快速模式为 preview 阶段，[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 明确提示“能力与规格可能随版本调整”，生产环境使用前需评估兼容性风险。

## 限制和注意事项

- **TPM 预留**：  
  - 创建后需等待实例状态变为“运行中”方可调用；  
  - 短时间内请求量快速拉升需预热，预热期间可能出现延迟波动，建议实现请求排队或重试机制（见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)）；  
  - 服务到期后 2 小时内仍可调用，但 14 小时后实例删除不可恢复。

- **快速模式**：  
  - 仅限 `glm-5.2-fast-preview`，不支持其他模型；  
  - 不支持 `stream=false` 下的 `reasoning_content` 字段（仅流式返回）；  
  - 返回结构中 `usage.completion_tokens_details.reasoning_tokens` 字段统计思考 token，计入总输出 token 计费。

- **共性限制**：  
  - 两者均不改变模型本身能力（如上下文长度、[多模态](../concepts/multi-modal.md)支持），仅优化调度与资源分配；  
  - TPM 预留与快速模式**不可叠加使用**：`glm-5.2-fast-preview` 不支持 TPM 预留，TPM 预留的模型 code 也不支持快速模式协议。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


