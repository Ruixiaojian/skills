# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：TPM 预留（保障专属容量）与快速模式（提升单请求输出速度）。二者定位不同，可独立使用或组合使用——TPM 预留解决**容量稳定性问题**，快速模式解决**单次响应时延问题**。开发者需根据业务对 SLA（如 P99 延迟、峰值并发容忍度）和成本模型的要求进行选型。

## 支持的模型/功能

- **TPM 预留**：为指定模型锁定专属 Tokens Per Minute（TPM）吞吐量，确保高峰期调用不被公共池限流影响。支持千问、GLM、DeepSeek、Kimi 等主流模型，覆盖华北2（北京）和新加坡地域。具体支持列表详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档中的“支持的模型”表格。
  
- **快速模式（Fast mode）**：当前为 preview 阶段，仅支持 `glm-5.2-fast-preview` 模型（北京/新加坡双地域），通过优化调度与计算流水线，将 TPS 提升至标准 API 的 1.5~2 倍（达 80~100 TPS），适用于 AI 编程助手、Agent 多步推理等对输出速度敏感的场景。详细支持模型与计费单价见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 文档。

> **注意**：TPM 预留与快速模式**不可叠加生效**。`glm-5.2-fast-preview` 是独立模型 ID，不支持为其创建 TPM 预留；反之，已预留的模型（如 `qwen3.7-max-2026-05-20`）无法通过追加参数启用快速模式。二者属于正交能力路径。

## 关键参数

| 参数 | TPM 预留 | 快速模式 |
|------|----------|----------|
| **核心指标** | 输入/输出 kTPM（1 kTPM = 1,000 tokens/min） | 无显式容量参数；依赖后端自动队列调度 |
| **溢出策略** | 可选：自动溢出至按量计费（默认）或仅预留容量返回 429 | 请求超出瞬时处理能力时进入排队队列，不立即限流（[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)） |
| **缓存折扣** | 支持（如 GLM-5.2 缓存命中部分按 25% 折算输入容量） | 支持（`glm-5.2-fast-preview` 缓存命中单价为 4 元/百万 token） |
| **长输入阶梯系数** | 部分模型支持（如 GLM-5.1 在 \[32K, 200K\] 区间输入系数为 1.33） | 不适用（当前仅支持固定输入长度上限，未公开阶梯规则） |

## 使用方式

- **TPM 预留**：  
  1. 在百炼控制台创建预留实例，获取专属模型 code（如 `tpm-qwen37max-abc123`）；  
  2. 将 API 请求中的 `model` 参数替换为该 code；  
  3. 调用域名与标准 API 一致（`https://dashscope.aliyuncs.com/...`），无需更换 endpoint。  
  示例见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的 Python/curl 调用片段。

- **快速模式**：  
  1. 直接使用 `glm-5.2-fast-preview` 作为 `model` 参数值；  
  2. **必须使用专属域名**：`https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`（region 如 `cn-beijing`）；  
  3. workspace_id 需从 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取。  
  完整调用示例参见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 文档。

## 限制和注意事项

- **TPM 预留**：  
  - 创建后需等待实例状态变为“运行中”方可调用；短时间内请求量快速拉升需预热，预热期间可能出现延迟波动，建议实现客户端重试或排队机制；  
  - 服务到期后 2 小时内仍可调用，但 14 小时后实例删除且不可恢复；  
  - 缩容/退订按 1.5 倍系数结算违约金，详情见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 计费说明。

- **快速模式**：  
  - 当前为 preview 阶段，能力与规格可能随版本调整，不建议用于生产环境的关键链路；  
  - 返回结构含 `reasoning_content` 字段（用于思考过程），流式响应需分别处理 `delta.reasoning_content` 和 `delta.content`；  
  - 错误码处理逻辑与标准 API 一致，详见 [错误码](https://help.aliyun.com/zh/model-studio/error-code)，但排队超时等新场景可能引入额外错误类型。

- **通用限制**：  
  - 两种模式均不支持自定义模型部署；  
  - TPM 预留专属 code 仅在对应地域有效（如北京预留的 code 不能在新加坡调用）；  
  - 快速模式暂不支持 `stream: true` 以外的高级参数（如 `temperature`, `top_p`）的精细调控，以文档为准。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


