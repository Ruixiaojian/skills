# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、[文件处理](../concepts/file-processing.md)等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过服务端持久化的事件流反馈全过程。其核心价值在于将开发者从代理循环编排、沙箱运维和状态管理中解放出来，聚焦于 Agent 逻辑本身。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（详见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 中的模型下拉列表）；模型需通过 `model.id` 字段显式指定。
- **内置工具集**：默认提供 7 个基础工具：`bash`（命令执行）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（文件搜索）、`download_file`（URL 下载）。可通过 `tools: [{"type": "builtin_toolkit"}]` 启用全部，或按需定制子集。
- **扩展能力**：
  - MCP 服务：接入外部工具服务（如数据库、API 网关），需在智能体配置中显式声明；
  - Skill：预置的端到端任务封装（如“数据清洗”、“PDF 解析”），可挂载复用；
  - 文件挂载：支持上传文件或从 URL 下载，挂载路径固定为 `/mnt/session/uploads/`（参见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。

> **注意**：文档 2 中示例使用 `qwen3-max`，而文档 1 的概述表格中列出 `qwen3.7-plus` 作为示例模型。实际可用模型以控制台下拉列表或 [模型服务文档](https://help.aliyun.com/zh/model-studio/model-list) 为准，二者无本质矛盾，仅反映不同时间点的典型值。

## 关键参数

| 参数 | 类型 | 说明 | 是否必需 |
|------|------|------|----------|
| `agent` | string | 智能体 ID（创建后返回），用于绑定会话 | ✅ |
| `environment_id` | string | 运行环境 ID，决定沙箱配置与预装依赖 | ✅ |
| `title` | string | 会话标题，仅用于标识，不影响执行 | ❌ |
| `resources` | array | 资源 ID 列表，指定挂载的文件或 URL 资源 | ❌（挂载文件时必需） |
| `timeout` | number | SSE 流超时（秒），默认 120，最大 3600 | ❌（推荐显式设置） |

环境配置关键字段：
- `config.type`: 必须为 `"cloud"`（当前仅支持云端托管）；
- `config.packages`: 支持 `apt`（系统包）与 `pip`（Python 包）两类预装项；
- `config.networking.type`: 可选 `"unrestricted"` 或 `"restricted"`（后者禁用外网访问）。

## 使用方式

1. **创建智能体**：调用 `/api/v1/agentstudio/agents` 接口，传入 `name`、`model.id`、`system` 和 `tools`。智能体 ID 可复用于多个会话（参见 [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)）。
2. **创建环境**：调用 `/api/v1/agentstudio/environments`，指定 `config.type="cloud"` 及所需 `packages`。环境可被多个会话共享（参见 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)）。
3. **发起会话**：调用 `/api/v1/agentstudio/sessions`，绑定 `agent` 与 `environment_id`，并可选传入 `resources` 挂载文件。
4. **交互与监听**：
   - 发送用户消息：`POST /sessions/{id}/events`，`input` 中包含 `role: "user"` 的 message；
   - 接收事件流：`GET /sessions/{id}/events/stream`，使用 SSE 协议解析 `message`、`tool_output`、`session_status` 等事件类型（参见 [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)）。

## 限制和注意事项

- **文件限制**：单个上传文件 ≤ 10 MB；挂载后路径固定为 `/mnt/session/uploads/`，不可自定义根路径。
- **会话隔离性**：同一资源挂载到多个会话时，各会话获得独立副本，修改互不影响；卸载后副本自动清理，原始资源保留。
- **超时控制**：SSE 流默认超时 120 秒，长任务建议显式设置 `timeout=3600`（最大值）；会话空闲超时为 30 分钟，超时后自动终止。
- **工具执行约束**：
  - `bash` 命令受沙箱权限限制，禁止 `sudo`、`reboot` 等高危操作；
  - `pip install` 仅在会话首次启动时生效，后续执行不重装（依赖需在环境 `packages` 中预置）；
  - `download_file` 仅支持 HTTP/HTTPS 协议，不支持认证头。
- **状态持久化**：事件历史在服务端完整留存，但会话 `status` 为 `terminated` 后不可再发送新事件；若需续接，必须新建会话并重新挂载资源。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


