# 函数调用

函数调用（Function Calling）是百炼平台中大语言模型主动识别用户意图、并按需触发外部工具或服务的能力。它允许模型在生成响应前，自主决定是否调用预定义的函数（如搜索、计算、数据库查询等），并将结果整合进最终输出，从而实现可控、可扩展的智能体行为。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台主要应用于**文本生成类模型**（特别是 `qwen3-*` 系列），是构建智能体（Agent）的核心机制，具体体现为以下三类场景：

- **[OpenAI 兼容接口](openai-compatible-interface.md)（Chat Completions）**：通过 `tools` 数组注册函数 Schema，并设置 `tool_choice`（如 `"auto"` 或指定函数名）启用调用；模型返回 `tool_calls` 字段，开发者需解析并执行对应函数，再将结果以 `tool` 角色消息回传发起下一轮推理。
- **DashScope 原生接口**：使用 `tools` + `enable_tool_choice: true` 显式开启；支持更细粒度控制，例如 `tool_choice: "none"` 强制禁用、`"required"` 强制调用至少一个函数；返回结构统一为 `output.choices[0].message.tool_calls`，含 `function.name` 和 `function.arguments`（JSON 字符串）。
- **Responses API（专为智能体设计）**：无需手动管理 `tool_calls` 生命周期——平台自动完成函数发现、调用、结果注入与上下文维护；开发者仅需提供 `tools` 定义和业务逻辑函数，平台会透明处理多轮交互与状态流转，适用于快速搭建搜索增强、代码解释、实时数据查询等 Agent 应用。

> ⚠️ 注意：函数调用能力**仅限文本生成模型**（如 `qwen3.7-plus`、`qwen3.7-max`、`qwen3-coder-plus`），不支持视觉（Qwen-VL）、语音（Qwen-Audio）、3D（Tripo）或向量/重排序类模型。Qwen-VL 等多模态模型虽支持工具调用的 *语义理解*，但其原生协议不开放 `tool_calls` 输出字段。

## 关键参数和配置

| 参数 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `tools` | array[object] | 必填。函数定义列表，每个对象为标准 JSON Schema 描述（含 `name`, `description`, `parameters`）；Schema 需严格符合 OpenAPI 3.0 规范，否则模型无法解析。 | `[{"name": "web_search", "description": "联网搜索最新信息", "parameters": {"type": "object", "properties": {"query": {"type": "string"}}}}]` |
| `tool_choice` | string / object | 控制调用策略：<br>- `"auto"`（默认）：由模型自主判断是否调用；<br>- `"none"`：禁止调用；<br>- `"required"`：必须调用至少一个；<br>- `{"type": "function", "function": {"name": "xxx"}}`：强制调用指定函数。 | `"auto"`, `{"type": "function", "function": {"name": "get_weather"}}` |
| `enable_tool_choice` | boolean | DashScope 原生接口专用。设为 `true` 才启用函数调用能力（即使提供了 `tools`）。 | `true` |
| `max_tool_rounds` | integer | DashScope 原生接口可选。限制函数调用最大轮数（防止死循环），默认 `3`，取值范围 `1–5`。 | `3` |

## 面向开发者，简洁实用

- ✅ **推荐实践**：优先使用 `qwen3.7-plus` 或 `qwen3.7-max` 模型 + DashScope 原生接口，获得最稳定、最完整的函数调用支持（包括 `max_tool_rounds`、`enable_tool_choice` 等控制能力）。
- ✅ **调试技巧**：首次集成时，先用 `tool_choice: "none"` 获取纯文本响应，验证 [prompt](../guides/prompt.md) 和 tools 定义；再切换为 `"auto"`，检查返回中是否出现 `tool_calls` 字段及参数格式是否合法。
- ⚠️ **避坑提示**：
  - `tools` 中的 `parameters` 必须是 JSON Schema 对象，**不能是 Python dict 或字符串**；建议用 `json.dumps(schema)` 校验格式；
  - 函数执行失败后，务必以 `role: "tool"`、`content: <error_message>` 形式回传错误，否则模型可能重复调用；
  - [OpenAI 兼容接口](openai-compatible-interface.md)中，`function_call` 字段已逐步被 `tool_calls` 替代，SDK 调用请直接访问 `response.choices[0].message.tool_calls`；
  - 所有函数调用均计入 token 消耗（含 `tools` 定义、`tool_calls` 输出、`tool` 消息输入），长链路 Agent 需监控 `usage.total_tokens` 防超限。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [more about models](../api/more-about-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


