# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，负责会话生命周期管理、沙箱环境调度、工具执行协调及事件流推送。开发者通过 REST 或 SDK 创建 Agent（模型+提示词+技能）、Environment（执行沙箱）和 Session（运行实例），以事件驱动方式与智能体交互。所有资源均按工作空间隔离，支持版本控制与软归档。

## 支持的模型/功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼托管大模型（见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 示例），不支持自定义模型或外部模型接入。
- **核心功能**：
  - Agent：支持系统提示词、工具绑定、Skill 挂载（需指定具体版本号，不支持 `latest`），每次更新生成新版本并自动递增 `version` 字段 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)；
  - Environment：支持 `cloud` 类型沙箱（预装 Python 环境），可复用且绑定后快照固化，更新不影响已运行会话 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)；
  - Session：状态机驱动（`idle` → `running` → `idle`/`terminated`），支持消息注入、中断、工具审批回填等事件类型 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)；
  - File：单文件上限 20 MB，审核通过（`status: available`）后方可挂载至沙箱或作为消息内容引用；
  - Skill：zip 包上传后需经安全扫描，仅 `active` 状态版本可挂载；挂载时必须显式指定 `version`，后续新版本不影响已挂载 Agent。

> **注意**：文档 2 中列出的 `/skills/{skill_id}/versions/{version}/download` 端点返回 OSS 预签名 URL，但文档 7 明确说明该 URL 有效期为 2 小时；而文档 2 的“可用 API”表格中未标注此时效约束，实际使用需以 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md) 文档为准。

## 关键参数

- **认证参数**：`Authorization: Bearer <API_KEY>`（全部请求必需），API Key 须归属目标工作空间。
- **Endpoint 构造**：`https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`，其中 `region` 当前仅支持 `cn-beijing`。
- **Agent 创建参数**：
  - `model.id`：必填，如 `"qwen-plus"`；
  - `system`：系统提示词（Python SDK 中为 `system_prompt`，Java SDK 中为 `instructions`），语义一致；
  - `skills`：数组，每个元素含 `skill_id` 与 `version`（不可省略）。
- **Environment 创建参数**：`config.type` 必须为 `"cloud"`（当前唯一支持类型）。
- **Session 创建参数**：`agent`（Agent ID）与 `environment_id`（Environment ID）为必填字段。
- **Event 发送参数**：`input` 为消息数组，每条消息需含 `role`（`user`/`assistant`/`tool`）、`type`（`message`/`tool_result`）及 `content`（文本或富媒体结构）。

## 使用方式

1. **初始化**：设置 `DASHSCOPE_API_KEY` 和 `AGENTSTUDIO_URL` 环境变量（[快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)）；
2. **资源创建**（建议长期复用）：
   - 调用 `POST /agents` 创建 Agent；
   - 调用 `POST /environments` 创建 Environment；
3. **会话交互**（每次任务）：
   - 调用 `POST /sessions` 绑定 Agent 与 Environment，获取 `session_id`；
   - 调用 `POST /sessions/{session_id}/events` 提交用户消息；
   - 调用 `GET /sessions/{session_id}/events/stream` 建立 SSE 连接，监听 `session_status` 及 `content` 事件；
4. **SDK 推荐**：Python SDK v1.26.2+ 或 Java SDK v2.22.24+，避免旧版本兼容问题（[API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）。

## 限制和注意事项

- **配额限制**：单个工作空间文件总容量上限 100 GB，单文件直传上限 20 MB，文件保留期 30 天（[File](../../raw/application-api-reference/managed-agents-api/files-api.md)）；
- **状态与生命周期**：
  - Agent/Environment 归档为软操作（`archived_at` 记录时间），已运行 Session 不受影响；删除 Environment 为硬操作，不可恢复；
  - Session 归档即进入 `terminated` 终态，不可再发送事件；删除 Session 将清除全部事件历史；
- **版本一致性**：Agent 更新需携带当前 `version` 作乐观锁，否则返回 409；Skill 挂载必须指定 `version`，无 `latest` 别名；
- **事件流可靠性**：SSE 连接可能中断，客户端需实现重连逻辑（含 `Last-Event-ID` 头续传），平台不保证事件投递顺序外的其他语义；
- **工具执行**：工具调用结果必须通过 `tool_result` 类型 Event 回填，且 `tool_call_id` 需与原始 `tool_use` 事件严格匹配。

## 来源文档

- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


