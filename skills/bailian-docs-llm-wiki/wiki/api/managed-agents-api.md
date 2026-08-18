# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、执行沙箱、工具调用与事件流。开发者通过 RESTful 接口或 SDK 创建 Agent、Environment、Session 等资源，并以事件驱动方式与智能体交互。所有操作均基于工作空间隔离，需通过 API Key 鉴权。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼托管模型，如 `qwen-plus`（见[快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)示例），不支持自定义模型 ID 或外部模型接入。
- **核心功能模块**：
  - `Agent`：封装模型、系统提示词、工具集与技能，支持版本化管理与软归档；
  - `Environment`：定义执行沙箱类型（如 `"type": "cloud"`）与预装依赖，可被多会话复用；
  - `Session`：绑定 Agent 版本与 Environment 快照的运行实例，具备明确状态机（`idle` → `running` → `idle`/`terminated`）；
  - `Event`：会话内原子操作载体，支持用户消息、工具审批、函数回填及 SSE 流式订阅；
  - `File`：独立文件资源，用于消息内容（图像/音频）或挂载至沙箱供工具读写；
  - `Skill`：zip 包封装的工具组合，需经安全扫描后按具体版本号挂载到 Agent。

> **注意**：文档 1 中列出的 `/files` 端点支持 `multipart/form-data` 上传，但文档 5 明确单文件直传上限为 **20 MB**；而文档 1 未提及该限制，实际开发中应以[File](../../raw/application-api-reference/managed-agents-api/files-api.md)为准。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `workspace_id` | 工作空间 ID，控制台右上角获取 | `ws_xxxxxxxxxxxx` | [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) |
| `region` | 地域 ID，当前**仅支持 `cn-beijing`** | `cn-beijing` | [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) |
| `model.id` | Agent 所用模型 ID | `"qwen-plus"` | [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) |
| `environment.config.type` | 沙箱类型，目前仅 `"cloud"` 可用 | `"cloud"` | [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) |
| `version` | Agent/Skill 的乐观锁字段，更新时必须提供当前值 | `1`, `2` | [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)、[Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md) |

## 使用方式

1. **初始化环境**：设置 `DASHSCOPE_API_KEY` 与 `AGENTSTUDIO_URL`（格式为 `https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`）；
2. **创建基础资源**：
   - 调用 `POST /agents` 创建 Agent（含 `model`、`system`）；
   - 调用 `POST /environments` 创建 Environment（含 `config.type`）；
3. **启动会话**：
   - 调用 `POST /sessions` 绑定 Agent 与 Environment，获得 `session_id`；
4. **驱动执行**：
   - 调用 `POST /sessions/{session_id}/events` 发送用户消息（`input` 字段为消息数组）；
   - 调用 `GET /sessions/{session_id}/events/stream` 建立 SSE 连接，监听 `session_status` 与 `content` 事件；
5. **可选扩展**：
   - 上传文件（`POST /files`）后在消息中引用或挂载至沙箱；
   - 创建 Skill 并挂载到 Agent，实现工具调用能力。

SDK 使用需确保版本合规：Python SDK ≥ v1.26.2，Java SDK ≥ v2.22.24（见[API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）。

## 限制和注意事项

- **地域限制**：Endpoint 中 `region` 当前**仅支持 `cn-beijing`**，其他地域返回 404；
- **配额限制**：
  - 单文件上传上限 20 MB，工作空间总容量 100 GB，文件保留期 30 天（见[File](../../raw/application-api-reference/managed-agents-api/files-api.md)）；
  - 分页接口 `limit` 最大为 100，`page` 默认从 1 开始；
- **版本与归档行为**：
  - Agent 更新采用全量替换 + 乐观锁（需带 `version`），失败返回 409；Environment 更新同理但无乐观锁要求；
  - 归档（`archive`）均为软操作，不影响已存在会话；删除（`DELETE`）为硬操作，不可恢复；
- **状态一致性**：
  - Session 状态变更仅通过 SSE `session_status` 事件通知，**不保证 HTTP 响应体中 `status` 字段实时更新**；
  - 已挂载的 Skill 版本不受后续上传影响，挂载时必须显式指定 `version`，不支持 `latest`。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


