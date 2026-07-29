# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、沙箱环境、工具执行与事件流。开发者通过 RESTful 接口或 SDK 创建 Agent、Environment、Session 等资源，并以事件驱动方式与智能体交互。所有请求需通过 API Key 鉴权，且严格绑定工作空间与地域。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼托管大模型（详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)），模型 ID 通过 `model.id` 字段指定（如 `"qwen-plus"`）。
- **核心功能模块**：
  - **Agent**：封装模型、系统提示词、工具集与 Skill，支持版本化管理与软归档；
  - **Environment**：定义沙箱类型（如 `"cloud"`）与预装依赖，独立于 Agent 生命周期；
  - **Session**：绑定 Agent 快照与 Environment 实例，状态机驱动（`idle` → `running` → `idle`/`terminated`）；
  - **File**：作为消息内容（图像/音频）或沙箱挂载文件，上传后需审核通过（`status: "available"`）方可使用；
  - **Skill**：以 ZIP 包形式封装工具组合，上传后需安全扫描（`status: "active"`）才可挂载到 Agent，挂载时必须显式指定 `version`（不支持 `latest`）。

> **注意**：文档 2 的快速开始示例中 `model` 字段直接传字符串 `"qwen-plus"`，而文档 1 的 API 总览明确要求 `model` 为对象结构 `{"id": "qwen-plus"}`。实际调用应以 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 的 JSON Schema 为准，否则将返回 400 错误。

## 关键参数

| 参数 | 位置 | 说明 | 示例 |
|------|------|------|------|
| `Authorization` | Header | API Key 鉴权，格式为 `Bearer <your-api-key>` | `Bearer sk-xxx` |
| `workspace_id` | Endpoint 路径 | 工作空间 ID，形如 `ws_xxxxxxxxxxxx` | `ws_abc123` |
| `region` | Endpoint 路径 | 当前仅支持 `cn-beijing` | `cn-beijing` |
| `agent.id` & `environment_id` | `/sessions` 请求体 | Session 创建时必需，绑定 Agent 快照与 Environment 实例 | `"agent_xxx"`, `"env_xxx"` |
| `input` | `/sessions/{id}/events` 请求体 | 用户消息数组，每项含 `role`、`type`、`content`；`content` 支持文本、图像等多模态 | `[{"role":"user","type":"message","content":[{"type":"text","text":"..."}]}]` |
| `limit` / `page` | 查询参数 | 分页控制，默认 `limit=20`，最大 `100`；响应含 `next_page` 字段 | `?limit=50&page=2` |

## 使用方式

1. **初始化**：设置环境变量 `DASHSCOPE_API_KEY` 和 `AGENTSTUDIO_URL`（格式见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）；
2. **资源创建**：
   - 先创建 `Agent`（含模型、系统提示、Skill 列表）；
   - 再创建 `Environment`（指定沙箱类型与依赖）；
   - 最后创建 `Session`，绑定二者 ID；
3. **任务执行**：
   - 向 `/sessions/{session_id}/events` 发送 `input` 事件触发执行；
   - 通过 `/sessions/{session_id}/events/stream` 建立 SSE 连接，实时接收 `session_status` 变更与输出事件；
4. **SDK 调用**：Python SDK v1.26.2+ 或 Java SDK v2.22.24+ 提供 `Client.agents.create()`、`client.sessions.events.stream()` 等封装方法，简化流程（参见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)）。

## 限制和注意事项

- **地域限制**：Endpoint 中 `region` 仅支持 `cn-beijing`，其他地域请求将失败；
- **配额限制**：单文件直传上限 **20 MB**，工作空间总容量上限 **100 GB**，文件保留期 **30 天**（超期可能被自动清理），详见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)；
- **版本锁定**：Agent 更新采用乐观锁（请求体需带当前 `version`），Session 创建时锁定 Agent 与 Environment 的快照版本，后续更新不影响已运行会话；
- **状态终态**：`terminated` 为会话终态，不可恢复；归档（`archive`）为软操作，不影响已有会话，但禁止新建会话引用；
- **Skill 安全约束**：Skill 新版本上传后需通过安全扫描（`status: "active"`）才可挂载，挂载时必须指定具体 `version`，且不支持动态解析 `latest`（参见 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)）。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


