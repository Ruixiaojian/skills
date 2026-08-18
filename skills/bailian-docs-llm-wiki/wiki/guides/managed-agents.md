# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时、有状态任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，开发者只需关注智能体逻辑配置，无需自行编排代理循环或维护沙箱基础设施。其核心差异在于服务端持久化事件历史、支持中断续接的会话模型，以及隔离的云端容器执行环境。

## 支持的模型与功能

- **模型支持**：支持百炼全系列大模型（如 `qwen3-max`、`qwen3.7-plus` 等），模型由智能体配置指定，调用时按实际 token 消耗计费（详见[计费](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)）。
- **内置工具**：默认提供 7 个基础工具：`bash`（命令执行）、`read`/`write`/`edit`（文件读写编辑）、`glob`/`grep`（文件搜索）、`download_file`（URL 下载）。所有工具均在沙箱内安全执行。
- **扩展能力**：
  - **MCP 服务**：通过 MCP 协议接入外部工具服务；
  - **Skill**：复用预置的端到端任务流程封装；
  - **文件挂载**：支持上传文件或从 URL 下载，并以只读副本形式挂载至 `/mnt/session/uploads/` 路径下，单文件 ≤10 MB（参见[Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)）。

> **注意**：文档 4 中快速开始示例使用 `"tools": [{"type": "builtin_toolkit"}]` 的简写方式，而文档 1 明确列出具体工具名称；实际 API 接受两种形式，但推荐显式声明工具列表（如 `["bash", "read", "write"]`）以提升可维护性与调试清晰度。

## 关键参数

创建各资源时需关注以下核心参数：

| 资源类型 | 必填参数 | 说明 |
|----------|----------|------|
| **Agent** | `name`, `model.id`, `system`, `tools` | `model.id` 必须为百炼已开通的模型 ID；`tools` 可为工具名称数组或 `{"type": "builtin_toolkit"}`；`system` 用于定义角色与行为约束 |
| **Environment** | `name`, `config.type` | `config.type` 当前仅支持 `"cloud"`（云端托管沙箱）；`config.packages` 可指定 `apt`/`pip` 预装包；`config.networking.type` 可设为 `"unrestricted"` 或 `"restricted"` |
| **Session** | `agent`, `environment_id`, `title` | `agent` 为智能体 ID（非名称）；`environment_id` 为环境 ID；`title` 仅用于标识，不影响执行 |

## 使用方式

遵循“Agent → Environment → Session”三级创建顺序：

1. **创建 Agent**：通过控制台向导或 API 定义模型、系统提示词与工具组合。例如 Python SDK：
   ```python
   agent = client.agents.create(
       name="data-analyst",
       model="qwen3-max",
       system_prompt="你是数据分析专家，使用 pandas 处理 CSV 文件。",
       tools=["bash", "read", "write", "edit", "glob", "grep"],
   )
   ```

2. **创建 Environment**：独立于 Agent 创建沙箱环境，支持复用。例如预装数据分析依赖：
   ```python
   env = client.environments.create(
       name="data-sandbox",
       config={
           "type": "cloud",
           "packages": {"pip": ["pandas", "numpy", "matplotlib"]},
           "networking": {"type": "unrestricted"},
       },
   )
   ```

3. **创建 Session**：绑定 Agent 与 Environment，可选挂载资源（文件）：
   ```python
   session = client.sessions.create(
       agent=agent.id,
       environment_id=env.id,
       title="Q3 销售数据分析",
       # resources=[{"id": "res_xxx", "mount_path": "/mnt/session/uploads/sales.csv"}]
   )
   ```

4. **交互与流式消费**：向会话发送用户消息，通过 SSE 流接收事件（`message`、`tool_call`、`tool_output`、`session_status` 等）：
   ```python
   client.sessions.events.send(session.id, events=[user_message("分析 /mnt/session/uploads/sales.csv")])
   with client.sessions.events.stream(session.id) as stream:
       for event in stream:
           if event.type == "message":
               print(event.content[0].text)
   ```

完整流程可参考 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 中的控制台向导与各语言 SDK 示例。

## 限制和注意事项

- **会话生命周期**：会话处于 `running` 状态即开始计费（0.5 元/小时），空闲（`idle`）不计费；务必调用 `terminate` 显式终止不再使用的会话。
- **沙箱隔离性**：每个会话拥有独立沙箱，挂载文件为副本，修改不影响原始资源或其他会话；卸载后副本自动清理。
- **网络与依赖**：沙箱默认禁用外网访问（`networking.type: "restricted"`），如需调用公网 API 或下载远程资源，必须在 Environment 中显式配置 `"networking": {"type": "unrestricted"}`。
- **文件路径约定**：所有挂载文件统一位于 `/mnt/session/uploads/` 下，系统提示词与工具调用中应直接引用该绝对路径。
- **事件持久化**：所有事件（含用户输入、工具调用、模型输出、错误）在服务端持久化，可通过 API 查询历史，但 SSE 流仅推送实时事件。

> **注意**：文档 7 明确计费起始时间为 2026-08-17 09:00:00（UTC+8），此前为免费试用期；开发者需确认工作空间开通时间及额度有效期，避免产生意外账单。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [计费](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)


