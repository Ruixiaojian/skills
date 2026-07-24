# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：**TPM 预留**（保障专属容量）与**快速模式**（提升单请求输出速度）。二者解决不同维度的性能瓶颈：前者确保业务高峰期的容量确定性，后者优化单次响应的 token 生成速率（TPS）。开发者需根据 SLA 要求（如是否容忍限流、是否要求确定性吞吐）选择合适方案。

## 支持的模型/功能

- **TPM 预留**：为指定模型锁定专属输入/输出吞吐量（单位：kTPM），支持千问、GLM、DeepSeek、Kimi 等主流模型，覆盖华北2（北京）和新加坡地域。详情见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **快速模式**：当前仅支持 `glm-5.2-fast-preview` 模型（preview 阶段），通过底层调度与解码优化将 TPS 提升至标准 API 的 1.5~2 倍（达 80~100 TPS），适用于 AI 编程助手、Agent 多步推理等对输出延迟敏感的场景。详情见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。
- > **注意**：两套机制互不兼容——TPM 预留需使用专属 `model` code，而快速模式需显式指定 `-fast-preview` 后缀模型 ID；**不可在同一请求中同时启用二者**。快速模式暂不支持 TPM 预留，其调用仍受公共资源池限流约束（但采用排队而非立即拒绝）。

## 关键参数

| 参数 | TPM 预留 | 快速模式 |
|------|----------|-----------|
| **核心指标** | 输入/输出 kTPM（刚性配额） | TPS（实际输出速率，非配额） |
| **计费单位** | 按天预付 kTPM（输入/输出分开计价） | 按实际输入/输出 token 计费（与标准 API 一致） |
| **缓存支持** | 支持（如 GLM-5.2 缓存命中按 25% 折算输入容量） | 支持（`cached_tokens` 字段可见，单价同标准 API） |
| **长输入处理** | 支持阶梯系数（如 GLM-5.1 在 \[32K, 200K\] 区间输入系数 1.33） | 未明确说明阶梯系数，按标准模型规格执行 |
| **溢出行为** | 可选「自动溢出至按量」或「仅预留容量（返回 429）」 | 请求排队，不立即限流（[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)） |

## 使用方式

- **TPM 预留**：  
  1. 在控制台创建预留实例，获取专属 `model` code；  
  2. 将 API 请求中的 `model` 参数替换为该 code（如 `"qwen37max-20260520-tpm-abc123"`）；  
  3. 调用域名与标准 API 相同（`https://dashscope.aliyuncs.com/...`）。详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

- **快速模式**：  
  1. 使用专用接入域名：`https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`（`{workspace_id}` 和 `{region}` 需从控制台获取）；  
  2. `model` 参数设为 `glm-5.2-fast-preview`；  
  3. 支持[流式输出](../concepts/streaming-output.md)，响应中包含 `reasoning_content` 和 `content` 字段分离推送。详见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。

## 限制和注意事项

- **TPM 预留**：  
  - 创建后需等待实例状态变为「运行中」方可调用；短时间内请求量激增时存在短暂预热期，可能出现延迟波动，建议实现客户端重试或排队机制；  
  - 缩容/退订会产生违约金（已用部分按 1.5 倍系数结算），且退订后专属 `model` code 立即失效；  
  - 服务到期后 14 小时内资源被彻底删除，不可恢复。

- **快速模式**：  
  - 当前为 preview 阶段，模型 ID、性能指标及地域支持可能调整，不建议用于生产环境长期依赖；  
  - 仅支持 `glm-5.2-fast-preview`，其他模型暂无对应快速版本；  
  - 虽支持排队，但队列深度有限，极端高峰仍可能触发限流（返回 `429 Too Many Requests`），需监控 `usage.prompt_tokens_details.cached_tokens` 等字段评估缓存效率。

- > **注意**：文档 1 中提及“PTU 专属部署”属于更高阶的部署形态（物理隔离实例），与本主题的“model high speed inference”无直接关联，不应混淆；其适用场景（高吞吐高性能）和接入方式（替换 `model` code）虽类似 TPM 预留，但技术实现与 SLA 保障等级不同，详见 [模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


