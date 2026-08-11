# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过服务端持久化的事件流反馈执行过程。相比无状态的智能体应用，Managed Agents 支持中断续接、跨轮次状态保持和细粒度事件观测。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（详见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）；模型需在创建 Agent 时显式指定，不支持运行时动态切换。
- **内置工具集**：默认提供 7 个基础工具：`bash`（命令执行）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（文件搜索）、`download_file`（URL 下载）。可通过 `tools: [{"type": "builtin_toolkit"}]` 启用全部，或按需定制子集。
- **扩展能力**：
  - MCP 服务：接入外部工具服务（如数据库、API 网关），需在 Agent 配置中显式声明；
  - Skill：预置的端到端任务封装（如“数据清洗”“PDF 解析”），可复用但暂未在快速开始流程中默认启用；
  - 文件挂载：支持上传本地文件或从 URL 下载，挂载路径固定为 `/mnt/session/uploads/`，单文件上限 10 MB（参见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。

> **注意**：文档 3 中示例使用 `qwen3-max`，而文档 1 表格中仅列出 `qwen3.7-plus` 作为示例模型。实际可用模型以控制台下拉列表或 [API 文档](https://help.aliyun.com/zh/model-studio/agent-create) 为准，建议以最新控制台界面或 `GET /api/v1/agentstudio/models` 接口返回为准。

## 关键参数

| 参数 | 类型 | 说明 | 是否必需 |
|------|------|------|----------|
| `name` | string | 智能体名称，用于控制台识别 | 是（API 创建时必填） |
| `model.id` | string | 模型 ID，如 `"qwen3-max"` | 是 |
| `system` / `system_prompt` | string | 系统提示词，定义角色与行为边界 | 是（空字符串亦可） |
| `tools` | array | 工具配置数组，如 `[{"type": "builtin_toolkit"}]` | 是（至少需启用一个工具） |
| `environment_id` | string | 运行环境 ID，指向已创建的沙箱配置 | 创建 Session 时必需 |
| `resources` | array | 资源挂载列表，含 `resource_id` 和 `mount_path` | 可选（用于文件输入） |

环境配置关键字段：
- `config.type`: 当前仅支持 `"cloud"`（云端托管沙箱）；
- `config.packages`: 支持 `apt`（Debian 包）和 `pip`（Python 包）两级预装，如 `{"apt": ["ffmpeg"], "pip": ["pandas"]}`；
- `config.networking.type`: `"unrestricted"`（默认）或 `"restricted"`（禁用外网）。

## 使用方式

1. **创建 Agent**：通过控制台向导或 API 定义模型、系统提示词与工具组合。Agent 创建后生成唯一 ID（如 `agent_xxx`），可被多个会话复用（参见 [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)）。
2. **创建 Environment**：独立于 Agent 配置沙箱，支持预装依赖与网络策略。同一环境可被多个会话共享（参见 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)）。
3. **创建 Session**：绑定 Agent ID 与 Environment ID，可同时指定 `resources` 挂载文件。Session 是有状态的运行实例，其事件历史在服务端持久化（参见 [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)）。
4. **交互与监控**：
   - 发送用户消息：`POST /sessions/{session_id}/events`，内容为标准 Message 格式；
   - 订阅事件流：`GET /sessions/{session_id}/events/stream`，接收 SSE 流，事件类型包括 `message`、`tool_call`、`tool_output`、`session_status` 等；
   - 实时调试：控制台提供事件类型筛选（User/Agent/Tool/Error 等），便于定位执行卡点。

## 限制和注意事项

- **会话生命周期**：单次会话最长运行 2 小时，超时自动终止；手动调用 `terminate` 接口可提前结束。
- **资源隔离**：挂载文件在沙箱内为只读副本（除非显式 `write` 修改），修改不影响原始资源；同一资源挂载至多个会话时，各会话沙箱内副本相互隔离。
- **工具权限**：`bash` 工具默认禁止 `sudo`、`rm -rf /` 等高危命令，沙箱内无 root 权限；`download_file` 仅支持 HTTP/HTTPS 协议。
- **状态维护**：会话状态（含文件系统变更、环境变量）仅在该 Session 生命周期内有效，不可跨 Session 继承；若需长期状态，须通过挂载资源或外部存储（如 OSS）显式持久化。
- **错误处理**：工具执行失败时返回 `error` 类型事件，包含 stderr 输出；模型生成异常（如无限循环调用）将触发服务端熔断并推送 `session_status: "error"` 事件。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


