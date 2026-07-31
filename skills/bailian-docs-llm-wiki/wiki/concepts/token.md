# Token

Token 是百炼平台中用于计量模型调用资源消耗的核心计费与监控单位，特指大语言模型（LLM）及全模态模型在推理过程中处理的文本单元——包括输入 Prompt 中的词元（tokenized text）和模型生成的输出内容。一个 Token 通常对应一个子词（subword）或标点符号，其具体切分方式由模型所采用的 tokenizer 决定（如 Qwen 系列使用 QwenTokenizer），并非简单按字符或字数计算。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费计量**：所有文本生成类模型（如 `qwen3.7-plus`、`glm-5.2`）、全模态模型（如 `qwen-omni`）均按 **输入 Token 数 + 输出 Token 数** 的总和计费；向量嵌入（`text-embedding-v3`）等仅按输入 Token 计费；[多模态输入](multimodal-input.md)（如图像 URL）会经预处理折算为等效 Token 数参与计费。
- **用量监控**：在「模型监控」中，Token 是大语言模型用量的核心统计维度，支持分钟级趋势分析、免费额度消耗追踪及告警配置；在「应用监控」中，每个 `LLM` 节点自动上报 `input_tokens`、`output_tokens` 和 `total_tokens`，用于链路级成本归因与性能诊断。
- **配额控制**：Token Plan 订阅服务以 Credits 为统一单位，1 Credit ≈ 1 Token（具体换算系数依模型而异，详见各模型定价页），个人版采用双窗口（每 5 小时 + 每 7 天）Token 消耗限额，团队版按月度固定 Credits 额度管理。
- **API 调用约束**：`max_tokens` 参数直接限制模型单次响应的最大输出 Token 数；`temperature`、`top_p` 等参数虽不直接影响 Token 数，但间接影响输出长度与稳定性；结构化输出（`response_format="json_object"`）需确保 Prompt 中含 `"json"` 关键词，否则可能因解析失败导致额外 Token 浪费。
- **模型评测**：在模型评测任务中，被评测模型的每次推理消耗的 Token 会计入调用成本；若使用大模型评估（裁判模型），其评分过程本身也按 Token 计费，需在维度配置中明确指定裁判模型（如 `qwen-max`）。

## 关键参数和配置

| 参数/配置项 | 说明 | 注意事项 |
|-------------|------|----------|
| `max_tokens` | 控制模型单次响应最大输出 Token 数 | 必须在模型支持范围内（如 `qwen3.7-plus` 最大为 8192），超限将返回 `400 Bad Request` |
| `input_tokens` / `output_tokens` | 应用监控中 LLM 节点自动上报的细分指标 | 可用于识别“高输入低输出”（提示冗余）或“高输出低信息密度”（生成拖沓）等优化点 |
| Credits-to-Token 换算 | Token Plan 中 1 Credit ≈ 1 Token（基准值），实际按模型精度动态调整 | 例如 `qwen3.8-max-preview` 折扣后为 0.1 Credit/Token（夜间 0.02 Credit/Token），详情见[模型定价页](https://help.aliyun.com/zh/model-studio/model-pricing) |
| 免费额度 | 新用户赠送 10,000 Credits（约 10,000 Token），按模型 Code 独立核算 | 免费额度用尽后自动切换至付费账户，支持在控制台开启「用完即停」开关 |

## 面向开发者，简洁实用

- ✅ **快速估算 Token 数**：使用 [DashScope Tokenizer 工具](https://dashscope.console.aliyun.com/tokenizer) 或 SDK 中 `dashscope.Tokenizer.count_tokens()` 方法，传入 `model` 和 `text` 即可获取精确值（支持多轮对话 `messages` 格式）。
- ✅ **避免意外超限**：调用前始终校验 `max_tokens` 是否合理；对长文档输入，优先使用 `qwen-long` 等长上下文模型，并设置 `truncation_strategy="auto"`。
- ✅ **监控与优化**：在应用监控中筛选 `total_tokens > 1000` 的 Span，结合 Prompt 和 Output 分析低效生成；对高频调用场景，复用推理结果集进行评测而非重复调用。
- ❌ **不要硬编码 Token 逻辑**：不同模型 tokenizer 不同（如 `glm-5` 与 `qwen3` 切分结果差异可达 20%），务必通过 API 或官方工具动态计算。
- ❌ **不要混淆 Token 与字符**：中文平均约 1.5–2 字符/Token，英文约 0.75 单词/Token；直接按字数估算会导致严重偏差。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)
- [preparations](../api/preparations.md)


