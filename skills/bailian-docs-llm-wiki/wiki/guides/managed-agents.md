# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时、有状态任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，开发者无需自行编排代理循环或维护容器基础设施。所有事件（用户输入、工具调用、模型响应、状态变更）通过服务端持久化，并以 SSE 流式推送，支持中断、续接与跨轮上下文保持。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3-plus` 等 Qwen 系列大模型（详见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 中的模型下拉列表），模型选择直接影响工具调用决策质量与代码生成能力。
- **核心功能**：
  - **命令执行**：通过 `bash` 工具在沙箱中运行任意 shell 命令；
  - **文件操作**：内置 `read`/`write`/`edit`/`glob`/`grep`/`download_file` 六类文件工具，支持读写、搜索、编辑及 URL 下载；
  - **资源挂载**：可上传本地文件（≤10 MB）并挂载至 `/mnt/session/uploads/` 路径，供智能体直接访问；
  - **MCP 服务与 Skill**：支持接入外部 MCP 工具服务，或复用预置 Skill 封装端到端流程。

> **注意**：文档 2 中列出的默认工具含 `bash`、`read`、`write`、`edit`、`glob`、`grep`、`download_file` 共 7 个，但文档 6 的挂载路径说明仅提及 `/mnt/session/uploads` 前缀，未覆盖其他挂载方式（如 `download_file` 默认下载路径未明确）。实际开发中应以 API 响应中的 `file_path` 字段为准，避免硬编码路径。

## 关键参数

创建各组件时需关注以下关键参数：

| 组件 | 参数 | 说明 |
|------|------|------|
| **Agent** | `model.id` | 必填，指定模型 ID（如 `"qwen3-max"`）；[构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md) 强调其与系统提示词、工具的组合性 |
| | `system` / `system_prompt` | 定义角色与行为约束，影响工具选择倾向和输出格式 |
| | `tools` | 支持 `{"type": "builtin_toolkit"}`（启用全部内置工具）或显式声明工具列表 |
| **Environment** | `config.type` | 必填，目前仅支持 `"cloud"`（云端托管沙箱） |
| | `config.packages` | 可选，指定 `apt`/`pip`/`conda` 包列表，用于预装依赖（如 `["pandas", "numpy"]`） |
| | `config.networking.type` | 可选，`"unrestricted"`（默认）允许外网访问；`"restricted"` 禁用外网 |
| **Session** | `agent` | 必填，Agent ID 字符串 |
| | `environment_id` | 必填，Environment ID 字符串 |
| | `resources` | 可选数组，每个元素含 `resource_id` 和 `mount_path`（如 `"/mnt/session/uploads"`） |

## 使用方式

遵循“Agent → Environment → Session”三级创建顺序：

1. **创建 Agent**：配置模型、系统提示词与工具，获得唯一 `agent_id`（如 `agent_xxx`）；
2. **创建 Environment**：定义沙箱类型与预装包，获得 `env_id`（如 `env_xxx`）；[配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md) 明确指出环境可被多个会话复用；
3. **创建 Session**：绑定 `agent_id` 与 `env_id`，可选挂载资源，获得 `session_id`（如 `sesn_xxx`）；
4. **发送事件 & 订阅流**：
   - 向 `/sessions/{session_id}/events` POST 用户消息（`role: "user"`）；
   - 通过 `/sessions/{session_id}/events/stream` 建立 SSE 连接，实时接收 `message`、`tool_output`、`session_status` 等事件；[委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md) 强调所有交互均以事件形式记录与持久化。

## 限制和注意事项

- **会话生命周期**：会话处于 `running` 状态即产生运行时费用（0.5 元/小时），空闲（`idle`）不计费；务必调用 `terminate` 接口及时释放资源；
- **文件限制**：单次上传文件 ≤10 MB；挂载后副本独立于原始资源，会话内修改不影响其他会话或源文件；
- **网络与安全**：沙箱默认启用外网（`unrestricted`），若需隔离，必须显式设置 `networking.type: "restricted"`；
- **计费范围**：费用由三部分独立构成——会话运行时费、模型 token 费、工具/MCP 调用费；免费额度（10 小时）仅抵扣运行时费，不覆盖后两者；
- **状态管理**：SSE 流中 `session_status` 事件值为 `"idle"` 或 `"terminated"` 时应主动关闭连接，避免长连接泄漏。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [计费](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)


