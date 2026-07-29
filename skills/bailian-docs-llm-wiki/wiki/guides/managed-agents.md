# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过服务端持久化的事件流反馈全过程。相比无状态的智能体应用，Managed Agents 支持中断续接、有状态上下文和细粒度的沙箱控制。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（详见 [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)），模型需在创建 Agent 时显式指定。
- **内置工具集**：默认提供 `bash`（命令执行）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（文件搜索）、`download_file`（URL 下载）共 7 个 builtin_toolkit 工具；也可通过 MCP 服务或 Skill 接入自定义能力。
- **扩展能力**：
  - 支持挂载上传文件或远程 URL 资源，统一挂载至 `/mnt/session/uploads/` 下（见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）；
  - 支持在沙箱中预装 `apt`/`pip` 包（如 `pandas`、`ffmpeg`），通过 Environment 配置实现；
  - 支持 unrestricted 网络访问（需显式配置 `networking.type: "unrestricted"`）。

> **注意**：文档 2 中 Java SDK 示例未传入 `packages` 和 `networking` 字段，而 Python 和 Bash 示例完整包含；实际使用时应以 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md) 文档为准，Java SDK 需补全 `config` 参数。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agent` | string | 是 | Agent ID（由 `agents.create` 返回） |
| `environment_id` | string | 是 | Environment ID（由 `environments.create` 返回） |
| `title` | string | 否 | 会话标题，仅用于标识，不影响执行 |
| `resources` | array of objects | 否 | 挂载资源列表，每个对象含 `resource_id` 和 `mount_path`（见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)） |
| `timeout` | integer (seconds) | 否 | 会话空闲超时，默认 300 秒；最大支持 3600 秒 |

## 使用方式

1. **创建 Agent**：调用 `POST /api/v1/agentstudio/agents`，指定 `name`、`model.id`、`system` 和 `tools`（推荐 `"builtin_toolkit"`）；
2. **创建 Environment**：调用 `POST /api/v1/agentstudio/environments`，`config.type` 必须为 `"cloud"`，可选配 `packages` 和 `networking`；
3. **创建 Session**：调用 `POST /api/v1/agentstudio/sessions`，绑定 `agent` 与 `environment_id`，可选传 `resources`；
4. **发送事件**：调用 `POST /api/v1/agentstudio/sessions/{session_id}/events`，`input` 为标准消息数组（`role: "user"`）；
5. **订阅事件流**：发起 SSE 请求 `GET /api/v1/agentstudio/sessions/{session_id}/events/stream`，监听 `message`、`tool_output`、`session_status` 等事件类型。

所有步骤均支持控制台向导与 SDK/API 两种方式，详细接口规范参见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)。

## 限制和注意事项

- 单个上传文件 ≤ 10 MB；沙箱内总磁盘空间默认 5 GB，暂不支持扩容；
- `bash` 工具默认禁止危险命令（如 `rm -rf /`、`shutdown`），但允许 `rm -f` 等受限操作；
- 会话空闲超时后自动终止（默认 5 分钟），已持久化的事件历史仍可查询；
- 挂载的文件在会话中为只读副本（除非显式 `write` 修改），修改不影响原始资源；
- 当前不支持跨会话共享内存或进程间通信，状态隔离严格基于沙箱边界。

> **注意**：文档 1 将“支持中断与续接”列为核心特性，但文档 5（委派任务给 Agent）未说明具体续接机制；实际开发中，续接需通过 `sessions.resume`（非标准 REST endpoint）或重建会话并复用历史事件重放实现，建议以最新 API 文档为准。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


