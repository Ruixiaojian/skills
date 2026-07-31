# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、自主决策并调用外部工具（插件）完成特定任务的核心能力。它通过结构化协议让模型输出标准化的[工具调用](tool-use.md)指令（`tool_calls`），由客户端执行实际调用并将结果回传，从而实现“规划-执行-反思”的闭环推理流程。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用能力在百炼平台中并非通用默认功能，而是**按模型和接口类型差异化支持**，需明确启用并遵循对应协议：

- **文本生成类模型（如 `qwen3.7-plus`、`qwen3.5-omni-realtime`）**：  
  在 `/api/v1/services/...` 或 OpenAI 兼容 `chat/completions` 接口调用中，通过 `tools` 参数声明可用工具列表，并设置 `tool_choice`（如 `"auto"` 或指定 `tool`）。模型将返回 `tool_calls` 字段（含 `id`、`function.name`、`function.arguments`），**客户端必须解析、执行调用、获取结果，并以 `tool_message` 形式再次提交给模型继续推理**。

- **Responses API（智能体专用接口）**：  
  是函数调用最简化的落地方式。只需在请求中传入 `tools`，平台自动完成[工具调用](tool-use.md)、结果注入与多轮编排，开发者无需手动处理 `tool_calls` 和 `tool_message` 的往返逻辑。适用于快速构建具备搜索、计算、文生图等能力的智能体应用。

- **Omni Realtime WebSocket 接口**：  
  仅 `qwen3.5-omni-realtime` 系列支持 `tools` 参数（与 `enable_search` 互斥）。[工具调用](tool-use.md)发生在实时语音/文本会话中，需通过 `response.create` 事件触发，并在 `tool_call` 事件中接收调用指令；客户端执行后，须通过 `tool_response` 事件回传结果。

- **插件市场与工作流应用**：  
  在控制台配置插件时，“函数调用”体现为模型的**自主决策权**：当启用“大模型识别”参数模式时，模型根据上下文判断是否需要调用、调用哪个插件及传入何参数；而在工作流节点中，插件调用由人工编排驱动，不依赖函数调用机制。

> ⚠️ 注意：`qwen-omni-turbo-realtime`、`qwen3.7-max`（部分快照版）、`qwen-audio` 等模型**不支持函数调用**；Qwen-Audio 系列仅支持 DashScope 原生协议，且无工具调用能力。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 必填 |
|------|------|------|------|------|
| `tools` | 请求 body 顶层 | `array` | 工具定义列表，每个对象含 `type="function"`、`function.name`、`function.description`、`function.parameters`（JSON Schema 格式） | 是（启用函数调用时） |
| `tool_choice` | 请求 body 顶层 | `string` 或 `object` | 控制调用策略：`"none"`（禁用）、`"auto"`（模型自主决定）、`{"type": "function", "function": {"name": "xxx"}}`（强制指定） | 否（默认 `"auto"`） |
| `tool_choice`（Responses API） | 请求 body 顶层 | `string` | 仅支持 `"auto"` 或 `"none"` | 否 |
| `previous_response_id`（Responses） | 请求 body 顶层 | `string` | 上一轮响应的 `id`（UUID），用于维持多轮工具调用上下文 | 多轮调用时必填 |
| `biz_params`（自定义插件） | 请求 body `tools` 内或顶层 | `object` | 业务透传参数，用于传递鉴权 [Token](token.md)、用户 ID 等非语义信息 | 按插件配置要求 |

- **工具定义规范**：`function.parameters` 必须为合法 JSON Schema（支持 `string`、`number`、`boolean`、`object`、`array`），`object` 类型的子属性不可为空（否则发布失败）。
- **工具 ID 对齐**：`function.name` 必须与插件市场或自定义插件中注册的 `tool_id` 完全一致（区分大小写）。
- **安全要求**：首次使用插件前，主账号需授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`；RAM 用户需额外获得 `ram:CreateServiceLinkedRole` 权限。

## 面向开发者，简洁实用

- ✅ **推荐路径**：优先使用 **Responses API**，它封装了函数调用全流程，大幅降低集成复杂度。
- ✅ **调试技巧**：开启 `stream: false` + `enable_thinking: true`，可清晰观察模型的思考链（Thought）与工具调用决策过程。
- ✅ **错误排查**：若模型未返回 `tool_calls`，检查 `tools` 是否有效、`tool_choice` 是否为 `"auto"`、模型是否支持该能力（参见 [model experience](model-experience.md)）。
- ❌ **避免陷阱**：不要在 `qwen-omni-turbo-realtime` 等不支持模型上设置 `tools`；勿将 `tools` 放入 `extra_body`（[OpenAI 兼容接口](openai-compatible-api.md)）或 `messages` 中——必须置于请求 body 顶层。
- 🚀 **生产建议**：对高并发场景，工具调用结果回传应异步化处理，避免阻塞模型推理；敏感工具（如支付、数据库操作）务必在客户端做二次鉴权与参数校验。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [model experience](../guides/model-experience.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [plug in](../guides/plug-in.md)


