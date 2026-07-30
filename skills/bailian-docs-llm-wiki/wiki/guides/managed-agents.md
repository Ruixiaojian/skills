# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主运行命令、读写文件、安装依赖，并支持中断续接与事件历史持久化。其核心价值在于将代理循环、沙箱编排与工具调度等基础设施复杂性从应用侧剥离，开发者可专注 Agent 逻辑本身。

## 支持的模型与功能

- **模型支持**：支持 `qwen3-max`、`qwen3.7-plus` 等百炼主流大模型（详见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 中的模型下拉列表）。
- **内置工具集**：默认提供 7 个基础工具：`bash`（命令执行）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（文件搜索）、`download_file`（URL 下载）。也可通过 `builtin_toolkit` 统一启用全部工具。
- **扩展能力**：
  - 挂载预置 Skill 封装端到端流程；
  - 接入外部 MCP 服务；
  - 上传本地文件或从 URL 下载资源挂载至 `/mnt/session/uploads/` 路径（见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）；
  - 在沙箱中预装 `apt`/`pip` 包（如 `pandas`, `ffmpeg`），支持动态依赖安装。

> **注意**：文档 5 中称“环境可被多个会话复用”，而文档 1 的“工作流程”描述为“配置运行环境 → 发起会话”，未明确复用语义；实际 API 设计与控制台行为均支持环境复用，以文档 5 和 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 中的环境创建示例为准。

## 关键参数

| 参数 | 类型 | 说明 | 来源 |
|------|------|------|------|
| `agent` | string | 智能体 ID（创建后返回），必填 | [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md) |
| `environment_id` | string | 运行环境 ID，必填 | [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) |
| `resources` | array | 挂载资源列表，含 `resource_id` 与 `mount_path`（如 `/mnt/session/uploads/`） | [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md) |
| `tools` | array | 工具配置，支持 `{"type": "builtin_toolkit"}` 或显式工具列表 | [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md) |
| `config.packages` | object | 环境预装包，格式为 `{"apt": [...], "pip": [...]}` | [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) |

## 使用方式

1. **创建智能体**：指定名称、模型 ID、系统提示词和工具（如 `{"type": "builtin_toolkit"}`），获取 `agent.id`。
2. **创建运行环境**：定义沙箱类型（`type: "cloud"`）、网络策略（如 `"unrestricted"`）及预装包，获取 `environment.id`。
3. **发起会话**：绑定智能体 ID 与环境 ID，可选挂载资源（`resources` 字段），获取 `session.id`。
4. **交互与监听**：
   - 发送用户消息：向 `/sessions/{id}/events` POST 含 `role: "user"` 的消息；
   - 接收 SSE 流：GET `/sessions/{id}/events/stream`，解析 `message`、`tool_output`、`session_status` 等事件类型；
   - 支持运行中干预：发送新 `user` 事件可重定向执行路径。

所有步骤均支持控制台向导与 SDK/API（Python/Java/Bash 示例见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）。

## 限制和注意事项

- **文件大小限制**：单个上传文件 ≤ 10 MB（[Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。
- **沙箱隔离性**：同一资源挂载到多个会话时，各会话拥有独立副本，修改互不影响；卸载后副本自动清理。
- **会话生命周期**：SSE 流需设置合理超时（如 Python 示例中 `timeout=120.0`），`session_status` 为 `"idle"` 或 `"terminated"` 时应主动关闭流。
- **模型兼容性**：非 `qwen3` 系列模型可能不支持全部工具调用协议，建议优先选用文档明确列出的模型。
- **权限要求**：调用方账号须在目标工作空间内具备 `Managed Agents` 相关操作权限（见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 前置准备）。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)


