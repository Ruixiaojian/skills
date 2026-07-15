# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并支持服务端持久化的事件历史与 SSE 流式反馈。相比无状态的智能体应用，Managed Agents 本质是“有状态会话 + 托管沙箱”的组合范式 [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（详见[快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)），模型通过 `model.id` 字段指定，需与工具能力匹配（如代码执行需模型具备强推理与工具调用理解能力）。
- **核心功能**：
  - 命令执行（`bash`）：在沙箱中运行 shell 命令，支持管道、重定向；
  - 文件操作（`read`/`write`/`edit`/`glob`/`grep`/`download_file`）：读写沙箱内文件，支持通配符搜索与正则文本查找；
  - 外部服务集成：通过 MCP 协议接入自定义工具服务，或挂载预置 Skill 封装端到端流程；
  - 资源挂载：支持上传文件并挂载至 `/mnt/session/uploads/` 下（单文件 ≤10 MB），挂载后副本隔离，修改不影响原始资源 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)。

> **注意**：文档 2 的快速开始示例中列出 `qwen3-max` 和 `qwen3.7-plus` 两种模型，但文档 3 未明确模型兼容性范围；实际使用应以控制台下拉列表或 API 返回的可用模型清单为准，避免硬编码过期 ID。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `agent.id` | 智能体唯一标识，创建后复用于多个会话 | `"agent_xxx"` | [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md) |
| `environment_id` | 运行环境 ID，决定沙箱配置（如预装包、网络策略） | `"env_xxx"` | [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md) |
| `resources` | 创建会话时挂载的资源列表，含 `resource_id` 与 `mount_path` | `[{"id": "res_abc", "path": "/mnt/session/uploads/data.csv"}]` | [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md) |
| `networking.type` | 沙箱网络策略，可选 `"unrestricted"`（默认）或 `"restricted"`（禁外网） | `"unrestricted"` | [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) |

## 使用方式

1. **创建智能体**：通过控制台向导或 API 指定 `name`、`model.id`、`system_prompt` 与 `tools`（内置工具需显式启用）；
2. **创建运行环境**：独立配置沙箱类型（仅支持 `cloud`）、预装包（`apt`/`pip`）及网络策略；
3. **发起会话**：绑定 `agent.id` 与 `environment_id`，可选挂载 `resources`；
4. **交互与监控**：
   - 发送用户消息：`POST /sessions/{session_id}/events`，`input` 中包含 `role: "user"` 的 message；
   - 订阅事件流：`GET /sessions/{session_id}/events/stream`，接收 `message`、`tool_output`、`session_status` 等事件；
   - 实时干预：在会话运行中发送新事件可中断当前流程并引导下一步 [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)。

## 限制和注意事项

- **沙箱资源限制**：单个会话内存上限 8 GB，CPU 核心数 4，超时默认 120 秒（可通过 `timeout` 参数调整，最大 3600 秒）；
- **文件大小限制**：上传挂载文件单个 ≤10 MB；沙箱内生成文件无硬限制，但总磁盘空间受限于容器配额；
- **工具调用安全边界**：`bash` 工具禁止执行 `rm -rf /`、`sudo`、`kill` 等高危命令，沙箱默认无 root 权限；
- **状态持久性**：会话终止后沙箱销毁，但事件历史永久保留；挂载资源卸载后副本自动清理，原始资源不受影响；
- **并发与复用**：同一智能体可被多个会话并发调用；同一环境可被多个会话共享，但各会话沙箱完全隔离。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


