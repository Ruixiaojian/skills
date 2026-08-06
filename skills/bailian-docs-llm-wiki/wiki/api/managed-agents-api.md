# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，支持创建、配置和运行可复用的 Agent 实例，并通过 Session 驱动状态机执行任务。API 采用 RESTful 设计，配合 SSE 事件流实现低延迟结果推送，适用于需要长期运行、工具调用与沙箱隔离的智能体应用。所有资源（Agent、Environment、Session 等）均按工作空间隔离，支持版本控制与软归档。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼托管大模型（详见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 中的端到端示例），不支持自定义模型或外部模型接入。
- **核心功能模块**：
  - **Agent**：封装模型、系统提示词、技能（Skill）与工具包；支持多版本管理与乐观锁更新，会话创建时锁定快照版本 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)。
  - **Environment**：定义执行沙箱类型（如 `"type": "cloud"`）及预装依赖，独立于 Agent 生命周期，可被多个 Session 复用 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)。
  - **Skill**：以 ZIP 包形式上传工具组合，需经安全扫描后方可挂载；挂载时必须指定具体 `version`，不支持 `latest` 别名 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)。
  - **File**：支持 ≤20 MB 的文件直传，用于消息内容（如图像）或挂载至沙箱；上传后进入 `checking` 审核态，仅 `available` 状态可使用。

> **注意**：文档 3 中列出 `PATCH /agents/{agent_id}` 为更新端点，但文档 2 明确说明更新接口为 `POST /agents/{agent_id}` 且采用全量替换语义。实际应以文档 2 的 `POST` 方式为准，`PATCH` 属过时描述。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `DASHSCOPE_API_KEY` | Header | string | 是 | `Authorization: Bearer <key>`，用于鉴权 |
| `workspace_id` | Endpoint path | string | 是 | 工作空间 ID（如 `ws_xxxxxxxxxxxx`），参与构造 `AGENTSTUDIO_URL` |
| `model.id` | Agent 创建请求体 | string | 是 | 模型 ID，当前仅支持 `qwen-plus` 等白名单模型 |
| `environment.config.type` | Environment 创建请求体 | string | 是 | 沙箱类型，目前仅支持 `"cloud"` |
| `session.agent` / `session.environment_id` | Session 创建请求体 | string | 是 | 分别为 Agent ID 与 Environment ID，绑定快照 |
| `events.input` | Event 发送请求体 | array | 是 | 符合 OpenAI-style 的 message 数组，`role` 仅支持 `"user"`（工具回执由平台自动注入） |

## 使用方式

完整调用流程分五步，需严格顺序执行：

1. **创建 Agent**：调用 `POST /agents`，指定 `model`、`system` 提示词及可选 `skills`；返回 `agent_id` 与初始 `version=1`。
2. **创建 Environment**：调用 `POST /environments`，`config.type="cloud"` 为唯一有效值。
3. **创建 Session**：调用 `POST /sessions`，传入 `agent` 和 `environment_id`，获得 `session_id`，初始状态为 `idle`。
4. **发送 Event**：调用 `POST /sessions/{session_id}/events`，提交用户消息（`input` 字段），触发状态转为 `running`。
5. **订阅 SSE 流**：调用 `GET /sessions/{session_id}/events/stream`，监听 `session_status`（`idle`/`running`/`terminated`）及 `message` 事件，直至收到终态。

SDK 使用需确保版本合规：Python SDK ≥ v1.26.2，Java SDK ≥ v2.22.24（见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)）。

## 限制和注意事项

- **配额限制**：单文件 ≤20 MB；工作空间总存储 ≤100 GB；文件保留期 30 天，超期可能被自动清理（见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)）。
- **状态与生命周期**：
  - Agent/Environment 归档为软操作（`archived_at` 记录时间），不影响已有 Session；删除 Environment 为硬操作，不可恢复。
  - Session 状态机严格遵循 `idle → running → idle/terminated`，`terminated` 为终态，仅可通过 `DELETE` 清除历史。
- **版本与兼容性**：
  - Agent 更新需携带当前 `version` 值作乐观锁，失败返回 409；已创建 Session 始终使用创建时的快照版本。
  - Skill 版本上传后需等待 `status=active` 才可挂载，挂载后即使新版本发布也不影响已绑定 Agent。
- **安全约束**：Skill ZIP 包必须通过安全扫描（`checking → active/rejected`），`rejected` 状态详情中提供具体风险路径；未审核通过的 Skill 不可挂载。

## 来源文档

- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


