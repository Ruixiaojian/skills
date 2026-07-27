# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、沙箱环境、工具执行与事件流。开发者通过 REST 或 SDK 调用，可快速构建具备多步推理、工具调用与状态感知能力的智能体应用。所有资源（Agent、Environment、Session 等）均以工作空间为作用域，支持细粒度版本控制与软/硬归档策略。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼托管大模型（详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)），不支持自定义模型或外部模型接入。
- **核心功能模块**：
  - `Agent`：封装模型、系统提示词、技能（Skill）与工具配置；每次更新自动递增 `version`，会话创建时锁定快照 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)；
  - `Environment`：定义沙箱类型（如 `"cloud"`）与预装依赖，独立于 Agent 管理，可被多个 Session 复用 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)；
  - `Session`：绑定 Agent 快照与 Environment 的运行实例，遵循 `idle → running → idle/terminated` 状态机 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)；
  - `Skill`：以 zip 包形式封装工具组合，上传后需通过安全扫描（`checking → active/rejected`），挂载到 Agent 时必须指定具体 `version` [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)；
  - `File`：支持上传 ≤20 MB 文件，经审核后可用于消息内容或挂载至沙箱；单 workspace 总容量上限 100 GB，保留期 30 天 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)。

> **注意**：文档 2 中示例使用 `"model": "qwen-plus"` 字符串形式，而文档 1 的 API 总览表格中 `Agent` 创建请求体示例写为 `"model": {"id": "qwen-plus"}`。实际接口要求为对象格式 `{"id": "<model_id>"}`，字符串形式将导致 400 错误 —— 请以 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中的 JSON Schema 为准。

## 关键参数

| 参数 | 位置 | 说明 | 示例 |
|------|------|------|------|
| `Authorization` | Header | API Key 鉴权，格式 `Bearer <your-api-key>` | `Bearer sk-xxx` |
| `workspace_id` | Endpoint 域名 | 工作空间 ID，形如 `ws_xxxxxxxxxxxx` | `ws_abc123def456` |
| `region` | Endpoint 域名 | 当前仅支持 `cn-beijing` | `cn-beijing` |
| `agent.id` & `environment_id` | `/sessions` 请求体 | 创建 Session 时必需，绑定 Agent 快照与 Environment | `"agent": "agt_xxx", "environment_id": "env_yyy"` |
| `version` | `/agents/{id}` 查询参数 | 查询 Agent 历史版本；更新时需在请求体中携带作为乐观锁 | `GET /agents/agt_xxx?version=2` |
| `limit` / `page` | 列表端点查询参数 | 分页控制，默认 `limit=20`，最大 `100`；`page` 首次不传，后续传 `next_page` | `?limit=50&page=2` |

## 使用方式

1. **准备环境**：开通百炼，创建 API Key 并导出为 `DASHSCOPE_API_KEY`；获取工作空间 ID 和地域（固定 `cn-beijing`）[API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。
2. **创建基础资源**：
   - 创建 `Agent`（含模型 ID、系统提示词、技能列表）；
   - 创建 `Environment`（指定 `"type": "cloud"` 或其他沙箱类型）；
   - 创建 `Session`，绑定二者 ID。
3. **驱动执行**：
   - 向 `/sessions/{session_id}/events` 发送 `user_message` 类型事件触发任务；
   - 通过 `/sessions/{session_id}/events/stream` 订阅 SSE 流，监听 `session_status` 变更及中间结果。
4. **SDK 推荐**：Python SDK ≥ v1.26.2，Java SDK ≥ v2.22.24；直接使用 `dashscope.agentstudio.Client` 封装了资源操作与流式订阅逻辑 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。

## 限制和注意事项

- **配额限制**：单文件 ≤20 MB；工作空间总存储 ≤100 GB；文件保留期 30 天（超期可能被清理）[File](../../raw/application-api-reference/managed-agents-api/files-api.md)。
- **版本与更新语义**：
  - Agent 更新为**全量替换 + 乐观锁**，请求体必须包含当前 `version`，否则返回 409；
  - Environment 更新也为**全量替换**，但无乐观锁机制，已绑定的运行中 Session 仍使用旧快照 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)。
- **归档与删除区别**：
  - 归档（`archive`）为软操作，资源仍可查询，已绑定 Session 不受影响；
  - 删除（`DELETE`）为硬操作，数据不可恢复（如 Environment、File、Skill 删除后其关联副本不受影响，但 Skill 删除后已挂载版本仍可用）。
- **安全性约束**：Skill zip 包必须通过安全扫描（`status: active`）才可挂载；File 上传后需等待 `status: available` 才能引用 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


