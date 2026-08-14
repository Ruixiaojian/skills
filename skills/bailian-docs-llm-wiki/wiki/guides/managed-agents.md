# managed agents

Managed Agents 是百炼平台提供的托管式智能体运行时，专为多步工具调用、代码执行、文件处理等长时有状态任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，开发者只需关注智能体逻辑配置，无需自行实现代理循环、沙箱编排或事件持久化。其核心抽象包括智能体（Agent）、运行环境（Environment）、会话（Session）和事件（Event）四层结构，支持通过控制台或 API 全流程管理。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（见[快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)），模型 ID 需在创建智能体时显式指定；模型调用费用按实际 token 消耗单独计费，不包含在会话运行时费中。
- **内置工具集**：默认提供 7 个内置工具：`bash`（命令执行）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（文件搜索）、`download_file`（URL 下载）。所有工具均在独立沙箱中执行，支持读写挂载路径 `/mnt/session/uploads/` 下的文件。
- **扩展能力**：支持接入 MCP 服务与 Skill（预置工具组合），用于封装外部系统调用或端到端工作流（见[概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)）。

> **注意**：文档 1 中示例使用 `qwen3.7-plus` 和 `qwen3-max`，但文档 7 的计费示例中仅提及 `qwen-plus`。实际可用模型以控制台下拉列表或 [模型服务目录](https://help.aliyun.com/zh/model-studio/model-list) 为准，`qwen3.*` 系列为新版模型，`qwen-plus` 为旧版，二者计费标准不同，请勿混用模型 ID。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 智能体唯一标识名，创建后不可修改 |
| `model.id` | string | 是 | 模型 ID，如 `"qwen3-max"`；必须为百炼已开通的模型 |
| `system` / `system_prompt` | string | 是 | 系统提示词，定义角色与行为边界；影响工具调用合理性 |
| `tools` | array | 否 | 工具配置数组，`[{"type": "builtin_toolkit"}]` 表示启用全部内置工具；也可按需指定单个工具对象 |
| `environment_id` | string | 是（创建 Session 时） | 运行环境 ID，决定沙箱类型、预装包与网络策略 |
| `resources` | array | 否（创建 Session 时） | 挂载资源列表，格式为 `[{"id": "res_xxx", "mount_path": "/mnt/session/uploads/data"}]`；详见[Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md) |

## 使用方式

1. **创建智能体**：通过控制台向导或 API 提交 `name`、`model.id`、`system` 和 `tools`；智能体 ID 创建后全局唯一，可复用于多个会话。
2. **创建运行环境**：配置沙箱类型（目前仅支持 `"cloud"`）、预装包（`apt`/`pip` 列表）与网络策略（如 `"unrestricted"`）；环境可被多个会话共享。
3. **创建会话**：绑定智能体 ID 与环境 ID，可选挂载资源；会话启动即开始计费（按小时精确计费）。
4. **交互与流式消费**：
   - 发送用户事件：使用 `POST /sessions/{id}/events` 提交 `input` 数组（含 `role: "user"` 的消息）；
   - 接收响应：通过 SSE 流 `GET /sessions/{id}/events/stream` 实时消费 `message`、`tool_output`、`session_status` 等事件类型；
   - 会话支持中断与续接：发送新事件可覆盖当前执行路径，状态与文件系统在会话生命周期内持续存在。

## 限制和注意事项

- **文件限制**：上传挂载的单个文件 ≤ 10 MB；所有挂载资源副本存放于 `/mnt/session/uploads/`，路径需在系统提示词中显式引用。
- **会话生命周期**：会话处于 `running` 状态即产生运行时费（0.5 元/小时），空闲不计费；务必调用 `terminate` 接口或在控制台手动终止不再使用的会话。
- **资源隔离性**：同一资源挂载至多个会话时，各会话获得独立副本，互不影响；卸载后副本自动清理，原始资源保留。
- **权限要求**：操作前需确保账号在目标工作空间具备 `Managed Agents` 相关 RAM 权限（见[快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）。
- **计费生效时间**：自 2026-08-17 09:00:00（UTC+8）起正式商业化，赠送 10 小时免费额度，有效期 30 天。

## 来源文档

- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [计费](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)


