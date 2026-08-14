# 函数调用

函数调用（Function Calling）是百炼平台支持的一种结构化工具协同机制，允许大模型在推理过程中主动识别用户意图、生成符合预定义 Schema 的函数调用请求，并交由外部系统执行；模型随后基于执行结果继续生成最终响应。该能力是构建智能体（Agent）、实现联网搜索、代码执行、数据库查询等复杂任务链路的核心基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

- **文本生成模型**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.7-flash` 等主力文本模型均原生支持函数调用。开发者通过 `tools` 参数注册工具列表（含名称、描述、JSON Schema），模型会在合适时机输出 `tool_calls` 字段（非自由文本），避免幻觉与格式错误。典型用于 RAG 中的实时知识检索、办公自动化中的日程/邮件操作、以及多步骤决策任务。
  
- **多模态模型**：`qwen3.7-plus` 和 `qwen3.7-flash` 视觉模型同样支持函数调用，适用于“看图决策+调用工具”混合场景，例如：分析发票图像后自动调用财务系统 API 创建报销单；或解析会议截图后触发日历工具安排后续会议。

- **语音转语音（S2S）与语音理解模型**：`qwen-audio-3.0-realtime-plus` 支持函数调用，可实现实时语音交互中的工具触发（如语音指令“查今天北京天气” → 调用气象 API）；`qwen3.5-omni-flash`（HTTP 模式）也支持，适用于视频内容分析后的动作调度（如检测到商品画面 → 调用电商比价服务）。

- **接口协议层**：函数调用能力仅在 **Chat Completions** 和 **Responses API** 接口中完整可用；OpenAI 兼容的 `completions`、`embedding`、`vision`（QVQ 流式）等接口不支持。注意：Qwen-Audio 系列模型**不支持 OpenAI 兼容协议**，其函数调用需通过 DashScope 原生协议实现。

## 关键参数和配置

- **`tools`**（必需）：数组类型，每个元素为 `{ "type": "function", "function": { "name", "description", "parameters" } }`。`parameters` 必须为 JSON Schema 对象（支持 `string`/`number`/`boolean`/`array`/`object` 及嵌套），百炼严格校验 Schema 合法性，非法 Schema 将导致 400 错误。

- **`tool_choice`**（可选）：控制调用策略：
  - `"auto"`（默认）：模型自主决定是否及调用哪个工具；
  - `"none"`：禁用函数调用，强制模型仅生成自然语言响应；
  - `{"type": "function", "function": {"name": "xxx"}}`：强制指定调用某函数（适用于确定性流程编排）。

- **`response_format`**（推荐配合使用）：当需确保模型输出严格结构化（如工具参数校验失败时重试），可设为 `{"type": "json_object"}`，提升 `tool_calls` 参数生成的稳定性。

- **工具执行与结果注入**：函数调用本身不执行——开发者需在收到含 `tool_calls` 的响应后，**同步执行对应工具逻辑**，再将结果以 `tool_message` 类型消息（含 `tool_call_id` 和 `content`）追加到对话历史，重新提交给模型完成后续推理。

- **注意事项**：
  - 单次请求最多支持 64 个工具定义；
  - 工具名（`function.name`）必须为 ASCII 字母/数字/下划线，长度 ≤ 64 字符；
  - 百炼不提供工具执行托管服务，所有工具逻辑需由业务侧实现并保障幂等性与超时控制；
  - 若模型未触发任何工具调用，响应中将不含 `tool_calls` 字段，此时应直接返回 `message.content`。

面向开发者：函数调用不是“黑盒[插件](plugin.md)”，而是明确的协议契约——你定义 Schema，模型生成合规请求，你执行并反馈结果。务必做工具侧错误处理与 fallback 设计，避免因单点失败阻断整个 Agent 流程。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more about models](../api/more-about-models.md)


