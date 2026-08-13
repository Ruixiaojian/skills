# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、执行沙箱、工具调用与事件流。开发者通过 REST 或 SDK 创建 Agent（智能体配置）、Environment（运行环境）、Session（执行实例）等资源，并以事件驱动方式与智能体交互。所有操作均基于工作空间隔离，需通过 API Key 鉴权。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台已发布的模型，如 `qwen-plus`；模型 ID 作为 `Agent` 创建/更新时的必填字段（见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）。  
- **核心功能模块**：
  - `Agent`：定义模型、系统提示词、工具集与技能挂载，支持版本化与软归档（见 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)）；
  - `Environment`：声明沙箱类型（如 `"cloud"`）与预装依赖，独立于 Agent 管理，可被多 Session 复用（见 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)）；
  - `Session`：绑定 Agent 版本快照与 Environment 实例，驱动状态机（`idle` → `running` → `idle`/`terminated`），是任务执行的最小单元（见 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)）；
  - `File`：支持上传 ≤20 MB 文件，用于消息内容（图像/音频）或挂载至沙箱供工具读写；文件需审核为 `available` 状态后方可使用（见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)）；
  - `Skill`：以 zip 包封装工具组合，上传后经安全扫描，仅 `active` 状态版本可挂载到 Agent；挂载时必须指定精确 `version`，不支持 `latest`（见 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)）。

> **注意**：文档 1 中列出的 `/skills/{skill_id}/versions/{version}/download` 端点返回的是 OSS 预签名 URL，但文档 7 的说明中将其路径误写为 `/content`，正确路径应为 `/download`（与端点表格一致）。请以 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md) 文档中的端点表格为准。

## 关键参数

- **Endpoint 基地址**：`https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`，其中 `workspace_id`（如 `ws_xxxxxxxxxxxx`）和 `region`（当前仅支持 `cn-beijing`）为必需拼接项（见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）。
- **鉴权**：全部请求须在 Header 中携带 `Authorization: Bearer <your-api-key>`。
- **分页参数**：列表接口（如 `/agents`, `/sessions`）支持 `limit`（默认 20，最大 100）与 `page`（首次不传，后续传上一次响应的 `next_page`）。
- **Agent 版本控制**：更新 Agent 时请求体必须包含当前 `version` 字段用于乐观锁校验；创建 Session 时自动锁定该 Agent 当前版本，后续 Agent 更新不影响已有 Session（见 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)）。
- **Event 输入格式**：向 `/sessions/{session_id}/events` 发送用户消息时，`input` 字段为消息数组，每条消息需含 `role`（`user`）、`type`（`message`）及 `content`（文本/文件引用等）。

## 使用方式

1. **初始化**：设置环境变量 `DASHSCOPE_API_KEY` 和 `AGENTSTUDIO_URL`（含 workspace_id 与 region），或通过 SDK 构造 Client（Python SDK ≥ v1.26.2，Java SDK ≥ v2.22.24）（见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 和 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)）。
2. **资源创建**（通常一次性）：
   - 创建 `Agent`（指定 `model`, `system` 等）；
   - 创建 `Environment`（指定 `config.type`，如 `"cloud"`）；
3. **会话执行**（每次任务）：
   - 调用 `POST /sessions` 绑定 Agent 与 Environment，获取 `session_id`；
   - 调用 `POST /sessions/{session_id}/events` 提交用户消息；
   - 调用 `GET /sessions/{session_id}/events/stream` 建立 SSE 连接，监听 `session_status` 变更与 `message` 事件，直至收到 `idle` 或 `terminated`。
4. **文件与技能集成**：
   - 先上传文件（`POST /files`），待其 `status` 变为 `available` 后，可在消息 `content` 中引用，或在 `Environment` 配置中挂载；
   - 技能需先上传 zip 包为 `File`，再用该 `file_id` 创建 `Skill`，扫描为 `active` 后，方可挂载到 Agent 的 `skills` 列表中并指定 `version`。

## 限制和注意事项

- **地域限制**：API 当前仅支持 `cn-beijing` 地域，其他 region 将返回错误（见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）。
- **文件限制**：单文件直传上限 20 MB；工作空间总容量上限 100 GB；文件保留期 30 天，超期可能被自动清理（见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)）。
- **环境删除风险**：`DELETE /environments/{environment_id}` 为硬删除，不可恢复；而归档（`POST /environments/{environment_id}/archive`）为软操作，已绑定的运行中 Session 仍可继续使用（见 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)）。
- **状态终态不可逆**：Session 归档后进入 `terminated` 终态，无法重启；若需新执行，必须创建新 Session（见 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)）。
- **SDK 版本要求**：Python SDK 必须 ≥ v1.26.2，Java SDK 必须 ≥ v2.22.24；旧版本不支持 Managed Agents 模块（见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 和 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)）。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


