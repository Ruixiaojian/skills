# model deployment 1

百炼平台的 `model deployment 1` 指代以 **预置吞吐（PTU）** 方式部署模型的核心能力，专为高并发、低延迟、流量可预估的生产场景设计。它通过预留确定性算力资源保障稳定 TPM 吞吐，支持长输入处理与前缀缓存优化，并提供细粒度额度监控与溢出策略控制。本文档聚焦 PTU 部署的关键技术事实，不涵盖模型单元（MU）或按 [Token](../concepts/token.md) 计费等其他部署模式。

## 支持的模型与功能

- **支持模型**：仅限平台预置的 PTU 可部署模型，包括 `glm-5.1`、`deepseek-v4-pro`、`qwen3.7-plus-2026-05-26` 等（具体清单以控制台实时可选为准）。调优后的 LoRA 模型**不支持 PTU 部署**，详见[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)文档。
- **核心功能**：
  - **长输入支持**：部分模型支持远超 32K token 的输入（如 `glm-5.1` 最高 200K，`deepseek-v4-pro` 最高 256K），超出基础长度部分按阶梯系数折算 TPM 消耗。
  - **前缀缓存**：对重复请求前缀自动缓存，命中时按模型专属折扣率（如 `glm-5.1` 为 0.2）折算输入额度，显著降低多轮对话与长文档分析成本。
  - **溢出策略**：创建时可选「自动溢出至按量计费」（默认，业务不中断）或「仅使用 PTU 容量」（超出返回 HTTP 429）。

> **注意**：文档 2 中表格显示 `glm-5.1` 输入上限为 `64K`，但文档 1 明确标注其支持 `200K`。以 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md) 的权威说明为准，`glm-5.1` 实际上限为 200K token。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `input_tpm` / `output_tpm` | 预置的每分钟输入/输出 [Token](../concepts/token.md) 数（KTPM），决定基础吞吐保障能力 | [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `ptu_capacity` | API 请求体中承载 `input_tpm` 和 `output_tpm` 的对象字段 | [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| 缓存折扣率 | 模型级固定值（如 `glm-5.1` 为 0.2），用于计算 `cached_tokens` 对应的额度减免 | [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md) |
| 阶梯系数 | 按输入长度分段应用（如 `glm-5.1` 在 `[0,32K)` 区间系数为 1.0，在 `[32K,200K]` 区间输入系数为 1.33） | [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md) |

## 使用方式

1. **控制台操作**：在百炼控制台 > **模型部署** > **创建部署**，选择「预置吞吐（PTU）」，填写模型、名称、`输入 KTPM` 和 `输出 KTPM`，并展开「预置吞吐额度计算器」辅助估算。
2. **API 调用**：使用 `POST /api/v1/deployments`，`plan` 字段设为 `"ptu"`，并在 `ptu_capacity` 对象中指定 `input_tpm` 与 `output_tpm` 值（单位：KTPM）。示例见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
3. **额度验证**：调用成功后，API 响应中 `service_tier` 字段为 `"ptu-standard"` 表示使用 PTU；`usage.prompt_tokens_details.cached_tokens`（OpenAI 兼容格式）或 `usage.input_tokens_details.cached_tokens`（DashScope 格式）大于 0 即表示缓存生效。

## 限制和注意事项

- **模型限制**：仅预置模型支持 PTU；LoRA 导入模型仅支持模型单元（MU）或按 [Token](../concepts/token.md) 计费，**不可部署为 PTU**，此限制在 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md) 文档中明确说明。
- **输入上限硬约束**：单次请求输入 token 数超过模型物理上限（如千问系列为 128K，DeepSeek 系列为 64K）时，无论 PTU 是否充足，均自动转为按量计费。
- **额度监控要点**：
  - 利用率 > 100% 属正常现象，因阶梯系数导致折算后消耗高于原始 token 数。
  - `provisioned_tokens` 字段反映已应用阶梯与缓存折扣的最终额度消耗，是计费依据。
- **溢出策略影响**：选择「仅使用 PTU 容量」时，超出额度的请求直接返回 429，无额外费用；选择「自动溢出」时，超出部分按对应模型的按量单价计费，响应头含 `x-dashscope-ptu-overflow:true`。

## 来源文档

- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


