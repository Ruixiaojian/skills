# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、沙箱环境、工具执行与事件流。开发者通过 REST 或 SDK 创建 Agent、Environment、Session 等资源，并以事件驱动方式与智能体交互。所有请求需通过 API Key 鉴权，且严格绑定工作空间与地域。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼托管大模型（详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)），模型 ID 通过 `model.id` 字段指定。
- **核心资源**：
  - `Agent`：定义模型、系统提示词、工具集与技能组合；支持版本化（每次更新自动递增 `version`）与软归档；
  - `Environment`：定义沙箱类型（如 `"cloud"`）与预装依赖，独立于 Agent 管理，可被多会话复用；
  - `Session`：绑定 Agent 快照与 Environment 的运行实例，状态机驱动（`idle` → `running` → `idle`/`terminated`）；
  - `File`：作为消息内容（图像/音频）或沙箱挂载文件，上传后需经安全审核（`status: available` 才可用）；
  - `Skill`：以 zip 包封装工具逻辑，上传后需通过安全扫描（`status: active` 方可挂载），挂载时必须显式指定 `version`（不支持 `latest`）。

> **注意**：文档 2 的快速开始示例中使用 `model: "qwen-plus"` 为字符串简写，而文档 1 的 API 总览明确要求 `model` 为对象结构 `{"id": "qwen-plus"}`。实际调用应以 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中的 JSON Schema 为准，避免因字段格式错误导致 400 响应。

## 关键参数

| 参数 | 位置 | 说明 | 示例 |
|------|------|------|------|
| `Authorization` | Header | API Key 鉴权凭证 | `Bearer sk-xxx` |
| `workspace_id` | Endpoint 路径 | 工作空间 ID，从控制台获取 | `ws_xxxxxxxxxxxx` |
| `region` | Endpoint 路径 | 当前仅支持 `cn-beijing` | `cn-beijing` |
| `agent_id` / `environment_id` | 请求体或路径 | 创建 Session 时必需绑定 | `"agent_xxx"`, `"env_xxx"` |
| `version` | Agent/Environment/Skill 更新请求体 | 乐观锁字段，必须携带当前值 | `"version": 3` |
| `input` | `/sessions/{id}/events` 请求体 | 用户消息数组，遵循 `role`/`type`/`content` 结构 | `[{"role":"user","type":"message","content":[{"type":"text","text":"..."}]}]` |

## 使用方式

1. **初始化**：导出 `DASHSCOPE_API_KEY` 与 `AGENTSTUDIO_URL`（形如 `https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`），[参考快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)；
2. **创建资源**：
   - 先创建 `Agent`（含模型与系统提示）和 `Environment`（含沙箱配置）；
   - 再创建 `Session`，绑定二者 ID；
3. **驱动执行**：
   - 向 `/sessions/{session_id}/events` 发送 `POST` 请求提交用户消息；
   - 通过 `/sessions/{session_id}/events/stream` 建立 SSE 连接，实时接收 `session_status` 变更与执行结果；
4. **SDK 推荐**：Python SDK ≥ v1.26.2，Java SDK ≥ v2.22.24；[详见 API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 限制和注意事项

- **配额限制**：单文件直传上限 20 MB，工作空间总容量上限 100 GB，文件保留期 30 天（[File](../../raw/application-api-reference/managed-agents-api/files-api.md)）；
- **状态一致性**：Agent/Environment 更新为全量替换，已运行的 Session 始终使用创建时锁定的快照版本，不受后续更新影响；
- **技能挂载**：Skill 必须通过安全扫描（`status: active`）后才可挂载，且挂载时需指定具体 `version`，新版本上传不影响已挂载的 Agent；
- **归档语义**：Agent/Environment/Session 归档均为软操作（`archived_at` 记录时间），已归档资源不可用于新建会话，但已有会话仍可正常运行；
- **错误定位**：所有响应均携带 `x-request-id`，提工单时务必提供该值。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


