# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，负责会话生命周期管理、沙箱环境调度、工具执行协调与事件流分发。开发者通过 REST 或 SDK 调用，可快速构建具备工具调用、多轮交互与状态感知能力的智能体应用。所有资源均按工作空间隔离，需配合 API Key 与地域化 Endpoint 使用。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼托管大模型（详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中的 `model.id` 字段示例）；不支持自定义模型或外部模型接入。
- **核心功能模块**：
  - **Agent**：封装模型、系统提示词、工具集与技能，支持版本化管理与软归档；
  - **Environment**：定义沙箱类型（如 `"cloud"`）、预装依赖与网络策略，独立于 Agent 生命周期；
  - **Session**：绑定 Agent 快照与 Environment 实例，驱动 `idle → running → idle/terminated` 状态机；
  - **Event**：支持用户消息、工具回填、中断指令等原子事件，提供 SSE 流式订阅；
  - **File**：上传后经安全审核（`checking` → `available`），可用于消息内容或挂载至沙箱；
  - **Skill**：以 zip 包形式封装工具组合，上传后需通过安全扫描（`checking` → `active`）方可挂载，挂载时必须指定具体版本号。

> **注意**：文档 2 的快速开始示例中使用 `model: "qwen-plus"` 作为字符串传入，而文档 1 的 API 总览中 `model` 字段结构为 `{"id": "qwen-plus"}`。实际请求体应严格遵循文档 1 的嵌套对象格式，否则将返回 400 错误 —— 此处以 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 为准。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，从控制台获取并配置为环境变量 |
| `workspace_id` | Endpoint path | string | 是 | 工作空间 ID（如 `ws_xxxxxxxxxxxx`），见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) |
| `region` | Endpoint path | string | 是 | 当前仅支持 `cn-beijing` |
| `agent.id` | Session 创建体 | string | 是 | Agent ID，创建时生成；会话锁定其 `version` 快照 |
| `environment_id` | Session 创建体 | string | 是 | Environment ID，会话绑定其快照 |
| `input` | `/sessions/{id}/events` 请求体 | array | 是 | 符合 ChatML 格式的 message 数组，如 `[{"role":"user","type":"message","content":[{"type":"text","text":"..."}]}]` |
| `limit` / `page` | 列表端点 Query | integer | 否 | 分页参数，默认 `limit=20`，最大 `100`；响应含 `next_page` 表示可继续翻页 |

## 使用方式

1. **初始化**：导出 `DASHSCOPE_API_KEY` 与 `AGENTSTUDIO_URL`（形如 `https://<workspace_id>.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio`）；
2. **资源准备**：
   - 创建 Agent（`POST /agents`），指定 `model.id`、`system` 等；
   - 创建 Environment（`POST /environments`），配置 `config.type`（如 `"cloud"`）；
3. **会话启动**：
   - 创建 Session（`POST /sessions`），传入 `agent` 和 `environment_id`；
   - 发送 Event（`POST /sessions/{id}/events`）触发执行；
4. **结果消费**：
   - 订阅 SSE 事件流（`GET /sessions/{id}/events/stream`），监听 `session_status` 变更及 `message` 内容；
   - 或轮询事件历史（`GET /sessions/{id}/events`）。

SDK 使用需满足最低版本要求：Python SDK ≥ v1.26.2，Java SDK ≥ v2.22.24 —— 具体安装与初始化方式参见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。

## 限制和注意事项

- **配额限制**：单文件直传上限 **20 MB**，工作空间总容量上限 **100 GB**，文件保留期 **30 天**（[File](../../raw/application-api-reference/managed-agents-api/files-api.md)）；
- **版本与快照**：Agent 更新采用全量替换 + 乐观锁（需带 `version` 字段），会话创建即锁定 Agent 与 Environment 快照，后续更新不影响运行中会话；
- **状态终态**：Session 归档（`POST /sessions/{id}/archive`）使其进入 `terminated` 终态，不可恢复；删除（`DELETE /sessions/{id}`）则彻底清除事件历史；
- **安全约束**：Skill 上传后必须通过安全扫描（`status: active`）才可挂载；File 仅 `available` 状态可被引用或挂载；
- **错误排查**：所有响应携带 `x-request-id`，提工单时务必提供该值以便定位问题。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


