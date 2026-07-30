# model high speed inference

百炼平台提供两种面向高吞吐、低延迟推理场景的加速能力：**TPM 预留（[Token](../concepts/token.md) Per Minute reservation）** 和 **快速模式（Fast mode）**。前者通过预付费锁定专属推理容量，保障业务高峰期的确定性 SLA；后者通过优化调度与计算路径，在标准 API 基础上提升输出 TPS（1.5~2 倍），适用于对响应速度敏感的实时交互场景。二者可独立使用，不互斥，但接入方式、计费模型与适用边界有本质区别。

## 支持的模型/功能

- **TPM 预留**：为指定模型（如 `qwen3.7-max-2026-05-20`、`glm-5.2`、`deepseek-v4-pro` 等）提供刚性容量保障，支持按天预付费购买输入/输出 kTPM，并生成专属模型 code。详情见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **快速模式**：当前仅开放 `glm-5.2-fast-preview` 模型（北京/新加坡地域），处于 preview 阶段，提供更高 TPS（80~100）和排队式限流策略，无需预留容量即可启用。详情见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。
- > **注意**：两套机制支持的模型集合无交集——TPM 预留覆盖多款主流大模型（含 Qwen、GLM、DeepSeek、Kimi），而快速模式目前仅支持 `glm-5.2-fast-preview`。文档 1 中列出的 `glm-5.2` 不等同于文档 2 的 `glm-5.2-fast-preview`，二者为不同模型实例，不可混用。

## 关键参数

| 参数 | TPM 预留 | 快速模式 |
|------|----------|-----------|
| **核心指标** | 输入/输出 kTPM（1 kTPM = 1,000 tokens/min） | TPS（80~100），无显式容量配额 |
| **计费单位** | 预付费（按天 × kTPM），预留内调用不额外计费；溢出部分按 token 计费 | 按实际输入/输出 token 计费，价格见[模型调用计费](https://help.aliyun.com/zh/model-studio/model-pricing) |
| **缓存折扣** | 支持（如 `glm-5.2` 缓存命中部分按 25% 折算容量） | 支持（`glm-5.2-fast-preview` 缓存命中单价为 4 元/百万 token） |
| **长输入阶梯系数** | 部分模型支持（如 `glm-5.1` 在 `[32K, 200K]` 区间输入系数为 1.33） | 文档未说明，当前默认无阶梯系数 |

## 使用方式

- **TPM 预留**：  
  1. 在控制台创建预留实例，获取专属模型 code（如 `tpm-qwen37max-abc123`）；  
  2. 将 API 请求中的 `model` 字段替换为该 code；  
  3. 调用域名与标准 API 一致（`https://dashscope.aliyuncs.com/...`）。详见 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) 中的「创建 TPM 预留」与「API 接入」章节。

- **快速模式**：  
  1. 使用专属域名：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（需从[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取 workspace_id）；  
  2. 直接指定 `model="glm-5.2-fast-preview"`，无需修改其他参数；  
  3. 支持流式响应，返回结构含 `reasoning_content` 与 `content` 字段分离。详见 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md) 中的「使用方式」与「使用示例」章节。

## 限制和注意事项

- **TPM 预留**：  
  - 创建后需等待实例状态变为「运行中」方可调用；短时间内请求量快速拉升时存在短暂预热期，可能出现延迟波动，建议实现客户端重试或排队机制；  
  - 服务到期后 2 小时内仍可调用，2~14 小时内实例已停止但可续费，14 小时后实例删除且不可恢复；  
  - 缩容/退订将按 1.5 倍系数结算违约金，退订后专属 model code 失效。

- **快速模式**：  
  - 当前为 preview 阶段，能力与规格可能随版本调整，不承诺长期兼容；  
  - 超出系统承载能力时请求进入排队队列，而非立即返回 429；  
  - 不支持 TPM 预留叠加使用（即不能为 `glm-5.2-fast-preview` 创建 TPM 预留）；  
  - > **注意**：文档 2 明确要求使用 `maas.aliyuncs.com` 域名，而文档 1 的 TPM 预留调用仍走 `dashscope.aliyuncs.com`。二者域名隔离，不可混用，否则请求将失败。

## 来源文档

- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


