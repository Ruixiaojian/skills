# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过服务端持久化的 SSE 事件流反馈全过程。相比无状态的智能体应用，Managed Agents 支持中断续接、跨轮次上下文保持与沙箱级状态隔离。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（详见 [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)），模型通过 `model.id` 字段指定，暂不支持非 Qwen 模型。
- **内置工具集**：默认提供 `bash`（命令执行）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（文件搜索）、`download_file`（URL 下载）共 7 个工具；可通过 `tools: [{"type": "builtin_toolkit"}]` 启用全部，或按需显式声明子集。
- **扩展能力**：
  - MCP 服务：接入外部工具服务（如数据库、API 网关）；
  - Skill：复用预置的端到端任务流程（如“生成报告”“清洗数据”）；
  - 文件挂载：支持上传 ≤10 MB 文件，挂载至 `/mnt/session/uploads/` 下供智能体访问（详见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。

> **注意**：文档 2 的快速开始示例中使用 `qwen3-max`，但文档 1 的概述表格中仅列出 `qwen3.7-plus` 作为示例。实际可用模型以控制台下拉列表或 [创建 Agent](https://help.aliyun.com/zh/model-studio/agent-create) API 文档为准，建议以最新控制台显示为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 智能体名称，仅用于标识，不影响行为 |
| `model.id` | string | 是 | 模型 ID，如 `"qwen3-max"`，必须为平台支持的模型 |
| `system` / `system_prompt` | string | 是 | 系统提示词，定义角色与行为边界，直接影响工具调用倾向 |
| `tools` | array | 否（默认启用全部内置工具） | 工具配置数组，如 `[{"type": "bash"}, {"type": "read"}]`；设为空数组则禁用所有工具 |
| `environment_id` | string | 是（创建会话时） | 运行环境 ID，指向已创建的沙箱配置（详见 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)） |
| `resources` | array | 否 | 挂载资源列表，每个元素含 `resource_id` 和 `mount_path`（如 `"/mnt/session/uploads"`） |

## 使用方式

1. **创建智能体**：通过控制台向导或 API 提交 `name`、`model.id`、`system` 和 `tools`；返回唯一 `agent.id`，后续会话复用该 ID（[构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)）。
2. **创建运行环境**：独立配置沙箱类型（目前仅支持 `"cloud"`）、预装包（`apt`/`pip`）、网络策略（`"unrestricted"` 或 `"restricted"`）；环境可被多个会话共享。
3. **发起会话**：调用 `sessions.create`，传入 `agent.id` 和 `environment_id`；若需挂载文件，须在 `resources` 中指定已创建的资源 ID。
4. **交互与监听**：
   - 发送用户消息：`POST /sessions/{session_id}/events`，`input` 中包含 `role: "user"` 的消息块；
   - 接收事件流：`GET /sessions/{session_id}/events/stream`，SSE 流中包含 `message`（输出）、`tool_call`（调用请求）、`tool_output`（执行结果）、`session_status`（`idle`/`terminated`）等事件类型。

## 限制和注意事项

- **沙箱约束**：云端沙箱默认无持久化存储，会话终止后沙箱销毁；文件挂载为只读副本（除非显式 `write` 修改），修改不影响原始资源。
- **资源大小**：单个上传文件 ≤10 MB；`packages.pip` 安装的依赖包总大小建议 ≤500 MB，超限可能导致环境初始化失败。
- **会话生命周期**：空闲超时默认 30 分钟（可配置），超时后状态变为 `idle`；主动调用 `terminate` 或异常中断后状态为 `terminated`，事件历史仍可查询。
- **工具调用安全**：`bash` 工具默认禁用危险命令（如 `rm -rf /`、`shutdown`），但 `apt install` 和 `pip install` 仍受沙箱资源限制影响执行成功率。
- **调试建议**：预览调试页支持按事件类型筛选（User/Tool/Tool_output/Error），推荐优先使用该功能定位工具调用失败原因（详见 [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)）。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


