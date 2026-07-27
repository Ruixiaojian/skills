# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并支持事件历史持久化与中断续接。相比无状态的智能体应用，Managed Agents 本质是服务端有状态的会话级执行引擎。

## 支持的模型与功能

- **模型支持**：支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 示例），模型通过 `model.id` 字段指定，需确保工作空间已开通对应模型权限。
- **核心功能**：
  - 命令执行（`bash`）：在沙箱中运行 shell 命令；
  - 文件操作（`read`/`write`/`edit`/`glob`/`grep`/`download_file`）：支持挂载文件、路径搜索、内容编辑；
  - MCP 服务接入：对接外部工具服务；
  - Skill 封装：复用预置端到端任务流程（如数据清洗、报告生成）；
  - 网络访问：默认受限，可通过环境配置 `networking.type: unrestricted` 开放（见 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)）。

> **注意**：文档 2 的快速开始示例中使用 `qwen3-max`，而文档 1 的概述表格中列出 `qwen3.7-plus` 作为示例模型；实际可用模型以控制台下拉列表或 [API 模型列表接口](https://help.aliyun.com/zh/model-studio/model-list) 为准，二者均有效，无矛盾。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `agent.id` | 智能体唯一标识，创建后复用于多个会话 | `"agent_xxx"` | [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md) |
| `environment_id` | 运行环境 ID，决定沙箱类型、预装包与网络策略 | `"env_xxx"` | [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) |
| `resources` | 创建会话时挂载的资源列表，含文件 ID 与目标路径 | `[{"id": "file_abc", "path": "/mnt/session/uploads/data.csv"}]` | [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md) |
| `input[].content[].text` | 用户消息文本，触发智能体启动执行 | `"分析 /mnt/session/uploads/sales.csv 中 Q3 的销售趋势"` | [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) |

## 使用方式

1. **创建智能体**：通过控制台向导或 API 配置模型、系统提示词与启用的工具（如 `bash`, `read`, `write`）。工具启用需显式声明 `enabled: true`（见 [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)）。
2. **配置运行环境**：独立创建沙箱环境，指定 `type: "cloud"`、预装包（`apt`/`pip`）及网络策略。环境可被多个会话复用。
3. **发起会话**：绑定智能体 ID 与环境 ID，可选挂载资源（文件上传后获得 `file_id`，按 `/mnt/session/uploads/xxx` 路径引用）。
4. **交互与监控**：
   - 发送用户事件：`POST /sessions/{session_id}/events`，携带 `role: "user"` 消息；
   - 订阅 SSE 流：`GET /sessions/{session_id}/events/stream`，监听 `message`、`tool_output`、`session_status` 等事件类型；
   - 实时干预：在会话运行中发送新 `user` 事件可引导方向，或调用中断接口终止当前任务。

## 限制和注意事项

- **文件大小限制**：单个上传文件 ≤ 10 MB（见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）；
- **沙箱隔离性**：挂载文件在会话内为副本，修改不影响原始资源与其他会话，卸载后副本自动清理；
- **会话生命周期**：会话状态包括 `idle`、`running`、`terminated`，`terminated` 后不可恢复，需新建会话；
- **工具调用超时**：`bash` 命令默认超时 60 秒，`download_file` 默认 300 秒，不可自定义调整；
- **凭证安全**：MCP 服务或外部工具所需的 API Key 等敏感信息，必须通过 [凭证管理](../../raw/application-user-guide/managed-agents/managed-agents-environment.md) 统一注入，禁止硬编码于系统提示词中。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


