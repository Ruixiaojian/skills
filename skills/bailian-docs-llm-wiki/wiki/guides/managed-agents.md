# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、[文件处理](../concepts/file-processing.md)等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过服务端持久化的事件流反馈全过程。相比无状态的智能体应用，Managed Agents 本质是“有状态会话即服务”。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（详见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）；模型通过 `model.id` 字段指定，不可动态切换。
- **内置工具集**：默认提供 7 个基础工具：`bash`（命令执行）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（文件搜索）、`download_file`（URL 下载）。可通过 `tools: [{"type": "builtin_toolkit"}]` 启用全部，或按需精简。
- **扩展能力**：
  - MCP 服务：接入外部工具服务（如数据库、API 网关），需在智能体配置中显式声明；
  - Skill：预置的端到端任务封装（如“PDF 解析+摘要生成”），可复用但暂不支持自定义 Skill 开发；
  - 文件挂载：支持上传文件或从 URL 下载，挂载路径固定为 `/mnt/session/uploads/...`，单文件上限 10 MB（见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。

> **注意**：文档 [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md) 仅说明“智能体是模型、系统提示词、工具等的组合”，未明确工具启用方式；而 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 明确要求通过 `tools: [{"type": "builtin_toolkit"}]` 启用内置工具集，后者为权威配置方式。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agent` | string | 是 | 智能体 ID（创建后返回），如 `"agent_xxx"` |
| `environment_id` | string | 是 | 运行环境 ID，如 `"env_xxx"` |
| `title` | string | 否 | 会话标题，用于 UI 标识，不影响执行 |
| `resources` | array | 否 | 资源挂载列表，每个元素含 `resource_id` 和 `mount_path`（见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)） |

- 系统提示词（`system` / `system_prompt` / `instructions`）在不同 SDK 中字段名不一致（Python 用 `system_prompt`，Java 用 `instructions`），但语义相同，用于定义角色与行为约束。
- 环境配置中 `config.type` 固定为 `"cloud"`（云端托管），暂不支持自建沙箱；`packages` 支持 `apt` 和 `pip` 两类预装包，网络策略仅支持 `"unrestricted"`。

## 使用方式

1. **创建智能体**：调用 `/api/v1/agentstudio/agents`，传入 `name`、`model.id`、`system` 和 `tools`（必须为 `{"type": "builtin_toolkit"}`）；
2. **创建运行环境**：调用 `/api/v1/agentstudio/environments`，指定 `name` 和 `config`（含 `type`, `packages`, `networking`）；
3. **创建会话**：调用 `/api/v1/agentstudio/sessions`，绑定 `agent` 和 `environment_id`，可选传入 `resources`；
4. **发送用户消息**：向 `/api/v1/agentstudio/sessions/{session_id}/events` POST 事件，`input` 中 `role: "user"`；
5. **接收事件流**：GET `/api/v1/agentstudio/sessions/{session_id}/events/stream`，响应为 SSE 流，需解析 `event: message`、`event: tool_output`、`event: session_status` 等类型（参考 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 的 SDK 示例）。

所有资源（智能体、环境、会话、挂载文件）均独立管理、可复用，例如同一环境可被多个会话共享，同一文件资源可挂载至不同会话。

## 限制和注意事项

- **会话生命周期**：会话默认最长运行 2 小时，超时自动终止；手动调用 `terminate` 接口可提前结束。
- **沙箱隔离性**：每个会话拥有独立容器实例，文件修改、包安装仅限当前会话生效，卸载后沙箱销毁（见 [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)）。
- **事件持久化**：所有事件（含用户输入、工具调用、模型输出、错误）在服务端完整留存，支持事后审计与调试，但不支持客户端主动删除历史。
- **文件路径硬编码**：挂载文件统一位于 `/mnt/session/uploads/` 下，系统提示词中需直接引用该路径（如 `"分析 /mnt/session/uploads/data.csv"`），不可更改。
- **权限控制**：需确保账号在目标工作空间具备 `AgentStudioFullAccess` 或至少 `AgentStudioReadOnly` + `AgentStudioExecution` 权限，否则创建/调用将失败。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


