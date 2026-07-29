# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、生成结构化工具调用请求，并交由外部系统执行的关键能力。它使大语言模型能突破纯文本生成边界，安全、可控地接入搜索、计算、代码执行、图像生成等真实世界服务，是构建智能体（Agent）、工作流和实时多模态应用的核心机制。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一接口，而是贯穿多个能力层的统一语义能力，具体体现为以下三类典型使用方式：

- **OpenAI 兼容 Chat 接口**：通过 `chat/completions` 请求中的 `tools` 字段声明可用函数（含名称、描述、参数 Schema），并设置 `tool_choice` 控制调用策略（如 `"auto"` 或指定工具名）。模型返回 `tool_calls` 结构，开发者解析后同步执行工具，再将结果以 `tool_message` 形式回传继续对话。适用于 `qwen3.7-plus`、`qwen-plus` 等支持 Function Calling 的文本模型。

- **插件（Plug-in）集成**：在智能体或工作流中启用插件时，底层即依赖函数调用协议。官方插件（如 `calculator`、`quark_search`）和自定义插件（需发布为 MCP 服务）均被注册为可调用函数。模型根据用户输入自动选择工具、填充参数，开发者无需手动解析 JSON Schema，平台自动完成工具路由与结果注入。

- **Omni Realtime API（WebSocket 实时交互）**：在语音/多模态实时会话中，通过 `session.update` 事件的 `tools` 参数动态注册函数。模型在流式响应过程中触发 `function_call` 类型事件，携带 `name` 和 `arguments`；客户端执行后，通过 `conversation.item.input_text` 或 `conversation.item.function_call_output` 回传结果。该模式支持低延迟、上下文连续的工具链协同，仅 `qwen3.5-omni-realtime` 系列完整支持。

> ⚠️ 注意：`enable_search`（模型级联网）与 `tools`（显式函数调用）互斥，不可同时启用；`qwen-omni-turbo-realtime` 等轻量模型不支持自定义 `tools`，仅提供内置能力。

## 关键参数和配置

| 参数 | 所属场景 | 说明 | 注意事项 |
|------|----------|------|----------|
| `tools` | 所有场景 | 工具定义列表，每个元素含 `type="function"`、`function.name`、`function.description`、`function.parameters`（JSON Schema） | Schema 必须严格符合 OpenAPI 3.0 规范；`parameters` 为必需字段，即使为空也需设为 `{}` |
| `tool_choice` | Chat 接口 | 控制模型是否及如何调用工具：`"none"`（禁用）、`"auto"`（默认）、`{"type": "function", "function": {"name": "xxx"}}`（强制指定） | 若未声明 `tools`，设置 `tool_choice` 将导致 400 错误 |
| `tool_message` | Chat 接口 | 工具执行完成后，以 `role="tool"`、`tool_call_id`、`content`（字符串或 JSON 对象）格式回传结果 | `tool_call_id` 必须与模型返回的 `id` 完全一致，否则会话中断 |
| `function_call` 事件 | Omni Realtime | WebSocket 流中推送的事件类型，含 `name` 和 `arguments` 字段 | `arguments` 为字符串，需 JSON.parse()；若解析失败，需返回错误事件终止会话 |
| `biz_params` / `user_defined_params` | 插件调用 | 用于透传业务参数（如 API Key、用户 ID），绕过模型抽取逻辑 | 仅对配置为“业务透传”的输入参数生效；敏感信息应通过 RAM 角色或环境变量注入，避免硬编码 |

## 面向开发者，简洁实用

- ✅ **首选 OpenAI 兼容方式**：新项目优先使用 `chat/completions` + `tools`，生态成熟、调试直观、SDK 支持完善。
- ✅ **插件即开即用**：业务空间内已授权的官方插件，直接绑定智能体即可启用，无需编写 Schema 或处理回调。
- ✅ **Realtime 场景慎用自定义工具**：`qwen3.5-omni-realtime` 支持完整函数调用，但需自行管理 WebSocket 连接、事件序列与超时重试；建议封装为 SDK 中间件。
- ❌ **避免混合模式**：不要在同一会话中混用 `enable_search` 和 `tools`；不要在不支持的模型（如 `qwen-coder-turbo`）上尝试函数调用。
- 🔐 **安全第一**：所有工具 URL、鉴权 [Token](token.md) 必须通过 RAM 角色或密钥管理服务（KMS）注入；禁止在 `instructions` 或用户输入中硬编码凭证。
- 📏 **参数校验前置**：在模型返回 `tool_calls` 后、执行前，务必校验 `arguments` 是否符合 Schema（推荐使用 `ajv` 库），防止无效调用引发异常。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [model experience](../guides/model-experience.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [plug in](../guides/plug-in.md)
- [omni realtime api](../api/omni-realtime-api.md)


