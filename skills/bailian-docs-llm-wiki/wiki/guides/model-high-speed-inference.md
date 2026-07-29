# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：**TPM 预留（[Token](../concepts/token.md) Per Minute Reservation）** 和 **快速模式（Fast Mode）**。前者通过预付费锁定专属容量保障稳定性，后者通过优化调度与计算路径提升单位时间输出吞吐量（TPS）。二者可独立使用，也可组合（如在 TPM 预留实例上启用 fast-preview 模型），适用于对响应速度、确定性 SLA 或成本敏感度有不同侧重的生产场景。

## 支持的模型与功能

- **TPM 预留**：为指定模型提供刚性容量保障，支持千问（Qwen）、GLM、DeepSeek、Kimi 等主流模型的多个版本（如 `qwen3.7-max-2026-05-20`、`glm-5.2`、`deepseek-v4-pro` 等），覆盖华北2（北京）和新加坡地域。详情见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **快速模式**：当前仅支持 `glm-5.2-fast-preview` 模型（北京/新加坡双地域），处于 preview 阶段，提供 1.5~2 倍于标准 API 的 TPS（最高达 80~100 TPS），并支持[流式输出](../concepts/streaming-output.md)中的 `reasoning_content` 分离推送。详情见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。
- > **注意**：两文档中对 `glm-5.2` 的缓存折扣描述存在差异——[TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 明确其缓存命中部分按 25% 折算容量；而 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 表格中标注“缓存命中”为 `4元`（疑似误标为单价），实际缓存机制应以 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 文档为准，快速模式继承基础模型的缓存能力但未额外调整折扣率。

## 关键参数

| 参数 | TPM 预留 | 快速模式 |
|------|----------|-----------|
| **核心指标** | 输入/输出 kTPM（1 kTPM = 1,000 tokens/min） | TPS（tokens per second），实测 80~100 |
| **计费单位** | 预付费（按天，kTPM × 天数） + 溢出按量 | 按 token 计费（输入/输出单价独立，与标准 API 一致） |
| **容量保障** | 专属、刚性兑付（不共享） | 无专属容量，依赖公共资源池 + 排队缓冲 |
| **溢出行为** | 可选：自动降级至按量（默认）或返回 429 | 请求进入排队队列，不立即限流 |
| **缓存支持** | 支持（各模型有明确缓存折扣率与阶梯系数） | 继承基础模型缓存能力（如 `glm-5.2-fast-preview` 对应 `glm-5.2` 的 25% 缓存折扣） |

## 使用方式

- **TPM 预留**：  
  1. 在控制台创建预留实例，获取专属 `model` code（如 `tpm-qwen37max-abc123`）；  
  2. 将 API 请求中的 `model` 字段替换为该 code；  
  3. 调用域名与标准 API 一致（`https://dashscope.aliyuncs.com/...`）。详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的「创建 TPM 预留」与「API 接入」章节。

- **快速模式**：  
  1. 直接使用 fast-preview 模型 ID（如 `glm-5.2-fast-preview`）作为 `model` 参数；  
  2. **必须使用专属接入域名**：`https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`（region 如 `cn-beijing`）；  
  3. workspace_id 需在业务空间管理页面切换地域后查看。示例见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 中的 curl 与 Python 调用片段。

- > **注意**：快速模式 preview 版本不支持与 TPM 预留的专属 model code 混用——即不能将 `tpm-glm52-xxx` 作为 `glm-5.2-fast-preview` 的前缀。若需同时享受容量保障与高速输出，须为 `glm-5.2-fast-preview` 单独购买 TPM 预留（当前控制台暂未开放该模型的 TPM 预留入口，属能力缺口，建议关注后续更新）。

## 限制和注意事项

- **TPM 预留**：  
  - 创建后需等待实例状态变为「运行中」方可调用；  
  - 短时流量激增需预热（可能引发短暂延迟波动），建议实现客户端重试与排队；  
  - 退订后专属 model code 立即失效，请求回退至公共资源；  
  - 缩容/退订按 1.5 倍系数结算已用费用（见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 计费说明）。

- **快速模式**：  
  - 仅 preview 阶段，模型列表、性能指标与接口行为可能调整，不承诺长期兼容；  
  - 不支持所有标准 API 参数（如部分采样参数可能被忽略），以实际返回结果为准；  
  - 流式响应中 `reasoning_content` 与 `content` 字段分离推送，客户端需分别处理；  
  - 错误码体系与标准 API 一致，但排队超时等新场景可能引入额外错误类型（参见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 错误码文档）。

- **共性限制**：  
  - 两类能力均不改变模型本身的能力边界（如上下文长度、多模态支持等），仅优化推理调度与资源供给；  
  - TPM 预留与快速模式不可跨地域复用（北京预留不适用于新加坡 endpoint，反之亦然）。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


