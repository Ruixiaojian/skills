# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过服务端持久化的事件流反馈全过程。相比无状态的智能体应用，Managed Agents 本质是“有状态会话 + 托管沙箱 + 事件驱动”的组合能力。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）；模型需显式指定 ID，不支持通配符或别名。
- **内置工具**：默认提供 7 类工具：`bash`（命令执行）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（文件搜索）、`download_file`（URL 下载）。所有工具均在沙箱内受限执行，不可绕过权限控制。
- **扩展能力**：
  - **MCP 服务**：可接入符合 MCP 协议的外部工具服务；
  - **Skill**：复用预置的端到端任务流程（如数据清洗、PDF 解析）；
  - **自定义沙箱环境**：支持 `apt`/`pip` 包预装、网络策略（`unrestricted` 或 `restricted`）配置（见 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)）。

> **注意**：文档 2 示例中 Python SDK 创建 Agent 时使用 `system_prompt` 字段，而文档 5 明确说明字段名为 `system`；实际 API 以 `system` 为准（[构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)），SDK 封装可能存在命名差异，请以 OpenAPI Schema 为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agent` | string | 是 | 智能体 ID（创建后返回），非名称 |
| `environment_id` | string | 是 | 运行环境 ID，非名称；同一环境可被多个会话复用 |
| `title` | string | 否 | 会话标题，仅用于管理标识，不影响执行 |
| `resources` | array | 否 | 资源挂载列表，格式为 `[{"resource_id": "...", "mount_path": "/mnt/session/uploads/data"}]`；挂载路径必须以 `/mnt/session/uploads/` 开头（见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)） |
| `timeout`（SSE 流） | number | 否 | 推荐设为 `120.0` 秒以上，避免长任务被意外中断 |

## 使用方式

1. **创建智能体**：调用 `POST /api/v1/agentstudio/agents`，指定 `model.id`、`system` 提示词和 `tools` 列表（含 `builtin_toolkit` 结构）；
2. **创建环境**：调用 `POST /api/v1/agentstudio/environments`，配置 `config.type="cloud"` 及 `packages`；
3. **发起会话**：调用 `POST /api/v1/agentstudio/sessions`，绑定 `agent` 和 `environment_id`，可选传入 `resources`；
4. **发送用户消息**：调用 `POST /api/v1/agentstudio/sessions/{session_id}/events`，`input` 中包含 `role: "user"` 的 message 块；
5. **订阅事件流**：`GET /api/v1/agentstudio/sessions/{session_id}/events/stream`，使用 `text/event-stream` 头解析 SSE，关注 `message`、`tool_output`、`session_status` 等事件类型。

## 限制和注意事项

- **文件限制**：单个上传文件 ≤ 10 MB；挂载后路径固定为 `/mnt/session/uploads/xxx`，不可自定义根目录（见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）；
- **沙箱隔离**：每个会话独占容器实例，资源挂载为副本，修改互不影响；
- **超时控制**：会话默认最长运行 2 小时，超时自动终止；SSE 流需客户端主动维持连接，建议设置 `timeout` ≥ 120 秒；
- **工具调用安全**：`bash` 工具默认禁用危险命令（如 `rm -rf /`、`sudo`），且无法访问宿主机文件系统；
- **状态管理**：会话支持中断（`PATCH /sessions/{id}/status` → `"interrupted"`）与续接，但重启后仅恢复事件历史，不恢复内存状态。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


