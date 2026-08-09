# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，开发者只需关注智能体逻辑本身，无需自行实现代理循环、沙箱编排或事件持久化。其核心抽象包括智能体（Agent）、运行环境（Environment）、会话（Session）和事件（Event）四个层级 [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus` 等 Qwen 系列大模型（具体以控制台下拉列表为准），模型通过 `model.id` 字段指定，如 `"qwen3-max"`。  
- **内置工具集**：默认提供 7 个 `builtin_toolkit` 工具：`bash`（命令执行）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（文件搜索）、`download_file`（URL 下载）。工具启用需显式声明，例如 `{"type": "builtin_toolkit"}` [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)。  
- **扩展能力**：支持挂载 MCP 服务与 Skill 封装的端到端流程；支持通过 `resources` 挂载上传文件（≤10 MB），挂载路径固定为 `/mnt/session/uploads/...`，且副本隔离、生命周期独立于会话 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)。

> **注意**：文档 4 中称“智能体是模型、系统提示词、工具、MCP 服务和技能的组合配置”，但实际创建 API（见文档 1）中 `tools` 字段仅接受工具定义，而 MCP 和 Skill 需在智能体创建后通过独立接口追加，二者并非原子化创建项。建议以 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md) 的 API 示例为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 智能体名称，仅用于标识，不参与执行 |
| `model.id` | string | 是 | 模型 ID，如 `"qwen3-max"`，必须为平台支持的模型 |
| `system` / `instructions` | string | 否（但强烈建议） | 系统提示词，定义角色与行为边界；Java SDK 使用 `instructions`，Python/CLI 使用 `system_prompt` 或 `system`，存在字段名不一致问题 |
| `tools` | array | 否（默认无工具） | 工具配置数组，如 `[{"type": "builtin_toolkit"}]`；空数组即禁用所有工具 |
| `environment_id` | string | 是（会话级） | 运行环境 ID，指向已创建的沙箱配置 |
| `resources` | array | 否 | 资源挂载列表，格式为 `[{"resource_id": "...", "mount_path": "/mnt/session/uploads/data.csv"}]` |

## 使用方式

1. **创建智能体**：调用 `POST /api/v1/agentstudio/agents`，传入 `name`、`model.id`、`system` 和 `tools`；返回 `agent.id` 与 `version`。  
2. **创建运行环境**：调用 `POST /api/v1/agentstudio/environments`，指定 `config.type="cloud"` 及 `packages`（如 `{"pip": ["pandas"]}`）；环境可被多个会话复用 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)。  
3. **创建会话**：调用 `POST /api/v1/agentstudio/sessions`，绑定 `agent` ID 与 `environment_id`，可选传入 `resources` 挂载文件。  
4. **交互**：  
   - 发送用户消息：`POST /sessions/{session_id}/events`，`input` 中包含 `role: "user"` 的 message 事件；  
   - 接收流式响应：`GET /sessions/{session_id}/events/stream`（SSE），监听 `message`、`tool_output`、`session_status` 等事件类型。

## 限制和注意事项

- **沙箱约束**：云端托管环境默认网络受限（`networking.type="restricted"`），如需外网访问（如 `download_file`），必须在环境创建时显式设置 `"networking": {"type": "unrestricted"}`。  
- **文件大小**：上传挂载的单个文件 ≤10 MB；沙箱内生成的临时文件无硬性上限，但受容器资源配额限制。  
- **会话状态**：会话支持中断与续接，但 `session_status` 变为 `terminated` 后不可恢复；`idle` 状态下会话保活 24 小时，超时自动清理。  
- **权限要求**：操作需账号在目标工作空间具备 `ManagedAgentsFullAccess` 或等效自定义权限策略。  
- **调试建议**：预览调试页支持按事件类型筛选（User/Tool/Tool_output/Error），推荐结合 `curl -N` 或 Python `stream()` 实时观察工具调用链路，避免仅依赖最终 `message` 输出。

## 来源文档

- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)


