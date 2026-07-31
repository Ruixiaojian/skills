# Token

Token 是百炼平台中用于计量模型推理资源消耗的核心单位，表示模型处理的文本、图像、音频等模态数据的基本语义单元。在百炼体系中，Token 不仅是计费与配额的基础粒度，也是性能监控、容量规划和调用优化的关键指标。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与配额（Token Plan）**：Token Plan 以 Credits 为统一计价单位，其消耗量由实际输入/输出 Token 数、模型类型、思考模式启用状态及 Harness [工具调用](tool-use.md)次数动态计算。例如 `qwen3.6-plus` 单次请求约消耗 3.18 Credits，已包含 [prompt](../guides/prompt.md) 缓存、推理输入、生成输出等全部 Token 开销。个人版按 5 小时/7 天滚动窗口限额，团队版按月度总 Credits 额度管理。

- **高性能推理（TPM 预留 / 快速模式）**：TPM（Tokens Per Minute）是衡量吞吐能力的硬性指标，用户通过预付费锁定 `input_tpm` 和 `output_tpm`（单位：kTPM），保障高并发下确定性响应；快速模式虽不支持 TPM 预留，但 `glm-5.2-fast-preview` 的 TPS（tokens per second）提升直接反映在 Token 输出速率上，适用于对首 Token 延迟敏感的实时交互场景。

- **可观测性（模型监控 & 应用监控）**：所有监控维度均以 Token 为统计基础——模型监控中 `model_usage` 指标精确到输入/输出 Token 总量；应用监控则在 `LLM` 节点级展示单次 Span 的 Token 总量（输入 + 输出）及首 Token 耗时，支撑链路级成本归因与性能瓶颈定位。

- **API 调用约束（Preparations）**：`max_tokens` 参数直接限制模型最大输出长度，必须在模型支持范围内（如 `qwen3.7-max` 最大输出为 8192 tokens）；[多模态](multi-modal.md)输入（如含 `image_url` 的 `content` 数组）会显著增加视觉 Token 消耗，需注意纯文本模型不支持此类输入，否则触发 400 错误。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `max_tokens` | 模型单次响应的最大输出 Token 数 | 必须为整数且 ≥1，不可超过模型文档声明的上限；设为 1 时仍会消耗输入 Token |
| `input_tpm` / `output_tpm` | TPM 预留中分别承诺的每分钟输入/输出 Token 容量 | 单位为 kTPM（1,000 tokens/min），需按模型阶梯系数估算，缓存命中可降低实际消耗 |
| Token 统计口径 | 输入 Token：[prompt](../guides/prompt.md) 内容经 tokenizer 后的 token 数（含 system/user/assistant 角色标记）<br>输出 Token：模型生成内容的 token 数（不含 stop token） | 图像/视频 URL 作为输入时，其视觉 Token 消耗由模型内部编码器计算，不对外暴露原始数值；流式响应中 `delta.content` 的 token 数实时累加 |
| Credits 换算 | 非固定单价，取决于模型、Token 用量、[工具调用](tool-use.md)等组合因素 | 例如 `web_search` [工具调用](tool-use.md)会额外增加 Credits 消耗，具体值见控制台用量明细 |

## 面向开发者，简洁实用

- ✅ **调试建议**：首次调用后立即查看 [模型用量页面](https://bailian.console.aliyun.com/?tab=costing-balance#/costing-balance/usage-statistics)，筛选对应 `model` 和 `apikey_id`，确认 Token 消耗是否符合预期（延迟约 1 小时）；开启高级监控后可查分钟级日志，精准定位高 Token 消耗请求。
- ✅ **优化技巧**：缩短 [prompt](../guides/prompt.md)、禁用非必要工具、启用缓存（对重复 prompt 可降本）、选择 Flash 类模型（如 `qwen3.6-flash`）可显著降低 Token/Credits 消耗。
- ✅ **安全红线**：Token Plan 明确禁止自动化脚本批量调用——单次请求若无用户交互上下文或高频固定 pattern，可能被判定为违规并封禁 API Key。
- ✅ **开发验证**：使用 CLI 快速估算 Token：`bl text estimate --message "你的提示词"`（支持[多模态](multi-modal.md)输入 URL）；SDK 中可通过 `response.usage` 字段获取 `prompt_tokens`、`completion_tokens`、`total_tokens`。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [preparations](../api/preparations.md)


