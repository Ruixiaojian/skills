# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、生成结构化工具调用请求，并交由执行引擎安全执行外部能力的核心机制。它不是传统编程中的函数调用，而是大语言模型基于自然语言输入，自主规划、参数填充并触发预定义工具（如搜索、代码执行、图像生成等）的推理-决策-执行闭环。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一接口能力，而是贯穿多个服务层级的统一语义能力，具体体现为：

- **OpenAI 兼容 Chat Completions 接口**：通过 `tools` 数组声明工具描述（OpenAI 格式），配合 `tool_choice` 控制调用策略（`"auto"`/`"required"`/`{"type": "function", "function": {"name": "xxx"}}`）。模型返回 `tool_calls` 字段，开发者需解析后同步执行工具，再将结果以 `tool_message` 形式回传继续对话。  
- **DashScope 原生接口**：使用 `tool_list`（而非 `tools`）传入工具定义，支持更细粒度控制（如 `enable_search`、`enable_code_interpreter` 等开关），部分模型（如 `qwen-max`）还支持 `output_format: "json"` 强制结构化输出，便于解析调用意图。  
- **Managed Agents（托管智能体）**：函数调用被封装为 `Skill` 的自动触发行为。Agent 在创建时挂载 Skill（含工具定义与权限），Session 运行时由平台 Runtime 自动完成意图识别、参数提取、沙箱内安全执行及结果注入，开发者无需手动处理 `tool_calls`。  
- **Omni Realtime API（实时多模态）**：仅 `qwen3.5-omni-realtime` 系列支持，通过 `tools` 参数启用，且与 `enable_search` 互斥；调用过程嵌入 WebSocket 流中，模型在语音/文本混合输入下实时生成 `tool_use` 事件，适用于低延迟语音助手场景。  
- **插件（Plug-in）体系**：函数调用的上层抽象。官方/三方/自定义插件均通过统一 `tool_id` 注册，模型根据插件描述自动决策是否调用；参数映射、鉴权（Bearer/Basic/AppCode）、在线调试均由插件平台管理，降低集成复杂度。  
- **Responses API（智能体专用）**：函数调用被完全隐藏——无需配置 `tools`，模型内置联网搜索、代码解释器等能力，自动触发并融合结果到最终回复中，适合快速构建免编排的智能助手。

> ✅ 关键共识：无论哪种形式，“函数调用”本质都是 **模型输出结构化指令 → 执行引擎调用外部服务 → 结果反馈给模型继续推理** 的三步链路。平台差异仅在于声明方式、执行主体（开发者 vs 平台 Runtime）和管控粒度（原始工具 vs 插件封装）。

## 关键参数和配置

| 参数 | 位置 | 说明 | 注意事项 |
|------|------|------|----------|
| `tools` / `tool_list` | 请求体 `input` 或 `parameters` 中 | 工具定义列表，采用 OpenAI Schema 或 DashScope 自定义格式 | OpenAI 接口必须用 `tools`；DashScope 原生用 `tool_list`；Managed Agents 使用 `skill_ids` 替代 |
| `tool_choice` | 请求体（OpenAI）或 `parameters.tool_choice`（DashScope） | 控制调用策略 | `"auto"`（默认，模型决定）、`"none"`（禁用）、`"required"`（强制调用）、或指定函数名；Omni Realtime 不支持此参数 |
| `enable_search` / `enable_code_interpreter` | DashScope `parameters` | 内置工具快捷开关 | 仅 DashScope 原生接口支持；与 `tools` 同时存在时，优先级低于显式 `tools` |
| `tool_id` | 插件调用上下文 | 插件市场中工具的唯一标识符 | 必须从控制台复制，大小写敏感；自定义插件需先发布为 MCP 服务 |
| `input parameters`（插件） | 插件配置页 | 定义工具所需输入字段、类型及传参方式（“大模型识别” or “业务透传”） | Object 类型子属性不能为空；GET 请求禁止使用 Object 类型 |

## 面向开发者，简洁实用

- **起步建议**：新项目优先使用 **插件（Plug-in）体系** —— 官方插件开箱即用，自定义插件支持在线调试，避免手写工具 Schema 和参数解析逻辑。  
- **控制精度**：需精细控制调用时机与参数时，选 **OpenAI 兼容 Chat Completions + `tools`**；需最大灵活性（如动态开关、JSON 强约束）时，选 **DashScope 原生接口**。  
- **省心省力**：构建长期运行的智能体应用，直接使用 **Managed Agents** —— 平台托管会话、沙箱、技能生命周期，你只需关注 Agent 设计与 Skill 编排。  
- **避坑提醒**：  
  - `functions` 参数已废弃，一律改用 `tools`；  
  - `qwen2.5+` 模型不支持旧版 `function_call` 字段；  
  - [OpenAI 兼容接口](openai-compatible-api.md)不支持 `response_format: { "type": "json_object" }`，若需 JSON 输出，请用 DashScope 的 `output_format: "json"`；  
  - 插件删除 = 关联应用立即失效，操作前务必确认。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [managed agents api](../api/managed-agents-api.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [plug in](../guides/plug-in.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more about models](../api/more-about-models.md)


