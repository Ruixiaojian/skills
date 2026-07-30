# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、[文件处理](../concepts/file-processing.md)等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主运行命令、读写文件、安装依赖，并通过持久化的事件流反馈全过程。开发者只需关注 Agent 逻辑与任务编排，无需自行实现代理循环、沙箱编排或工具调度基础设施。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（详见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）；模型 ID 需严格匹配平台已发布版本，不支持自定义模型镜像。
- **核心功能**：
  - 工具调用：内置 `bash`、`read`、`write`、`edit`、`glob`、`grep`、`download_file` 7 类工具，默认全启用；
  - MCP 服务接入：可挂载外部工具服务（[构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md) 中说明其为可选配置）；
  - Skill 封装：支持预置技能组合，用于端到端流程抽象；
  - [文件处理](../concepts/file-processing.md)：支持上传挂载（单文件 ≤10 MB）、URL 下载、沙箱内读写编辑（[Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md) 明确路径约定为 `/mnt/session/uploads/...`）。

> **注意**：文档 2 中称“支持命令执行、文件操作、MCP 服务、Skill”，而文档 3 和文档 4 均未明确列出具体工具集；实际可用工具以 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 中列出的 7 个内置工具为准，该文档为最新且具操作性，应作为权威参考。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model.id` | string | 是 | 模型 ID，如 `"qwen3-max"`；不支持别名或版本通配符 |
| `system` / `system_prompt` | string | 是 | 系统提示词，定义角色与行为边界；控制台预填通用模板，API 创建时需显式传入 |
| `tools` | array | 否（默认全启用） | 工具配置数组，最小粒度为 `{"type": "builtin_toolkit"}`；暂不支持按单个工具启停（如仅启用 `bash` 而禁用 `grep`） |
| `environment_id` | string | 是（创建 Session 时） | 运行环境 ID，指向独立托管的沙箱容器（[配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md) 强调其复用性） |
| `resources` | array | 否 | 挂载资源列表，含 `resource_id` 与 `mount_path`；挂载后路径固定为 `/mnt/session/uploads/...` |

## 使用方式

1. **创建智能体**：通过控制台向导或 API 指定名称、模型、系统提示词和工具（[快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 提供完整示例）；
2. **创建环境**：配置云端沙箱类型、预装包（`apt`/`pip`）、网络策略（`unrestricted` 或 `restricted`）；
3. **创建会话**：绑定智能体 ID 与环境 ID，可同时指定 `resources` 挂载文件；
4. **发送事件**：使用 `POST /sessions/{id}/events` 提交用户消息（`role: "user"`），内容支持[多模态](../concepts/multi-modal.md)块（text、file_ref 等）；
5. **接收响应**：通过 SSE 流订阅 `/sessions/{id}/events/stream`，监听 `message`、`tool_call`、`tool_output`、`session_status` 等事件类型。

## 限制和注意事项

- **会话生命周期**：单次会话最长运行 2 小时，超时自动终止；可通过 `session_status` 事件监听 `idle` 或 `terminated` 状态；
- **文件限制**：上传挂载文件单个 ≤10 MB，总挂载容量无明确上限但受工作空间配额约束；
- **环境复用**：一个 Environment 可被多个 Session 复用，但同一 Session 仅能绑定一个 Environment；
- **工具执行隔离**：所有工具调用均在沙箱内执行，`bash` 命令无法访问宿主机，`write`/`edit` 仅作用于 `/mnt/session/` 下路径；
- **上下文持久化**：会话内文件系统状态跨事件保持，但 Session 终止后沙箱销毁，副本不保留；
- **权限要求**：调用方账号需在目标工作空间具备 `AgentStudioFullAccess` 或等效细粒度权限（[快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 明确前置权限条件）。

## 来源文档

- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)




