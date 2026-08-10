# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过服务端持久化的事件流反馈全过程。相比无状态的智能体应用，Managed Agents 更适合需跨轮次保持上下文、文件系统状态和中断续接能力的复杂任务。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（详见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）；模型通过 `model.id` 字段指定，不可动态切换。
- **内置工具集**：默认提供 7 个基础工具：`bash`（命令执行）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（文件搜索）、`download_file`（URL 下载）。也可通过 `builtin_toolkit` 统一启用全部工具。
- **扩展能力**：
  - 支持挂载预置 Skill 封装端到端流程；
  - 集成 MCP 服务接入外部工具；
  - 支持挂载上传文件或远程 URL 资源（单文件 ≤10 MB），挂载路径固定为 `/mnt/session/uploads/...`（见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。

> **注意**：文档 [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md) 中未明确列出工具类型约束，但 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 明确要求工具必须为 `{"type": "builtin_toolkit"}` 或显式声明工具列表，不支持自定义工具注册。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agent` | string | 是 | 智能体 ID（如 `"agent_xxx"`），由 `agents.create()` 返回 |
| `environment_id` | string | 是 | 运行环境 ID（如 `"env_xxx"`），决定沙箱配置与预装依赖 |
| `title` | string | 否 | 会话标题，仅用于标识，不影响执行 |
| `resources` | array | 否 | 挂载资源列表，每个元素含 `resource_id` 和 `mount_path`（见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)） |

## 使用方式

1. **创建智能体**：调用 `agents.create()`，指定 `name`、`model.id`、`system_prompt` 和 `tools`（推荐 `{"type": "builtin_toolkit"}`）；
2. **创建环境**：调用 `environments.create()`，设置 `config.type = "cloud"`，并可选配置 `packages.apt`/`packages.pip` 和 `networking.type`；
3. **发起会话**：调用 `sessions.create()`，绑定 `agent` 与 `environment_id`，可选传入 `resources`；
4. **发送事件**：向 `sessions/{id}/events` POST 用户消息（`role: "user"`，`type: "message"`）；
5. **接收响应**：通过 SSE 流订阅 `sessions/{id}/events/stream`，监听 `message`、`tool_output`、`session_status` 等事件类型。

所有 API 均需 `Authorization: Bearer $DASHSCOPE_API_KEY` 认证，且 endpoint 中 `{workspace_id}` 需替换为实际工作空间 ID（参见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 的完整示例）。

## 限制和注意事项

- **沙箱隔离性**：每个会话独占一个云端容器实例，环境配置（如 `pip install`）仅作用于该会话，不可跨会话共享；
- **资源挂载**：挂载文件为只读副本（除非显式 `write` 修改），修改仅影响当前会话沙箱内副本，原始资源与其它会话不受影响；
- **超时控制**：SSE 流建议设置客户端超时（如 Python 示例中 `timeout=120.0`），服务端默认空闲 5 分钟后自动终止会话；
- **模型限制**：`qwen3-max` 等模型暂不支持 `stream=True` 的逐 token 输出，所有 `message` 事件均为完整响应块；
- **权限要求**：调用方账号须在目标工作空间具备 `AgentStudioFullAccess` 或等效权限（见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 前置准备）。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


