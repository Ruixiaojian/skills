# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、执行沙箱、工具调用与事件流。开发者通过 RESTful 接口或 SDK 创建 Agent（智能体配置）、Environment（运行环境）、Session（运行实例）等资源，并以事件驱动方式与智能体交互。所有操作均基于工作空间隔离，需通过 API Key 鉴权。

## 支持的模型与功能

- **模型支持**：Agent 创建时通过 `model.id` 指定模型，当前支持 `qwen-plus` 等百炼托管大模型（详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中的 Endpoint 说明）。
- **核心资源**：
  - `Agent`：封装模型、系统提示词、工具集与技能，支持版本化管理与软归档；
  - `Environment`：定义沙箱类型（如 `"cloud"`）与预装依赖，可被多 Session 复用；
  - `Session`：绑定 Agent 快照与 Environment 实例的一次运行，状态机驱动（`idle` → `running` → `idle`/`terminated`）；
  - `File`：独立文件资源，用于消息内容（图像/音频）或挂载至沙箱供工具读写；
  - `Skill`：zip 包封装的工具组合，需经安全扫描后按具体版本号挂载到 Agent。

> **注意**：文档 2 的快速开始示例中使用 `model: "qwen-plus"` 作为字符串，而文档 1 的 API 总览中 `model` 字段结构为 `{"id": "qwen-plus"}`。实际请求体必须遵循文档 1 的嵌套对象格式，否则将返回 400 错误 —— 请以 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中的字段定义为准。

## 关键参数

| 参数 | 位置 | 说明 | 示例 |
|------|------|------|------|
| `Authorization` | Header | API Key 鉴权，格式为 `Bearer <your-api-key>` | `Bearer sk-xxx` |
| `workspace_id` | Endpoint 路径 | 工作空间 ID，形如 `ws_xxxxxxxxxxxx` | `ws_abcd1234` |
| `region` | Endpoint 路径 | 当前仅支持 `cn-beijing` | `cn-beijing` |
| `agent.version` | Agent 更新请求体 | 乐观锁字段，更新时必须携带当前版本号，不一致返回 409 | `"version": 3` |
| `file_id` | File/Skill 相关接口 | 上传文件后返回的唯一 ID，用于创建 Skill 或挂载至 Session | `file_abc123` |
| `session_status` | SSE 事件流 | 事件对象中的字段，用于监听会话状态变更（如 `"idle"`、`"running"`） | 见 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md) |

## 使用方式

1. **初始化**：设置环境变量 `DASHSCOPE_API_KEY` 和 `AGENTSTUDIO_URL`（拼接自 `workspace_id` 与 `region`），或通过 SDK 构造 Client；
2. **资源准备**：
   - 创建 Agent（含 `model`, `system`, 可选 `skills`）；
   - 创建 Environment（指定 `config.type`，如 `"cloud"`）；
   - （可选）上传 File 并等待 `status: "available"`，再用于 Skill 创建或消息内容；
   - （可选）创建 Skill 并上传版本，待 `status: "active"` 后挂载至 Agent；
3. **运行会话**：
   - `POST /sessions` 绑定 Agent 与 Environment，获取 `session_id`；
   - `POST /sessions/{session_id}/events` 发送用户消息（`input` 字段为消息数组，支持 `text`/`image_url`/`file_id` 等类型）；
   - `GET /sessions/{session_id}/events/stream` 建立 SSE 连接，实时接收 `session_status` 与 `output` 事件；
4. **清理**：可对 Session、Environment、Skill 执行归档（软删除）或删除（硬删除），File 删除不影响已挂载副本。

SDK 调用需确保版本兼容：Python SDK ≥ v1.26.2，Java SDK ≥ v2.22.24 —— 具体要求见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 限制和注意事项

- **配额限制**：
  - 单文件上传上限 **20 MB**，工作空间总容量 **100 GB**，文件保留期 **30 天**（[File](../../raw/application-api-reference/managed-agents-api/files-api.md)）；
  - 分页接口 `limit` 最大值为 100，`page` 从 1 开始（首次请求可省略）；
- **状态与生命周期**：
  - Agent/Environment/Session 归档均为**软操作**，不影响已运行的会话；但归档后不可用于新建会话（[Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)、[Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)、[Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)）；
  - Environment 删除为**硬操作**，不可恢复；Skill 删除将清除其所有版本，但已挂载旧版本的 Agent 不受影响；
- **安全约束**：
  - File 与 Skill 均需通过安全审核（`checking` → `available`/`active`），仅审核通过后方可使用；
  - Skill 挂载到 Agent 时**必须指定具体 version**，不支持 `latest` 别名；
- **版本一致性**：
  - Session 创建时锁定 Agent 的 `version` 与 Environment 的快照，后续更新不影响该 Session；
  - Agent 更新采用全量替换语义，请求体必须包含当前 `version` 值用于乐观锁校验。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


