# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，负责会话生命周期管理、沙箱环境调度、工具执行协调与事件流分发。开发者通过 REST 或 SDK 创建 Agent（智能体配置）、Environment（执行沙箱）、Session（运行实例），并以事件驱动方式与 Agent 交互。所有资源均归属工作空间，支持版本控制、软归档与细粒度权限隔离。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼托管大模型（详见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 中的端到端示例）。模型 ID 需在创建 Agent 时显式指定，不支持动态切换。
- **核心功能**：
  - Agent：支持系统提示词、工具绑定、Skill 挂载（需指定具体版本号）；每次更新生成新版本，会话创建时锁定快照 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)。
  - Environment：定义沙箱类型（如 `"type": "cloud"`）与预装依赖；运行中会话使用绑定时刻的快照，更新不影响已有会话 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)。
  - Session：状态机驱动（`idle` → `running` → `idle`/`terminated`），支持消息注入、中断、工具审批回填等事件类型 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)。
  - File：支持上传 ≤20 MB 文件，用于消息内容或挂载至沙箱；审核通过后状态为 `available` 方可引用 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)。
  - Skill：以 ZIP 包封装工具，上传后需通过安全扫描（状态 `active` 才可挂载）；挂载时必须指定精确 `version`，不支持 `latest` 别名 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)。

> **注意**：文档 2 中“可用 API”表格将 `/skills/{skill_id}/versions/{version}/download` 的路径写为 `/skills/{skill_id}/versions/{version}/download`，但文档 7 明确其实际端点为 `/skills/{skill_id}/versions/{version}/content`（返回预签名 URL）。以文档 7 为准。

## 关键参数

| 参数 | 位置 | 说明 | 示例 |
|------|------|------|------|
| `DASHSCOPE_API_KEY` | Header | 鉴权凭证，格式 `Bearer <key>` | `Authorization: Bearer sk-xxx` |
| `workspace_id` | Endpoint | 工作空间 ID，拼入 base URL | `ws_xxxxxxxxxxxx.cn-beijing.maas.aliyuncs.com` |
| `agent.id` & `environment_id` | `POST /sessions` body | 创建 Session 必填，绑定快照 | `{"agent": "agent_xxx", "environment_id": "env_xxx"}` |
| `version` | `PATCH /agents/{id}` body | Agent 更新时必需的乐观锁字段 | `"version": 3`（当前版本） |
| `file_id` | `POST /skills` 或消息 content | 文件资源标识符，仅 `status=available` 时有效 | `"file_id": "file_xxx"` |

## 使用方式

1. **环境准备**：导出 `DASHSCOPE_API_KEY` 和 `AGENTSTUDIO_URL`（按 `https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio` 拼接）[快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。
2. **资源创建**（顺序不可逆）：
   - 创建 Agent（含模型、system [prompt](../guides/prompt.md)、[skill](../guides/skill.md)s 列表）
   - 创建 Environment（指定沙箱类型及依赖）
   - 创建 Session（绑定 agent + environment）
3. **交互流程**：
   - `POST /sessions/{id}/events` 提交用户消息（`user_message`）或工具回执；
   - `GET /sessions/{id}/events/stream` 建立 SSE 连接，监听 `session_status` 变更及 `message` 事件；
   - 当 `session_status` 变为 `idle` 或 `terminated` 时结束流式消费。
4. **SDK 调用**：Python SDK 要求 ≥v1.26.2，Java SDK ≥v2.22.24；旧版本需强制升级 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 限制和注意事项

- **配额限制**：单文件 ≤20 MB；工作空间总存储 ≤100 GB；文件保留期 30 天，超期可能被自动清理 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)。
- **状态约束**：
  - 归档（archive）为软操作，已归档的 Agent/Environment/Session 不可用于新建会话，但已存在的会话不受影响；
  - 删除（DELETE）为硬操作，对应资源及关联数据（如 Environment 删除、Session 删除）不可恢复；
  - Session 状态变更仅通过 SSE 推送，`GET /sessions/{id}` 返回的是查询时刻快照，非实时状态。
- **版本与快照**：Agent 更新后 `version` 自增，但已有 Session 仍运行旧版本；Environment 更新不影响已绑定会话的运行时快照 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 和 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)。
- **安全要求**：Skill ZIP 包必须通过安全扫描（`status=active`）才可挂载；File 上传后需等待 `status=available` 才能使用。

## 来源文档

- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


