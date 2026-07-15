# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，负责会话生命周期管理、沙箱环境调度、工具执行协调与事件流分发。开发者通过 REST 或 SDK 创建 Agent（智能体配置）、Environment（执行沙箱）、Session（运行实例），并以事件驱动方式与 Agent 交互。所有资源均归属工作空间，支持版本控制、软归档与细粒度权限隔离。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼托管大模型（详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)），不支持自定义模型或外部模型接入。
- **核心功能**：
  - Agent：封装模型、系统提示词、工具列表与 Skill 挂载，支持版本化与软归档；
  - Environment：定义沙箱类型（如 `"type": "cloud"`）及预装依赖，独立于 Agent 管理，可被多 Session 复用；
  - Session：绑定 Agent 版本快照与 Environment 快照，状态机驱动（`idle` → `running` → `idle`/`terminated`）；
  - Event：支持用户消息、工具调用审批、函数结果回填等原子事件，通过 SSE 流式推送；
  - File：支持 ≤20 MB 文件直传，审核通过后（`status: "available"`）可作为消息内容或挂载至沙箱；
  - Skill：以 zip 包形式封装工具组合，需经安全扫描后按具体版本号挂载到 Agent。

> **注意**：文档中多次提及 `"qwen-plus"` 为示例模型，但 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档未明确列出当前支持的全部模型 ID；实际可用模型请以控制台或 `/agents` 创建接口返回的 `model.id` 枚举为准，避免硬编码。

## 关键参数

| 参数 | 位置 | 说明 | 示例 |
|------|------|------|------|
| `DASHSCOPE_API_KEY` | Header | 鉴权凭证，格式 `Bearer <key>` | `sk-xxx` |
| `workspace_id` | Endpoint 路径 | 工作空间 ID，用于构造 Base URL | `ws_xxxxxxxxxxxx` |
| `region` | Endpoint 路径 | 当前仅支持 `cn-beijing` | `cn-beijing` |
| `agent.model.id` | Agent 创建请求体 | 模型 ID，必须为平台支持的托管模型 | `"qwen-plus"` |
| `environment.config.type` | Environment 创建请求体 | 沙箱类型，目前仅 `"cloud"` 可用 | `"cloud"` |
| `session.agent` / `session.environment_id` | Session 创建请求体 | 引用已创建的 Agent ID 与 Environment ID | `"agent_xxx"`, `"env_xxx"` |
| `event.input` | Event 发送请求体 | 用户消息数组，遵循 OpenAI-style message 格式 | `[{"role":"user","content":[{"type":"text","text":"..."}]}]` |

## 使用方式

1. **环境准备**：导出 `DASHSCOPE_API_KEY` 与 `AGENTSTUDIO_URL`（形如 `https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`），[详见快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)；
2. **资源创建**（建议复用）：
   - 创建 Agent：指定 `model.id`、`system` 提示词、可选 `skills` 列表；
   - 创建 Environment：指定 `config.type` 及其他沙箱参数；
3. **会话交互**：
   - 创建 Session，绑定 Agent 与 Environment；
   - `POST /sessions/{id}/events` 发送用户消息触发执行；
   - `GET /sessions/{id}/events/stream` 建立 SSE 连接，监听 `session_status` 与 `message` 事件；
4. **SDK 推荐**：Python SDK ≥ v1.26.2，Java SDK ≥ v2.22.24（[API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中明确要求）。

## 限制和注意事项

- **配额限制**：单文件上传上限 20 MB，工作空间总存储上限 100 GB，文件保留期 30 天（[File](../../raw/application-api-reference/managed-agents-api/files-api.md)）；
- **版本锁定**：Session 创建时锁定 Agent 的 `version` 与 Environment 快照，后续更新不影响已有 Session；
- **归档非删除**：Agent/Environment/Session 归档为软操作（`archived_at` 字段填充），已归档资源仍可查询，但不可用于新建 Session；
- **硬删除风险**：`DELETE /environments/{id}` 或 `DELETE /sessions/{id}` 为不可逆操作，将彻底清除配置或事件历史；
- **SSE 连接**：客户端需处理连接中断重试，并根据 `session_status` 事件判断会话终态（`idle` 或 `terminated`），避免无限等待；
- **Skill 安全约束**：Skill 必须通过安全扫描（`status: "active"`）才可挂载，且挂载时必须指定具体 `version`，不支持 `latest` 动态引用。

## 来源文档

- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


