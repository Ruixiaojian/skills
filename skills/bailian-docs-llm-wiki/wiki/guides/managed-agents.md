# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台在服务端统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过持久化的事件历史支持中断续接。相比无状态的智能体应用，Managed Agents 更适用于需跨轮次保持上下文与文件系统状态的复杂任务。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（详见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）；模型通过 `model.id` 字段指定，不可动态切换。
- **核心功能**：
  - 命令执行（`bash`）：在沙箱中运行 shell 命令，支持管道、重定向等标准语法；
  - 文件操作：`read`、`write`、`edit`、`glob`、`grep`、`download_file` 六类内置工具，覆盖读取、写入、编辑、通配匹配与文本搜索；
  - 外部集成：通过 MCP 服务接入第三方工具，或挂载 Skill 封装端到端流程；
  - 资源挂载：支持上传文件并挂载至 `/mnt/session/uploads/` 下，会话内修改不影响原始资源（见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。

> **注意**：文档 2 中示例使用 `qwen3-max`，而文档 1 的概述部分列举为 `qwen3.7-plus`；实际可用模型以控制台下拉列表或 [API 文档](https://help.aliyun.com/zh/model-studio/agent-create) 为准，建议以最新控制台为准。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `agent.id` | 智能体唯一标识，创建后复用 | `"agent_abc123"` | [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md) |
| `environment_id` | 运行环境 ID，决定沙箱配置（如预装包、网络策略） | `"env_def456"` | [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md) |
| `resources` | 创建会话时可选挂载的资源列表，格式为 `[{"id": "res_xyz", "mount_path": "/mnt/session/uploads/data.csv"}]` | — | [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md) |
| `input`（事件） | 用户消息结构，必须为 `role: "user"` + `type: "message"` + `content` 数组 | `[{ "role": "user", "type": "message", "content": [{ "type": "text", "text": "分析 sales.csv" }] }]` | [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md) |

## 使用方式

1. **创建智能体**：通过控制台向导或 API 指定模型、系统提示词和启用的工具（如 `bash`, `read`, `write`），返回 `agent.id`；
2. **创建运行环境**：独立配置沙箱类型（仅支持 `cloud`）、预装包（`apt`/`pip`）、网络策略（`unrestricted` 或 `restricted`）；
3. **发起会话**：绑定 `agent.id` 与 `environment_id`，可选传入 `resources` 挂载文件；
4. **交互与监听**：
   - 发送用户事件：`POST /sessions/{session_id}/events`，携带 `input` 消息；
   - 接收流式响应：`GET /sessions/{session_id}/events/stream`，SSE 协议，事件类型包括 `message`、`tool_call`、`tool_output`、`session_status` 等。

所有步骤均支持控制台操作与 SDK/API 调用，推荐生产环境使用 SDK 封装（如 Python `client.sessions.events.stream()`）。

## 限制和注意事项

- **沙箱隔离性**：每个会话独占一个云端容器，但同一环境下的多个会话**不共享**文件系统或进程空间；
- **文件大小限制**：单个上传文件 ≤ 10 MB（见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）；
- **工具启用粒度**：工具需在创建智能体时显式启用（如 `{"name": "bash", "enabled": true}`），运行时不可动态增删；
- **会话生命周期**：空闲超时默认 30 分钟，超时后自动终止；主动中断需调用 `PATCH /sessions/{id}` 设置 `status=terminated`；
- **状态持久化范围**：事件历史在服务端持久化，但沙箱内存、未保存的临时文件在会话终止后即销毁。

> **注意**：文档 2 的 Java 示例中 `AgentCreateParam.builder().instructions(...)` 使用了 `instructions` 字段，而文档 1 和文档 3 明确使用 `system` 或 `system_prompt` 字段；实际 API 以 `system` 为准（参见 [创建 Agent](https://help.aliyun.com/zh/model-studio/agent-create)），Java SDK 的 `instructions` 属于过时别名，应统一使用 `systemPrompt` 或对应字段。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


