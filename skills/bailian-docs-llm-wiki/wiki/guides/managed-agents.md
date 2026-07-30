# managed agents

Managed Agents 是百炼平台提供的托管式智能体运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，开发者只需关注智能体逻辑配置，无需自行实现代理循环、沙箱编排或事件持久化。其核心抽象包括智能体（Agent）、运行环境（Environment）、会话（Session）和事件（Event）四层结构，支持服务端有状态会话与 SSE 事件流实时反馈。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（详见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)），模型通过 `model.id` 字段指定，必须显式声明。
- **内置工具集**：默认提供 7 个基础工具：`bash`（命令执行）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（路径与文本搜索）、`download_file`（URL 下载）。工具以 `{"type": "builtin_toolkit"}` 方式声明，不可按单个工具粒度开关。
- **扩展能力**：
  - **MCP 服务**：可接入外部工具服务（见 [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)）；
  - **Skill**：预置的端到端任务封装（如数据清洗、报告生成），在智能体创建后追加；
  - **资源挂载**：支持上传文件并挂载至 `/mnt/session/uploads/` 路径，单文件上限 10 MB（见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。

> **注意**：文档 1 中“快速开始”页面描述工具可“按需取消勾选”，但 API 创建时仅支持整体启用 `builtin_toolkit`；实际不支持禁用其中部分工具——该 UI 描述与后端行为不一致，应以 API 行为为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 智能体名称，仅用于标识，不影响运行 |
| `model.id` | string | 是 | 模型 ID，如 `"qwen3-max"`，不支持别名或版本通配 |
| `system` / `instructions` | string | 是 | 系统提示词，定义角色与行为边界；Java SDK 使用 `instructions`，Python/Bash 使用 `system` 或 `system_prompt` |
| `tools` | array | 是 | 固定为 `[{"type": "builtin_toolkit"}]`，暂不支持自定义工具或第三方插件 |
| `environment_id` | string | 是（会话级） | 运行环境 ID，必须提前创建；环境可被多个会话复用（见 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)） |
| `resources` | array | 否 | 挂载资源列表，格式为 `[{"resource_id": "...", "mount_path": "/mnt/session/uploads/data.csv"}]` |

## 使用方式

1. **创建智能体**：调用 `POST /api/v1/agentstudio/agents`，传入 `name`、`model.id`、`system` 和 `tools`（见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 示例）；
2. **创建运行环境**：调用 `POST /api/v1/agentstudio/environments`，指定 `config.type="cloud"` 及 `packages`（apt/pip）、`networking` 等沙箱配置；
3. **创建会话**：调用 `POST /api/v1/agentstudio/sessions`，绑定 `agent` ID 与 `environment_id`，可选传入 `resources`；
4. **发送用户消息**：向 `sessions/{id}/events` 发送 `input` 数组，`role="user"`，`content` 为文本块；
5. **接收事件流**：通过 `sessions/{id}/events/stream` 建立 SSE 连接，监听 `message`、`tool_call`、`tool_output`、`session_status` 等事件类型。

## 限制和注意事项

- **沙箱隔离性**：每个会话独占一个云端容器实例，挂载文件为副本，会话间文件系统完全隔离；
- **会话生命周期**：会话默认最长运行 2 小时（超时自动终止），可通过 `session_status` 事件监听 `idle` 或 `terminated` 状态；
- **网络访问**：沙箱默认禁用外网访问；如需开放，必须在环境配置中显式设置 `networking: {"type": "unrestricted"}`；
- **资源复用**：文件资源、环境、智能体均可跨会话复用，但会话本身不可复用——每次任务需新建会话；
- **调试建议**：预览调试页支持按事件类型筛选（User/Tool/Tool_output/Error），便于定位工具调用失败原因（见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）；
- **错误处理**：工具执行失败时返回 `error` 事件，含 `stderr` 输出；模型生成异常（如 token 超限）触发 `model_error` 事件，需在客户端主动捕获。

## 来源文档

- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


