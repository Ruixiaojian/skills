# 函数调用

函数调用（Function Calling）是百炼平台中大语言模型主动识别用户意图、生成结构化工具调用请求，并交由外部系统执行的能力。它使模型能突破纯文本生成边界，安全、可控地接入计算、搜索、多模态生成等真实世界能力，是构建智能体（Agent）、工作流（Workflow）和高阶 Assistant 应用的核心机制。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一 API 特性，而是贯穿多个调用路径的**统一能力层**，具体使用方式取决于所选接口与模型：

- **DashScope 原生接口（推荐）**：通过 `tools` 参数声明可用函数列表（含 `name`、`description`、`parameters`），配合 `tool_choice`（如 `"auto"`、`"required"` 或指定 `{"type": "function", "function": {"name": "xxx"}}`）精确控制调用行为。模型返回 `tool_calls` 字段，包含函数名与参数 JSON；开发者需解析并同步/异步执行对应工具，再将结果以 `tool_message` 形式回传继续对话。这是功能最完整、参数最灵活的方式，支持 `parallel_tool_calls`、`response_format: { "type": "json_object" }` 等高级能力。

- **Anthropic 兼容 Messages 接口**：使用 `tool_use` 数组声明工具，模型在 `content` 中返回 `{"type": "tool_use", "name": "...", "input": {...}}` 结构。注意：Qwen 模型对 `stop_sequences` 的处理逻辑与 Anthropic 原生不同，实际行为请以官方文档为准。

- **OpenAI 兼容 Chat Completions 接口**：支持基础 `tools` 和 `tool_choice`，但**不支持 `parallel_tool_calls`、`response_format`（JSON mode）及细粒度 `tool_choice` 控制**。适用于快速迁移 OpenAI 项目，但复杂工具编排建议切换至 DashScope 原生接口。

- **Responses API（智能体原生响应）**：内置联网搜索、代码解释器、网页提取等官方工具，无需显式声明 `tools`。通过 `enable_search: true` 或 `code_interpreter: true` 开关启用，模型自动规划调用流程并维护上下文状态，适合开箱即用的智能体场景。

- **插件（Plug-in）体系**：函数调用是插件能力的底层支撑。官方插件（如 `quark_search`、`code_interpreter`）和自定义插件均被注册为标准化函数，可在智能体、工作流或 Assistant API 中按需启用。插件调用由模型自主触发（智能体模式）或人工编排（工作流节点），其输入/输出参数、鉴权配置均通过函数签名定义。

> ✅ **关键提示**：  
> - 所有通用文本/视觉模型（如 `qwen3.7-plus`、`qwen-vl-plus`）均支持函数调用，但 `deepseek-v4-pro` 等第三方模型明确标注“不支持内置工具”；  
> - `qwen3.7-plus` 是当前结构化输出与函数调用能力最均衡的旗舰模型，推荐新项目首选；  
> - 函数调用本身不计费，但**工具执行产生的资源消耗（如搜索API调用、图像生成Token）单独计费**。

## 关键参数和配置

| 参数 | 类型 | 说明 | 是否必需 | 备注 |
|------|------|------|----------|------|
| `tools` | array | 工具函数定义列表，每个对象含 `name`（字符串）、`description`（字符串）、`parameters`（JSON Schema） | 否（但启用调用必须提供） | `parameters` 必须为合法 JSON Schema，`required` 字段需显式声明必填项 |
| `tool_choice` | string / object | 控制模型是否及如何调用工具：<br>`"none"`：禁用调用<br>`"auto"`：模型自主决定（默认）<br>`"required"`：强制调用一个工具<br>`{"type": "function", "function": {"name": "xxx"}}`：指定调用某函数 | 否（默认 `"auto"`） | DashScope 原生接口支持全部值；[OpenAI 兼容接口](openai-compatible-api.md)仅支持 `"none"`/`"auto"`/`"required"` |
| `enable_search` | boolean | Responses API 专用开关，启用内置联网搜索 | 否（默认 `false`） | 与 `quark_search` 插件功能重叠，但更轻量、无需插件授权 |
| `code_interpreter` | boolean | Responses API 专用开关，启用内置 Python 执行环境 | 否（默认 `false`） | 禁止网络访问与文件上传，仅预装 `pandas`/`matplotlib`/`sympy` 等依赖 |

- **工具执行后回传格式（必需）**：  
  当模型返回 `tool_calls` 后，必须构造 `messages` 数组追加一条 `role: "tool"` 消息，格式为：  
  ```json
  {
    "role": "tool",
    "content": "<tool_execution_result>",
    "tool_call_id": "<id_from_tool_calls>"
  }
  ```
  缺少 `tool_call_id` 或内容格式错误将导致后续推理失败。

- **安全与权限**：  
  - 自定义插件需配置鉴权（Header/Query），Token 通过 `biz_params` 或控制台变量注入；  
  - 子业务空间调用工具时，必须使用该空间专属 API Key，且工具需已在空间内显式授权。

## 面向开发者，简洁实用

- **起步最快**：用 `qwen3.7-plus` + DashScope 原生接口，`tools` 定义清晰，`tool_choice: "auto"` 即可跑通首个调用闭环。  
- **调试技巧**：开启 `stream: true` 观察模型思考过程；检查响应中的 `finish_reason` —— `"tool_calls"` 表示成功触发，`"stop"` 表示未调用。  
- **错误排查**：  
  - `130040` 错误 → `tools` 中 `parameters` 缺少 `description` 或 `type`；  
  - `130022` 错误 → `Object` 类型参数在 GET 请求中被拒绝，改用 POST；  
  - 工具无响应 → 确认 `tool_call_id` 严格匹配，且 `content` 为字符串（非 JSON 对象）。  
- **生产建议**：  
  - 工具执行超时需设置合理 `timeout` 并捕获异常，避免阻塞对话；  
  - 敏感操作（如支付、删库）务必在工具实现层做二次确认，不可依赖模型判断；  
  - 使用 `qwen3.7-plus-20240701` 等版本号锁定模型，避免因升级导致函数签名变更。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [model experience](../guides/model-experience.md)
- [more about models](../api/more-about-models.md)
- [plug in](../guides/plug-in.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


