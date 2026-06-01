# assistantapi

Assistant API 是百炼平台提供的一套用于构建大模型智能体（Assistant）的接口，涵盖智能体管理、对话线程管理、消息管理和运行控制等功能。**该 API 目前处于下线状态**，建议开发者迁移至 Responses API（内置多种工具并支持多轮上下文管理）作为替代方案。

> **注意**：所有 7 篇原始文档均标注 Assistant API 为"下线中"，新项目不应再使用此 API。

## 核心组件

Assistant API 采用多层对象模型，主要包括以下组件：

| 组件 | 说明 |
|------|------|
| **Assistant** | 智能体实例，绑定模型、tools、instructions 等配置 |
| **Thread** | 对话线程，承载一组有序的 Message |
| **Message** | 线程中的消息，目前 role 仅支持 `user` |
| **Run** | 在指定 Thread 上执行 Assistant 的运行实例 |
| **Run Step** | 运行过程中的具体步骤（模型调用 / 工具调用） |

所有 Assistant 和 Thread 实例均持久化存储在百炼服务器上，目前没有失效日期。

## 支持的模型与工具

根据 [Assistants（下线中）](../../raw/application-api-reference/assistantapi/assistant.md) 中的示例，Assistant 支持以下模型和工具配置：

**模型**：`qwen-max` 等通义千问系列模型（可按需更换）。

**内置工具类型**：
- `code_interpreter`：代码解释器
- `search`（夸克搜索）
- `text_to_image`：文生图
- `function`：自定义函数调用

**采样参数**：`temperature`、`top_p`、`top_k`（均为可选）。

## 基本使用流程

典型调用流程为：创建 Assistant → 创建 Thread → 添加 Message → 创建 Run → 轮询/流式获取结果。

详细的端到端代码示例见 [Assistant API 调用示例（下线中）](../../raw/application-api-reference/assistantapi/call-example.md)，其中包含非流式和流式两种模式以及函数调用场景。

### 关键接口端点

| 资源 | 操作 | HTTP 方法 & 路径 |
|------|------|-----------------|
| Assistant | 创建 | `POST /api/v1/assistants` |
| Assistant | 列表 | `GET /api/v1/assistants` |
| Thread | 创建 | `POST /api/v1/threads` |
| Thread | 检索 | `GET /api/v1/threads/{thread_id}` |
| Message | 创建 | `POST /api/v1/threads/{thread_id}/messages` |
| Run | 创建 | `POST /api/v1/threads/{thread_id}/runs` |
| Run Step | 列表 | `GET /api/v1/threads/{thread_id}/runs/{run_id}/steps` |

所有请求需在 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`。

### [流式输出](../concepts/streaming.md)

创建 Run 时设置 `"stream": true` 即可启用[流式输出](../concepts/streaming.md)。流式数据以 SSE（Server-Sent Events）格式返回，由 `event` 和 `data` 组成。关键事件包括 `thread.message.delta`（消息增量）和 `thread.run.step.delta`（工具调用增量）。[流式输出](../concepts/streaming.md)的详细参数说明参见 [Assistant API 流式输出参数说明（下线中）](../../raw/application-api-reference/assistantapi/event-streaming.md)。

支持流式输出的内置工具：代码解释器、夸克搜索、文生图和计算器。其他工具不支持流式增量，需通过常规方式获取调用结果。

## 关键参数说明

### Run 创建参数

| 参数 | 类型 | 必须 | 说明 |
|------|------|------|------|
| `thread_id` | string | 是 | 路径参数，目标线程 ID |
| `assistant_id` | string | 是 | 要运行的 Assistant ID |
| `model` | string | 否 | 覆盖 Assistant 中定义的模型 |
| `instructions` | string | 否 | 覆盖 Assistant 中定义的 system [prompt](../guides/prompt.md) |
| `tools` | array | 否 | 覆盖 Assistant 中定义的工具列表 |
| `stream` | boolean | 否 | 是否启用流式返回 |
| `temperature` | float | 否 | 控制随机性 |
| `top_p` | float | 否 | 核采样阈值 |

### Run 状态流转

Run 的 `status` 字段可能为：`queued` → `in_progress` → `completed` / `requires_action` / `failed` / `cancelled` / `expired`。

当状态为 `requires_action` 时，表示需要开发者提交函数调用结果（通过 `submit_tool_outputs`）后才能继续执行。

## SDK 版本要求

- **Python SDK**：`dashscope >= 1.18.0`（通过 `pip install -U dashscope` 更新）
- **Java SDK**：`>= 2.14.2`

## 限制和注意事项

1. **下线状态**：Assistant API 正在下线，请尽快迁移至 Responses API。
2. **Message role 限制**：创建消息时 role 目前仅支持 `"user"`。
3. **metadata 限制**：最多 16 个键值对，键最大 64 字符，值最大 512 字符。
4. **与智能体应用的区别**：控制台创建的"智能体应用"和 Assistant API 创建的 Assistant 功能相互独立、不可互通。
5. **Workspace ID**：仅当使用子业务空间 API Key 时才需要传入 `workspace` 参数。
6. **自定义插件鉴权**：通过 tools 数组中的 `auth` 字段传递用户级鉴权 token，格式为 `{"type": "user_http", "user_token": "bearer-token"}`。

## 来源文档

- [Threads（下线中）](../../raw/application-api-reference/assistantapi/thread.md)
- [Assistants（下线中）](../../raw/application-api-reference/assistantapi/assistant.md)
- [Messages（下线中）](../../raw/application-api-reference/assistantapi/message.md)
- [Runs（下线中）](../../raw/application-api-reference/assistantapi/runs.md)
- [Run Steps（下线中）](../../raw/application-api-reference/assistantapi/run-steps.md)
- [Assistant API 流式输出参数说明（下线中）](../../raw/application-api-reference/assistantapi/event-streaming.md)
- [Assistant API 调用示例（下线中）](../../raw/application-api-reference/assistantapi/call-example.md)

