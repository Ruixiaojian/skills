# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、结构化提取参数，并按需触发外部工具或服务执行确定性操作的核心能力。它使大模型从“文本生成器”升级为“可执行智能体”，在保持自然语言交互体验的同时，精准对接计算、搜索、图像生成等现实世界能力。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非独立功能模块，而是贯穿于多个技术路径的底层能力机制，具体体现为以下三类典型使用方式：

- **模型原生支持（Function Calling 原生模式）**：  
  `qwen3.7-plus`、`qwen3.7-max`、`qwen-audio-3.0-realtime-plus` 等旗舰模型在推理过程中**自主解析用户输入**，自动判断是否需要调用函数、选择合适工具、生成符合 Schema 的参数 JSON，并将执行结果无缝注入后续生成。该模式无需工作流编排，适用于 Assistant API 或智能体应用中的轻量级工具链（如计算器、实时搜索、代码解释器）。

- **[插件](plugin.md)系统驱动（Plugin-Driven 调用）**：  
  当使用官方/三方/自定义[插件](plugin.md)时，函数调用表现为模型对[插件](plugin.md)工具的**语义化调度**。模型基于插件注册时提供的 `name`、`description` 和 `parameters` 描述，动态生成调用请求；平台负责参数校验、鉴权转发、结果归一化。此方式解耦模型与工具实现，支持复杂业务逻辑（如 GitHub 检索、二维码生成、文生图），且所有插件调用均通过统一的函数调用协议完成。

- **[OpenAI 兼容接口](openai-compatible-api.md)显式声明（OpenAI-style Tool Calling）**：  
  使用 `/chat/completions` 等 [OpenAI 兼容接口](openai-compatible-api.md)时，开发者需在请求中显式传入 `tools` 数组（含工具定义）和 `tool_choice` 策略（如 `"auto"` 或指定 `{"type": "function", "function": {"name": "calculator"}}`）。百炼后端将模型输出的 `tool_calls` 字段解析为标准函数调用指令，并返回结构化响应。该方式便于 LangChain 等框架快速集成，兼容性强。

> ⚠️ 注意：并非所有模型均支持函数调用。例如 `qwen3.7-max` 支持函数调用但**不支持结构化 JSON 输出**（即无法强制返回纯 JSON 格式），而部分轻量模型（如 `qwen-turbo`）可能仅支持有限工具集。实际使用前请以控制台模型详情页或 [model experience](model-experience.md) 文档为准。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 示例值 |
|------|------|------|------|--------|
| `tools` | 请求体顶层 | array | 定义可用函数列表，每个元素包含 `type="function"`、`function.name`、`function.description`、`function.parameters`（JSON Schema） | `[{"type":"function","function":{"name":"calculator","description":"执行数学运算","parameters":{"type":"object","properties":{"expression":{"type":"string"}}}}}]` |
| `tool_choice` | 请求体顶层 | string / object | 控制调用策略：`"none"`（禁用）、`"auto"`（模型自主决策）、或指定函数对象 | `"auto"` 或 `{"type":"function","function":{"name":"quark_search"}}` |
| `enable_search` | 请求体顶层（旧版） | boolean | 已逐步被 `tools` 替代；若启用，模型可能隐式调用联网搜索，但**不返回原始搜索结果**（与 `quark_search` 插件有本质区别） | `true`（不推荐，优先用 `tools`） |
| `parameters.tool_call_timeout_ms` | `parameters` 内（异步/高级场景） | integer | 函数调用超时时间（毫秒），影响整体响应延迟 | `15000` |

- **工具注册要求**：自定义插件需在控制台完整填写 `parameters` 输入字段（含类型、描述、是否必填）及 `output` 字段映射，否则函数调用会因参数解析失败而中断。
- **Schema 规范**：`function.parameters` 必须为合法 JSON Schema（支持 `string`/`number`/`boolean`/`array`/`object`），嵌套层级建议 ≤2 层，避免模型误解析。
- **错误处理**：当模型生成非法 `tool_calls`（如参数缺失、类型错误）时，API 返回 `400 Bad Request` 并附带 `error.code=130011`，需检查工具定义与用户输入匹配度。

## 面向开发者，简洁实用

- ✅ **首选方案**：新项目统一使用 `tools` + `tool_choice` 方式，兼容 OpenAI 生态，调试清晰，权限可控。
- ✅ **生产建议**：对稳定性要求高的场景，显式指定 `tool_choice`（而非 `"auto"`），避免模型跳过必要工具。
- ✅ **调试技巧**：开启 `stream=true` 时，函数调用信息在 `delta.tool_calls` 中分块返回；非流式响应中直接查看 `choices[0].message.tool_calls`。
- ❌ **避坑提示**：勿混用 `enable_search` 与 `tools`；`qwen3.7-max` 支持函数调用但不返回结构化 JSON，如需 JSON 输出请改用 `qwen3.7-plus` 或启用 `response_format={"type": "json_object"}`（若模型支持）。
- 📦 **SDK 提示**：Python SDK 中，`dashscope.Generation.call()` 不直接支持 `tools`，请改用 `dashscope.ChatCompletion.create()`；LangChain 推荐使用 `ChatTongyi` 而非 `ChatOpenAI` 以获得完整函数调用支持。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [plug in](../guides/plug-in.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more about models](../api/more-about-models.md)


