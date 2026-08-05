# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、执行沙箱、工具调用与事件流。开发者通过 REST API 或 SDK 创建 Agent、Environment、Session 等资源，并以事件驱动方式与智能体交互。所有请求需通过 API Key 鉴权，Endpoint 按工作空间与地域动态生成。

## 支持的模型与功能

- **模型支持**：Agent 创建时通过 `model.id` 指定模型，当前支持 `qwen-plus` 等百炼托管模型（详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）；不支持自定义模型或外部模型接入。
- **核心功能模块**：
  - **Agent**：封装模型、系统提示词、工具列表与技能集合；每次更新生成新版本，会话创建时锁定快照 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)。
  - **Environment**：定义执行沙箱类型（如 `"type": "cloud"`）与预装依赖，可被多个 Session 复用 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)。
  - **Skill**：以 ZIP 包形式上传工具组合，需经安全扫描后方可挂载；挂载时必须指定具体版本号，不支持 `latest` 别名 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)。
  - **File**：支持图像、音频、文本等格式上传，用于消息内容或挂载至沙箱；单文件上限 20 MB，审核通过后状态为 `available` 方可使用。

## 关键参数

| 参数 | 位置 | 说明 | 示例 |
|------|------|------|------|
| `Authorization` | Header | API Key 鉴权，格式为 `Bearer <your-api-key>` | `Bearer sk-xxx` |
| `workspace_id` | Endpoint 路径 | 工作空间 ID，形如 `ws_xxxxxxxxxxxx` | `ws_abc123` |
| `region` | Endpoint 路径 | 当前仅支持 `cn-beijing` | `cn-beijing` |
| `agent.id` & `environment_id` | `/sessions` 请求体 | 创建 Session 时必需，绑定 Agent 快照与 Environment | `{"agent": "agent_xxx", "environment_id": "env_xxx"}` |
| `input` | `/sessions/{id}/events` 请求体 | 用户消息结构，必须为 `role: "user"` 的 message 数组 | `[{"role": "user", "type": "message", "content": [{"type": "text", "text": "..." }] }]` |
| `limit` / `page` | 查询参数 | 分页控制，默认 `limit=20`，最大 `100`；响应含 `next_page` 字段 | `?limit=50&page=2` |

> **注意**：文档 2 中示例使用 `system_prompt` 字段创建 Agent，但文档 3 明确要求字段名为 `system`（非 `system_prompt`），实际请求应以 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档为准，否则返回 400 错误。

## 使用方式

1. **准备环境**：开通百炼、创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`，获取工作空间 ID 和地域（当前仅 `cn-beijing`）。
2. **创建基础资源**：
   - 调用 `POST /agents` 创建 Agent（需指定 `model.id` 和 `system`）；
   - 调用 `POST /environments` 创建 Environment（如 `{"config": {"type": "cloud"}}`）；
   - （可选）上传 File 并通过 `POST /skills` 创建 Skill，待扫描状态为 `active` 后挂载到 Agent。
3. **启动会话**：
   - 调用 `POST /sessions` 绑定 Agent 与 Environment，获得 `session_id`；
   - 调用 `POST /sessions/{id}/events` 发送用户消息触发执行；
   - 调用 `GET /sessions/{id}/events/stream` 建立 SSE 连接，监听 `session_status` 变更及输出事件。
4. **SDK 接入**：推荐使用 DashScope Python SDK v1.26.2+ 或 Java SDK v2.22.24+，自动处理鉴权与事件流解析（参见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)）。

## 限制和注意事项

- **配额限制**：单文件直传 ≤20 MB；工作空间总存储 ≤100 GB；文件保留期 30 天，超期可能被自动清理。
- **状态与生命周期**：
  - Agent/Environment/Session 归档均为软操作（`archived_at` 记录时间），不影响已运行会话；但归档后不可用于新建会话。
  - Environment 删除为硬操作，不可恢复；Skill 删除后已挂载旧版本仍有效。
  - Session 状态机严格遵循 `idle → running → idle/terminated`，`terminated` 为终态，仅支持查询与删除。
- **安全约束**：
  - File 与 Skill 上传后均需安全扫描，状态为 `available` 或 `active` 才可使用；`rejected` 状态需根据 `error_info` 修正后重传。
  - 工具调用结果必须通过 `POST /sessions/{id}/events` 回填，且 `event.type` 必须为 `tool_result`，否则 Agent 无法继续执行。
- **版本一致性**：Agent 更新需携带当前 `version` 值作乐观锁；Skill 挂载必须显式指定 `version`，不支持动态解析 `latest`。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)


