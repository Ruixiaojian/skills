# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、结构化提取参数，并自主触发外部工具或服务的核心能力。它使大模型从纯文本生成器升级为可执行动作的智能代理，支持在单次推理中完成搜索、计算、图像生成、代码执行等任务。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用能力深度集成于以下三类核心场景：

- **智能体（Agent）与 Assistant API**：模型根据用户输入自动判断是否需调用[插件](plugin.md)（如 `quark_search`、`calculator`），并生成符合 OpenAI Tool Calling 格式的 `tool_calls` 响应；开发者需在 `tools` 字段中声明可用工具定义（含 `function.name`、`description`、`parameters`），平台将自动完成参数解析与调用编排。  
- **文本生成模型（如 `qwen3.7-plus`、`qwen3.5-omni-plus`）**：原生支持 Function Calling，无需额外配置即可响应结构化请求；配合 `response_format={"type": "json_object"}` 可实现“先思考再调用”或“直接输出 JSON 结构”，适用于 RAG 后处理、API 编排等场景。  
- **工作流应用（Workflow）**：支持显式声明 `plugin_ids` 或通过 MCP 节点接入自定义[插件](plugin.md)，此时函数调用由流程引擎控制而非模型自主决策，适合确定性高、安全要求严的业务链路（如金融风控、政务审批）。

> ⚠️ 注意：并非所有模型均支持函数调用。需通过 `/api/v1/models` 接口查询模型能力标签（`function-calling: true`），或参考 [模型体验指南](guides/model-experience.md) 中各模型的“内置工具”支持状态。`qwen-turbo`、`deepseek-v4-flash` 等轻量模型默认不支持，`qwen3.5-omni-flash`（HTTP 版）支持但不支持联网搜索类[插件](plugin.md)。

## 关键参数和配置

| 参数 | 类型 | 说明 | 必填 |
|------|------|------|------|
| `tools` | array[object] | 工具定义列表，每个对象包含 `type="function"`、`function.name`、`description`、`parameters`（JSON Schema） | 是（启用函数调用时） |
| `tool_choice` | string \| object | 控制调用策略：`"auto"`（默认，模型自主决定）、`"none"`（禁用）、`{"type": "function", "function": {"name": "xxx"}}`（强制指定） | 否 |
| `response_format` | object | 指定输出格式：`{"type": "json_object"}` 可强制模型返回结构化 JSON（含工具调用字段），提升解析鲁棒性 | 否（推荐启用） |
| `plugin_ids` | array[string] | 在智能体/工作流 API 中显式启用的插件 ID 列表（如 `["qwen-calculator"]`），需提前在控制台授权 | 否（仅限应用层 API） |

- **工具定义要求**：`parameters` 必须为合法 JSON Schema（支持 `string`、`number`、`boolean`、`array`、`object`），避免使用 `null` 类型或未定义字段；`required` 数组需明确列出必填参数。
- **流式响应适配**：启用 `stream=True` 时，函数调用结果以 `delta.tool_calls` 分块返回，需按 `index` 顺序聚合；建议搭配 `incremental_output=True` 避免重复渲染。

## 面向开发者，简洁实用

- ✅ **快速验证**：用 `qwen3.7-plus` 模型 + `tools=[{"type":"function","function":{"name":"calculator","description":"Perform math calculation","parameters":{"type":"object","properties":{"expression":{"type":"string"}},"required":["expression"]}}}]` 测试基础调用。
- ✅ **错误排查**：若模型未触发工具，检查 `tools` 中 `description` 是否清晰、`parameters` 是否有歧义；常见报错 `130040`（参数描述缺失）需补全 `description` 字段。
- ✅ **生产建议**：  
  - 对安全性敏感场景（如支付、数据库操作），禁用 `tool_choice="auto"`，改用工作流节点显式控制；  
  - 使用 `response_format={"type": "json_object"}` + 客户端 JSON Schema 校验，避免字符串解析失败；  
  - 自定义插件务必测试 `biz_params` 透传逻辑，确保业务上下文（如用户 ID、会话 ID）准确注入。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [model experience](../guides/model-experience.md)
- [plug in](../guides/plug-in.md)
- [application support](../guides/application-support.md)


