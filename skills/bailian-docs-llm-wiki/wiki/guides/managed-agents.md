# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、[文件处理](../concepts/file-processing.md)等长时运行任务设计。平台在服务端统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过持久化的事件历史实现中断续接与调试可观测。相比无状态的智能体应用，Managed Agents 更适合有状态、需环境隔离与资源复用的复杂任务场景。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 中的模型下拉列表示例）；模型通过 `model.id` 字段指定，不可动态切换。
- **核心功能**：
  - **内置工具**：`bash`（命令执行）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（文件搜索）、`download_file`（URL 下载）；
  - **扩展能力**：支持挂载 MCP 服务接入外部 API，以及预置 Skill 封装端到端流程；
  - **资源挂载**：支持上传文件并挂载至 `/mnt/session/uploads/` 路径，单文件上限 10 MB，挂载后副本隔离、修改不污染源（详见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。

> **注意**：文档 4 的快速开始示例中 Python SDK 创建 Agent 时使用 `system_prompt` 参数，而文档 2 和文档 1 均明确使用 `system` 字段；实际 API 以 `system` 为准（[构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md) 中的字段说明与 API 文档一致），`system_prompt` 为旧版 SDK 兼容别名，新代码应统一使用 `system`。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agent` / `agent_id` | string | 是 | 智能体 ID（创建后返回），用于绑定会话 |
| `environment_id` | string | 是 | 运行环境 ID，决定沙箱类型、预装包与网络策略 |
| `title` | string | 否 | 会话标题，仅用于标识，不影响执行 |
| `resources` | array | 否 | 创建会话时指定挂载的资源列表（如文件 ID + 挂载路径）；也可运行时通过 `POST /sessions/{id}/resources` 追加 |
| `tools` | object | 否（但建议显式配置） | 在 Agent 创建时定义，格式为 `{"type": "builtin_toolkit", "configs": [...]}`；未启用的工具不会出现在工具调用候选中 |

## 使用方式

1. **创建智能体**：配置 `name`、`model`、`system` 和 `tools`，获取 `agent.id`；推荐通过 SDK 或 API 显式声明所需工具（如 `bash`, `read`, `write`），避免依赖默认全选（[快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 中控制台默认勾选 7 个工具，但生产环境应按需精简）。
2. **创建运行环境**：指定 `config.type`（目前仅支持 `"cloud"`）、`packages`（`apt`/`pip` 列表）和 `networking`（如 `"unrestricted"`）；环境可被多个会话复用。
3. **发起会话**：调用 `POST /sessions`，传入 `agent`、`environment_id` 和可选 `resources`；会话创建即启动，无需额外“启动”操作。
4. **交互与监控**：
   - 发送用户消息：`POST /sessions/{id}/events`，`input` 中包含 `role: "user"` 的 message；
   - 订阅事件流：`GET /sessions/{id}/events/stream`，接收 SSE 流，关键事件类型包括 `message`、`tool_call`、`tool_output`、`session_status`；
   - 运行时干预：可在任意时刻发送新 `user` 事件引导或覆盖当前任务方向。

## 限制和注意事项

- **沙箱隔离性**：每个会话独占一个云端容器实例，文件系统、进程、环境变量完全隔离；挂载文件为只读副本（除非显式 `write` 修改），卸载后自动清理。
- **超时与终止**：会话默认空闲超时为 30 分钟（`idle` 状态），主动调用 `POST /sessions/{id}/terminate` 可立即终止；长时间运行任务需确保客户端保持 SSE 连接活跃或定期发送心跳事件。
- **工具调用约束**：
  - `bash` 命令受沙箱安全策略限制，禁止 `sudo`、`reboot`、后台守护进程等高危操作；
  - `write` 工具写入路径必须位于 `/mnt/session/` 下（如 `/mnt/session/workspace/`），不可写入系统目录；
  - 文件操作路径需使用绝对路径，相对路径行为未定义。
- **资源复用边界**：智能体、环境、挂载资源三者均为独立资源，可交叉复用（如一个智能体搭配多个环境），但会话一旦创建，其绑定的智能体版本与环境配置即固化，不可动态变更。

> **注意**：文档 6 中“委派任务给 Agent”章节提及“审批工具调用”，但当前公开 API 与控制台均未开放人工审批工作流；该能力属于内部灰度功能，开发者应以 [会话操作](../../raw/application-user-guide/managed-agents/managed-agents-session.md) 中描述的标准状态机（`running` → `idle`/`terminated`）为准，暂不依赖审批机制。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)


