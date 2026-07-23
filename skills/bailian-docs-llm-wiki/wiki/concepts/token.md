# Token

Token 是百炼平台中用于计量模型调用资源消耗的核心单位，代表模型处理输入与生成输出所消耗的计算资源。它并非加密凭证，而是按字节、字符或语义单元（如子词）标准化统计的**计费与用量度量基准**，直接影响 Credits 扣减、性能监控和成本治理。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费计量**：Token 是 Token Plan 订阅服务的底层计费单元。每次调用（无论同步/异步）均按 `输入 Token 数 + 输出 Token 数` 动态折算 Credits，不同模型单价不同（如 `qwen3.6-plus` 约 3.18 Credits/次），思考模式（`enable_thinking`）或 Harness 工具调用会额外增加 Token 消耗。
  
- **性能观测**：在应用监控与模型监控中，`Token 总量` 是关键可观测指标，精确拆分为 `input_tokens` 和 `output_tokens`，用于分析首 Token 延时、TPS（Tokens Per Second）、单次请求成本效率，并支持按业务空间、API Key 或模型维度下钻分析。

- **能力约束**：部分模型通过 `max_output_tokens` 参数显式限制输出长度；上下文窗口（如 `qwen3.7-plus` 支持 1M Token）本质是输入 Token 的硬性上限；[多模态](multi-modal.md)输入（图像、视频、音频）会经预处理转换为等效 Token 量参与计费与限流。

- **[安全与合规](security-and-compliance.md)**：内容安全拦截、限流错误（HTTP 429）等事件在模型监控中关联 Token 消耗记录，便于定位异常调用（如恶意长 [prompt](../guides/prompt.md)）或优化提示工程以降低无效 Token 开销。

- **开发调试**：SDK 和 API 返回中通常包含 `usage` 字段（如 `"input_tokens": 127, "output_tokens": 89`），开发者应主动解析该字段用于本地成本估算、缓存策略或用户用量展示。

## 关键参数和配置

| 参数/字段 | 说明 | 开发者须知 |
|-----------|------|------------|
| `input_tokens` / `output_tokens` | API 响应 `usage` 对象中的标准字段，表示本次请求实际消耗的输入/输出 Token 数 | 必读字段，不可依赖估算值；流式响应中仅最终 completion 返回完整 usage |
| `max_output_tokens` | 可选请求参数，控制模型最大生成长度（Token 数），超出将截断 | 并非所有模型支持；设置过小可能导致输出不完整，过大可能增加成本与延迟 |
| `X-DashScope-OssResourceResolve: enable` | 使用 `oss://` URL 传入图片/视频时必需的 Header，否则平台无法解析资源并统计对应 Token | [多模态](multi-modal.md)调用必配，缺失将返回 400 错误 |
| `enable_thinking` | 布尔参数（文本模型专用），启用深度推理模式时显著增加中间 Token 消耗 | 需权衡效果与成本，建议 A/B 测试后启用 |
| `reasoning.effort` | 控制思考深度的数值参数（如 `"low"`/`"medium"`/`"high"`），影响 Token 消耗与响应时间 | 与 `enable_thinking` 协同生效，高 effort = 更高 Token 成本 |

> ⚠️ 注意：Token 统计严格绑定地域（仅华北2北京有效）、API Key 类型（`sk-sp-` 专属 Key）及 Base URL；跨地域或混用 Key 将导致 Token 计量失效或调用失败。

## 面向开发者，简洁实用

- **不要估算，要实测**：不同模型、不同输入内容（尤其含 emoji、代码、多语言）的 Token 数差异极大。使用 [DashScope Tokenizer 工具](https://help.aliyun.com/zh/model-studio/token-calculator) 或 SDK 的 `count_tokens()` 方法本地预估，再以 API 实际返回 `usage` 为准。
  
- **监控必看三项**：在控制台模型监控页，重点关注 `model_usage`（总用量）、`model_first_token_duration_p99`（首 Token 延时）、`model_call_failure_count`（失败次数）——三者共同反映 Token 效率与稳定性。

- **降本三技巧**：  
  ① 对长文档 RAG，用 `TextRetriever` 默认 100 片段限制 + 精准 query 降低输入 Token；  
  ② 图像理解任务优先用 `qwen3.7-plus` 原生支持，避免 Skill 中转带来的额外 Token 开销；  
  ③ 异步任务（如视频生成）虽不实时返回 Token，但可在 `/api/v1/tasks/{task_id}` 查询结果中获取 `usage` 字段。

- **调试黄金法则**：当遇到 `429 Too Many Requests` 或 `400 Bad Request`，第一检查点是 `usage` 字段是否超限（如输入超 1M Token）或 `max_output_tokens` 设置不合理。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [model experience](../guides/model-experience.md)
- [more about models](../api/more-about-models.md)
- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)


