# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台在服务端统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖并持久化事件历史。相比无状态的智能体应用，Managed Agents 支持中断续接、有状态上下文保持和会话级 SSE 事件流。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（详见 [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)）；模型需通过 `model.id` 字段显式指定，不支持动态路由或 fallback 模型。
- **内置工具集**：默认提供 `bash`、`read`、`write`、`edit`、`glob`、`grep`、`download_file` 7 个工具；可通过 `tools: [{"type": "builtin_toolkit"}]` 启用完整套件（见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）。
- **扩展能力**：
  - MCP 服务：接入外部工具服务；
  - Skill：挂载预置工具组合（如数据分析流程）；
  - 文件挂载：上传文件后自动挂载至 `/mnt/session/uploads/` 下，单文件上限 10 MB（参见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。

> **注意**：文档 2 中示例使用 `qwen3-max`，而文档 1 的表格示例写为 `qwen3.7-plus`；实际可用模型以控制台下拉列表或 [模型目录 API](https://help.aliyun.com/zh/model-studio/model-list) 返回为准，建议以最新控制台为准，避免硬编码过期 ID。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agent` / `agent_id` | string | 是（会话创建） | 智能体 ID，由 `agents.create()` 返回 |
| `environment_id` | string | 是（会话创建） | 运行环境 ID，由 `environments.create()` 返回 |
| `resources` | array | 否 | 资源挂载列表，含 `resource_id` 和 `mount_path`（见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)） |
| `title` | string | 否 | 会话标题，仅用于标识，不影响执行 |
| `system` / `system_prompt` | string | 是（智能体创建） | 定义角色与行为约束，直接影响工具调用倾向性 |
| `config.packages` | object | 否（环境创建） | 指定 `apt`/`pip`/`conda` 包，如 `"pip": ["pandas", "numpy"]` |

## 使用方式

1. **创建智能体**：调用 `POST /api/v1/agentstudio/agents`，传入 `name`、`model.id`、`system` 和 `tools`（[快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 提供多语言 SDK 示例）。
2. **创建运行环境**：调用 `POST /api/v1/agentstudio/environments`，指定 `config.type = "cloud"` 及所需预装包（同上）。
3. **发起会话**：调用 `POST /api/v1/agentstudio/sessions`，绑定 `agent` 和 `environment_id`，可选传入 `resources`。
4. **发送用户消息**：向 `sessions/{id}/events` POST 用户事件（`role: "user"`），内容为结构化 `input` 数组。
5. **接收事件流**：通过 `GET /sessions/{id}/events/stream` 建立 SSE 连接，监听 `message`、`tool_output`、`session_status` 等事件类型（[快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 给出完整流式消费示例）。

## 限制和注意事项

- **会话生命周期**：会话默认最长运行 2 小时，超时自动终止；可通过 `session_status` 事件监听 `terminated` 状态。
- **资源隔离**：挂载文件在会话沙箱内为只读副本（除非显式 `write` 修改），修改不影响原始资源，也不影响其他会话（[Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md) 明确说明）。
- **网络访问**：沙箱默认禁用外网；如需访问公网，必须在环境配置中显式设置 `networking: {"type": "unrestricted"}`（见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 环境配置示例）。
- **工具调用限制**：`bash` 命令执行受沙箱资源配额约束（CPU、内存、超时），长时间阻塞命令可能被强制终止；`download_file` 仅支持 HTTP/HTTPS URL，不支持私有 OSS 直链（需先通过 SDK 上传为资源再挂载）。
- **状态维护**：智能体本身无状态，所有上下文（文件系统、变量、进程）均绑定于会话及对应沙箱环境；切换环境或重启会话即丢失全部中间状态。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


