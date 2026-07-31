# managed agents

Managed Agents 是百炼平台提供的托管式智能体运行时，用于执行多步[工具调用](../concepts/tool-use.md)、代码执行、文件处理等长时有状态任务。平台统一托管会话状态、沙箱环境与事件历史，开发者只需关注智能体逻辑配置，无需自行实现代理循环、沙箱编排或工具执行基础设施。其核心抽象包括智能体（Agent）、运行环境（Environment）、会话（Session）和事件（Event）[概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)。

## 支持的模型与功能

- **模型支持**：支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（具体以控制台下拉列表为准），模型通过 `model.id` 字段指定。
- **内置工具集**：默认提供 7 个基础工具：`bash`（命令执行）、`read` / `write` / `edit` / `glob` / `grep`（文件操作）、`download_file`（URL 下载）。工具通过 `tools` 数组声明，支持 `"builtin_toolkit"` 简写形式。
- **扩展能力**：
  - MCP 服务：接入外部工具服务；
  - Skill：挂载预置端到端任务流程；
  - 文件挂载：上传文件后挂载至 `/mnt/session/uploads/` 路径供智能体访问 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)；
  - 自定义沙箱：支持在 Environment 中预装 `apt`/`pip` 包及配置网络策略。

> **注意**：文档 2 中示例使用 `qwen3.7-plus` 和 `qwen3-max`，但当前控制台实际可选模型列表可能因 region 或权限而异；请以控制台实时下拉选项或 `GET /api/v1/agentstudio/models` API 返回为准，避免硬编码过期 ID。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | ✓ | 智能体名称，仅用于标识，不参与执行逻辑 |
| `model.id` | string | ✓ | 模型 ID，如 `"qwen3-max"` |
| `system` / `system_prompt` | string | ✓ | 系统提示词，定义角色与行为边界（Python SDK 使用 `system_prompt`，Java 使用 `instructions`，需按 SDK 规范传参） |
| `tools` | array | ✗（默认全选） | 工具配置，如 `[{"type": "builtin_toolkit"}]`；空数组表示禁用所有工具 |
| `environment_id` | string | ✓（Session 创建时） | 运行环境 ID，必须已存在；Environment 可被多个 Session 复用 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md) |
| `resources` | array | ✗ | 会话创建时挂载的资源列表，格式为 `[{"id": "res_xxx", "mount_path": "/mnt/session/uploads/data.csv"}]` |

## 使用方式

1. **创建智能体**：通过控制台向导或 API 提交配置（含模型、系统提示词、工具）；
2. **创建运行环境**：独立配置云端沙箱（如预装 `pandas`, `ffmpeg`），环境可复用；
3. **创建会话**：绑定智能体 ID 与环境 ID，可同时挂载资源；
4. **发送事件**：向会话 `POST /events` 发送用户消息（`role: "user"`）；
5. **接收流式响应**：通过 SSE 订阅 `/events/stream`，监听 `message`、`tool_output`、`session_status` 等事件类型。

完整调用链路见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)，其中各步骤均提供 Bash/Python/Java SDK 示例。

## 限制和注意事项

- **文件限制**：单个上传文件 ≤ 10 MB；挂载后路径固定为 `/mnt/session/uploads/` 下，不可自定义根路径；
- **会话隔离性**：同一资源挂载到多个会话时，各会话沙箱内为独立副本，互不影响；
- **状态持久化**：事件历史在服务端持久化，但沙箱内文件仅在会话生命周期内有效，会话终止后自动清理；
- **超时控制**：SSE 流建议设置客户端超时（如 Python 示例中 `timeout=120.0`），服务端默认会话空闲 5 分钟自动终止；
- **权限要求**：操作前需确保账号在目标工作空间具备 `Managed Agents` 相关 RAM 权限，否则控制台或 API 均返回 403。

> **注意**：文档 3 称 Managed Agents “支持中断与续接”，但当前版本（v1.2）**不支持会话状态断点续跑**；中断后需新建会话并重新挂载资源与上下文。该能力规划中，详见 [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md) 中“支持中断与续接”描述，实际行为以当前 API 行为为准。

## 来源文档

- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


