# Token

Token 是百炼平台中用于计量模型输入与输出内容的基本单位，代表模型处理的最小语义片段（如词元、子词或字节对）。所有模型调用的计费、容量限制、性能监控和资源调度均以 Token 为统一计量基础。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费核心单元**：模型调用按实际消耗的输入 Token 和输出 Token 分别计费（如 `qwen3.7-plus` 输入 ¥12/百万 Token），免费额度、资源包、节省计划均以 Token 为抵扣单位。
- **容量控制依据**：TPM 预留（Token Per Minute）和模型部署中的 PTU/MU 规格，均以每分钟可处理的 Token 数（kTPM）为容量度量；RPM（Requests Per Minute）限流也隐式受限于单请求平均 Token 消耗。
- **性能监控指标**：模型监控与应用监控中，“Token 总量” = 输入 Token + 输出 Token，用于分析成本分布、首 Token 延迟（与输入 Token 量强相关）、吞吐瓶颈（TPS × 平均输出 Token）。
- **推理能力边界**：模型上下文长度（如 256K Token）、缓存折扣规则（如 glm-5.2 缓存命中部分按 25% 折算输入 Token 容量）、阶梯计价档位（0–32K / 32K–128K Token）均直接依赖 Token 数量。
- **思考模式控制**：在 OpenCode 或 Qwen Code 中启用 Thinking Mode 时，需显式配置 `budgetTokens`（如 `1024`），该值限制推理过程中用于内部规划的额外 Token 消耗，不计入用户输入 Token。

## 关键参数和配置

| 参数 | 说明 | 典型位置 | 示例 |
|------|------|----------|------|
| `input_tokens` / `output_tokens` | API 响应中返回的实际消耗 Token 数 | 所有模型调用响应体（`usage` 字段） | `"usage": {"input_tokens": 128, "output_tokens": 64}` |
| `budgetTokens` | 思考模式下允许使用的最大额外 Token 数 | OpenCode `opencode.json` / Qwen Code `/config` 命令 | `"budgetTokens": 1024` |
| `max_context_length` | 部署时指定模型支持的最大上下文 Token 数 | 模型部署 API 的 `deploy_spec` | `"max_context_length": 100000` |
| `tpm_limit` | 每分钟最大 Token 处理量（输出方向） | MU 部署配置 | `"tpm_limit": 1000` |
| `input_tpm` / `output_tpm` | TPM 预留中预购的输入/输出吞吐量（单位：kTPM） | TPM 预留创建参数 | `"input_tpm": 5000, "output_tpm": 500` |

> ⚠️ 注意：  
> - Token 计数由百炼平台服务端统一计算，开发者无需自行分词；不同模型 tokenizer 实现不同，同一文本在不同模型下 Token 数可能差异显著。  
> - 缓存命中、Batch 调用、长上下文等场景存在 Token 折算系数（如超 32K 输入按 1.33 系数折算），实际计费 Token = 原始 Token × 系数。  
> - 所有 Token 相关限制（如上下文长度、TPM 预留额度）均指 *服务端处理后的有效 Token 数*，不含协议层开销（如 SSE event 字段、JSON 序列化冗余）。

## 面向开发者，简洁实用

- **快速估算**：使用 [Token 计算器](https://bailian.console.aliyun.com/#/token-calculator) 输入文本，实时查看各模型下的 Token 数及预估费用。  
- **调试技巧**：若遇到 `429 Too Many Requests`，检查 `usage.input_tokens` 和 `usage.output_tokens`，确认是否超出 TPM 预留额度或 RPM 限流阈值。  
- **成本优化**：  
  - 对长文本优先启用前缀缓存（支持模型见文档）；  
  - Batch 调用可享 50% Token 单价折扣（不可与缓存折扣叠加）；  
  - 使用 `glm-5.2-fast-preview` 等快速模式模型，在相同 Token 消耗下提升 TPS，摊薄单位 Token 延迟成本。  
- **监控告警**：在模型监控中配置“单次请求输出 Token > 2000”告警，及时发现异常生成行为；结合应用监控的 Token 分布热力图，定位高消耗节点（如 LLM 节点 vs RETRIEVER 节点）。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)
- [test 1](../guides/test-1.md)


