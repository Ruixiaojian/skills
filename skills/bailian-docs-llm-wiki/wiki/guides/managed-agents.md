# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、[文件处理](../concepts/file-processing.md)等长时、有状态任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，开发者只需关注智能体逻辑配置，无需自行实现代理循环、沙箱编排或状态持久化。其核心差异在于服务端维护会话级上下文与文件系统状态，支持中断续接和 SSE 事件流式观测，区别于无状态的智能体应用模式（详见[概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)）。

## 支持的模型与功能

- **模型支持**：支持百炼全量推理模型（如 `qwen3-max`、`qwen3.7-plus`），模型选择在创建智能体时指定，调用时按实际 token 消耗计费（独立于运行时费）。
- **内置工具集**：默认提供 7 个基础工具：`bash`（命令执行）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（文件搜索）、`download_file`（URL 下载）。所有工具均在隔离沙箱中执行。
- **扩展能力**：
  - **MCP 服务**：通过标准 MCP 协议接入外部工具服务；
  - **Skill**：复用预置的端到端任务封装（如数据清洗、PDF 解析）；
  - **挂载资源**：支持上传文件并挂载至 `/mnt/session/uploads/` 路径，供智能体直接读取（详见[Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。

> **注意**：文档 4 中快速开始示例使用 `{"type": "builtin_toolkit"}` 表示启用全部内置工具，但该字段实际为占位符；真实 API 创建时需显式列出工具对象（如 `{"type": "bash"}`），否则工具将不生效。请以 [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md) 文档的字段定义为准。

## 关键参数

| 参数 | 说明 | 是否必需 | 示例 |
|------|------|----------|------|
| `name` | 智能体名称，用于控制台识别 | 是 | `"data-analyst"` |
| `model.id` | 模型 ID，必须为百炼已开通模型 | 是 | `"qwen3-max"` |
| `system` / `system_prompt` | 系统提示词，定义角色与行为约束 | 是 | `"你是数据分析专家，使用 pandas 处理 CSV 文件。"` |
| `tools` | 工具列表，每个元素为 `{ "type": "bash" }` 等结构 | 否（但无工具则无法执行操作） | `[{"type": "bash"}, {"type": "read"}]` |
| `environment_id` | 运行环境 ID，决定沙箱配置（如预装包、网络策略） | 创建会话时必需 | `"env_xxx"` |
| `resources` | 挂载资源列表，含 `resource_id` 和 `mount_path` | 否（仅需挂载文件时设置） | `[{"resource_id": "res_xxx", "mount_path": "/mnt/session/uploads/sales.csv"}]` |

## 使用方式

1. **创建智能体**：通过控制台向导或 API 配置模型、系统提示词与工具。智能体创建后生成唯一 ID，可被多个会话复用（[构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)）。
2. **配置运行环境**：独立创建沙箱环境（如预装 `pandas`、`ffmpeg`），支持 `apt`/`pip` 包管理及网络策略配置。环境亦可复用（[配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)）。
3. **发起会话**：绑定智能体 ID 与环境 ID 创建会话实例；可选挂载文件资源。
4. **交互与监控**：
   - 发送用户消息事件（`role: user`, `type: message`）触发执行；
   - 通过 SSE 流订阅实时事件（`message`, `tool_output`, `session_status` 等类型）；
   - 支持运行中发送新事件干预流程，或调用终止接口结束会话。

## 限制和注意事项

- **会话生命周期**：会话处于 `running` 状态即开始计费（0.5 元/小时），空闲（`idle`）状态不计费；务必及时终止不再使用的会话（[计费](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)）。
- **文件限制**：单次上传挂载文件 ≤ 10 MB；挂载后路径固定为 `/mnt/session/uploads/` 下，智能体需在系统提示词中明确引用完整路径。
- **沙箱隔离性**：每个会话拥有独立沙箱，挂载文件为副本，修改不影响原始资源或其他会话。
- **超时控制**：SSE 流建议设置 `timeout`（如 120 秒），避免长连接阻塞；会话无自动超时机制，需主动管理。
- **权限要求**：调用 API 前需确保账号在目标工作空间具备 `Managed Agents` 操作权限。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [计费](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


