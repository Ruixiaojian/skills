# model high speed inference

百炼平台提供两种面向高吞吐与低延迟场景的推理加速能力：TPM 预留（保障专属容量）和快速模式（提升单请求输出速度）。二者定位不同，可独立使用或组合使用——TPM 预留解决“能不能稳定跑满”的问题，快速模式解决“单次响应够不够快”的问题。开发者应根据业务对容量确定性（如 SLA 要求）与响应时延（如 TPS/首 token 延迟）的优先级进行选型。

## 支持的模型/功能

- **TPM 预留**：为指定模型锁定专属输入/输出吞吐量（单位：kTPM），确保高峰期不被公共资源限流影响。支持千问、GLM、DeepSeek、Kimi 等多个主流模型，具体列表见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档中的“支持的模型”表格。  
- **快速模式（Fast mode）**：Preview 阶段能力，通过优化推理调度与内存访问，提升单请求输出吞吐（TPS 达 80~100），适用于 AI 编程助手、Agent 多步推理等对首 token 和 token 流速敏感的场景。当前仅支持 `glm-5.2-fast-preview` 模型（[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 文档明确列出），其他模型暂未开放。

> **注意**：两篇文档对“模型支持范围”的描述存在明显差异——TPM 预留文档列出了十余个模型（如 `qwen3.7-max-2026-05-20`、`deepseek-v4-pro` 等），而快速模式文档仅声明 `glm-5.2-fast-preview` 可用。目前无证据表明其他模型已支持快速模式，因此以 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 的明确声明为准，不可自行尝试在非 listed 模型上添加 `-fast-preview` 后缀。

## 关键参数

| 能力类型 | 核心参数 | 说明 |
|----------|----------|------|
| TPM 预留 | `input_tpm` / `output_tpm` | 单位为 kTPM（1 kTPM = 1,000 tokens/min），需按模型实际阶梯系数与缓存折扣估算，详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的“容量计算器”与“长输入阶梯系数”表格。 |
| 快速模式 | 无显式参数 | 仅需将 `model` 设为 `glm-5.2-fast-preview`，并使用专属接入域名（如 `{workspace_id}.cn-beijing.maas.aliyuncs.com`），无需额外 query 或 header。 |

## 使用方式

- **TPM 预留**：创建成功后，系统生成专属模型 code（如 `tpm-qwen37max-xxx`），**必须**在 API 请求中将 `model` 参数替换为此 code 才能生效。标准调用方式不变，但需注意预热期可能引入短暂延迟波动（见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) “创建 TPM 预留”章节示例代码注释）。  
- **快速模式**：直接使用 `model="glm-5.2-fast-preview"` 发起请求，并确保 base_url 指向对应地域的 MaaS 域名（如华北2为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。流式响应中需分别处理 `delta.reasoning_content` 和 `delta.content` 字段（见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 的“使用示例”）。

## 限制和注意事项

- **TPM 预留**：  
  - 预留实例到期后 2 小时内仍可调用，2~14 小时内停止但可续费，14 小时后彻底删除且不可恢复；  
  - 缩容退订按 1.5 倍系数结算已用费用，公式见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) “计费与使用说明”；  
  - 超额请求自动降级至按量计费，不中断服务，但需监控“超额降级统计”避免成本失控。  

- **快速模式**：  
  - 当前为 preview 阶段，接口行为、模型能力及计费规则可能调整，不建议用于生产环境 SLA 保障场景；  
  - 超出 TPM 额度时请求进入排队队列而非立即限流，可能导致端到端延迟升高，需评估业务容忍度；  
  - `glm-5.2-fast-preview` 返回结构含 `reasoning_content` 字段，与标准 `glm-5.2` 不兼容，客户端需适配解析逻辑。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


