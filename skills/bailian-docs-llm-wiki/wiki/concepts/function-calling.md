# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、生成结构化工具调用请求，并交由外部系统执行关键操作的核心能力。它使大模型不仅能生成文本，还能动态调度联网搜索、代码解释、网页提取、数据库查询等外部工具，实现“思考—决策—执行”闭环。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非独立接口，而是**内嵌于特定协议和模型的能力**，需结合协议类型、模型选型与参数配置协同启用：

- **OpenAI 兼容 Responses 接口**：这是最简接入方式。模型自动判断是否需要调用工具（如用户问“今天北京天气如何？”），无需显式声明函数 schema；系统内置联网搜索、代码解释器等工具链，开发者只需传入 `model="qwen3.7-plus"` 并启用 `responses` 协议（Endpoint 为 `https://dashscope.aliyuncs.com/v1/responses`）。响应中会返回 `tool_calls` 数组，含 `function.name` 和 `function.arguments`，后续需自行解析并执行对应工具。

- **Anthropic 兼容 Messages 接口**：适用于需显式控制调用逻辑的场景。开发者必须在请求中提供 `tools` 数组（定义函数名、描述、参数 JSON Schema），模型在 `content` 中混合输出 `text` 与 `tool_use` 块。此模式支持多工具并行调用、带思考过程的逐步推理（配合 `enable_thinking=true`），适合构建可控的 Agent 工作流。

- **DashScope 原生接口**：不原生支持函数调用。若需该能力，必须自行实现工具调度逻辑：先调用模型获取结构化指令（如通过 `output_format="json"` 强制输出 JSON），再解析结果、调用对应服务、将结果拼入下一轮 `messages` 中重新提交——本质是“手动 Function Calling”。

- **多模态模型（如 `qwen3-vl-plus`）**：在 OpenAI Vision 兼容接口中同样支持函数调用，输入可含图像/视频 + 文本，模型能基于视觉内容触发工具（例如：“分析这张财报截图，计算净利润增长率” → 调用 OCR + 表格解析工具）。

> ⚠️ 注意：`qwen-turbo`、`qwen-flash` 等轻量模型**不支持函数调用**；仅 `qwen3.5/3.6/3.7` 系列（如 `qwen3.7-plus`）、`qwen-plus`、`qwen-vl-plus` 等旗舰模型具备该能力。调用前请确认模型文档明确标注 “支持 Function Calling”。

## 关键参数和配置

| 参数 | 类型 | 说明 | 必填性 | 备注 |
|------|------|------|--------|------|
| `tools` | array | 定义可用工具列表，每个元素含 `name`、`description`、`input_schema`（JSON Schema） | Anthropic Messages 必填；Responses 接口忽略 | `input_schema` 必须严格符合 JSON Schema 规范，否则模型无法正确生成参数 |
| `tool_choice` | string / object | 控制调用策略：`"auto"`（默认，模型自主决定）、`"none"`（禁用）、`{"type": "function", "function": {"name": "xxx"}}`（强制指定） | 可选 | 仅 Anthropic Messages 支持；Responses 接口始终为 `auto` |
| `enable_thinking` | boolean | 启用逐步推理模式，提升工具调用准确性（尤其复杂任务） | 可选 | 仅 `qwen3.5+` 系列有效；开启后 token 成本略增，需在请求 body 顶层传入 |
| `previous_response_id` | string | Responses API 多轮对话上下文锚点 | Responses 多轮必填 | 必须传入上一轮响应的顶层 `id`（如 `"resp_abc123"`），用于维持工具调用状态一致性 |

- **协议差异提醒**：
  - OpenAI Responses 接口的 `max_tokens` 限制**包含工具返回内容长度**，非仅模型生成部分；
  - Anthropic Messages 接口要求 `tools` 必须在首次请求即完整声明，后续轮次不可动态增删；
  - 所有函数调用场景均**不支持流式响应（`stream=true`）**，需等待完整响应后解析 `tool_calls` 或 `tool_use`。

## 面向开发者，简洁实用

- ✅ **快速起步**：用 Responses 接口 + `qwen3.7-plus`，无需定义工具，直接发送自然语言提问，检查响应中的 `tool_calls` 字段即可。
- ✅ **精准控制**：选 Anthropic Messages 协议，明确定义 `tools`，用 `tool_choice` 锁定行为，适合构建生产级 Agent。
- ❌ **避免踩坑**：勿对 `qwen-turbo` 等模型启用函数调用；勿在 DashScope 原生接口中期待自动工具调度；勿遗漏 `previous_response_id` 导致多轮上下文断裂。
- 🛠️ **调试建议**：开启 `enable_thinking=true` 并设置 `temperature=0.1`，可获得更稳定、可预测的工具调用输出；响应中 `usage.total_tokens` 包含工具调用开销，需纳入成本监控。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [model experience](../guides/model-experience.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more about models](../api/more-about-models.md)


