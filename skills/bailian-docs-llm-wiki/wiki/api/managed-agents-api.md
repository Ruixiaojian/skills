# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、执行沙箱、工具调用与事件流。开发者通过 RESTful 接口或 SDK 创建 Agent、Environment、Session 等核心资源，并以事件驱动方式与智能体交互。所有请求需通过 API Key 鉴权，基地址按工作空间与地域动态拼装。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼托管模型，如 `qwen-plus`（见[快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)示例），不支持 BYOM（Bring Your Own Model）。
- **核心功能模块**：
  - **Agent**：定义模型、系统提示词、工具包与技能挂载；支持版本化（每次更新自动递增 `version`），会话创建时锁定快照 [原文标题](../../raw/application-api-reference/managed-agents-api/agent-api.md)。
  - **Environment**：定义执行沙箱类型（如 `"type": "cloud"`）与预装依赖；环境可被多个 Session 复用，更新为全量替换，已绑定会话不受影响 [原文标题](../../raw/application-api-reference/managed-agents-api/environment-api.md)。
  - **Skill**：以 ZIP 包封装工具组合，上传后需通过安全扫描（状态为 `active` 方可挂载）；挂载时必须指定具体 `version`，不支持 `latest` [原文标题](../../raw/application-api-reference/managed-agents-api/skills-api.md)。
  - **File**：支持上传图像、音频、文本等文件（单文件 ≤20 MB），用于消息内容或挂载至沙箱；上传后进入安全审核，仅 `available` 状态可被引用。
  - **Session & Event**：Session 是 Agent 在 Environment 中的一次运行实例，状态机为 `idle` → `running` → `idle`/`terminated`；Event 为原子操作单元（用户消息、工具回填、中断等），支持同步发送与 SSE 流式订阅。

> **注意**：文档 1 中列出的 `/files/{file_id}/download` 端点在文档 7 中未提及，且实际响应结构与常规文件下载不一致；请以文档 7 的 `GET /files/{file_id}/versions/{version}/content`（返回预签名 URL）为准，该端点用于 Skill 包下载，非通用文件下载。

## 关键参数

| 资源 | 关键字段 | 说明 |
|------|----------|------|
| **Agent** | `model.id` | 必填，如 `"qwen-plus"`；不支持模型别名或自定义 endpoint |
| | `system` / `system_prompt` | 系统提示词字段名在 Python SDK 中为 `system_prompt`，REST API 中为 `system`（见[快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)与[Agent API](../../raw/application-api-reference/managed-agents-api/agent-api.md)差异） |
| | `version` | 更新时必传，用作乐观锁；409 表示版本冲突 |
| **Environment** | `config.type` | 当前仅支持 `"cloud"`，其他值将导致 400 错误 |
| **Session** | `agent`（REST） / `agent_id`（SDK） | REST 请求体中为 `agent: "agent_xxx"`，SDK 参数名为 `agentId` |
| | `environment_id` | 必填，绑定环境快照 |
| **Event** | `input`（数组） | 每个元素为 `{role: "user", type: "message", content: [...]}`；`content` 内容项支持 `text`、`image_url`、`file_id` 等类型 |
| **File** | `file_id` | 上传后返回，用于 Skill 创建、消息引用或沙箱挂载 |

## 使用方式

1. **认证与初始化**  
   设置环境变量 `DASHSCOPE_API_KEY` 和工作空间 ID，Endpoint 格式为 `https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`（`region` 固定为 `cn-beijing`）。

2. **典型调用链路**（按顺序执行）  
   - 创建 Agent（`POST /agents`）→ 获取 `agent_id`  
   - 创建 Environment（`POST /environments`）→ 获取 `environment_id`  
   - 创建 Session（`POST /sessions`，传入 `agent` 和 `environment_id`）→ 获取 `session_id`  
   - 发送 Event（`POST /sessions/{session_id}/events`）触发执行  
   - 订阅 SSE（`GET /sessions/{session_id}/events/stream`）接收[流式输出](../concepts/streaming-output.md)，监听 `session_status` 变更  

3. **SDK 适配要点**  
   - Python SDK v1.26.2+、Java SDK v2.22.24+ 为必需版本（见[API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）  
   - Python 中 `Client.agents.create()` 接受 `model="qwen-plus"` 字符串；REST 则需 `{"id": "qwen-plus"}` 对象  
   - 所有列表接口支持 `limit`（1–100）和 `page` 分页，响应含 `next_page` 字段指示是否还有下一页  

## 限制和注意事项

- **配额限制**：单文件 ≤20 MB；工作空间总文件容量 ≤100 GB；文件保留期 30 天，超期可能被自动清理（见[File](../../raw/application-api-reference/managed-agents-api/files-api.md)）。
- **状态与生命周期**：
  - Agent、Environment、Session 的“归档”均为软操作（保留数据，不可新建会话/环境/Session），而“删除”为硬操作（不可恢复）。
  - Environment 更新不影响已绑定的运行中 Session；Agent 更新后新 Session 自动使用新版，旧 Session 仍锁定原 `version`。
- **安全约束**：
  - File 与 Skill 上传后均需通过安全扫描，状态非 `available` 或 `active` 时不可使用。
  - Skill 挂载到 Agent 时必须指定 `version`，且该版本必须为 `active`；后续上传新版本不影响已挂载的 Agent。
- **错误处理**：所有响应含 `x-request-id`，提工单时务必提供；版本冲突返回 HTTP 409；无效模型 ID 或环境配置返回 HTTP 400。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)


