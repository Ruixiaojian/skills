# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过服务端持久化的事件流反馈执行过程。相比无状态的智能体应用，Managed Agents 支持中断续接、跨轮次上下文保持与沙箱级状态隔离。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（详见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）；模型需通过 `model.id` 字段显式指定，不支持动态路由或 fallback 模型。
- **内置工具集**：默认提供 7 个基础工具：`bash`（命令执行）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（文件搜索）、`download_file`（URL 下载）。所有工具均在沙箱内受限执行，无 root 权限。
- **扩展能力**：
  - 可集成 MCP 服务（通过 `mcp_servers` 字段注册外部工具服务）；
  - 可挂载 Skill 封装端到端流程（如数据清洗、PDF 解析）；
  - 支持挂载用户上传文件或远程 URL 资源（见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。

> **注意**：文档 2 中示例使用 `qwen3-max`，但文档 1 的概述表格中仅列出 `qwen3.7-plus` 作为示例模型。实际可用模型以控制台下拉列表或 [API 文档](https://help.aliyun.com/zh/model-studio/agent-create) 为准，建议以 `qwen3-max` 为首选生产模型。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 智能体名称，仅用于标识，不影响行为 |
| `model.id` | string | 是 | 模型 ID，如 `"qwen3-max"`，不可省略 |
| `system` / `system_prompt` | string | 是 | 系统提示词，定义角色与行为边界，直接影响工具调用倾向 |
| `tools` | array | 否（默认全启用） | 工具配置数组，如 `[{"type": "builtin_toolkit"}]`；禁用某工具需显式排除 |
| `environment_id` | string | 创建会话时必填 | 指向已创建的运行环境 ID，决定沙箱配置与预装依赖 |
| `resources` | array | 否 | 挂载资源列表，格式为 `[{"resource_id": "...", "mount_path": "/mnt/session/uploads/data"}]` |

## 使用方式

1. **创建智能体**：调用 `/api/v1/agentstudio/agents` 接口，传入 `name`、`model.id`、`system` 和 `tools`（参考 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 中的 API 示例）。
2. **创建运行环境**：调用 `/api/v1/agentstudio/environments`，指定 `config.type="cloud"` 及 `packages`（apt/pip）、`networking` 等沙箱配置（见 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)）。
3. **发起会话**：调用 `/api/v1/agentstudio/sessions`，绑定 `agent` ID 与 `environment_id`，可选传入 `title` 和 `resources`。
4. **交互与监听**：
   - 发送用户消息：`POST /sessions/{session_id}/events`，`input` 为标准 message 数组；
   - 实时接收事件：`GET /sessions/{session_id}/events/stream`，使用 SSE 流解析 `message`、`tool_output`、`session_status` 等事件类型（见 [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)）。

## 限制和注意事项

- **沙箱限制**：单次命令执行超时为 60 秒；内存上限 4 GB；磁盘空间上限 10 GB；网络访问默认受限（需显式配置 `networking.type="unrestricted"` 才允许外网请求）。
- **文件限制**：上传挂载的单个文件 ≤ 10 MB；沙箱内文件路径必须以 `/mnt/session/uploads/` 开头，硬编码路径在系统提示词中需严格匹配（见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。
- **状态持久性**：会话事件历史在服务端持久化，但沙箱文件系统**不跨会话保留**；同一资源被多个会话挂载时，各会话获得独立副本，修改互不影响。
- **权限隔离**：所有工具执行均在非 root 用户下运行，无法执行 `sudo`、`apt install` 等特权操作；依赖须在环境创建阶段预装，运行时不可动态安装。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


