# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时、有状态任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，开发者只需关注智能体逻辑配置，无需自行编排代理循环或维护沙箱基础设施。其核心差异在于服务端持久化事件历史、支持中断续接的会话模型，以及隔离的云端容器执行环境（详见[概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)）。

## 支持的模型与功能

- **模型支持**：支持百炼全系列大模型（如 `qwen3-max`、`qwen3.7-plus` 等），模型由智能体配置指定，调用时按实际 token 消耗计费（不含在运行时费中）。
- **内置工具集**：默认提供 7 个基础工具：`bash`（命令执行）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（文件搜索）、`download_file`（URL 下载）。所有工具均在沙箱内受限执行。
- **扩展能力**：
  - **MCP 服务**：可接入外部工具服务，通过 MCP 协议标准化集成；
  - **Skill**：预置封装的端到端任务流程（如数据清洗、PDF 解析），可挂载复用；
  - **文件挂载**：支持上传本地文件或通过 URL 下载，挂载至 `/mnt/session/uploads/` 路径供智能体访问（单文件 ≤10 MB）（详见[Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。

> **注意**：文档 3 中快速开始示例使用 `{"type": "builtin_toolkit"}` 表示启用全部内置工具，但该字段名未在 API 文档中明确定义；实际创建 Agent 时应显式传入工具列表（如 `[{ "type": "bash" }, { "type": "read" }]`），避免依赖模糊别名。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model.id` | string | 是 | 模型 ID（如 `"qwen3-max"`），决定推理能力与计费模型 |
| `system` / `system_prompt` | string | 否（但强烈建议） | 系统提示词，定义智能体角色、行为边界与工具使用规范 |
| `tools` | array | 否（默认为空） | 工具配置数组，每个元素为 `{ "type": "bash" }` 等结构 |
| `environment_id` | string | 是（创建会话时） | 运行环境 ID，决定沙箱类型、预装包与网络策略 |
| `resources` | array | 否 | 挂载资源列表，格式为 `[{"id": "res_xxx", "mount_path": "/mnt/session/uploads/data.csv"}]` |

环境配置关键字段：
- `config.type`: `"cloud"`（当前唯一支持类型）
- `config.packages`: 支持 `apt`（Debian 包）、`pip`（Python 包）安装列表
- `config.networking.type`: `"unrestricted"`（允许外网访问）或 `"restricted"`（仅限内网）

## 使用方式

1. **创建智能体**：通过控制台向导或 API 配置模型、系统提示词与工具。智能体创建后生成唯一 ID，可被多个会话复用（详见[构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)）。
2. **创建运行环境**：独立于智能体配置沙箱，支持预装依赖（如 `pandas`, `ffmpeg`）和网络策略。同一环境可被多个会话共享。
3. **发起会话**：绑定智能体 ID 与环境 ID，可选挂载资源（文件）。会话启动后即进入 `running` 状态并开始计费。
4. **交互与流式消费**：
   - 发送用户消息：调用 `/sessions/{session_id}/events` 接口提交 `input` 数组；
   - 接收事件流：通过 SSE 订阅 `/sessions/{session_id}/events/stream`，监听 `message`、`tool_output`、`session_status` 等事件类型；
   - 中断或干预：在会话运行中发送新 `user` 事件可覆盖当前任务流。

## 限制和注意事项

- **会话生命周期**：会话处于 `running` 状态即产生运行时费用（0.5 元/小时），空闲不计费；务必及时调用终止接口释放资源。
- **沙箱隔离性**：每个会话拥有独立沙箱，挂载文件为副本，修改不影响原始资源或其他会话（详见[Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。
- **计费解耦**：费用分为三部分独立结算——会话运行时费、模型 token 费、工具/MCP 调用费。免费额度（10 小时）仅抵扣运行时费，有效期 30 天。
- **文件路径约束**：所有挂载文件强制位于 `/mnt/session/uploads/` 下，系统提示词中需使用完整路径引用（如 `/mnt/session/uploads/report.pdf`），不可硬编码其他路径。
- **超时控制**：SSE 流默认超时 120 秒，长任务需在客户端设置合理 timeout 并处理重连逻辑。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [计费](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)


