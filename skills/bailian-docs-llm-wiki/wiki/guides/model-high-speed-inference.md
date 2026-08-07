# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：**TPM 预留**（保障专属容量）与**快速模式**（提升单请求输出速度）。二者解决不同维度的性能瓶颈：前者确保业务高峰期的确定性吞吐（TPM 级别 SLA），后者优化单次调用的 token 生成速率（TPS 提升）。开发者需根据流量稳定性、延迟敏感度和成本模型选择合适方案。

## 支持的模型/功能

- **TPM 预留**：为指定模型锁定专属输入/输出吞吐量（单位：kTPM），支持千问、GLM、DeepSeek、Kimi 等主流模型，覆盖华北2（北京）和新加坡地域。详情见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **快速模式**：当前仅支持 `glm-5.2-fast-preview` 模型（北京/新加坡双地域），通过底层调度与解码优化实现 1.5~2 倍 TPS 提升，适用于 AI 编程助手、Agent 多步推理等对首 token 和输出流速敏感的场景。详情见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。
- > **注意**：两套机制互不兼容——TPM 预留必须使用专属 model code 调用，而快速模式需显式指定 `-fast-preview` 后缀 model ID；不可将 TPM 预留的专属 code 用于快速模式，反之亦然。

## 关键参数

| 参数 | TPM 预留 | 快速模式 |
|------|----------|-----------|
| **核心指标** | 输入/输出 kTPM（刚性配额） | TPS（80~100，非配额制） |
| **计费单位** | 按天预付费（kTPM × 天数） | 按实际 token 计费（输入/输出单价独立） |
| **超额行为** | 可选：自动溢出至按量（默认）或返回 429 | 请求排队，不立即限流（无 429） |
| **缓存支持** | 支持（不同模型缓存折扣率不同，如 GLM-5.2 为 0.25） | 支持（`cached_tokens` 字段返回命中量） |
| **长输入处理** | 支持阶梯系数（如 GLM-5.1 在 \[32K,200K\] 区间输入系数 1.33） | 未明确说明阶梯系数，按标准 token 计费 |

## 使用方式

- **TPM 预留**：  
  1. 在控制台创建预留实例，获取专属 `model` code；  
  2. 将 API 请求中的 `model` 参数替换为该 code（如 `qwen38max-tpm-abc123`）；  
  3. 调用域名与标准 API 一致（`https://dashscope.aliyuncs.com/...`）。详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的「创建 TPM 预留」与「API 接入」章节。

- **快速模式**：  
  1. 直接在请求中指定 fast model ID（如 `glm-5.2-fast-preview`）；  
  2. 使用专属接入域名：`https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`（region 为 `cn-beijing` 或 `ap-southeast-1`）；  
  3. 流式响应中需分别处理 `delta.reasoning_content` 和 `delta.content` 字段。详见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 中的「使用方式」与「使用示例」章节。

## 限制和注意事项

- **TPM 预留**：  
  - 「按天」计费按自然日结算（当日 00:00 到期），非 24 小时滚动，建议开启自动续费；  
  - 扩缩容操作会触发 1.5 倍违约金计算，归零后专属 model code 仍保留但不再计费；  
  - 实例到期 14 小时后彻底删除且不可恢复，code 失效。

- **快速模式**：  
  - 当前为 preview 阶段，模型 ID、性能指标及计费规则可能调整；  
  - 不支持所有标准 API 参数（如部分采样参数兼容性需验证）；  
  - 返回结构含 `reasoning_content` 字段，需适配客户端解析逻辑。

- **共性约束**：  
  - 两者均要求业务空间已开通对应地域的模型服务权限；  
  - TPM 预留需提前估算容量（推荐使用控制台内置 [TPM 容量计算器](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)）；  
  - 快速模式暂不支持 TPM 预留绑定，其调用走独立资源池，不受公共限流影响但也不享受专属容量保障。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


