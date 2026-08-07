# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过服务端持久化的事件流反馈全过程。相比无状态的智能体应用，Managed Agents 支持中断续接、跨轮次上下文保持与细粒度运行干预。

## 支持的模型与功能

- **模型支持**：支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）；模型通过 `model.id` 字段指定，需与平台当前可用模型列表一致。
- **内置工具集**：默认提供 7 个基础工具：`bash`（命令执行）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（文件搜索）、`download_file`（URL 下载）。也可通过 `tools: [{"type": "builtin_toolkit"}]` 一次性启用全部（见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）。
- **扩展能力**：
  - MCP 服务：接入外部工具服务；
  - Skill：复用预置的端到端任务流程；
  - 挂载资源：上传文件或指定 URL，在沙箱中以 `/mnt/session/uploads/...` 路径访问（见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。

> **注意**：文档 6 中示例使用 `qwen3-max`，但文档 1 的概述表格中仅列出 `qwen3.7-plus` 作为示例模型。实际可用模型以控制台下拉列表或 `/api/v1/agentstudio/models` 接口返回为准，建议以 API 响应为准，避免硬编码过期模型 ID。

## 关键参数

| 参数 | 类型 | 说明 | 来源 |
|------|------|------|------|
| `agent` | string | 智能体 ID（创建后生成），必填 | [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md) |
| `environment_id` | string | 运行环境 ID，必填 | [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md) |
| `resources` | array | 挂载资源列表，含 `resource_id` 和 `mount_path`（路径必须以 `/mnt/session/uploads/` 开头） | [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md) |
| `input[].content[].text` | string | 用户消息内容，支持引用挂载文件路径（如 `/mnt/session/uploads/data.csv`） | [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) |
| `config.packages` | object | 环境预装包配置，支持 `apt`（Debian 包）和 `pip`（Python 包）字段 | [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) |

## 使用方式

1. **创建智能体**：定义名称、模型、系统提示词与工具集（见 [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)）；
2. **创建运行环境**：指定沙箱类型（目前仅支持 `cloud`）、网络策略（`unrestricted` 或 `restricted`）及预装依赖；
3. **发起会话**：绑定智能体 ID 与环境 ID，可选挂载资源；
4. **发送事件**：向 `sessions/{id}/events` POST 用户消息，触发智能体执行；
5. **接收事件流**：通过 SSE 订阅 `sessions/{id}/events/stream`，监听 `message`、`tool_call`、`tool_output`、`session_status` 等事件类型。

所有操作均支持控制台可视化配置与 REST API 调用（Python/Java SDK 封装亦可用），详见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 中的完整代码示例。

## 限制和注意事项

- **文件大小限制**：单个上传文件 ≤ 10 MB（见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）；
- **沙箱隔离性**：同一资源被多个会话挂载时，各会话获得独立副本，修改互不影响；卸载后副本自动清理；
- **会话生命周期**：会话状态包括 `running`/`idle`/`terminated`，`idle` 状态超时（默认 30 分钟）将自动终止，不可恢复；
- **工具调用约束**：`bash` 工具默认禁止 `sudo`、`rm -rf /` 等高危命令，且网络访问受 `networking.type` 控制；
- **事件历史**：所有事件（含用户输入、工具调用、模型输出、错误）在服务端持久化，可通过 `sessions/{id}/events` 查询，但不支持写入或修改。

> **注意**：文档 1 称“支持中断与续接”，但文档 6 的会话状态枚举中未包含 `paused` 或 `resumed` 状态，且当前 API 不提供显式暂停/恢复接口。实际中断仅能通过发送新 `user` 事件覆盖当前任务流，或调用 `DELETE /sessions/{id}` 终止会话——后者不可续接。该表述存在歧义，建议以 API 文档中 `session_status` 实际取值为准。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)


