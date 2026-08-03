# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、自主规划并调用外部工具（如搜索、代码执行、图像生成等）以完成复杂任务的核心能力。它不是简单的 API 转发，而是模型在推理过程中基于语义理解，动态生成结构化[工具调用](tool-use.md)请求，并等待结果后整合生成最终响应的闭环机制。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一接口特性，而是贯穿多个能力层的统一抽象，具体体现为以下三类使用方式：

- **模型原生支持（Model-native Function Calling）**  
  `qwen3.7-plus`、`qwen3.5-omni-plus` 等主流文本/全模态模型在底层已集成函数调用协议。开发者通过 DashScope 原生接口或 Omni Realtime API 的 `tools` 参数声明可用工具，模型将自动解析用户输入、选择工具、构造参数并触发调用。该模式无需额外编排，适用于智能体式轻量应用。

- **插件驱动调用（Plugin-based Invocation）**  
  在「插件」体系中，函数调用表现为对官方/三方/自定义插件的标准化调用。模型根据插件描述（tool description）和输入上下文决策是否调用，工具 ID（如 `quark_search`、`code_interpreter`）即为函数标识符。此方式与智能体应用、工作流应用深度集成，支持沙箱隔离、权限管控与审计追踪。

- **托管智能体运行时（Managed Agent Runtime）**  
  Managed Agents API 将函数调用纳入事件驱动生命周期：模型输出 `tool_use` 事件 → 平台调度对应 Skill 执行 → 回填 `tool_result` 事件 → 模型继续推理。整个过程由 `Session` 状态机管理，开发者只需关注工具注册、Skill 发布与事件监听，无需处理调用循环逻辑。

> ⚠️ 注意：OpenAI 兼容 Chat Completions 接口默认**不支持**函数调用；如需该能力，请选用 DashScope 原生接口、Omni Realtime API 或 OpenAI兼容-Responses 接口。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 示例 |
|------|------|------|------|------|
| `tools` | 请求体（JSON） | array | 必填。声明可被调用的函数列表，每个元素含 `name`、`description`、`parameters`（JSON Schema 定义） | `[{"name": "calculator", "description": "执行数学运算", "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}}}]` |
| `tool_choice` | 请求体（可选） | string / object | 控制调用策略：`"auto"`（默认，模型自主决策）、`"none"`（禁用）、`{"type": "function", "function": {"name": "xxx"}}`（强制指定） | `"auto"` |
| `enable_search` | 请求体（仅部分模型） | boolean | **与 `tools` 互斥**。启用内置联网搜索（基于夸克），非插件调用，不可与 `tools` 同时设置 | `true` |
| `tool_results` | 请求体（回调时） | array | 工具执行完成后，需将结果以 `tool_call_id` + `content` 格式回传，供模型继续推理 | `[{"tool_call_id": "call_abc123", "content": "结果：42"}]` |
| `X-DashScope-Tools-Mode` | Header（高级场景） | string | 实验性头，用于切换[工具调用](tool-use.md)协议版本（如 `v2` 支持多工具并行调用），默认 `v1` | `"v2"` |

## 面向开发者，简洁实用

- ✅ **首选实践**：使用 DashScope 原生接口（`/api/v1/services/aigc/text-generation/generation`）或 Omni Realtime API，它们提供最完整的函数调用控制与错误反馈。
- ✅ **参数验证**：`tools` 中的 `parameters` 字段必须为合法 JSON Schema（支持 `string`/`number`/`boolean`/`object`/`array`），空对象 `{}` 会被拒绝；建议用 `Value` 字段提供调用样例提升准确率。
- ✅ **调试技巧**：开启 `stream: true` 可实时观察模型是否生成 `tool_calls`；若未触发，检查工具描述是否清晰、用户问题是否明确包含工具适用意图（如“计算”、“搜索”、“画图”）。
- ❌ **避坑提示**：
  - 不要混用 `enable_search` 和 `tools` —— 二者功能重叠且互斥；
  - [OpenAI 兼容接口](openai-compatible-interface.md)需显式启用 `OpenAI兼容-Responses` 才支持[工具调用](tool-use.md)；
  - `code_interpreter` 插件禁止网络访问与文件上传，依赖列表以最新文档为准；
  - 自定义插件发布前必须通过测试且状态为 `active`，否则调用失败（错误码 `130022`）。

函数调用是构建生产级智能体的关键枢纽。善用它，即可让大模型从“回答者”升级为“执行者”。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [plug in](../guides/plug-in.md)
- [managed agents api](../api/managed-agents-api.md)
- [omni realtime api](../api/omni-realtime-api.md)


