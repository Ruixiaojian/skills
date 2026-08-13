# Token

Token 是百炼平台中用于计量模型输入与输出内容长度、计费、资源调度和性能监控的核心计量单位。一个 Token 通常对应一个子词（subword）或标点符号，在文本场景下近似为中文字符（约1.5–2字/Token）或英文单词（约3/4词/Token）；在[多模态](multimodal.md)场景中，图像、音频等输入也会按统一规则转换为等效 Token 数参与计费与限流。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与用量管理**：所有模型调用（含文本、视觉、语音等）均按实际消耗的输入 Token + 输出 Token 总量计费。用量可在「模型用量」页面按模型、API Key、时间范围实时查看，并作为套餐（如 Coding Plan、Token Plan）的消耗依据。
- **推理控制与资源约束**：
  - `max_tokens` 参数限制模型单次响应的最大输出长度，直接影响 Token 消耗与响应时长；
  - OpenCode 的 `budgetTokens`（如 `thinking.budgetTokens: 1024`）用于硬性限制思考链（Chain-of-Thought）阶段的 Token 使用上限，防止过度推理；
  - TPM（Tokens Per Minute）预留能力以 kTPM 为单位锁定专属吞吐容量，保障高并发下的 Token 处理确定性。
- **可观测性与调试**：
  - 应用监控中，每个 `LLM` 节点的「Token总量」= 输入 Token + 输出 Token，是分析智能体/工作流成本与效率的关键指标；
  - 模型监控支持开启推理日志后，精确记录每次调用的输入/输出原文及对应 Token 数，用于成本归因与效果回溯；
  - 「首 Token 耗时（TTFT）」和「非首 Token 延时」均以 Token 粒度衡量流式响应性能。
- **配额与限流**：账号级与业务空间级的 `model_limit` 和 `workspace_limit` 实际限制的是单位时间内的 Token 吞吐量（即 TPM），而非请求数；超限将触发 HTTP 429 响应。

## 关键参数和配置

| 参数 | 说明 | 推荐实践 |
|------|------|----------|
| `max_tokens` | 控制模型生成内容的最大 Token 数（输出侧） | 必须显式设置，避免意外长输出导致费用激增；建议设为业务所需上限的 1.2 倍 |
| `budgetTokens` | （OpenCode 场景）思考链阶段允许消耗的最大 Token 数 | 根据任务复杂度调整：简单代码补全设 256–512，复杂规划任务可设 1024–2048 |
| `input_tokens` / `output_tokens` | 监控日志中返回的实际消耗值（只读） | 用于成本分析、异常检测（如某次调用输出 Token 异常偏高） |
| TPM 预留值（kTPM） | 按天预购的输入/输出 Token 每分钟处理能力 | 高吞吐应用（如 Agent 批量执行）建议预留 ≥ 预估峰值 TPM × 1.5，避免排队 |

> ⚠️ 注意：  
> - Token 计算遵循各模型官方分词器（如 Qwen 使用 tiktoken 的 `qwen` 编码器），不支持自定义分词；  
> - [多模态](multimodal.md)输入（如图片）的 Token 折算由平台自动完成，开发者无需手动计算；  
> - 缓存命中（如 GLM-5.2 输入缓存）会按折扣系数（如 25%）折算 Token 消耗，降低实际费用。

## 面向开发者，简洁实用

- ✅ **必做**：所有生产环境 API 调用必须设置 `max_tokens`，并在监控中定期检查 `output_tokens` 分布，识别异常长响应。  
- ✅ **推荐**：启用模型监控的「推理日志」，结合 `input_tokens`/`output_tokens` 字段做细粒度成本审计；对关键 Agent 设置 `budgetTokens` 防止失控推理。  
- ❌ **避免**：依赖默认 `max_tokens`（不同模型差异大）；在未开通高级监控时尝试解析原始日志推算 Token；将 Token 数直接等同于字符数做前端预估（误差可达 ±30%）。  
- 🔧 **调试技巧**：使用 [模型列表 API](https://dashscope.aliyuncs.com/api/v1/models) 查询目标模型的 `context_length` 和 `pricing`，确认其 Token 容量与单价；通过 `curl -v` 或 SDK 日志捕获响应头中的 `X-DashScope-Token-Usage`（若启用）快速验证 Token 计算。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)
- [more about models](../api/more-about-models.md)


