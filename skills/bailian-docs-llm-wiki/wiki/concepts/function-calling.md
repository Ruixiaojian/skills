# 函数调用

函数调用（Function Calling）是百炼平台支持的核心智能体能力，指大模型在推理过程中主动识别用户意图、生成结构化工具调用请求（而非仅输出自然语言），并将结果交由外部系统执行后整合返回。该机制是构建可执行智能体（Agent）、实现联网搜索、代码解释、数据库查询等自动化任务的基础。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用能力在百炼平台中并非独立接口，而是**深度集成于多种协议与模型能力中**，具体使用方式依调用协议和模型类型而异：

- **OpenAI 兼容 Chat Completions 接口**：支持基础函数调用，需传入 `tools` 数组（JSON Schema 定义）和 `tool_choice`（如 `"auto"` 或 `"required"`）。模型返回 `tool_calls` 字段，开发者需解析并同步执行对应函数，再将结果以 `tool_message` 形式回传继续对话。适用于快速迁移 LangChain、LlamaIndex 等生态项目。

- **DashScope 原生接口**：提供最完整的函数调用支持，包括：
  - 更精细的 `tool_choice` 控制（如 `{"type": "function", "name": "search_web"}` 强制指定函数）；
  - 支持多轮工具调用链（单次响应可含多个 `tool_calls`）；
  - 工具执行失败时自动重试或降级（需配合 `enable_thinking: true`）；
  - 返回字段明确区分 `output.tool_calls` 与 `output.text`，便于解耦处理。

- **Responses API（增强型智能体原生接口）**：开箱即用的函数调用体验——无需手动定义 `tools`，平台已预置联网搜索、网页提取、代码解释器等内置工具。开发者只需启用 `enable_search: true` 或声明 `input.tools = ["code_interpreter"]`，模型自动调度并返回结构化结果，大幅降低 Agent 开发门槛。

- **全模态模型（如 `qwen3.5-omni-plus`、`qwen3.7-plus`）**：支持跨模态函数调用，例如在图文混合输入中，模型可基于图像内容触发 `ocr_extract` 工具，或结合语音转写结果调用 `translate` 工具。所有模态输入统一通过 `input` 字段传递，函数调用逻辑由模型统一编排。

> ⚠️ 注意：`qwen-vl` 和 `qwen-audio` 模型**仅通过 DashScope 原生接口支持函数调用**；[OpenAI 兼容接口](openai-compatible-interface.md)不适用。此外，私有调优模型（子业务空间部署）**仅支持 DashScope 原生协议的函数调用**，不兼容 OpenAI 格式。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tools` | array of object | 否（但启用函数调用时必填） | 工具定义列表，每个对象为标准 JSON Schema（含 `name`, `description`, `parameters`），用于告知模型可用能力。DashScope 和 Anthropic 接口支持完整 Schema；OpenAI 接口要求严格遵循其格式。 |
| `tool_choice` | string / object | 否 | 控制调用策略：<br>• `"auto"`：模型自主决定是否及何时调用（默认）<br>• `"required"`：强制必须调用至少一个工具<br>• `{"type": "function", "name": "xxx"}`：指定唯一可调用函数（DashScope 原生独有） |
| `enable_search` / `enable_code_interpreter` | boolean | 否（仅 Responses API） | 启用平台预置工具的快捷开关，替代手动定义 `tools`，适用于标准场景。 |
| `input.tools` | array of string | 否（仅 Responses API） | 显式声明本次请求允许使用的内置工具名（如 `["web_search", "code_interpreter"]`），比全局开关更灵活。 |
| `enable_thinking` | boolean | 否（推荐启用） | 启用逐步推理模式，使模型在调用函数前生成中间思考链（`reasoning_steps`），提升调用准确率与可调试性，尤其适用于复杂多步任务。 |

- **流式响应注意**：函数调用相关字段（如 `tool_calls`）**仅在完整响应中返回**，流式模式（`stream=true`）下不会分块推送 `delta.tool_calls`。如需实时感知调用意图，建议先禁用流式获取完整响应，或结合 `enable_thinking` 分析中间推理文本。

- **安全与权限**：函数调用本身不执行外部操作，仅生成请求。实际执行需开发者在服务端完成鉴权、参数校验与沙箱执行。百炼不代理工具执行，也不存储工具返回数据。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [model experience](../guides/model-experience.md)
- [more about models](../api/more-about-models.md)


