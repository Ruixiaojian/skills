# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、执行沙箱、工具调用与事件流。开发者通过 REST 或 SDK 创建 Agent（智能体配置）、Environment（运行环境）、Session（运行实例）并驱动交互，无需自行维护模型推理、沙箱隔离或状态同步。所有请求需通过工作空间专属 Endpoint 和 API Key 鉴权。

## 支持的模型与功能

- **模型支持**：Agent 创建时通过 `model.id` 指定，当前支持 `qwen-plus` 等百炼托管大模型（具体列表见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）。
- **核心资源**：覆盖 Agent（含版本控制与归档）、Environment（沙箱类型与依赖配置）、Session（状态机驱动的运行实例）、File（20 MB 以内直传文件，用于消息内容或沙箱挂载）及 Skill（zip 封装的工具包，需安全扫描后挂载）五大类资源。
- **交互模式**：支持同步事件提交（`POST /sessions/{session_id}/events`）与异步 SSE 流式订阅（`GET /sessions/{session_id}/events/stream`），实时接收 `session_status` 变更与工具执行结果。

## 关键参数

| 参数 | 位置 | 说明 | 示例 |
|------|------|------|------|
| `Authorization` | Header | 必填，Bearer [Token](../concepts/token.md) 格式，值为 API Key | `Bearer sk-xxx` |
| `workspace_id` | Endpoint 路径 | 工作空间 ID，拼入 Base URL | `ws_xxxxxxxxxxxx` |
| `region` | Endpoint 路径 | 当前仅支持 `cn-beijing` | `cn-beijing` |
| `version` | Agent 更新请求体 | 乐观锁字段，更新时必须携带当前版本号，成功后自动 +1；[Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档明确要求该字段用于并发控制 |
| `file_id` | Skill/File 相关请求体 | 文件上传后返回的唯一 ID，用于 Skill 创建或 Session 消息引用 | `file_xxx` |
| `limit` / `page` | 查询参数 | 分页控制，`limit` 默认 20、最大 100；`page` 首次不传，后续传 `next_page` 值 | `?limit=50&page=2` |

> **注意**：文档 3（快速开始）中示例使用 `system_prompt` 字段创建 Agent，但文档 2（Agent）和文档 1（API 总览）均明确使用 `system` 字段；实际请求体应以 `system` 为准，`system_prompt` 为过时别名，SDK 可能已做兼容映射，但原始 REST 接口仅接受 `system`。

## 使用方式

1. **初始化**：设置环境变量 `DASHSCOPE_API_KEY` 和 `AGENTSTUDIO_URL`（格式为 `https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`），详见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。
2. **资源创建**：
   - 先创建 `Agent`（定义模型、系统提示、技能）和 `Environment`（定义沙箱类型如 `"cloud"`）；
   - 再创建 `Session`，绑定二者 ID，获得 `session_id`。
3. **任务执行**：
   - 向 `POST /sessions/{session_id}/events` 提交用户消息（`input` 字段为消息数组，支持 `text`/`image`/`file` 类型）；
   - 通过 `GET /sessions/{session_id}/events/stream` 建立 SSE 连接，监听 `session_status`（`idle`→`running`→`idle`/`terminated`）及工具调用事件。
4. **SDK 推荐**：Python 使用 `dashscope>=1.26.2`，Java 使用 `dashscope-sdk-java>=2.22.24`，可简化鉴权、分页与 SSE 封装；[API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中已明确版本要求。

## 限制和注意事项

- **配额限制**：单文件上传上限 **20 MB**，工作空间总文件容量上限 **100 GB**，文件保留期 **30 天**（超期可能被自动清理），详见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)。
- **状态与生命周期**：
  - Agent/Environment/Session 的“归档”均为软操作（仅标记 `archived_at`），不影响已有运行中会话；但归档后不可用于新建会话（Agent/Environment）或进入新任务（Session）。
  - Environment 删除为硬操作，不可恢复；Skill 删除将清除所有版本，但已挂载旧版本的 Agent 不受影响。
- **版本与快照**：Agent 更新后版本号递增，Session 创建时锁定其当时版本；Environment 更新不影响已绑定会话——二者均按“创建时快照”语义运行，确保会话行为可复现。
- **安全约束**：Skill zip 包上传后需经安全扫描，仅 `active` 状态版本可挂载；File 上传后需审核为 `available` 才可引用。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


