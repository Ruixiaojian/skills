# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步[工具调用](../concepts/tool-use.md)、代码执行、文件处理等长时运行任务设计。平台在服务端统一托管会话状态、沙箱环境与工具执行生命周期，支持事件历史持久化与 SSE 流式订阅。开发者可聚焦于 Agent 逻辑本身，无需自行实现代理循环、沙箱编排或工具执行基础设施，详见 [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（具体列表以控制台下拉菜单为准），模型通过 `model.id` 字段指定。
- **核心功能**：
  - 多步自主[工具调用](../concepts/tool-use.md)（bash、read、write、edit、glob、grep、download_file）
  - 沙箱内代码执行（支持 apt/pip 包安装、网络访问配置）
  - 文件系统操作（挂载上传文件、URL 下载、读写编辑）
  - MCP 服务与 Skill 集成（可选扩展）
  - 会话级上下文保持（含挂载资源隔离副本）

> **注意**：文档 1 示例中使用 `qwen3.7-plus` 作为模型 ID，而文档 2 的“支持的工具”部分未明确列出模型兼容性；实际可用模型请以控制台实时下拉选项或 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 页面为准，避免硬编码过期 ID。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 智能体名称，仅用于标识，不参与执行逻辑 |
| `model.id` | string | 是 | 模型 ID，如 `"qwen3-max"`，必须为平台支持的模型 |
| `system` / `instructions` | string | 是 | 系统提示词，定义角色与行为边界（SDK 差异见下文） |
| `tools` | array | 否（默认全启用内置工具） | 如 `[{"type": "builtin_toolkit"}]`，禁用需显式传空数组 |
| `environment_id` | string | 创建 Session 时必填 | 运行环境 ID，指向独立托管的沙箱容器 |
| `resources` | array | 否 | 挂载资源列表，格式为 `[{ "id": "res_xxx", "mount_path": "/mnt/session/uploads/data.csv" }]` |

> **注意**：Python SDK 使用 `system_prompt` 参数，Java SDK 使用 `instructions`，Bash API 使用 `system` 字段 —— 三者语义一致但命名不统一，需按 SDK 文档适配，详见 [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)。

## 使用方式

1. **创建智能体**：配置模型、系统提示词与工具（[快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 提供控制台向导与 API 示例）。
2. **创建运行环境**：定义云端沙箱类型、预装包（apt/pip）、网络策略（[配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)）。
3. **发起会话**：绑定智能体 ID 与环境 ID，可同时挂载资源（[委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)）。
4. **交互与监控**：
   - 发送用户消息事件（`role: user`, `type: message`）
   - 订阅 SSE 事件流（`/sessions/{id}/events/stream`），监听 `message`、`tool_call`、`tool_output`、`session_status` 等事件类型
   - 调试时可通过控制台“预览调试”标签页实时筛选事件类型

## 限制和注意事项

- **文件大小限制**：单个上传挂载文件 ≤ 10 MB（[Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。
- **沙箱隔离性**：同一资源挂载到多个会话时，各会话获得独立副本；会话内修改不影响原始资源或其他会话。
- **会话生命周期**：会话无活跃事件超 2 小时自动终止（`session_status: terminated`），不可续接；需新建会话继续任务。
- **[工具调用](../concepts/tool-use.md)范围**：内置工具仅限沙箱内执行，无法访问宿主机或外部私有网络（除非环境配置 `networking.type: unrestricted` 且白名单放行）。
- **权限要求**：操作前需确保账号在目标工作空间具备 `ManagedAgentsFullAccess` 或等效自定义权限。

## 来源文档

- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)


