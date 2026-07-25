# 函数调用

函数调用（Function Calling）是百炼平台中模型与外部能力协同的核心机制，指大语言模型在推理过程中，根据用户输入自主识别、规划并触发预定义工具（如搜索、代码执行、图像生成等）的结构化交互过程。该能力不依赖客户端主动发起，而是由模型基于语义理解动态决策是否调用、调用哪个工具及传入何种参数，最终将工具返回结果融入生成回复，实现“感知—决策—执行—合成”的闭环智能。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台并非单一接口功能，而是贯穿多个抽象层级的横切能力，其具体形态和控制粒度因使用场景而异：

- **基础模型 API（Qwen 系列）**：通过 DashScope 原生接口或 OpenAI 兼容 `chat/completions` 的 `tools` 字段声明可用工具，模型返回 `tool_calls` 结构（含 `function.name` 和 `function.arguments`），开发者需自行解析、执行工具、拼接结果并再次请求模型完成终稿。适用于需完全掌控工具调度逻辑的高级场景。

- **Responses API 与 Managed Agents**：函数调用被深度封装为平台托管能力。模型自动完成工具选择、参数提取、并发调用与结果聚合；开发者仅需配置工具（插件或 MCP 服务）并启用对应能力（如 `enable_search: true`），无需处理中间响应。平台负责沙箱隔离、超时控制、错误重试与上下文注入。

- **Application Call（应用调用）**：当调用已发布的智能体或工作流时，“函数调用”表现为应用内部的自动行为。若该应用已挂载插件或 MCP 工具，整个调用链路对调用方透明——输入一句话，输出最终答案，中间所有工具调用均由平台在后台完成。

- **插件（Plug-in）与 MCP 协议**：这是函数调用的基础设施层。“插件”定义工具能力元信息（ID、输入/输出 Schema、鉴权方式）；“MCP”提供标准化通信协议（Streamable HTTP），使任意符合规范的外部服务可被统一接入并参与模型的函数调用决策。二者共同构成百炼的工具生态底座。

- **工作流（Workflow）**：函数调用以显式节点形式存在。开发者手动拖拽插件或 MCP 节点到画布，配置输入来源（如上一节点输出、用户输入）与输出映射，形成确定性执行路径。此时调用非模型自主决策，而是流程编排驱动。

## 关键参数和配置

函数调用的实际生效依赖以下关键配置项，需按所选场景正确设置：

| 场景 | 关键参数 | 说明 | 注意事项 |
|------|----------|------|----------|
| **模型 API（OpenAI/DashScope）** | `tools`（array） | 工具定义列表，每个对象含 `function.name`、`function.description`、`function.parameters`（JSON Schema） | `parameters` 必须为有效 JSON Schema，缺失或格式错误将导致工具不可见；DashScope 接口还支持 `tool_choice` 控制调用强制性（`auto`/`required`/`none`） |
| | `tool_choice` | 模型调用策略 | `required` 强制调用（至少一个）、`none` 禁用调用；默认 `auto`（模型自主判断） |
| **Responses API / Managed Agents** | `enable_search`、`enable_code_interpreter` 等开关 | 启用内置工具链 | 开关为布尔值，启用后模型自动决定是否及何时调用，无需声明 `tools` |
| **插件集成** | `tool_id` | 插件内工具唯一标识 | 必须在控制台发布成功且状态为 `active`；同一智能体最多关联 10 个工具 |
| **MCP 服务** | `tool.name` | MCP Server 提供的工具名 | 必须与 MCP Server `/tools` 接口返回的 `name` 字段严格一致；不支持通配符或模糊匹配 |
| **Application Call** | `biz_params`（异步） / `input` 中嵌套结构 | 透传业务参数至插件或工作流节点 | 键名必须与插件配置的输入参数名完全一致，否则参数丢失 |

> ⚠️ 通用约束：所有工具调用均受安全沙箱限制（如 `code_interpreter` 禁止网络访问）、配额限制（单次调用耗时上限、并发数）及计费规则约束，详见各服务文档。

## 面向开发者，简洁实用

- **快速验证**：优先使用 Responses API 或 Application Call，开启 `enable_search` 即可体验联网问答，无需写工具解析逻辑。
- **精细控制**：若需自定义工具行为（如调用私有 API、组合多个工具结果），选用 DashScope 原生接口 + `tools` 参数，按 `tool_calls` → 执行 → `tool_responses` → 再请求的三步循环实现。
- **避免陷阱**：
  - 不要混用参数命名：`max_tokens`（OpenAI） ≠ `max_output_tokens`（DashScope）；`tool_choice`（DashScope） ≠ `function_call`（旧版 OpenAI）。
  - 工具参数描述（`description`）必须清晰准确，直接影响模型参数提取成功率。
  - MCP 自定义服务必须部署在函数计算 FC 并配置 VPC（如需访问云资源），本地服务无法被平台调用。
- **调试建议**：开启 `debug` 模式（如 `debug: {"enable": true}`）或查看 `usage` 字段中的 `tool_calls` 计数，确认调用是否触发；流式响应中注意 `delta.tool_calls` 的增量更新。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [managed agents api](../api/managed-agents-api.md)
- [application call](../api/application-call.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [plug in](../guides/plug-in.md)
- [model context protocol](../guides/model-context-protocol.md)


