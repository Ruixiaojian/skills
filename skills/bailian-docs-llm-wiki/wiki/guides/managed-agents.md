# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过服务端持久化的事件历史实现中断续接。相比无状态的智能体应用，Managed Agents 更适合需要有状态上下文、文件系统语义和可控执行环境的场景。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（详见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）；模型通过 `model.id` 字段指定，创建后不可变更。
- **核心功能**：
  - 命令执行（`bash`）：在沙箱中运行任意 shell 命令；
  - 文件操作（`read`/`write`/`edit`/`glob`/`grep`/`download_file`）：支持读写、搜索、编辑沙箱内文件；
  - MCP 服务接入：通过标准 MCP 协议集成外部工具服务；
  - Skill 封装：复用预置的端到端任务流程（如数据分析、文档解析）；
  - 资源挂载：上传文件或从 URL 下载后挂载至 `/mnt/session/uploads/` 下指定路径，供智能体直接访问（详见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。

> **注意**：文档 2 中示例使用 `qwen3-max`，但文档 1 的概述表格中列出的是 `qwen3.7-plus`；实际可用模型以控制台下拉列表或 [API 文档](https://help.aliyun.com/zh/model-studio/agent-create) 为准，建议优先参考控制台实时枚举值。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `agent.id` | 智能体唯一标识，创建后用于绑定会话 | `"agent_xxx"` | [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md) |
| `environment_id` | 运行环境 ID，决定沙箱类型、预装包与网络策略 | `"env_xxx"` | [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md) |
| `resources` | 创建会话时指定的挂载资源列表（ID + 挂载路径） | `[{"id": "res_abc", "mount_path": "/mnt/session/uploads/data.csv"}]` | [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md) |
| `input`（事件） | 用户消息内容，需为符合 OpenAI-style 的 `message` 数组 | `[{"role": "user", "type": "message", "content": [{"type": "text", "text": "分析 sales.csv"}]}]` | [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md) |

## 使用方式

1. **创建智能体**：定义名称、模型、系统提示词与启用的工具（内置工具集默认全选），返回 `agent.id`；
2. **创建运行环境**：指定沙箱类型（`cloud`）、预装包（`apt`/`pip`）、网络策略（如 `"unrestricted"`），返回 `environment_id`；
3. **创建会话**：绑定 `agent.id` 与 `environment_id`，可选传入 `resources` 挂载文件；
4. **发送事件**：向会话 POST 用户消息（`input` 字段），触发智能体执行；
5. **接收事件流**：通过 SSE 接口（`/sessions/{id}/events/stream`）订阅实时事件，包括 `message`、`tool_call`、`tool_output`、`session_status` 等类型。

所有步骤均支持控制台向导与 API 双路径，推荐开发者优先使用 SDK（Python/Java/Bash 示例见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）。

## 限制和注意事项

- **文件限制**：单个上传文件 ≤ 10 MB；挂载后路径固定为 `/mnt/session/uploads/` 下子路径，不可自定义根目录；
- **沙箱隔离性**：同一资源被多个会话挂载时，各会话获得独立副本，修改互不影响；卸载后副本自动清理；
- **会话生命周期**：会话状态（`idle`/`running`/`terminated`）由服务端维护，不依赖客户端连接；超时未活动会话可能被自动终止（默认超时时间需查阅最新 API 文档）；
- **工具权限**：`bash` 工具默认禁止危险命令（如 `rm -rf /`、`shutdown`），具体黑名单策略以平台实际执行为准；
- **模型能力约束**：工具调用逻辑高度依赖模型对 `system_prompt` 和工具描述的理解，复杂流程建议显式在提示词中说明调用顺序与错误处理机制。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


