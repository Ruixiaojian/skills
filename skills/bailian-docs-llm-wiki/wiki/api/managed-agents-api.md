# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，统一管理会话生命周期、执行沙箱（Environment）、工具调用与事件流。开发者通过 REST 或 SDK 创建 Agent、Environment、Session 等资源，并以事件驱动方式与智能体交互。所有请求需通过 API Key 鉴权，且严格绑定工作空间与地域。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼平台已发布的推理模型（详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)），模型 ID 通过 `model.id` 字段指定。
- **核心功能模块**：
  - **Agent**：封装模型、系统提示词、技能（Skill）与工具配置；每次更新自动递增 `version`，会话创建时锁定快照 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)。
  - **Environment**：定义沙箱类型（如 `"type": "cloud"`）与预装依赖，可被多个 Session 复用；更新为全量替换，已绑定会话使用创建时快照 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)。
  - **Skill**：以 ZIP 包形式上传工具组合，需经安全扫描后方可挂载；挂载时必须显式指定 `version`，不支持 `latest` [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)。
  - **File**：支持上传 ≤20 MB 文件，用于消息内容（图像/音频）或挂载至沙箱；上传后进入 `checking` 审核状态，仅 `available` 状态可引用 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)。

> **注意**：文档 2 的快速开始示例中使用 `model="qwen-plus"` 作为字符串传入 Python SDK，而文档 1 的 REST 示例中使用 `{"id": "qwen-plus"}` 对象结构。实际 REST 接口要求 `model` 字段为对象（含 `id`），SDK 封装已做适配，开发者直接按 SDK 文档传参即可，无需手动构造 model 对象。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，从控制台获取并配置为环境变量 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) |
| `workspace_id` | Endpoint path | string | 是 | 工作空间 ID（如 `ws_xxxxxxxxxxxx`），拼入 base URL |
| `region` | Endpoint path | string | 是 | 当前仅支持 `cn-beijing` |
| `agent.id` / `environment_id` | Session 创建 body | string | 是 | 创建 Session 时必须显式绑定 Agent 与 Environment ID |
| `version` | Agent 更新 body | integer | 是（乐观锁） | 更新 Agent 时需携带当前 `version` 值，不一致返回 409 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) |
| `file_id` | Skill 创建 / File 挂载 body | string | 是（按场景） | Skill 创建需引用已上传且 `status=available` 的 File ID；挂载文件到 Session 同理 |

## 使用方式

完整调用流程为五步闭环（见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)）：

1. **创建 Agent**：指定 `model.id`、`system` 提示词及可选 `skills` 列表；
2. **创建 Environment**：指定 `config.type`（如 `"cloud"`）及其他沙箱参数；
3. **创建 Session**：传入 `agent`（ID）与 `environment_id`，获得 `session_id`；
4. **发送 Event**：向 `/sessions/{session_id}/events` POST 用户消息（`input` 数组），触发 `running` 状态；
5. **订阅 SSE 流**：GET `/sessions/{session_id}/events/stream`，监听 `session_status` 变更直至 `idle` 或 `terminated`。

推荐使用官方 SDK（Python v1.26.2+ / Java v2.22.24+），避免手动拼接 URL 与鉴权头。SDK 自动处理分页、重试与流式解析。

## 限制和注意事项

- **配额限制**：单文件上传上限 **20 MB**，工作空间总文件容量上限 **100 GB**，文件保留期 **30 天**（超期可能被清理）[File](../../raw/application-api-reference/managed-agents-api/files-api.md)。
- **状态与生命周期**：
  - Agent / Environment / Session 的“归档”均为软操作（`archived_at` 记录时间），不影响已存在会话；“删除”为硬操作，不可恢复。
  - Environment 更新不影响已绑定会话，但 Agent 更新后新建会话将使用新版本。
- **安全约束**：
  - Skill 上传后必须通过安全扫描（`status=active`）才可挂载；`rejected` 状态需检查 `error_info` 修复后重传。
  - File 与 Skill 均需审核通过（`available` / `active`）才能在会话中使用。
- **事件语义**：`POST /sessions/{session_id}/events` 仅接受用户消息、中断指令等原子事件；工具调用结果需通过 `tool_result` 类型事件回填，非直接 HTTP 响应。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


