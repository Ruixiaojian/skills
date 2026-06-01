# Token

Token 是大语言模型处理文本的基本计量单位。模型在推理时，会将输入文本拆分为一系列 Token 进行理解和生成，因此 Token 既是衡量模型处理量的核心指标，也是百炼平台计费、监控和资源管理的基础度量。

## 什么是 Token

Token 不等同于字或词。一个中文汉字通常对应 1～2 个 Token，一个英文单词通常对应 1～4 个 Token，具体取决于模型所使用的分词器（Tokenizer）。在百炼平台中，1M Token 约等于 70 万汉字。

每次模型调用产生的 Token 分为两部分：

| 类型 | 说明 |
|------|------|
| **输入 Token** | 用户提交的 Prompt、系统指令、上下文历史等 |
| **输出 Token** | 模型生成的回复内容，包括思考过程（如开启思考模式） |

## 计费中的 Token

百炼平台的大语言模型按量付费以 Token 为核心计费单位，输入 Token 和输出 Token 分别定价。例如：

- `qwen3.7-max`：输入 12 元/百万 Token，输出 36 元/百万 Token
- `qwen3.6-plus`：输入 2 元/百万 Token（≤256K），输出 12 元/百万 Token

**抵扣顺序**：免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费。

在 Token Plan 团队版中，单次调用的 Credits 消耗由模型类型、输入/缓存/输出 Token 用量共同决定。Coding Plan 则按调用次数计量，不直接按 Token 计费。

> **注意**：不同模态的模型计量单位不同。大语言模型和向量模型按 Token 计量，图像生成按张计量，视频和语音按秒计量。

## 上下文窗口与 Token 限制

上下文窗口（Context Window）定义了模型单次调用能处理的最大 Token 总量（输入 + 输出），是选型的关键参数：

| 上下文窗口 | 代表模型 |
|-----------|---------|
| 1M Token | `qwen3.7-max`、`qwen3.6-plus`、`qwen3.6-flash`、`deepseek-v4-pro` |
| 256K Token | `qwen3.6-max-preview`、`kimi-k2.6` |
| 128K～198K Token | `glm-5.1`（198K）、`MiniMax-M2.5`（192K） |

开启思考模式时，思考内容也会占用 Token 预算。不同模型的思考预算（Thinking Budget）不同，如 `qwen3.7-max` 为 256K Token，`qwen3.6-flash` 为 128K Token。

## 关键参数

| 参数 | 说明 | 使用场景 |
|------|------|---------|
| `max_tokens` | 限制模型单次输出的最大 Token 数 | 控制输出长度和成本 |
| `enable_thinking` | 开启思考模式，模型逐步推理后再输出 | 复杂推理任务，会增加输出 Token 消耗 |
| `dimensions` | 向量模型输出维度（非 Token 参数，但输入受 Token 限制） | 向量检索场景 |

向量模型同样受 Token 限制约束：`text-embedding-v4` 单行最大 8,192 Token，`text-embedding-v2` 单行最大 2,048 Token。

## 监控与观测中的 Token

### 模型监控

在模型监控中，Token 相关的核心指标包括：

- **TPM**（Tokens Per Minute）：每分钟处理的 Token 数
- **平均单次请求调用量**：单次调用的平均 Token 消耗
- **model_usage**：PromQL 指标，用于在 Grafana 等工具中查询 Token 用量

用量统计页面支持按业务空间维度查看 Token 消耗趋势，数据延迟约 1 小时，支持查看最近 30 天的数据。

### 应用观测

在应用观测中，可以按以下维度筛选和统计 Token：

- **Token 总量**、**输入 Token**、**输出 Token**：支持数值比较过滤
- **监控统计**：展示 Token 总量趋势、平均单次请求 Token 量等聚合指标
- **LLM 节点**：Token 量 = 输入 Token + 输出 Token

## 成本优化建议

- **合理设置 `max_tokens`**：避免模型生成不必要的冗长输出。
- **按任务选模型**：简单任务优先使用轻量级模型（如 `qwen3.6-flash`），降低单 Token 成本。
- **优化 Prompt**：精简输入内容，减少无效的输入 Token。
- **使用批量推理**：对延迟要求不高的场景，输入和输出单价按实时推理的 50% 计费。
- **利用上下文缓存**：重复前缀的请求可享受输入 Token 折扣。
- **配置用量告警**：通过模型监控对 Token 消耗设置告警阈值，及时发现异常。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [test 1](../guides/test-1.md)
- [model inference](../guides/model-inference.md)
- [general text embedding](../api/general-text-embedding.md)

