# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、[文件处理](../concepts/file-processing.md)等长时运行任务设计。平台在服务端统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过持久化的事件历史支持中断续接。该能力显著降低开发者构建代理循环、沙箱编排和工具调度基础设施的运维负担。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）；模型需通过 `model.id` 字段显式指定，不支持动态路由或 fallback 模型。
- **核心工具集**：
  - 命令执行（`bash`）
  - 文件操作（`read`、`write`、`edit`、`glob`、`grep`）
  - 文件下载（`download_file`）
  - MCP 服务接入与 Skill 调用（见 [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)）
- **运行环境能力**：支持预装 `apt`/`pip` 包、配置网络策略（如 `unrestricted`）、挂载用户上传文件（见 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)）。

> **注意**：文档 3 的快速开始示例中 Python SDK 创建 Agent 时使用了 `system_prompt` 参数，而文档 4 的 [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md) 明确指出字段名为 `system`；实际 API 以 `system` 为准，`system_prompt` 为旧版别名，已弃用。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agent` | string | 是 | 智能体 ID（创建后返回），非名称 |
| `environment_id` | string | 是 | 运行环境 ID，非名称 |
| `title` | string | 否 | 会话标题，仅用于标识，不影响执行 |
| `resources` | array | 否 | 资源挂载列表，格式为 `[{"resource_id": "...", "mount_path": "/mnt/session/uploads/data"}]`（见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)） |

## 使用方式

1. **创建智能体**：配置模型、系统提示词（`system` 字段）和启用的工具（`tools` 数组），返回唯一 `agent.id`；
2. **创建运行环境**：指定 `config.type="cloud"` 及可选 `packages` 和 `networking`，返回 `environment.id`；
3. **发起会话**：POST `/sessions`，传入 `agent` 和 `environment_id`，支持同步挂载资源；
4. **交互与监听**：
   - 发送用户消息：POST `/sessions/{id}/events`，`input` 中包含 `role: "user"` 的 message；
   - 接收流式响应：GET `/sessions/{id}/events/stream`，使用 SSE 解析 `message`、`tool_output`、`session_status` 等事件类型。

所有步骤均支持控制台向导与 REST API / SDK（Python/Java/Bash 示例详见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）。

## 限制和注意事项

- **文件大小限制**：单个上传文件 ≤ 10 MB（见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）；
- **沙箱隔离性**：每个会话拥有独立容器实例，挂载文件为副本，修改不影响原始资源或其他会话；
- **会话生命周期**：空闲超时默认 30 分钟（`idle` 状态），超时后自动终止；可通过发送新事件重置计时；
- **工具启用粒度**：工具需在 `tools.configs` 中显式设 `"enabled": true`，未声明或设为 `false` 的工具不可用；
- **路径约定**：挂载文件统一位于 `/mnt/session/uploads/` 下，系统提示词中应直接引用该绝对路径。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


