# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，负责会话生命周期管理、沙箱环境调度、工具执行协调及事件流分发。开发者通过 REST 或 SDK 创建 Agent（含模型与系统提示）、Environment（运行沙箱）、Session（运行实例），再以事件驱动方式交互。所有资源均支持版本控制、归档与分页查询。

## 支持的模型/功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼托管大模型（详见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 中的端到端示例）；不支持自定义模型 ID 或外部模型接入。
- **核心功能模块**：
  - **Agent**：封装模型、系统提示词、工具列表与 Skill 挂载配置；每次更新生成新版本，会话创建时锁定快照 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)。
  - **Environment**：定义沙箱类型（如 `"type": "cloud"`）与预装依赖，独立于 Agent 管理，可被多会话复用 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)。
  - **Skill**：以 zip 包形式封装工具组合，上传后需通过安全扫描（状态为 `active` 才可挂载），挂载时必须指定具体版本号，不支持 `latest` 别名 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)。
  - **File**：作为消息内容（图像/音频）或沙箱挂载文件使用；单文件上限 20 MB，审核状态为 `available` 后方可引用。

> **注意**：文档 2 的 API 总览中列出 `/skills/{skill_id}/versions/{version}/download` 端点返回 OSS 预签名 URL，但文档 7 明确说明该接口路径为 `/skills/{skill_id}/versions/{version}/content`（非 `/download`）。实际应以文档 7 的 `GET /skills/{skill_id}/versions/{version}/content` 为准。

## 关键参数

- **认证参数**：全部请求需在 Header 中携带 `Authorization: Bearer <your-api-key>`，API Key 须归属目标工作空间。
- **Endpoint 构造**：`https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`，其中 `region` 当前仅支持 `cn-beijing`。
- **Agent 创建参数**：
  - `model.id`：必需，如 `"qwen-plus"`；
  - `system`：必需，系统提示词字符串；
  - `skills`：可选，数组，每个元素为 `{ "id": "skl_xxx", "version": 1 }`。
- **Environment 创建参数**：`config.type` 必需，取值 `"cloud"`（云沙箱）或 `"local"`（暂未开放）。
- **Session 创建参数**：`agent`（Agent ID）与 `environment_id`（Environment ID）均为必需字段。
- **Event 发送参数**：`input` 为消息数组，每条消息需含 `role`（`"user"` 或 `"assistant"`）、`type`（`"message"`）、`content`（文本或富媒体数组）。

## 使用方式

1. **初始化**：导出 `DASHSCOPE_API_KEY` 与 `AGENTSTUDIO_URL` 环境变量（见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)）；
2. **资源准备**（通常一次性）：
   - 调用 `POST /agents` 创建并复用 Agent；
   - 调用 `POST /environments` 创建并复用 Environment；
   - （可选）调用 `POST /files` 上传文件，待 `status="available"` 后使用；
   - （可选）调用 `POST /skills` 创建 Skill 并上传版本，待 `status="active"` 后挂载至 Agent；
3. **会话执行**（按需高频）：
   - 调用 `POST /sessions` 绑定 Agent 与 Environment，获取 `session_id`；
   - 调用 `POST /sessions/{session_id}/events` 提交用户消息；
   - 调用 `GET /sessions/{session_id}/events/stream` 建立 SSE 连接，监听 `session_status`（`idle`/`running`/`terminated`）及 `message` 事件；
4. **SDK 接入**：Python SDK v1.26.2+ 与 Java SDK v2.22.24+ 已完整封装上述流程，推荐优先使用（见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 中的 SDK 示例）。

## 限制和注意事项

- **配额限制**：单文件直传 ≤ 20 MB；工作空间总文件容量 ≤ 100 GB；文件保留期 30 天，超期可能被自动清理（见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)）。
- **状态机约束**：
  - Session 状态为 `idle` 时才可接收新事件；`running` 状态下重复提交事件将被拒绝；
  - `terminated` 为终态，不可恢复；归档操作（`POST /sessions/{session_id}/archive`）会将其置为 `terminated`。
- **版本与快照**：
  - Agent 更新采用乐观锁，请求体必须包含当前 `version` 字段，否则返回 409；
  - Environment 更新不影响已绑定会话，其内部使用绑定时刻的快照；
  - Skill 新版本上传不影响已挂载旧版本的 Agent。
- **安全性**：
  - File 与 Skill 均需通过安全审核（`checking` → `available`/`active`），未通过者不可使用；
  - 所有工具调用均在隔离沙箱中执行，禁止访问宿主机或网络（除非显式配置白名单）。
- **调试建议**：所有响应头含 `x-request-id`，提工单时务必提供，便于平台侧快速定位问题。

## 来源文档

- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


