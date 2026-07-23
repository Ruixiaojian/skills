# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、自主选择并执行外部工具（如插件、Skill、代码解释器、搜索服务等）的核心能力机制。它不是简单的 API 转发，而是模型在推理过程中基于语义理解，按需生成结构化工具调用请求（含工具 ID 与参数），再由平台运行时安全调度、执行并注入结果回上下文，最终生成自然语言回复。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台并非单一接口能力，而是贯穿多个抽象层级的横切行为模式，具体体现为以下三类典型场景：

- **API 层显式声明调用**：在 DashScope 原生接口或 Anthropic 兼容 Messages 接口中，开发者通过 `tools` 字段传入工具定义（JSON Schema），并可选设置 `tool_choice` 控制调用策略（如 `"auto"`、`{"type": "function", "function": {"name": "calculator"}}`）。模型据此生成 `tool_calls` 输出，平台自动完成调用、结果注入与多轮续写。
  
- **智能体托管运行时（Managed Agents）中的隐式决策调用**：在 Managed Agents 中，函数调用完全由 Agent 运行时自主触发。开发者只需在 Agent 配置中挂载 Skill 或插件，无需在每次请求中重复声明 `tools`。Agent 根据 `SKILL.md` 的 `description` 或插件元数据，在会话中动态判断是否调用、调用哪个 Skill/插件，并处理其输入输出——整个过程对上层应用透明。

- **插件与 Skill 的能力封装层调用**：插件（Plugin）和 Skill 是函数调用的“能力载体”。插件面向通用服务（如 `quark_search`, `code_interpreter`），支持业务透传参数与鉴权；Skill 面向文件/数据处理任务（如 `xlsx-parser`），依赖精准的 `description` 触发。二者均通过统一的工具调用协议被模型识别和调度，但生命周期、配置方式与安全约束不同（如 Skill ZIP 包禁止二进制，插件需通过安全扫描）。

> ⚠️ 注意：OpenAI 兼容的 `/v1/chat/completions` 接口**不支持显式传入 `tools`**；其增强版 `/v1/chat/completions`（即 OpenAI 兼容-Responses）虽能自动启用搜索/代码解释器，但属于平台预置的全自动流水线，**不开放自定义工具注册与参数控制**，与 DashScope 和 Managed Agents 的可控性存在本质差异。

## 关键参数和配置

| 参数/配置项 | 所属场景 | 说明 | 是否必需 | 备注 |
|-------------|----------|------|----------|------|
| `tools` | DashScope / Anthropic Messages API | 工具定义数组，每个元素为符合 JSON Schema 的对象，描述工具名称、描述、参数类型与约束 | 否（启用函数调用时必需） | 不支持 [OpenAI 兼容接口](openai-compatible-interface.md)；Schema 中 `required` 字段必须准确声明必填参数 |
| `tool_choice` | DashScope / Anthropic Messages API | 控制模型是否及如何调用工具：`"auto"`（默认）、`"none"`（禁用）、或指定工具名 | 否 | 指定工具名时，模型将强制调用该工具（即使不必要），适用于确定性流程 |
| `biz_params` | Assistant API / 插件调用 | 业务系统透传的上下文参数（如用户 ID、会话 ID），供插件后端鉴权或个性化处理 | 否（按插件需求） | 仅对支持业务透传的插件生效；不参与模型推理，不暴露给模型 |
| `description`（Skill） | Skill | Skill 的功能描述文本，是模型触发调用的唯一依据 | 是 | 必须包含适用输入、支持操作、典型关键词、**明确的不适用场景**；模糊描述将导致误调用 |
| `enable_search` / `enable_code_interpreter` | DashScope 原生接口 | 布尔开关，快捷启用预置工具链 | 否 | 仅 DashScope 支持；与 `tools` 互斥，二者不可同时使用 |

## 面向开发者，简洁实用

- ✅ **优先选 DashScope 接口**：若需精细控制工具调用（如自定义工具、指定参数、多工具协同），务必使用 DashScope 原生 endpoint（`/api/v1/services/aigc/text-generation/generation`），而非 [OpenAI 兼容接口](openai-compatible-interface.md)。
- ✅ **Skill 描述要“防错”**：写 `SKILL.md` 的 `description` 时，用“当用户说……时可用，但当用户说……时**不可用**”句式，比单纯罗列功能更有效。
- ✅ **插件调用前必验权限**：子账号首次使用插件，需主账号授予 `ram:CreateServiceLinkedRole` 权限，否则返回错误码 `140052`。
- ❌ **勿在 [OpenAI 兼容接口](openai-compatible-interface.md)中传 `tools`**：该字段会被忽略，且可能引发 400 错误。
- ❌ **勿在 Managed Agents Session 创建时传 `tools`**：Agent 已绑定 Skill/插件，工具集由 Agent 快照固化，请求体中添加 `tools` 字段无效。
- 🔧 **调试技巧**：开启 `stream=true` 并监听 `tool_calls` 事件（DashScope）或 `event: tool_call`（Managed Agents SSE），可实时观察模型是否识别意图、参数是否正确生成。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [managed agents api](../api/managed-agents-api.md)
- [plug in](../guides/plug-in.md)
- [skill](../guides/skill.md)
- [application component api reference](../api/application-component-api-reference.md)


