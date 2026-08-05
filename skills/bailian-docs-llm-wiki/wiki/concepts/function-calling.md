# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、结构化生成工具调用请求，并协同外部能力完成复杂任务的核心机制。它不是简单的 API 请求转发，而是模型基于对话上下文与预设工具 Schema，自主决策“何时调用、调用哪个、传什么参数”的推理过程，最终通过标准化协议将结果注入后续推理链。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一接口能力，而是贯穿多个抽象层级的横切能力，具体体现为以下四类实践模式：

- **DashScope 原生 API 的 `tools` + `tool_calls` 交互**：开发者在请求中显式传入 JSON Schema 定义的 `tools` 列表；模型返回 `output.choices[0].message.tool_calls` 数组（含 `function.name` 和 `function.arguments`）；客户端需解析、执行对应 HTTP 调用，并将结果以 `tool_outputs` 形式回填至下一轮请求。适用于需要完全控制工具调度逻辑的高定制场景。

- **Managed Agents 的 Skill 自动路由**：Skill 作为 ZIP 包上传，其 `SKILL.md` 中的 `description` 字段被模型用于语义匹配；当用户输入（如“把 PDF 表格转成 Excel”）命中描述中的触发关键词与输入类型时，智能体自动调用该 Skill，无需显式声明工具列表。强调“零配置、语义驱动”。

- **Application Call（应用调用）中的插件/工作流节点**：在智能体或工作流应用中，插件（Plugin）或 MCP 服务作为预置能力模块被绑定；模型根据对话内容自主决定是否调用（智能体模式），或由工作流引擎按编排顺序强制调用（工作流模式）。调用参数可来自模型抽取（`大模型识别`）或业务系统透传（`biz_params`）。

- **MCP（Model Context Protocol）服务集成**：MCP 是标准化的工具调用协议层，支持 SSE 或 HTTP 方式接入第三方服务（如地图、图表生成）；在智能体中启用后，模型可像调用内置工具一样自然触发 MCP 服务，平台自动处理协议转换、鉴权与结果注入，开发者只需关注服务端实现。

> ⚠️ 注意：`qwen-turbo` 等轻量模型**不支持函数调用**；仅 `qwen-plus`、`qwen-max` 及 VL 系列等高级模型具备此能力。OpenAI 兼容的 Chat Completions 接口**不原生支持函数调用**，需自行封装；而 DashScope 原生、Anthropic Messages、Managed Agents、Application Call 等均原生支持。

## 关键参数和配置

| 参数/配置项 | 所属场景 | 说明 | 示例 |
|-------------|----------|------|------|
| `tools` | DashScope / Anthropic Messages | 工具定义数组，每个元素为 JSON Schema 描述的函数元信息（`type`, `function.name`, `function.description`, `function.parameters`） | `[{"type":"function","function":{"name":"calculator","description":"计算数学表达式","parameters":{"type":"object","properties":{"expression":{"type":"string"}}}}}]` |
| `tool_calls` | DashScope 响应字段 | 模型输出的结构化调用指令，含 `id`、`function.name`、`function.arguments` | `{"id":"call_abc123","function":{"name":"calculator","arguments":"2+3*4"}}` |
| `tool_outputs` | 下一轮请求字段 | 客户端执行工具后，必须将结果按 `id` 映射回填，格式为 `[{ "tool_call_id": "...", "content": "..." }]` | `[{"tool_call_id":"call_abc123","content":"14"}]` |
| `description`（`SKILL.md`） | Skill | 决定 Skill 是否被调用的核心语义描述，必须明确输入类型、操作、触发词、排除场景 | `"支持解析.xlsx文件中的销售数据，清洗空值并按月份汇总；触发词：'整理销售表'、'导出月度汇总'；不处理图片表格。"` |
| `tool_id` | Plugin / Application Call | 插件唯一标识符，用于在应用配置或 API 中引用 | `"quark_search"`, `"code_interpreter"` |
| `biz_params` | Application Call / Workflows | 业务系统透传的结构化参数，可被模型抽取或直接注入插件/MCP 节点 | `{"city": "杭州", "date": "2025-04-25"}` |

## 面向开发者，简洁实用

- ✅ **首选 DashScope 原生协议**：若需最大灵活性（如动态工具列表、自定义执行逻辑），直接使用 `/api/v1/services/aigc/text-generation/generation` 接口，传 `tools` 并处理 `tool_calls`/`tool_outputs`。
- ✅ **快速上线选 Managed Agents**：上传 Skill ZIP 包，专注写好 `SKILL.md` 描述，平台自动完成路由与沙箱执行，免去 HTTP 封装与状态管理。
- ✅ **复用生态用 Application Call**：已发布智能体/工作流应用，直接调用 `POST /apps/{app_id}/completion`，通过 `input` 和 `biz_params` 驱动插件或 MCP 服务。
- ❌ **避免硬编码内部字段**：如 `payload__input__text` 等非公开字段可能变更，始终以控制台调试器生成结构或官方 API 文档为准。
- 🔑 **权限必配**：首次使用任何函数调用能力（Skill/Plugin/MCP），必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`，否则调用失败。
- 📏 **[Token](token.md) 注意**：每次函数调用会增加输入 [Token](token.md)（工具描述+调用结果注入），可能导致总长度超 32768 token 限制，建议精简 `description` 和 `parameters` Schema。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [managed agents api](../api/managed-agents-api.md)
- [application call](../api/application-call.md)
- [model context protocol](../guides/model-context-protocol.md)
- [plug in](../guides/plug-in.md)
- [skill](../guides/skill.md)


