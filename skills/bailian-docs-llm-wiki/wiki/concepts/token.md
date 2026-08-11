# Token

Token 是百炼平台中用于计量模型输入、输出及工具调用消耗的最小计费与资源单位。它并非原始字符或字节，而是由模型 tokenizer 对文本、图像描述、语音指令等内容进行语义化切分后生成的离散单元；一次完整调用的总 Token 量 = 输入 Token + 输出 Token（部分场景如 Embedding 或 Harness 工具调用另有独立计算规则）。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用计费**：所有文本、[多模态](multi-modal.md)、语音、向量类模型调用均以 Token 为基本计量单位。例如调用 `qwen3.8-max` 时，输入 200 字中文约消耗 250–300 Token，输出 100 字约消耗 120–150 Token（具体取决于 tokenizer 实现和内容复杂度）；图像生成模型（如 `qwen-image-2.0`）则按提示词 Token + 生成分辨率隐式开销综合折算 Credits。
  
- **Token Plan 统一抵扣**：Token Plan 不直接暴露 Token 单价，而是将 Token 消耗映射为 Credits 抵扣。同一模型在不同输入长度、输出长度、是否启用 Thinking 模式或调用 Harness 工具（如 `web_search`）时，Credits 消耗非线性增长——例如启用 `code_interpreter` 后，除基础 Token 外还会额外抵扣工具执行成本。

- **可观测性监控核心指标**：
  - **应用观测**中，“Token 总量”字段精确展示每个 LLM 节点的 `input_tokens + output_tokens`，可用于分析智能体/工作流中各步骤的资源占比；
  - **模型监控**中，Token 是用量统计的核心维度，支持按 `model`、`apikey_id`、`workspace_id` 等多维下钻，用于成本归因与性能优化；
  - **评测系统**（应用评测 / 模型评测）中，所有大模型评估器（Grader）的运行均按实际消耗 Token 计费，需在任务配置前预估预算。

- **参数控制边界**：`max_tokens` 是开发者显式控制输出长度的关键参数，直接影响 Token 消耗上限与响应成本。其取值必须在模型文档标明的最大输出 Token 范围内（如 `qwen3.7-plus` 最大为 8192），超限将触发 `Range of max_tokens should be [1, xxx]` 错误。

## 关键参数和配置

| 参数 | 说明 | 开发者须知 |
|------|------|------------|
| `max_tokens` | 控制模型最大输出长度的整数参数 | 必须显式传入，且 ≤ 模型支持上限；设为过小值可能导致截断，过大则增加成本与延迟；默认值不生效，未传将报错 |
| `temperature` / `top_p` | 影响输出多样性，间接影响实际输出 Token 数量 | 虽不直接计费，但高 `temperature` 可能导致更长、更发散的响应，从而增加 Token 消耗 |
| `enable_thinking=true` | 启用推理链模式（仅特定模型支持） | 强制要求 `stream=true` 和 `incremental_output=true`；思考过程本身产生额外 Token，计入总消耗 |
| Credits（Token Plan） | Token Plan 的统一计量单位 | 不等于原始 Token 数，而是经模型类型、工具调用、上下文长度加权后的 Credits；实际消耗以控制台「用量明细」为准，不可简单换算 |

## 面向开发者，简洁实用

- ✅ **必做**：所有 API 调用必须显式指定 `model` 和 `max_tokens`；遗漏 `model` 将返回 `Model not exist.`，遗漏 `max_tokens` 将触发校验失败。
- ✅ **查用量**：实时 Token 消耗可在控制台「模型监控 → 用量统计」或「应用观测 → Span 详情」中查看，精度达分钟级（高级监控开通后）。
- ✅ **控成本**：对长上下文场景，优先使用支持 128K 上下文的模型（如 `qwen3.8-max`），避免因分段调用导致 Token 重复编码；对确定性任务（如 JSON 结构化输出），配合 `response_format={"type": "json_object"}` 减少无效重试 Token。
- ❌ **勿假设**：不要将字符数 ≈ Token 数（中文平均 ~1.2–1.5 Token/字，但标点、emoji、URL、代码会显著拉高）；不要跨模型套用 Token 估算公式（不同 tokenizer 差异大）。
- 🚨 **注意隔离**：Token Plan 使用 `sk-sp-` 开头的专属 API Key，与通用 `sk-` Key 完全隔离；混用将导致 `404 model not found` 或鉴权失败。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [preparations](../api/preparations.md)
- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)
- [application evaluation](../guides/application-evaluation.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)


