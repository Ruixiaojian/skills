# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过服务端持久化的事件历史实现中断续接。其核心价值在于将代理循环、沙箱编排与工具调度等基础设施复杂性从开发者侧剥离。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（详见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）；模型需在创建 Agent 时显式指定，不支持运行时动态切换。
- **内置工具集**：默认提供 `bash`（命令执行）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（文件搜索）、`download_file`（URL 下载）共 7 个基础工具；可通过 `tools: [{"type": "builtin_toolkit"}]` 启用全部，或按需精简。
- **扩展能力**：
  - **MCP 服务**：接入外部工具服务（如数据库、API 网关），需在 Agent 配置中声明；
  - **Skill**：复用预置的端到端任务流程（如“PDF 解析+摘要生成”），可后续追加；
  - **文件挂载**：支持上传本地文件或指定 URL，挂载至 `/mnt/session/uploads/` 路径下供智能体访问（详见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。

> **注意**：文档 2 中示例使用 `qwen3-max`，而文档 1 的概述表格中仅列出 `qwen3.7-plus`；实际可用模型以控制台下拉列表或 [API 文档](https://help.aliyun.com/zh/model-studio/agent-create) 实时为准，建议以控制台或 `GET /api/v1/agentstudio/models` 接口返回为准。

## 关键参数

| 参数 | 类型 | 说明 | 必填 |
|------|------|------|------|
| `name` | string | 智能体/环境/会话的可读名称，仅用于标识 | 是（Agent/Environment/Session 均需） |
| `model.id` | string | 模型 ID（如 `"qwen3-max"`），必须为平台已开通的模型 | 是（Agent） |
| `system` / `system_prompt` | string | 系统提示词，定义角色与行为边界；影响工具调用倾向性 | 是（Agent） |
| `tools` | array | 工具配置数组，`[{"type": "builtin_toolkit"}]` 表示启用全部内置工具 | 是（Agent） |
| `config.type` | string | 环境类型，固定为 `"cloud"`（云端托管沙箱） | 是（Environment） |
| `config.packages` | object | 沙箱预装包，支持 `apt`（Debian 包）、`pip`（Python 包）字段 | 否（默认空） |
| `config.networking.type` | string | 网络策略，`"unrestricted"`（允许外网访问）或 `"restricted"`（仅内网） | 否（默认 `"restricted"`） |
| `resources` | array | 会话级挂载资源列表，含 `resource_id` 和 `mount_path`（如 `"/mnt/session/uploads"`） | 否（文件处理场景推荐） |

## 使用方式

1. **创建智能体**：调用 `POST /api/v1/agentstudio/agents`，传入 `name`、`model`、`system` 和 `tools`；返回 `agent.id` 用于后续引用（[构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)）。
2. **创建运行环境**：调用 `POST /api/v1/agentstudio/environments`，指定 `config.type="cloud"` 及可选 `packages`；环境可被多个会话复用（[配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)）。
3. **发起会话**：调用 `POST /api/v1/agentstudio/sessions`，绑定 `agent.id` 与 `environment_id`，可选传入 `resources` 挂载文件。
4. **交互与流式消费**：
   - 发送用户消息：`POST /api/v1/agentstudio/sessions/{session_id}/events`，`input` 中包含 `role: "user"` 的 message；
   - 接收事件流：`GET /api/v1/agentstudio/sessions/{session_id}/events/stream`，使用 SSE 协议监听 `message`、`tool_output`、`session_status` 等事件（[委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)）。

## 限制和注意事项

- **文件大小限制**：单个上传文件 ≤ 10 MB（[Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。
- **沙箱隔离性**：每个会话拥有独立沙箱副本，挂载文件的修改不影响原始资源或其他会话；卸载后副本自动清理。
- **会话生命周期**：空闲超时默认 30 分钟（可配置），超时后状态变为 `idle`；主动调用 `terminate` 或异常终止后状态为 `terminated`，事件历史仍保留。
- **网络访问**：默认沙箱网络受限（`"restricted"`），如需外网访问（如 `curl` 下载、`pip install`），必须在 `config.networking.type` 中显式设为 `"unrestricted"`。
- **调试建议**：控制台「预览调试」页支持按事件类型（User/Tool/Tool_output/Error）筛选，便于定位工具调用失败原因；生产环境应捕获 `error` 类事件并做降级处理。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


