# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、自主规划并执行外部工具或内置能力的核心机制。它使模型不再仅生成文本，而是能按需触发代码执行、联网搜索、图像生成、文件操作等具体动作，并将结构化结果整合进推理链路，实现“思考—决策—行动”的闭环。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一技术实现，而是贯穿多个能力层的统一语义机制，具体体现为以下三类场景：

- **插件调用（Plugin-based Function Calling）**  
  适用于智能体应用、工作流和 Assistant API。开发者通过 `tools` 数组声明可用工具（如 `calculator`、`quark_search`），模型根据用户输入和工具描述自主决定是否调用、调用哪个工具及传入哪些参数。调用由模型生成结构化 `tool_calls` 响应，平台自动路由并执行，结果再注入上下文供后续推理。

- **内置工具调用（Built-in Tool Calling，Managed Agents）**  
  在 Managed Agents 中，函数调用表现为对沙箱内预置能力的直接调用，如 `bash`（执行命令）、`read`/`write`（文件读写）、`download_file`（下载 URL）。无需显式注册工具，只需在 Agent 配置中启用 `tools: [{"type": "builtin_toolkit"}]`，模型即可在代码执行、数据处理等长时任务中自主触发。

- **[多模态](multi-modal.md)模型原生支持（Native Function Calling in Multimodal Models）**  
  `qwen3.5-omni-plus`、`qwen3.7-plus`、`qwen3.8-max` 等旗舰模型原生支持函数调用能力，可同时处理文本、图像、音频、视频输入，并在理解[多模态](multi-modal.md)内容后发起工具调用（例如：分析截图中的表格 → 调用 `code_interpreter` 进行计算 → 返回可视化图表）。该能力与模型架构深度耦合，无需额外插件配置。

> ⚠️ 注意：`enable_search` 是模型参数，用于隐式增强检索能力，**不属于函数调用范畴**；它不返回结构化工具调用事件，也无法被开发者控制或观测。真正的函数调用必须显式声明 `tools` 并依赖 `tool_calls` 响应。

## 关键参数和配置

| 参数 | 位置 | 说明 | 示例 |
|------|------|------|------|
| `tools` | 请求体 `tools` 字段（Assistant API / Managed Agents / 工作流） | 必填数组，定义可用工具列表。每个工具需包含 `type`（如 `"plugin"` 或 `"builtin"`）、`function.name`（工具 ID）、`function.description`（自然语言描述，直接影响调用准确性）及 `function.parameters`（JSON Schema 定义） | `[{"type":"plugin","function":{"name":"calculator","description":"执行数学运算","parameters":{"type":"object","properties":{"expression":{"type":"string"}},"required":["expression"]}}}]` |
| `tool_choice` | Assistant API 请求体 | 控制调用策略：`"auto"`（默认，模型自主决策）、`"none"`（禁用调用）、`{"type":"function","function":{"name":"xxx"}}`（强制指定） | `{"type":"function","function":{"name":"text_to_image"}}` |
| `tools`（Managed Agents） | Agent 创建请求体 `tools` 字段 | 启用内置工具集，支持全量启用或子集声明 | `[{"type":"bash"},{"type":"write"}]` 或 `[{"type":"builtin_toolkit"}]` |
| `system_prompt` | Agent / Assistant 配置 | 系统提示词中需明确指令模型“可调用工具”，并简要说明工具用途。模糊或缺失描述会导致调用失败 | `"你是一个数据分析助手，可调用 calculator 和 code_interpreter 工具进行计算和绘图。"` |

## 面向开发者，简洁实用

- ✅ **必做**：所有函数调用均需在请求中显式提供 `tools` 定义；工具描述必须用自然语言、带具体示例（如 `"计算表达式 '2^10 + sqrt(144)' 的结果"`），避免抽象术语。
- ✅ **调试技巧**：若模型未触发调用，优先检查 `system_prompt` 是否授权、`tools` 描述是否清晰、`input` 是否含明确动作意图（如“算一下”“搜一下”“画个图”）。
- ✅ **错误定位**：关注响应中的 `finish_reason` 字段——`"tool_calls"` 表示成功触发；`"stop"` 表示未调用；`"length"` 表示被截断，需检查 `max_tokens` 或上下文长度。
- ❌ **禁止**：不要混淆 `enable_search`（隐式参数）与函数调用；不要在 `tools` 中重复声明同一工具 ID；Object 类型参数的子属性不能为空（否则返回错误码 130022）。
- 🚀 **最佳实践**：首次集成建议使用控制台“调试预览”功能，实时查看 `tool_call` 事件及 `tool_output` 结果，快速验证工具链路完整性。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [plug in](../guides/plug-in.md)
- [managed agents api](../api/managed-agents-api.md)
- [managed agents](../guides/managed-agents.md)
- [application call](../api/application-call.md)


