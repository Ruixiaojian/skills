# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：**TPM 预留（[Token](../concepts/token.md) Per Minute Reservation）** 和 **快速模式（Fast Mode）**。前者通过预购专属容量保障确定性吞吐与稳定性，适用于流量可预估、不可接受限流的关键业务；后者通过底层调度与硬件优化提升单请求输出速度（TPS），适用于对响应延迟敏感的实时交互场景。二者可独立使用，也可组合部署（例如在 TPM 预留实例上启用 fast 模型）。

## 支持的模型/功能

- **TPM 预留**：为指定模型锁定专属推理吞吐量（单位：kTPM），支持输入/输出维度独立配置，确保高峰期调用不受公共资源池限流影响。支持模型详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档中的“支持的模型”表格，覆盖千问、GLM、DeepSeek、Kimi 等主流模型的多个版本（如 `qwen3.7-max-2026-05-20`、`glm-5.2`、`deepseek-v4-flash` 等），按地域（华北2/新加坡）分列定价与阶梯系数。

- **快速模式**：当前仅支持 `glm-5.2-fast-preview` 模型（[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)），处于 preview 阶段，提供 1.5~2 倍于标准 API 的 TPS（达 80~100 TPS），并引入排队机制缓解瞬时超载，不立即返回 429。

> **注意**：两篇文档对 `glm-5.2` 的缓存折扣描述存在差异——TPM 预留文档称其支持 `0.25` 缓存命中折扣（即缓存部分按 25% 折算容量），而快速模式文档未提及缓存折扣，且计费单价中“缓存命中”列为 `4元`（疑似指缓存命中时的输入单价）。实际缓存行为以 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中明确列出的参数为准，快速模式因处于 preview 阶段，其缓存策略可能尚未同步或未开放配置。

## 关键参数

| 参数 | TPM 预留 | 快速模式 |
|------|----------|----------|
| **核心指标** | 输入/输出 kTPM（1 kTPM = 1,000 tokens/min） | TPS（tokens per second），实测 80~100 |
| **计费单位** | 预付费（按天，kTPM × 天数） | 按 token 计费（与标准 API 一致） |
| **溢出策略** | 可选：自动溢出至按量计费（默认）或仅预留容量（返回 429） | 请求排队，不立即限流 |
| **专属标识** | 生成唯一 `dedicated model code`，需替换 API 中 `model` 字段 | 使用固定模型 ID（如 `glm-5.2-fast-preview`） |
| **接入域名** | 通用 DashScope 域名（`https://dashscope.aliyuncs.com/...`） | 地域专属域名（`https://{workspace_id}.{region}.maas.aliyuncs.com/...`） |

## 使用方式

- **TPM 预留**：  
  1. 在百炼控制台创建预留实例，选择目标模型、输入/输出 kTPM、购买时长及溢出策略；  
  2. 获取详情页中的 **专属模型 code**；  
  3. 将 API 请求中的 `model` 参数替换为该 code（[TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中提供了 Python/curl 示例）；  
  > 注意：实例需处于“运行中”状态方可生效；首次大流量请求前存在短暂预热期，建议实现客户端重试。

- **快速模式**：  
  1. 确保业务空间已开通对应地域（如华北2）的 MaaS 服务；  
  2. 从 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取 `workspace_id`；  
  3. 构造请求 URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`；  
  4. 设置 `model: "glm-5.2-fast-preview"`（[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 提供了 OpenAI 兼容 SDK 调用示例）；  
  > 注意：`stream: true` 时需分别处理 `delta.reasoning_content` 和 `delta.content` 字段。

## 限制和注意事项

- **TPM 预留**：  
  - 预留容量按日计费，缩容/退订按 1.5 倍系数结算违约金；  
  - 服务到期后 2 小时内仍可调用，14 小时后实例删除且不可恢复；  
  - 专属模型 code 在退订后立即失效，回退至公共资源（按量计费）。

- **快速模式**：  
  - 当前仅 `glm-5.2-fast-preview` 可用，其他模型暂不支持；  
  - 处于 preview 阶段，接口行为、性能指标及计费规则可能调整，不建议用于生产环境长期依赖；  
  - 不支持与 TPM 预留直接绑定（即无法为 `glm-5.2-fast-preview` 创建 TPM 预留），但可在同一业务空间下并行使用两者。

- **共性限制**：  
  - 两种模式均要求请求符合百炼 API 规范（如 `messages` 格式、`stream` 参数等）；  
  - 缓存能力依赖模型本身支持（如 `glm-5.2` 支持缓存，`qwen3.6-flash` 不支持），具体参见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的“长输入阶梯系数和缓存折扣”表格。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


