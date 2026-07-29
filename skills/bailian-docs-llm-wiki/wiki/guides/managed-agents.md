# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过服务端持久化的事件流反馈全过程。相比无状态的智能体应用，Managed Agents 提供有状态会话、中断续接与沙箱级资源隔离能力。

## 支持的模型与功能

- **支持模型**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（详见 [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)）；模型需在创建 Agent 时显式指定，不支持运行时动态切换。
- **内置工具**：默认提供 `bash`（命令执行）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（文件搜索）、`download_file`（URL 下载）共 7 个 builtin_toolkit 工具；所有工具均在沙箱内受限执行，无 root 权限。
- **扩展能力**：
  - 可挂载预置 Skill 封装端到端流程；
  - 支持接入 MCP 服务调用外部 API；
  - 支持挂载上传文件或远程 URL 资源（单文件 ≤10 MB），挂载路径固定为 `/mnt/session/uploads/...`（详见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。

> **注意**：文档 2 中示例使用 `qwen3-max`，而文档 1 的表格示例为 `qwen3.7-plus`；实际可用模型以控制台下拉列表或 [API 文档](https://help.aliyun.com/zh/model-studio/agent-create) 为准，旧模型名可能已下线。

## 关键参数

| 参数 | 说明 | 必填 | 示例 |
|------|------|------|------|
| `agent.id` | 智能体唯一标识，创建后复用 | 是 | `"agent_xxx"` |
| `environment_id` | 运行环境 ID，决定沙箱配置 | 是 | `"env_xxx"` |
| `tools` | 工具列表，仅支持 `{"type": "builtin_toolkit"}` 或显式工具数组 | 是（至少一项） | `[{"type": "builtin_toolkit"}]` |
| `resources` | 挂载资源列表（含 `resource_id` 和 `mount_path`） | 否 | `[{"resource_id": "res_abc", "mount_path": "/mnt/session/uploads/data.csv"}]` |
| `networking.type` | 环境网络策略，仅支持 `"unrestricted"` 或 `"restricted"`（默认） | 否 | `"unrestricted"` |

## 使用方式

1. **创建智能体**：调用 `POST /api/v1/agentstudio/agents`，指定 `name`、`model.id`、`system` 和 `tools`（参考 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 中的 API 示例）。
2. **创建环境**：调用 `POST /api/v1/agentstudio/environments`，配置 `config.type="cloud"` 及 `packages`（如 `pip: ["pandas"]`）、`networking`。
3. **创建会话**：调用 `POST /api/v1/agentstudio/sessions`，绑定 `agent` 和 `environment_id`，可选传入 `resources`。
4. **发送事件**：向 `POST /api/v1/agentstudio/sessions/{session_id}/events` 提交用户消息（`role: "user"`），内容为标准 Message 格式。
5. **接收事件流**：通过 SSE 订阅 `GET /api/v1/agentstudio/sessions/{session_id}/events/stream`，监听 `message`、`tool_output`、`session_status` 等事件类型。

## 限制和注意事项

- **沙箱约束**：所有命令在无特权 Linux 容器中执行，禁止访问宿主机、修改系统时间、使用 `sudo` 或启动后台守护进程。
- **资源隔离**：同一资源挂载到多个会话时，各会话获得独立副本；会话终止后副本自动清理，原始资源不受影响（详见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。
- **超时机制**：SSE 流默认超时 120 秒，需客户端主动重连；会话空闲 30 分钟自动进入 `idle` 状态，可手动唤醒或终止。
- **文件大小限制**：上传文件单个 ≤10 MB；沙箱内临时文件总容量受环境配额限制，超出将触发 `tool_error` 事件。
- **状态持久化**：事件历史在服务端完整保留，但会话 `status` 仅反映当前运行态（`running`/`idle`/`terminated`），不自动保存中间文件系统快照。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


