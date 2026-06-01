# Assistant API

Assistant API 是百炼平台提供的大模型应用开发接口，旨在帮助开发者快速构建个人助理、智能导购等应用。相比文本生成 API，它内置了[多轮对话管理](../concepts/multi-turn-conversation.md)和工具调用组件，降低了开发成本。**该 API 目前处于下线状态，建议迁移至 Responses API。**

> **注意**：根据 [Assistant API（下线中）](../../raw/application-user-guide/assistant-api.md) 文档，Assistant API 正在下线，官方建议迁移至 Responses API，后者同样内置多种工具并支持多轮上下文管理。

## 核心概念与使用流程

构建一个 Assistant 应用通常需要依次完成以下四个步骤：

1. **创建 Assistant**：配置大模型、指令和工具列表，定义 Assistant 要执行的任务。
2. **创建 Thread**：Thread 记录用户和 Assistant 之间的所有消息，实现多轮对话。
3. **创建 Message**：Message 是承载用户输入和 Assistant 回复的容器。
4. **创建 Run**：Run 代表 Assistant 处理对话的完整流程，包括模型推理和工具调用，支持[流式输出](../concepts/streaming.md)。

智能体应用与 Assistant 虽然均为大模型应用，但功能相互独立：智能体应用通过控制台创建和管理，通过应用调用 API 进行调用；Assistant 仅通过 Assistant API 进行全生命周期管理。

## 支持的模型

根据 [Assistant API（下线中）](../../raw/application-user-guide/assistant-api.md) 的说明，支持以下千问系列模型：

| 模型系列 | 模型标识符 |
|---------|-----------|
| 千问-Turbo | `qwen-turbo` |
| 千问-Plus | `qwen-plus` |
| 千问-Max | `qwen-max` |

> **注意**：千问-Turbo、千问-Plus、千问-Max 的快照版本（如 `qwen-plus-1220`）仅兼容"函数调用"及"知识检索增强"工具，其他工具的兼容性以实际运行结果为准。

## 支持的工具

| 工具名称 | 标识符 | 用途 |
|---------|--------|------|
| 代码解释器 | `code_interpreter` | 执行 Python 代码，适用于编程、数学计算、数据分析 |
| 夸克搜索 | `quark_search` | 实时检索网络信息 |
| 文生图 | `text_to_image` | 将文字描述转为图像 |
| 计算器 | `calculator` | 执行精确运算任务 |
| 生成二维码 | `generate_qrcode` | 将文本转换为二维码 |
| GitHub 搜索 | `github_search` | 搜索 GitHub 项目信息 |
| 函数调用 | `function` | 在本地设备执行特定功能，无需外部网络 |
| 知识检索增强（RAG） | `rag` | 检索外部知识，增强回答准确性 |
| 自定义插件 | `${plugin_id}` | 连接自定义业务接口 |

## 核心能力

### 内置对话管理

Thread 机制自动维护对话历史，开发者无需手动管理上下文。通过 `Runs.create()` 创建运行后，可监听事件流（如 `thread.message.delta`、`thread.run.completed` 等）获取实时响应。

### 工具调用

当 Run 事件返回 `thread.run.requires_action` 时，表示需要执行工具调用。开发者解析 `tool_calls` 中的函数名和参数，在本地执行后通过 `Runs.submit_tool_outputs()` 提交结果，Assistant 将基于工具输出继续生成回复。

### 多智能体系统

Assistant API 提供了构建多智能体（Multi Agent）系统的基础模板，支持通过规划 Agent 确定执行顺序，依次调用不同 Agent 处理任务，并将前一个 Agent 的输出作为后续 Agent 的参考输入。

## 限制和注意事项

- **下线状态**：如 [Assistant API（下线中）](../../raw/application-user-guide/assistant-api.md) 所述，该 API 正在下线，新项目应优先使用 Responses API。
- **快照模型限制**：模型快照版本仅支持函数调用和 RAG 两种工具。
- **插件兼容性**：自定义插件的兼容性需以实际执行结果为准。
- **与智能体应用的区别**：Assistant 与控制台中的智能体应用功能完全独立，不可混用管理方式和调用接口。

## 来源文档

- [Assistant API（下线中）](../../raw/application-user-guide/assistant-api.md)

