# managed agents

Managed Agents 是百炼平台提供的托管式智能体运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，开发者只需关注 Agent 逻辑（模型、提示词、工具组合），无需自行实现代理循环、沙箱编排或事件持久化。所有事件（用户输入、工具调用、模型响应、状态变更）均以结构化形式在服务端持久化，并通过 SSE 流实时推送。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（具体列表以控制台下拉菜单为准）。模型需通过 `model.id` 字段显式指定，如 `"model": {"id": "qwen3-max"}` —— 注意 Java SDK 示例中误省略了 `{"id": ...}` 结构，实际 API 要求严格遵循该格式，详见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)。
- **核心功能**：
  - 工具调用：内置 `bash`、`read`、`write`、`edit`、`glob`、`grep`、`download_file` 7 个工具，默认全选；
  - MCP 服务接入：支持对接外部工具服务；
  - Skill 封装：可挂载预置技能（如数据分析流水线），复用端到端任务流程；
  - 文件处理：支持上传挂载、URL 下载、沙箱内读写编辑；
  - 沙箱隔离：每个会话运行于独立云端容器，支持 apt/pip 包安装与自定义网络策略。

> **注意**：文档 1 的 Java 创建示例中 `AgentCreateParam.builder().model("qwen3-max")` 写法与实际 API 不符；正确方式应为 `.model(Model.builder().id("qwen3-max").build())`，否则将返回 400 错误。该不一致已在 [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md) 中明确要求模型字段为对象结构。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 智能体名称，仅用于标识，不影响运行 |
| `model.id` | string | 是 | 模型 ID，必须从平台支持列表中选择（如 `"qwen3-max"`） |
| `system` / `instructions` | string | 是 | 系统提示词，定义角色与行为边界；控制台字段名为 `system`，Java SDK 使用 `instructions`，二者语义等价 |
| `tools` | array | 否（但无工具则无法执行操作） | 工具配置数组，至少含一个 `builtin_toolkit` 条目；每个工具需显式声明 `enabled: true`（见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)） |
| `environment_id` | string | 是（创建 Session 时） | 运行环境 ID，指向已创建的沙箱配置 |
| `resources` | array | 否 | 挂载资源列表，格式为 `[{"resource_id": "...", "mount_path": "/mnt/session/uploads/data"}]`；路径必须以 `/mnt/session/uploads/` 开头 |

## 使用方式

1. **创建智能体**：通过控制台向导或 API 提交配置（模型、系统提示词、工具）；
2. **创建运行环境**：定义沙箱类型（`cloud`）、预装包（`apt`/`pip`）、网络策略（如 `"unrestricted"`）；
3. **发起会话**：绑定智能体 ID 与环境 ID，可同时指定挂载资源；
4. **发送事件**：使用 `POST /sessions/{session_id}/events` 提交用户消息（`role: "user"`）；
5. **订阅事件流**：通过 `GET /sessions/{session_id}/events/stream` 建立 SSE 连接，监听 `message`、`tool_call`、`tool_output`、`session_status` 等事件类型。

所有步骤均支持控制台操作与 SDK/API 调用，完整流程参见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)。

## 限制和注意事项

- **文件大小限制**：单个上传文件 ≤ 10 MB（见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）；
- **沙箱隔离性**：挂载资源在会话内为只读副本（写入不影响原始资源），卸载后副本自动清理；
- **会话状态**：会话支持中断与续接，但沙箱容器在会话 `terminated` 后销毁，未持久化的临时文件丢失；
- **工具启用规则**：即使在 `builtin_toolkit` 中声明了工具名，也必须在 `configs` 中显式设置 `"enabled": true`，否则工具不可用；
- **路径硬编码**：所有挂载文件默认位于 `/mnt/session/uploads/` 下，系统提示词中需直接引用该绝对路径（如 `/mnt/session/uploads/report.csv`），不可使用相对路径或环境变量替代。

## 来源文档

- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


