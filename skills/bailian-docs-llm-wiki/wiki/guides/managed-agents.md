# managed agents

Managed Agents 是百炼平台提供的托管式智能体运行时，专为多步工具调用、沙箱内代码执行、文件处理等长时有状态任务设计。平台统一托管会话状态、隔离沙箱环境与工具执行生命周期，开发者只需关注智能体逻辑配置与事件交互，无需自行实现代理循环、沙箱编排或状态持久化。其核心抽象包括智能体（Agent）、运行环境（Environment）、会话（Session）和事件（Event）四层结构。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（详见[快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)），模型通过 `model.id` 字段指定，调用产生的 token 消耗按对应模型公开计费标准单独结算。
- **内置工具集**：默认提供 7 个基础工具：`bash`（命令执行）、`read`/`write`/`edit`/`glob`/`grep`（文件操作）、`download_file`（URL 下载）。所有工具均在独立沙箱中执行，支持读写 `/mnt/session/uploads/` 下挂载的文件。
- **扩展能力**：支持挂载 MCP 服务与 Skill（预置工具组合），用于接入外部系统或封装端到端流程；资源挂载（如上传文件）独立于会话管理，可复用（参见[Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。

> **注意**：文档 1 中示例使用 `qwen3-max` 和 `qwen3.7-plus`，但文档 2 的概述未明确列出具体模型 ID；实际开发应以控制台下拉列表或 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 中的可用值为准，避免硬编码过时模型名。

## 关键参数

创建智能体、环境、会话时需配置以下关键字段：

| 资源 | 必填参数 | 说明 |
|------|----------|------|
| **Agent** | `name`, `model.id`, `system`（或 `instructions`）, `tools` | `tools` 推荐使用 `{"type": "builtin_toolkit"}` 启用全部内置工具；`system` 定义角色与行为约束（Java SDK 使用 `instructions` 字段） |
| **Environment** | `name`, `config.type`（`cloud` 为唯一支持类型）, `config.packages`（可选） | `config.networking.type` 可设为 `unrestricted`（默认）或 `restricted`；`packages` 支持 `apt`/`pip` 两类依赖安装 |
| **Session** | `agent`, `environment_id`, `title`（可选）, `resources`（可选） | `resources` 用于挂载已创建的文件资源，格式为 `[{"id": "res_xxx", "mount_path": "/mnt/session/uploads/data.csv"}]` |

## 使用方式

完整工作流分四步，支持控制台向导与 API 两种方式：

1. **创建智能体**：定义模型、系统提示词与工具集（参见[构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)）；
2. **配置运行环境**：创建云端沙箱，声明预装依赖（参见[配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)）；
3. **发起会话**：绑定智能体与环境，可选挂载资源（参见[委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)）；
4. **事件交互**：通过 `POST /sessions/{id}/events` 发送用户消息，通过 `GET /sessions/{id}/events/stream` 订阅 SSE 流接收 `message`、`tool_output`、`session_status` 等事件。

> **注意**：文档 1 的 Java 示例中 `AgentCreateParam.builder().instructions(...)` 与 Python 示例的 `system_prompt=` 不一致，且文档 3 未说明字段命名差异；实际调用应以各 SDK 最新文档为准，推荐优先使用 `system_prompt`（Python/Go）或 `system`（REST API）字段。

## 限制和注意事项

- **文件限制**：单个上传文件 ≤ 10 MB，挂载后路径固定为 `/mnt/session/uploads/xxx`，不可自定义根路径；
- **会话生命周期**：会话处于 `running` 状态即产生运行时费用（0.5 元/小时），空闲不计费；必须显式调用 `terminate` 接口或在控制台终止，否则持续计费（参见[计费](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)）；
- **沙箱隔离性**：每个会话拥有独立沙箱副本，对挂载文件的修改不影响原始资源或其他会话；
- **模型与工具费用分离**：运行时费、模型 token 费、工具/MCP 调用费三者独立计费，无捆绑折扣；
- **免费额度**：商业化后赠送 10 小时运行时免费额度，仅抵扣运行时费，30 天内有效。

## 来源文档

- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [计费](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)


