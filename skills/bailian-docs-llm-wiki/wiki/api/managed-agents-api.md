# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，负责会话生命周期管理、沙箱环境调度、工具执行协调与事件流分发。开发者通过 REST 或 SDK 创建 Agent（智能体配置）、Environment（运行沙箱）、Session（运行实例），再以事件驱动方式与 Agent 交互。所有资源均归属工作空间，需通过 API Key 鉴权。

## 支持的模型/功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼平台已开放的推理模型（详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）；模型 ID 在创建 Agent 时通过 `model.id` 字段指定。
- **核心功能**：
  - Agent：封装模型、系统提示词、工具集与 Skill（技能包），支持版本化与归档；
  - Environment：定义沙箱类型（如 `"type": "cloud"`）及预装依赖，可被多个 Session 复用；
  - Session：绑定 Agent 快照与 Environment 快照的运行实例，状态机驱动（`idle` → `running` → `idle`/`terminated`）；
  - Event：支持用户消息、工具调用审批、函数结果回填等原子事件，通过 SSE 流式推送；
  - File：独立文件资源，用于消息内容（图像/音频）或挂载至沙箱供工具读写；
  - Skill：zip 包封装的工具组合，需经安全扫描后挂载到 Agent，挂载时锁定具体版本号。

> **注意**：文档中提及的 `"qwen-plus"` 为当前唯一明确支持的模型 ID，其他模型未在任何原始文档中列出或验证；若尝试使用未声明模型，将返回 400 错误。该限制在 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 和 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中一致，无矛盾。

## 关键参数

| 参数 | 位置 | 说明 | 示例 |
|------|------|------|------|
| `DASHSCOPE_API_KEY` | HTTP Header / 环境变量 | 鉴权凭证，格式 `Bearer <sk-xxx>` | `sk-abc123...` |
| `workspace_id` | Endpoint 路径 | 工作空间 ID，从控制台获取 | `ws_xxxxxxxxxxxx` |
| `region` | Endpoint 路径 | 当前仅支持 `cn-beijing` | `cn-beijing` |
| `agent.model.id` | `POST /agents` 请求体 | 模型 ID，必须为平台支持值 | `"qwen-plus"` |
| `environment.config.type` | `POST /environments` 请求体 | 沙箱类型，当前仅 `"cloud"` 有效 | `"cloud"` |
| `session.agent` & `session.environment_id` | `POST /sessions` 请求体 | Agent ID 与 Environment ID，绑定快照 | `"agent_xxx"`, `"env_xxx"` |
| `event.input` | `POST /sessions/{id}/events` 请求体 | 用户消息数组，遵循 `role`/`type`/`content` 结构 | `[{"role":"user","type":"message","content":[{"type":"text","text":"..."`}]}]` |

## 使用方式

1. **准备环境**：导出 `DASHSCOPE_API_KEY` 与 `AGENTSTUDIO_URL`（形如 `https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`），[详见快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)；
2. **创建基础资源**：
   - 调用 `POST /agents` 创建 Agent（含模型与系统提示）；
   - 调用 `POST /environments` 创建 Environment（指定沙箱类型）；
3. **启动会话**：
   - 调用 `POST /sessions` 绑定 Agent 与 Environment，获得 `session_id`；
4. **交互执行**：
   - 调用 `POST /sessions/{id}/events` 提交用户消息；
   - 调用 `GET /sessions/{id}/events/stream` 建立 SSE 连接，实时接收 `session_status` 变更与消息事件；
5. **可选扩展**：
   - 上传文件（`POST /files`），用于消息内容或挂载至沙箱；
   - 创建并挂载 Skill（`POST /[skill](../guides/skill.md)s` → `POST /agents/{id}` 更新 `[skill](../guides/skill.md)s` 字段）。

SDK 使用需确保版本兼容：Python SDK ≥ v1.26.2，Java SDK ≥ v2.22.24，[安装方法见 API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 限制和注意事项

- **配额限制**：
  - 单文件上传上限 20 MB，工作空间总容量上限 100 GB，文件保留期 30 天（[File](../../raw/application-api-reference/managed-agents-api/files-api.md)）；
  - 列表接口默认 `limit=20`，最大 `limit=100`，支持分页（[API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）；
- **版本与归档**：
  - Agent 与 Environment 更新均为**全量替换**，更新请求体必须携带当前 `version` 作为乐观锁（Agent）或隐式覆盖（Environment）；
  - 归档（`archive`）为软操作，不影响已有 Session，但禁止新建 Session 绑定；
  - 删除（`DELETE /environments/{id}` 或 `/sessions/{id}`）为硬操作，不可恢复；
- **状态与生命周期**：
  - Session 状态变更（`idle`/`running`/`terminated`）仅通过 SSE 事件流通知，**不保证** `GET /sessions/{id}` 实时反映最新状态；
  - 已挂载的 File 或 Skill 版本不受其源资源删除影响；
- **安全约束**：
  - Skill 必须通过安全扫描（`status: active`）后方可挂载，且挂载时必须指定具体 `version`，不支持 `latest`；
  - 文件上传后需等待审核状态变为 `available` 才可使用。

## 来源文档

- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


