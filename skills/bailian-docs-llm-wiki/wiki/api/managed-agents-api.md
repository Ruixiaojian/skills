# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，负责会话生命周期管理、沙箱环境调度、工具执行协调与事件流分发。开发者通过 REST 或 SDK 创建 Agent（智能体配置）、Environment（执行沙箱）、Session（运行实例），并以事件驱动方式交互。所有资源均归属工作空间，需通过 API Key 鉴权。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼托管大模型（详见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 中的端到端示例）。模型 ID 作为 `agent.model.id` 字段传入，不支持自定义模型或外部模型接入。
- **核心功能**：
  - Agent：封装模型、系统提示词、工具列表与 Skill（技能包）；支持版本化与归档，每次更新自动递增 `version` 并采用乐观锁校验 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)。
  - Environment：定义沙箱类型（如 `"type": "cloud"`）与预装依赖；支持软归档与硬删除，已绑定会话使用创建时的快照 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)。
  - Session：绑定 Agent 版本与 Environment 快照，状态机驱动（`idle` → `running` → `idle`/`terminated`）；支持事件注入与 SSE 流式订阅 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)。
  - File：支持 ≤20 MB 文件直传，审核通过后（`status: "available"`）可挂载至沙箱或作为消息内容 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)。
  - Skill：以 ZIP 包形式上传，经安全扫描后方可挂载；挂载时必须指定具体 `version`，不支持 `latest` 别名 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)。

> **注意**：文档 2 中列出的 `/skills/{skill_id}/versions/{version}/download` 端点返回 OSS 预签名 URL，但实际调用需额外鉴权（非仅 API Key），该细节未在原始文档中明确说明，建议优先使用 SDK 封装的下载方法。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `DASHSCOPE_API_KEY` | Header / 环境变量 | string | 是 | 认证凭据，格式 `Bearer <key>` |
| `workspace_id` | Endpoint 路径 | string | 是 | 工作空间 ID（如 `ws_xxxxxxxxxxxx`），拼入 Base URL |
| `region` | Endpoint 路径 | string | 是 | 当前仅支持 `cn-beijing` |
| `agent.model.id` | `POST /agents` 请求体 | string | 是 | 模型 ID，例如 `"qwen-plus"` |
| `environment.config.type` | `POST /environments` 请求体 | string | 是 | 沙箱类型，目前仅 `"cloud"` 可用 |
| `session.agent` & `session.environment_id` | `POST /sessions` 请求体 | string | 是 | 分别为 Agent ID 与 Environment ID |
| `event.input` | `POST /sessions/{id}/events` 请求体 | array | 是 | 消息数组，每个元素含 `role`（`"user"`）、`type`（`"message"`）、`content`（含 `text` 或 `file_id`） |

## 使用方式

1. **初始化**：设置 `DASHSCOPE_API_KEY` 和 `AGENTSTUDIO_URL`（形如 `https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`）[快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。
2. **创建资源**（建议复用）：
   - 创建 Agent：指定 `model.id`、`system` 提示词、可选 `skills` 列表；
   - 创建 Environment：指定 `config.type`（`"cloud"`）及可选依赖；
   - 创建 Session：绑定 Agent 与 Environment，返回 `session_id`。
3. **交互**：
   - 发送事件：`POST /sessions/{id}/events`，传入 `input` 数组；
   - 订阅结果：`GET /sessions/{id}/events/stream`，监听 `session_status` 与 `content` 事件。
4. **SDK 推荐**：Python SDK ≥ v1.26.2，Java SDK ≥ v2.22.24；直接调用 REST 时需严格遵循 JSON 格式与分页参数（`limit`/`page`）[API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 限制和注意事项

- **配额限制**：单文件 ≤20 MB；工作空间总存储 ≤100 GB；文件保留期 30 天，超期可能被清理 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)。
- **状态一致性**：Agent 更新后新会话使用新版，旧会话仍锁定原 `version`；Environment 更新不影响已绑定会话；Skill 新版本上传后，已挂载旧版本的 Agent 不受影响。
- **安全约束**：Skill 必须通过安全扫描（`status: "active"`）才可挂载；File 上传后需等待 `status: "available"` 才能使用。
- **错误处理**：所有响应含 `x-request-id`，提工单时必须提供；Agent 更新失败常见于 `version` 乐观锁冲突（HTTP 409）。
- **地域限制**：Endpoint 仅支持 `cn-beijing`，其他地域暂不可用。

## 来源文档

- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


