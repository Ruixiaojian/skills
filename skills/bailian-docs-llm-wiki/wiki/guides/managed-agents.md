# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，用于执行多步工具调用、代码执行、文件处理等长时运行任务。平台在服务端统一托管会话状态、沙箱环境与工具执行生命周期，开发者无需自行实现代理循环、沙箱编排或事件持久化。其核心抽象包括智能体（Agent）、运行环境（Environment）、会话（Session）和事件（Event）四个层级，支持有状态、可中断、可续接的会话式交互 [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)。

## 支持的模型与功能

- **模型支持**：支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（具体以控制台下拉列表为准），模型通过 `model.id` 字段指定；不支持自定义模型部署，仅限百炼托管模型。
- **内置工具**：默认提供 7 个内置工具：`bash`（命令执行）、`read`/`write`/`edit`（文件读写与编辑）、`glob`（路径通配）、`grep`（文本搜索）、`download_file`（从 URL 下载）。工具启用状态需显式配置（如 `{"name": "bash", "enabled": true}`），未启用则不可调用 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)。
- **扩展能力**：
  - **MCP 服务**：可接入符合 MCP 协议的外部工具服务；
  - **Skill**：预置的工具组合封装，用于端到端任务流程（如数据清洗、报告生成）；
  - **文件挂载**：支持上传文件并挂载至 `/mnt/session/uploads/` 路径，会话内可直接通过工具访问；单文件上限 10 MB [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)。

> **注意**：文档 1 的 Java SDK 示例中 `AgentCreateParam.builder().instructions(...)` 使用了 `instructions` 字段，而文档 2 和文档 3 均明确使用 `system_prompt` 或 `system` 字段；实际 API 以 `system`（Python/HTTP）或 `systemPrompt`（Java SDK v1.2+）为准，旧版 `instructions` 已弃用，建议统一使用 `system`。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 智能体名称，仅用于标识，不影响行为 |
| `model.id` | string | 是 | 模型 ID，如 `"qwen3-max"`，必须为平台支持的托管模型 |
| `system` | string | 是 | 系统提示词，定义角色、约束与行为准则 |
| `tools` | array | 否（但无工具则无法执行操作） | 工具配置数组，每个元素含 `type="builtin_toolkit"`、`default_config` 和 `configs`（含 `name` 与 `enabled`） |
| `environment_id` | string | 创建 Session 时必填 | 运行环境 ID，指向已创建的云端沙箱 |
| `resources` | array | 否 | 创建 Session 时可指定挂载资源列表，格式为 `[{ "resource_id": "...", "mount_path": "/mnt/session/uploads/data.csv" }]` |

## 使用方式

1. **创建智能体**：通过控制台向导或 API 提交 `POST /api/v1/agentstudio/agents`，传入 `name`、`model`、`system` 和 `tools`；智能体 ID 可复用于多个会话 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)。
2. **创建运行环境**：独立于智能体创建沙箱，支持 `cloud` 类型（百炼托管容器），可配置 `packages.apt`/`packages.pip` 安装依赖及 `networking.type`（如 `"unrestricted"`）。
3. **发起会话**：调用 `POST /api/v1/agentstudio/sessions`，绑定 `agent`（ID）、`environment_id`，并可选传入 `resources` 挂载文件。
4. **交互与流式消费**：
   - 发送用户消息：`POST /api/v1/agentstudio/sessions/{session_id}/events`，`input` 中包含 `role: "user"` 消息；
   - 接收事件流：`GET /api/v1/agentstudio/sessions/{session_id}/events/stream`，SSE 流返回 `message`、`tool_call`、`tool_output`、`session_status` 等事件类型，需按 `event.type` 解析 [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)。

## 限制和注意事项

- **沙箱隔离性**：每个会话运行在独立云端容器中，挂载文件为副本，会话间互不影响；卸载后副本自动清理，原始资源保留。
- **会话生命周期**：会话默认最长运行 2 小时（超时自动终止），可通过 `session_status` 事件监听 `idle` 或 `terminated` 状态。
- **工具调用限制**：
  - `bash` 命令受沙箱权限限制，禁止 `sudo`、`reboot`、`kill -9` 等高危操作；
  - `download_file` 仅支持 HTTP/HTTPS 协议，不支持认证头注入；
  - `glob` 和 `grep` 作用域限定在 `/mnt/session/` 下，不可跨沙箱路径访问。
- **调试建议**：预览调试页支持按事件类型（如 `Tool_output`、`Error`）筛选，便于定位工具执行失败原因；生产环境应订阅 SSE 流并实现重连逻辑（推荐 30s 超时 + 指数退避）。

## 来源文档

- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


