# 函数调用

函数调用（Function Calling）是百炼平台支持的核心能力之一，指大语言模型在生成响应过程中，主动识别用户意图并结构化地选择、参数化调用外部工具（如搜索、代码执行、API 服务等），从而将自然语言请求转化为可执行动作的能力。该机制使模型具备“行动力”，是构建智能体（Agent）、自动化工作流和复杂交互式应用的基础。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用能力在百炼平台中并非全局默认启用，其可用性与行为高度依赖所选接口协议和模型：

- **DashScope 原生接口**：完全支持自定义函数调用。开发者通过 `tools` 参数传入 JSON Schema 格式的工具定义列表（含 `name`、`description`、`parameters`），模型返回结构化的 `tool_calls` 字段，包含 `function.name` 和 `function.arguments`；后续需由业务代码解析并执行对应工具，再将结果以 `tool_message` 形式回填至对话历史继续推理。

- **Anthropic 兼容-Messages 接口**：支持 `tool_use` 结构化输出，语义与 DashScope 一致，但响应格式遵循 Anthropic 的 `content` 数组规范（含 `{"type": "tool_use", "id": "...", "name": "...", "input": {...}}`）。注意：`system` 提示词被截断至 4096 token，可能影响工具描述的完整性。

- **OpenAI 兼容-Responses 接口**：**不支持自定义 `tools`**，仅内置三类预置工具（联网搜索、代码解释器、网页内容提取），由平台自动触发与执行，开发者无法增删或修改。该模式下无需传 `tools`，也无需手动处理 `tool_calls`，适合快速搭建免运维助手。

- **OpenAI 兼容-Chat Completions 接口**：**不支持任何函数调用能力**（包括 `tool_calls` 字段解析），即使传入 `tools` 参数也会被忽略。若需结构化工具交互，请切换至 DashScope 或 Anthropic 兼容接口。

> ✅ 提示：`qwen3.7-plus` 是当前唯一同时支持「自定义函数调用 + 内置工具 + 结构化 JSON 输出」的旗舰模型；`qwen3.7-max` 虽推理更强，但明确不支持函数调用与结构化输出，选型时请按需权衡。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 注意事项 |
|------|------|------|------|----------|
| `tools` | array | 否（启用函数调用时必填） | 工具定义列表，每个元素为符合 OpenAPI 3.0 Schema 的 JSON 对象，必须包含 `name`（字符串，无空格/特殊字符）、`description`（功能说明）、`parameters`（JSON Schema 描述输入结构） | 仅 DashScope 原生与 Anthropic 兼容接口支持；[OpenAI 兼容接口](openai-compatible-interface.md)传入将被静默忽略 |
| `tool_choice` | string / object | 否 | 控制模型调用策略：<br>• `"auto"`（默认）：由模型自主决定是否调用及调用哪个工具<br>• `"none"`：禁止调用任何工具<br>• `{"type": "function", "function": {"name": "xxx"}}`：强制调用指定工具 | DashScope 接口支持全部值；Anthropic 兼容接口仅支持 `"auto"` 和 `"none"` |
| `enable_search` / `enable_code_interpreter` | boolean | 否（仅 Responses 接口） | OpenAI 兼容-Responses 中用于开关内置工具的布尔参数 | 仅该接口有效，与 `tools` 互斥；不可与自定义工具混用 |
| `output_format` | string | 否 | 当需返回结构化 JSON 时设为 `"json"`（DashScope 接口），确保模型严格按 schema 输出 | 与函数调用配合使用可提升 `arguments` 解析可靠性；[OpenAI 兼容接口](openai-compatible-interface.md)不支持此参数 |

## 面向开发者，简洁实用

- ✅ **首选 DashScope 接口**：如需完整控制权（自定义工具、精确参数校验、错误重试、多轮 tool_message 管理），务必使用 DashScope 原生 endpoint（`/api/v1/services/aigc/text-generation/generation`），并严格按 `input.messages` + `tools` + `tool_choice` 组织请求。
- ⚠️ **避免混淆接口能力**：不要在 [OpenAI 兼容接口](openai-compatible-interface.md)中尝试传 `tools`，也不会收到 `tool_calls`；也不要期望 Responses 接口返回可解析的 `function.arguments` —— 它只返回执行后的自然语言结果。
- 🔍 **调试建议**：首次集成时，先用 `stream: false` 发送非流式请求，检查响应中是否存在 `output.choices[0].message.tool_calls`（DashScope）或 `content` 中的 `tool_use`（Anthropic）；确认结构后再接入流式解析逻辑。
- 🛡️ **安全实践**：所有 `tool_calls` 的 `arguments` 均为模型生成的字符串，**必须经 JSON Schema 校验 + 白名单参数过滤 + 沙箱执行**，严禁直接 `eval()` 或透传至敏感系统。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [model experience](../guides/model-experience.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more about models](../api/more-about-models.md)


