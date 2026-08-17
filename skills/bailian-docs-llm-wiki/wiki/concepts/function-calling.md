# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、生成结构化工具调用请求，并交由外部系统执行关键操作的核心能力。它使大模型能突破纯文本生成边界，安全、可控地接入实时搜索、代码执行、图像生成、API 服务等外部能力，实现“思考—规划—执行—整合”的闭环。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台并非单一接口特性，而是贯穿多个能力层的横切机制，具体体现为：

- **OpenAI 兼容 Chat Completions 接口**：通过 `tools` 数组声明可用函数，设置 `tool_choice="auto"` 或指定函数名，模型返回 `tool_calls` 结构（含 `function.name` 和 `function.arguments`）。注意：该接口**不支持流式响应中的 `delta.tool_calls`**，工具调用结果统一以 `content` 字段返回。
  
- **DashScope 原生与 Anthropic Messages 接口**：原生支持完整 `tool_calls` 流式解析（`delta.tool_calls`），便于前端实时渲染调用过程；Anthropic 接口还支持显式控制 `tool_use` 行为与 `thinking` 链路，适合需精细编排执行逻辑的场景。

- **Managed Agents（托管智能体）**：函数调用被深度集成进会话生命周期。Agent 定义时绑定 Skill（即函数集合），Session 执行中自动触发工具调用，结果通过 `Event` 类型（如 `tool_result`）流式推送至 SSE 订阅端，开发者无需手动解析或重试。

- **插件（Plug-in）体系**：所有插件（官方/三方/自定义）本质即注册的可调用函数。模型通过 `tools` 声明后，即可自主决策调用 `quark_search`、`calculator`、`code_interpreter` 等工具；插件市场提供参数映射示例，显著提升 `arguments` 生成准确率。

- **Responses API（增强对话）**：内置联网搜索、网页提取、代码解释器三类函数，**无需显式声明 `tools`**，模型自动维护调用上下文并整合结果，适合快速构建具备增强推理能力的应用。

## 关键参数和配置

| 参数 | 位置 | 说明 | 注意事项 |
|------|------|------|----------|
| `tools` | 请求体（必填） | 工具定义数组，每个元素为 `{ "type": "function", "function": { "name", "description", "parameters" } }` | [OpenAI 兼容接口](openai-compatible-interface.md)需 JSON Schema 格式；DashScope 原生接口支持更灵活的参数类型声明 |
| `tool_choice` | 请求体（可选） | 控制调用策略：`"none"`（禁用）、`"auto"`（默认）、`{"type": "function", "function": {"name": "xxx"}}`（强制） | Anthropic Messages 使用 `tool_use` 字段替代 |
| `enable_thinking` | 请求体顶层（可选） | 启用思考模式，生成 reasoning tokens，辅助更可靠的函数参数推断 | 仅部分模型（如 `qwen3.7-plus`）支持；Batch 场景下必须作为 JSONL `body` 顶层字段 |
| `previous_response_id` | Responses API 请求头或请求体 | 多轮对话中注入历史工具执行结果的关键 ID | 必须传入上一轮响应的顶层 `id`（UUID），非消息内 `id` |

> ⚠️ 重要限制：  
> - `qwen-vl` 与 `qwen-audio` 系列模型**不支持 Anthropic Messages 接口**，函数调用需通过 DashScope 原生接口实现；  
> - `code_interpreter` 插件**禁止网络访问与文件上传**，依赖版本已固化；  
> - 单个智能体最多绑定 **10 个工具**，超限需精简或聚合功能。

## 面向开发者，简洁实用

- ✅ **快速启用**：只需在请求中添加 `tools` 数组 + `tool_choice="auto"`，模型即自动规划调用，无需修改业务逻辑。  
- ✅ **安全可控**：所有工具调用均经沙箱（Managed Agents）或鉴权网关（插件）执行，输入/输出受严格参数校验。  
- ✅ **调试友好**：使用 DashScope 原生或 Anthropic 接口，可流式捕获 `tool_calls` → `tool_result` 全链路事件，精准定位参数错误。  
- ✅ **生产就绪**：Managed Agents 提供 Session 状态机与 SSE 事件流，天然适配长周期、多步骤函数调用场景。  
- ❌ **避免踩坑**：勿在 [OpenAI 兼容接口](openai-compatible-interface.md)中依赖 `delta.tool_calls`；勿对 `qwen-vl` 模型使用 `tool_use`；自定义插件 Object 参数子属性**不能为空**。  

函数调用不是附加功能，而是百炼平台“模型即服务”架构的中枢能力——它让模型真正成为可调度、可审计、可扩展的智能执行单元。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [managed agents api](../api/managed-agents-api.md)
- [model experience](../guides/model-experience.md)
- [plug in](../guides/plug-in.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


