# model high speed inference

百炼平台提供两种面向高吞吐、低延迟推理场景的核心能力：**快速模式（Fast mode）** 与 **TPM 预留（TPM Reservation）**。二者分别从模型侧优化与资源侧保障两个维度提升推理性能：快速模式通过轻量级推理路径实现更高 TPS（1.5~2 倍于标准 API），适用于对输出速度敏感的实时交互场景；TPM 预留则为指定模型锁定专属吞吐容量，确保业务高峰期不受公共资源限流影响。两者可独立使用，也可组合部署以兼顾性能与稳定性。

## 支持的模型/功能

- **快速模式**：当前仅支持 `glm-5.2-fast-preview` 模型（[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)），已在华北2（北京）和新加坡地域开放。该模型在保持与 `glm-5.2` 相同语义能力基础上，显著降低首 token 延迟并提升整体 TPS。
  
- **TPM 预留**：支持多款主流模型，包括 `千问3.8-Max`、`千问3.6-Flash-2026-04-16`、`GLM-5.2`、`GLM-5.1`、`DeepSeek-v4-Flash/Pro`、`Kimi-K2.6` 等（[TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)）。各模型支持的输入/输出 TPM 起步值、阶梯系数及缓存折扣策略不同，需以控制台实时展示为准。

> **注意**：文档 1 中 `glm-5.2-fast-preview` 被列为快速模式唯一支持模型，而文档 2 的 TPM 预留表格中明确列出 `GLM-5.2`（非 `-fast-preview` 后缀）作为可预留模型。二者模型 ID 不同，**不可混用**：快速模式必须使用 `glm-5.2-fast-preview`；TPM 预留必须使用对应基础模型（如 `qwen3.8-max` 或 `glm-5.2`）创建后生成的专属 model code。

## 关键参数

| 参数 | 快速模式 | TPM 预留 |
|------|----------|-----------|
| **核心标识** | `model="glm-5.2-fast-preview"` | `model="<dedicated-model-code>"`（由控制台生成） |
| **接入域名** | `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://dashscope.aliyuncs.com/compatible-mode/v1`（标准兼容地址）或工作区专属地址（取决于部署配置） |
| **计费单位** | 按 token（输入+输出）计费，单价见文档内价格表 | 按 kTPM（每千 token/分钟）预付费 + 可选溢出按 token 计费 |
| **容量保障** | 无专属容量，依赖排队队列缓解限流（[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)） | 专属刚性兑付，预留范围内 100% 容量保障 |
| **超额处理** | 请求自动进入排队队列，不返回 429 | 可选：「自动溢出至按量」（默认）或「仅预留容量，超限返回 429」 |

## 使用方式

- **快速模式**：无需额外配置，只需在标准 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)中将 `model` 设为 `glm-5.2-fast-preview`，并确保使用正确的 workspace 域名（[快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)）。流式响应中需分别处理 `delta.reasoning_content` 和 `delta.content` 字段。
  
- **TPM 预留**：
  1. 登录百炼控制台 → **TPM 预留** 页面 → 创建实例，选择目标模型、输入/输出 TPM、购买时长及溢出策略；
  2. 实例状态变为「运行中」后，在详情页「概览」Tab 复制专属 `model code`；
  3. 将 API 请求中的 `model` 参数替换为该 code 即可生效（[TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)）。
  
  > **注意**：TPM 预留实例首次启用或扩缩容后存在短暂预热期（秒级），期间可能出现延迟波动，建议客户端实现请求排队或指数退避重试。

## 限制和注意事项

- **快速模式限制**：处于 preview 阶段，模型能力、规格及可用地域可能随版本调整；不支持所有标准 API 参数（如 `temperature`、`top_p` 等采样参数受限，具体以实际响应为准）；暂不支持缓存命中率优化（文档 1 表格中“缓存命中”列值为 4 元，但未说明是否启用缓存逻辑）。
  
- **TPM 预留限制**：专属 model code 与预留实例强绑定，退订后立即失效；缩容/退订涉及违约金计算（已用部分按 1.5 倍系数结算）；服务到期后 14 小时内资源将被彻底删除且不可恢复（[TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)）。
  
- **共性注意事项**：
  - 两类方案均需确保 API Key 具备对应模型调用权限；
  - 快速模式与 TPM 预留**不可叠加使用**：`glm-5.2-fast-preview` 不支持 TPM 预留；TPM 预留仅作用于其绑定的基础模型（如 `glm-5.2`），不能用于 `glm-5.2-fast-preview`；
  - 流式响应中，`reasoning_content` 与 `content` 的分块推送顺序和粒度因模型实现而异，客户端应以字段存在性而非顺序做判断。

## 来源文档

- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)
- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)


