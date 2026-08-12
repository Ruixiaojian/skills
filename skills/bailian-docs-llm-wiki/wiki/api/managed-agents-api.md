# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、沙箱环境、工具执行与事件流。开发者通过 REST API 或 SDK 创建 Agent、Environment、Session 等资源，并以事件驱动方式与智能体交互。所有请求需通过 API Key 鉴权，基地址按工作空间与地域动态生成。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼托管大模型（详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中的示例），不支持自定义模型或外部模型接入。
- **核心功能模块**：
  - `Agent`：定义模型、系统提示词、技能挂载；支持版本化与软归档（[Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)）。
  - `Environment`：配置工具执行沙箱（如 `"type": "cloud"`），支持预装依赖；独立于 Agent 管理，可被多 Session 复用（[Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)）。
  - `Session`：绑定 Agent 与 Environment 的运行实例，状态机驱动（`idle` → `running` → `idle`/`terminated`）（[Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)）。
  - `Skill`：以 ZIP 包封装工具组合，上传后需安全扫描，挂载时必须指定具体版本号（[Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)）。
  - `File`：支持上传图像、音频、文本等文件，用于消息内容或沙箱挂载；单文件上限 20 MB，审核通过后状态为 `available` 才可使用（[File](../../raw/application-api-reference/managed-agents-api/files-api.md)）。

> **注意**：文档 2 的快速开始示例中使用 `"model": "qwen-plus"` 字符串形式，而文档 1 的 API 总览中 `POST /agents` 请求体示例写为 `"model": {"id": "qwen-plus"}`。实际接口要求为对象格式 `{"id": "qwen-plus"}`，字符串形式将导致 400 错误 —— 请以 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中的结构为准。

## 关键参数

| 参数 | 位置 | 说明 | 示例 |
|------|------|------|------|
| `Authorization` | Header | API Key 鉴权，格式为 `Bearer <your-api-key>` | `Bearer sk-xxx` |
| `workspace_id` | Endpoint 路径 | 工作空间 ID，形如 `ws_xxxxxxxxxxxx` | `ws_abc123def456` |
| `region` | Endpoint 路径 | 当前仅支持 `cn-beijing` | `cn-beijing` |
| `agent.id` & `environment_id` | `POST /sessions` 请求体 | Session 必须显式绑定 Agent ID 与 Environment ID | `"agent": "agent_xxx", "environment_id": "env_yyy"` |
| `version` | `PATCH /agents/{id}` 请求体 | Agent 更新需携带当前 `version` 值作为乐观锁 | `"version": 3` |
| `limit` / `page` | 查询类端点 Query | 分页参数，默认 `limit=20`，最大 `limit=100`；`page` 从 1 开始 | `?limit=50&page=2` |

## 使用方式

1. **准备环境**：开通百炼，创建 API Key 并设为 `DASHSCOPE_API_KEY` 环境变量；获取工作空间 ID 和地域（仅 `cn-beijing`）。
2. **创建基础资源**：
   - 调用 `POST /agents` 创建 Agent（含 `model.id`、`system` 等）；
   - 调用 `POST /environments` 创建 Environment（如 `{"type": "cloud"}`）；
   - （可选）上传文件 `POST /files`，待状态变为 `available` 后用于消息或挂载。
3. **启动会话**：
   - 调用 `POST /sessions` 绑定 Agent 与 Environment，获得 `session_id`；
   - 调用 `POST /sessions/{session_id}/events` 发送用户消息（`input` 字段为消息数组）；
   - 调用 `GET /sessions/{session_id}/events/stream` 订阅 SSE 流，监听 `session_status` 变更及输出事件。
4. **SDK 推荐**：Python SDK v1.26.2+ 或 Java SDK v2.22.24+，提供 `Client.agents.create()`、`client.sessions.events.stream()` 等封装方法（见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)）。

## 限制和注意事项

- **地域限制**：Endpoint 仅支持 `cn-beijing`，其他地域请求将返回 404（[API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）。
- **配额限制**：
  - 单文件上传上限 20 MB，工作空间总容量 100 GB，文件保留期 30 天（[File](../../raw/application-api-reference/managed-agents-api/files-api.md)）；
  - 列表接口 `limit` 最大值为 100，超出将被截断。
- **状态与生命周期**：
  - Agent、Environment、Skill 的“归档”均为软操作，不影响已存在的 Session；但归档后不可用于新建 Session（[Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)、[Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)、[Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)）；
  - Session 删除（`DELETE /sessions/{id}`）为硬删除，事件历史不可恢复；
  - Skill 新版本上传后需等待 `status` 变为 `active` 才能挂载，`rejected` 状态需根据 `error_info` 修复后重传。
- **版本锁定**：Session 创建时锁定 Agent 当前版本；Skill 挂载必须指定具体 `version`，不支持 `latest`（[Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)）。
- **事件语义**：`POST /sessions/{id}/events` 仅用于注入事件（用户消息、中断、工具回填等），不触发执行；执行由平台自动驱动，结果通过 SSE 流推送。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)


