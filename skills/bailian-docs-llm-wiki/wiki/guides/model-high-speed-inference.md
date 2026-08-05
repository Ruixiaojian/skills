# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：TPM 预留（保障专属容量）和快速模式（提升单请求输出速度）。二者定位不同，可独立使用或组合使用——TPM 预留解决**容量稳定性问题**，快速模式解决**单次响应时延问题**。开发者应根据业务对“确定性吞吐”或“端到端延迟”的核心诉求选择方案。

## 支持的模型/功能

- **TPM 预留**：为指定模型锁定专属 [Token](../concepts/token.md)s Per Minute（TPM）吞吐量，确保高峰期不被公共池限流影响。支持千问、GLM、DeepSeek、Kimi 等主流模型，覆盖华北2（北京）与新加坡地域。具体支持列表详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档中的「支持的模型」表格。
  
- **快速模式（Fast mode）**：当前为 preview 阶段，仅支持 `glm-5.2-fast-preview` 模型，通过优化调度与显存管理提升 TPS 至标准 API 的 1.5~2 倍（达 80~100 TPS），适用于 AI 编程助手、Agent 多步推理等对输出速度敏感的场景。详细支持模型与计费单价见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 文档。

> **注意**：两篇原始文档在模型命名规范上存在不一致。`tpm-reservation.md` 中使用 `glm-5.2`（无 `-fast-preview` 后缀），而 `fast-mode.md` 明确要求使用 `glm-5.2-fast-preview` 作为 model 参数。二者为不同服务形态，不可混用；调用快速模式必须使用带 `-fast-preview` 后缀的专用 model ID。

## 关键参数

| 参数 | TPM 预留 | 快速模式 |
|------|----------|----------|
| **核心指标** | 输入/输出 kTPM（1 kTPM = 1,000 tokens/min） | 无显式容量参数，依赖后端自动调度队列 |
| **溢出策略** | 可选：自动溢出至按量计费（默认）或仅预留容量返回 429 | 请求超出当前可用算力时进入排队队列，不立即限流（[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)） |
| **缓存折扣** | 支持（如 GLM-5.2 缓存命中部分按 25% 折算容量） | 支持（`glm-5.2-fast-preview` 在北京/新加坡均支持缓存命中计费） |
| **长输入阶梯系数** | 部分模型支持（如 glm-5.1 在 \[32K, 200K\] 区间输入系数为 1.33） | 文档未提及阶梯系数，实际行为以控制台或最新 API 响应为准 |

## 使用方式

- **TPM 预留**：创建成功后，系统生成专属模型 code（如 `tpm-qwen38max-abc123`），需将 API 请求中的 `model` 参数替换为此 code。接入域名与标准 API 一致（如 `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`）。详情参见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中「创建 TPM 预留」与「API 接入」章节。

- **快速模式**：直接使用专用 model ID（如 `glm-5.2-fast-preview`），**必须使用专属接入域名**：`https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1/chat/completions`（region 如 `cn-beijing`）。标准 dashscope 域名不支持快速模式。示例见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 文档中的 curl 与 Python 调用片段。

> **注意**：快速模式 preview 阶段能力可能调整，且其 model ID 与 TPM 预留生成的专属 code 完全独立——不能将 `glm-5.2-fast-preview` 用于 TPM 预留，也不能将 TPM 预留生成的 code 用于快速模式调用。

## 限制和注意事项

- **TPM 预留**：
  - 付费周期按**自然日**计算（当日 00:00 到次日 00:00），非连续 24 小时，购买时间影响实际有效时长（详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)）；
  - 扩缩容操作中（变配中状态）服务不中断，但归零输入/输出 TPM 会触发 1.5 倍违约金结算；
  - 专属模型 code 在实例到期 14 小时后永久删除，不可恢复。

- **快速模式**：
  - 当前仅支持 `glm-5.2-fast-preview`，不支持其他模型；
  - 返回结构含 `reasoning_content` 字段，流式响应需分别处理 `delta.reasoning_content` 和 `delta.content`；
  - 因处于 preview 阶段，错误码、SLA 及功能边界可能变更，请关注控制台公告。

- **共性注意事项**：
  - 两种模式均需确保业务空间已开通对应地域的模型服务权限；
  - 高并发突增时，TPM 预留实例需短暂预热（数秒），期间可能出现延迟波动，建议客户端实现重试或排队机制（[TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中明确提示）；
  - 快速模式的排队机制不保证绝对低延迟，极端负载下仍可能产生可观排队时延。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


