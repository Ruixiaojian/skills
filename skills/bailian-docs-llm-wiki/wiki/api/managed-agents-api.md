# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、沙箱环境、工具执行与事件流。开发者通过 RESTful 接口或 SDK 创建 Agent、Environment、Session 等资源，并以事件驱动方式与智能体交互。所有操作均基于工作空间隔离，需通过 API Key 鉴权。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼托管大模型（详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)），模型 ID 通过 `model.id` 字段指定，不支持自定义模型接入。
- **核心功能模块**：
  - **Agent**：封装模型、系统提示词、技能（Skill）与工具配置；支持版本化管理与软归档，每次更新自动递增 `version` 并采用乐观锁校验 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)。
  - **Environment**：定义沙箱类型（如 `"cloud"`）与预装依赖，独立于 Agent 管理，可被多个 Session 复用；运行中 Session 始终使用创建时绑定的环境快照 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)。
  - **Session**：一次运行实例，绑定 Agent 版本与 Environment 快照，状态机为 `idle → running → idle/terminated`；状态变更通过 SSE 事件流实时推送 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)。
  - **File**：支持上传 ≤20 MB 文件，经安全审核后状态变为 `available` 方可挂载至沙箱或作为消息内容；单工作空间总容量上限 100 GB，保留期 30 天 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)。
  - **Skill**：以 zip 包封装工具组合，上传后需通过安全扫描（状态：`checking` → `active`/`rejected`）；挂载到 Agent 时必须显式指定 `version`，不支持 `latest` 别名 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)。

> **注意**：文档 1 中列出的 `/files` 端点支持 `multipart/form-data` 上传，但文档 6 明确要求单文件上限为 **20 MB**；若文档 1 未说明该限制，以文档 6 为准。

## 关键参数

- **Endpoint**：`https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`，其中 `workspace_id`（如 `ws_xxxxxxxxxxxx`）和 `region`（当前仅支持 `cn-beijing`）为必填。
- **鉴权**：所有请求需在 Header 中携带 `Authorization: Bearer <your-api-key>`。
- **分页参数**：列表接口（如 `/agents`, `/sessions`）支持 `limit`（默认 20，最大 100）和 `page`（首次不传，后续传上一次响应的 `next_page`）。
- **Agent 创建关键字段**：`name`（字符串）、`model.id`（如 `"qwen-plus"`）、`system`（系统提示词）、`skills`（技能 ID 列表，每个需已处于 `active` 状态）。
- **Session 创建关键字段**：`agent`（Agent ID）、`environment_id`（Environment ID）；创建后即进入 `idle` 状态。
- **Event 发送格式**：`POST /sessions/{session_id}/events` 请求体中 `input` 为消息数组，每条消息含 `role`（`user`/`assistant`）、`type`（`message`）、`content`（文本或富媒体数组）。

## 使用方式

1. **初始化**：设置环境变量 `DASHSCOPE_API_KEY` 和 `AGENTSTUDIO_URL`（按工作空间与地域拼装），或通过 SDK 构造 Client（Python SDK ≥ v1.26.2，Java SDK ≥ v2.22.24）[API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。
2. **资源创建**（通常一次性）：
   - 调用 `POST /agents` 创建 Agent；
   - 调用 `POST /environments` 创建 Environment；
3. **会话执行**（每次任务）：
   - 调用 `POST /sessions` 创建 Session（绑定 Agent 与 Environment）；
   - 调用 `POST /sessions/{session_id}/events` 发送用户消息；
   - 调用 `GET /sessions/{session_id}/events/stream` 建立 SSE 连接，监听 `session_status` 变更及 `message` 事件，直至收到 `idle` 或 `terminated`。
4. **SDK 示例**：Python 中使用 `dashscope.agentstudio.Client`，Java 中使用 `AgentStudioClient`，均提供 `agents.create()`、`sessions.create()`、`sessions.events.send()` 和 `sessions.events.stream()` 等高层封装方法 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。

> **注意**：文档 2 的 Bash 示例中 `curl -X POST ... /sessions/{session_id}/events` 发送消息后，需主动调用 `/events/stream` 订阅；而 Python/Java SDK 的 `stream()` 方法内部已处理长连接与自动重连，推荐优先使用 SDK。

## 限制和注意事项

- **地域限制**：API 当前仅支持 `cn-beijing` 地域，其他地域 Endpoint 将返回 404。
- **配额限制**：
  - 单文件上传上限 20 MB，工作空间总存储 100 GB，文件保留期 30 天；
  - Session 事件历史默认保留 7 天（具体策略以控制台为准）；
  - Skill zip 包大小建议 ≤50 MB（虽未明文限制，但过大易导致扫描超时）。
- **状态一致性**：
  - Agent/Environment 更新为全量替换，缺省字段视为清空；已运行的 Session 不受更新影响；
  - File/Skill 上传后需等待 `status` 变为 `available`/`active` 后方可使用，直接引用 `checking` 状态资源将失败。
- **错误处理**：
  - 所有响应含 `x-request-id`，提工单时务必提供；
  - 乐观锁冲突（如 Agent 更新时 `version` 不匹配）返回 HTTP 409；
  - 文件审核失败（`rejected`/`type_rejected`）或 Skill 扫描失败（`rejected`）需检查 `error_info` 字段定位问题。

- **归档行为**：Agent、Environment、Session 的归档均为软操作（记录 `archived_at`），不影响已存在会话，但禁止用于新建会话；删除（`DELETE`）为硬操作，不可恢复。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


