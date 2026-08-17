# 函数调用

函数调用（Function Calling）是百炼平台模型（特别是 Qwen3 系列及全模态旗舰模型）原生支持的核心能力，允许模型在推理过程中主动识别用户意图、生成结构化工具调用请求（而非仅输出自然语言），并将结果交由外部系统执行后注入上下文，实现可控、可扩展的智能体行为。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中不是独立 API，而是嵌入在标准对话接口（如 `/chat/completions` 和 `/responses`）中的语义能力，需配合模型能力、系统提示词与参数配置协同生效：

- **智能体构建**：当使用 `qwen3.7-plus`、`qwen3.5-omni-plus`、`deepseek-v4-*` 等支持 Function Calling 的模型时，开发者通过 `tools` 参数声明可用函数（JSON Schema 描述），模型会自动判断是否需要调用、选择哪个函数、并填充合法参数。返回结果中 `tool_calls` 字段即为结构化调用指令，无需正则解析或关键词匹配。
  
- **内置工具链集成**：`/responses` 接口对 `qwen3.*` 系列模型默认启用联网搜索、网页抓取、代码解释器等内置工具，此时函数调用由平台自动管理——开发者无需传入 `tools`，但需通过 `enable_thinking=true` 显式开启思考链，确保模型在调用前进行合理规划。

- **RAG 与知识库联动**：结合百炼知识库服务，可将知识检索封装为自定义 `tool`，模型在回答中触发该函数，平台自动执行向量检索并注入 top-k 结果，实现“思考→检索→合成”的闭环。

- **多模态协同控制**：在 `qwen3.5-omni-plus` 等全模态模型中，函数调用可与音视频输入共存（如用户上传语音+提问“查下今天北京天气”，模型调用天气 API 并返回结构化响应），但注意：**联网搜索与 Function Calling 不可同时启用**（二者互斥，需根据场景二选一）。

> ⚠️ 注意：并非所有模型均支持。`qwen-coder-turbo`、`text-embedding-*`、`qwen-audio-*`（除 S2S 模型外）、`qwen3-vl-embedding` 等专用模型**不支持**函数调用；`qwen3-omni-flash` 支持函数调用但不支持联网搜索；`qwen3.5-omni-plus` 支持二者之一，不可共存。

## 关键参数和配置

| 参数 | 类型 | 说明 | 必填性 |
|------|------|------|--------|
| `tools` | array of objects | 定义可用函数列表，每个对象含 `type="function"`、`function.name`、`function.description`、`function.parameters`（JSON Schema） | 仅当使用自定义工具时必填；内置工具（如 `/responses`）无需提供 |
| `tool_choice` | string or object | 控制调用策略：`"auto"`（默认，模型自主决定）、`"none"`（禁用）、`{"type": "function", "function": {"name": "xxx"}}`（强制指定） | 可选，建议显式设为 `"auto"` 或 `"none"` 避免歧义 |
| `response_format` | object | 若需模型最终输出严格 JSON，可设 `{"type": "json_object"}`，但注意：**启用后模型将不再返回 `tool_calls`**（二者互斥） | 可选，与函数调用不可共存 |
| `enable_thinking` | boolean | 仅 `/responses` 接口有效，必须设为 `true` 才能激活内置工具链（含函数调用逻辑） | 使用 `/responses` + 内置工具时必填 |
| `previous_response_id` | string | 用于多轮对话中延续工具调用上下文，确保后续响应能关联前序 `tool_calls` 和执行结果 | 强烈推荐在智能体多轮交互中传入 |

- **调用流程关键点**：
  - 模型首次响应可能含 `tool_calls`（无 `content`），此时需开发者解析并执行对应函数；
  - 执行完成后，需将结果以 `tool_message` 格式（含 `tool_call_id` 和 `content`）作为新消息发回，模型据此生成最终自然语言回复；
  - 百炼 SDK（Python/Node.js）已内置 `parse_tool_calls()` 和 `build_tool_message()` 工具方法，推荐直接复用。

## 面向开发者，简洁实用

- ✅ **快速验证**：用 `qwen3.7-plus` + 最小 `tools` 示例（如一个 `get_weather` 函数），观察返回是否含 `tool_calls`；
- ✅ **生产建议**：始终设置 `tool_choice: "auto"`，避免硬编码导致模型拒答；对敏感操作（如数据库写入），务必在函数执行层做权限校验与参数白名单过滤；
- ❌ **避坑提醒**：
  - 不要混用 `response_format={"type":"json_object"}` 和 `tools` —— 二者冲突，API 将报错；
  - `qwen3.5-omni-plus` 启用 `tool_choice` 后，自动禁用联网搜索，反之亦然；
  - 临时 API Key 继承全部权限，若 `tools` 指向内部服务，需确保该 Key 作用域受限，防止越权调用。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [model experience](../guides/model-experience.md)


