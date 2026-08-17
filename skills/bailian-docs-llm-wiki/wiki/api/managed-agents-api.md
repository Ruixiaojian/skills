# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、执行沙箱、工具调用与事件流。开发者通过 RESTful 接口或 SDK 创建和编排 Agent、Environment、Session 等核心资源，实现可复用、可审计、可流式交互的智能体应用。所有操作均基于工作空间隔离，并通过 API Key 鉴权。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼托管大模型（详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)），模型 ID 通过 `model.id` 字段指定，不可自定义外部模型。
- **核心资源**：
  - **Agent**：封装模型、系统提示词、工具集与技能，支持版本化管理（每次更新自动递增 `version`）；
  - **Environment**：定义沙箱类型（如 `"cloud"`）与预装依赖，独立于 Agent 生命周期，可被多会话复用；
  - **Session**：绑定 Agent 版本快照与 Environment 实例的一次运行，状态机驱动（`idle` → `running` → `idle`/`terminated`）；
  - **Event**：会话内原子操作单元，支持用户消息、工具审批、函数回填等，可通过 SSE 流式订阅；
  - **File**：20 MB 单文件上限，上传后需经安全审核（`checking` → `available`），仅 `available` 状态可挂载或作为消息内容；
  - **Skill**：zip 包封装的工具组合，上传后触发安全扫描，挂载到 Agent 时必须显式指定 `version`（不支持 `latest`）。

> **注意**：文档 2 的快速开始示例中使用 `model: "qwen-plus"` 作为字符串传入 Python SDK 的 `create()` 方法，而文档 1 的 REST 示例中使用嵌套对象 `{"id": "qwen-plus"}`。实际 REST 接口要求 `model` 为对象格式（见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)），SDK 将其封装为字符串属正常抽象，但直接调用 REST 时必须遵循对象结构。

## 关键参数

| 参数 | 位置 | 说明 | 示例 |
|------|------|------|------|
| `Authorization` | Header | API Key 鉴权，格式为 `Bearer <your-api-key>` | `Bearer sk-xxx` |
| `workspace_id` | Endpoint 路径 | 工作空间 ID，形如 `ws_xxxxxxxxxxxx` | `ws_abc123` |
| `region` | Endpoint 路径 | 当前仅支持 `cn-beijing` | `cn-beijing` |
| `agent.version` | Agent 更新请求体 | 乐观锁字段，必须与当前版本一致，否则返回 409 | `"version": 3` |
| `environment.config.type` | Environment 创建/更新体 | 沙箱类型，目前仅支持 `"cloud"` | `{"type": "cloud"}` |
| `session_status` | SSE 事件字段 | 会话状态变更通知，取值为 `idle`/`running`/`terminated` | `"session_status": "idle"` |
| `file.status` | File 元数据 | 上传后审核状态，仅 `available` 可用 | `"status": "available"` |

## 使用方式

1. **初始化**：设置环境变量 `DASHSCOPE_API_KEY` 和 `AGENTSTUDIO_URL`（拼接自 `workspace_id` 与 `region`），参考 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)；
2. **创建资源**：
   - 先创建 `Agent`（含模型与系统提示）和 `Environment`（含沙箱配置）；
   - 再调用 `POST /sessions` 绑定二者，获得 `session_id`；
3. **驱动执行**：
   - 向 `POST /sessions/{session_id}/events` 发送用户消息（`input` 字段为消息数组）；
   - 通过 `GET /sessions/{session_id}/events/stream` 建立 SSE 连接，监听 `session_status` 与 `content` 事件；
4. **扩展能力**：
   - 上传文件后，将其 `file_id` 用于 `Skill` 创建或作为消息中的 `file` 类型 content；
   - 将 Skill 版本挂载至 Agent 时，在 Agent 创建/更新体的 `skills` 数组中指定 `{ "skill_id": "...", "version": 1 }`。

## 限制和注意事项

- **地域限制**：Endpoint 中 `region` 当前**仅支持 `cn-beijing`**，其他地域将返回 404（见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）；
- **配额限制**：
  - 单文件直传上限 **20 MB**，工作空间总容量 **100 GB**，文件保留期 **30 天**（见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)）；
  - 分页接口 `limit` 最大为 100，`page` 默认从 1 开始（首次请求可不传）；
- **状态与生命周期**：
  - Agent/Environment/Session 的“归档”均为软操作（写入 `archived_at`），不影响已运行会话；但 Environment 的 `DELETE` 是硬删除，不可恢复；
  - Session 状态变更仅通过 SSE 事件推送，`GET /sessions/{id}` 返回的是查询时刻快照，不保证实时性；
- **版本一致性**：Agent 更新需携带当前 `version` 作乐观锁；Skill 挂载必须指定具体 `version`，上传新版本不影响已挂载的 Agent 行为（见 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)）。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


