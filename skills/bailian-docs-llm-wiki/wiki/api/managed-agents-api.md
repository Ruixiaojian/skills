# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，统一管理会话生命周期、沙箱环境、工具执行与事件流。开发者通过 REST API 或 SDK 创建 Agent、Environment、Session 等资源，并以事件驱动方式与智能体交互。所有请求需通过 API Key 鉴权，且依赖工作空间 ID 与地域标识构造 Endpoint。

## 支持的模型与功能

- **模型支持**：Agent 配置中 `model.id` 字段指定模型，当前支持 `qwen-plus` 等百炼托管模型（详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）。
- **核心资源**：
  - `Agent`：定义模型、系统提示词、工具集与技能组合；每次更新生成新版本，会话创建时锁定快照 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)。
  - `Environment`：定义沙箱类型（如 `"type": "cloud"`）与预装依赖，可被多个 Session 复用 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)。
  - `Session`：绑定 Agent 快照与 Environment 的运行实例，状态机驱动（`idle` → `running` → `idle`/`terminated`）[Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)。
  - `File`：支持 ≤20 MB 直传，审核通过（`status: available`）后可用于消息内容或挂载至沙箱 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)。
  - `Skill`：zip 包封装的工具集合，上传后需安全扫描（`checking` → `active`），挂载到 Agent 时必须显式指定 `version` [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)。

> **注意**：文档 3 的 Bash 示例中 `POST /agents` 请求体使用 `"model": {"id": "qwen-plus"}`，而文档 2 的 Agent 创建说明未明确要求嵌套对象结构；实际调用应以 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中的端点定义为准，该文档明确列出 `/agents` 接口支持 `model.id` 字段。

## 关键参数

| 参数 | 位置 | 说明 | 示例 |
|------|------|------|------|
| `Authorization` | Header | API Key 鉴权 | `Bearer sk-xxx` |
| `workspace_id` | Endpoint 路径 | 工作空间 ID，控制台获取 | `ws_xxxxxxxxxxxx` |
| `region` | Endpoint 路径 | 当前仅支持 `cn-beijing` | `cn-beijing` |
| `version` | Agent 更新请求体 | 乐观锁字段，更新时必须携带当前值，成功后自动 +1 | `1` |
| `limit` / `page` | 查询参数 | 分页控制，默认 `limit=20`，最大 `100` | `?limit=50&page=2` |
| `file_id` | Skill 创建 / File 挂载 | 文件资源唯一标识，需为 `available` 状态 | `file_xxx` |

## 使用方式

1. **初始化**：设置环境变量 `DASHSCOPE_API_KEY` 与 `AGENTSTUDIO_URL`（格式：`https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`）。
2. **资源创建**（按序）：
   - 创建 `Agent`（含模型、系统提示、技能引用）；
   - 创建 `Environment`（指定沙箱类型）；
   - 创建 `Session`（绑定 `agent_id` 与 `environment_id`）。
3. **任务提交与接收**：
   - `POST /sessions/{session_id}/events` 发送用户消息（`input` 数组）；
   - `GET /sessions/{session_id}/events/stream` 建立 SSE 连接，监听 `session_status` 与 `content` 事件。
4. **SDK 调用**：Python SDK ≥ v1.26.2，Java SDK ≥ v2.22.24；推荐使用 `dashscope.agentstudio.Client` 封装资源操作 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。

## 限制和注意事项

- **配额限制**：单文件 ≤20 MB；工作空间总存储 ≤100 GB；文件保留期 30 天，超期可能被自动清理。
- **状态约束**：
  - 归档（`archive`）均为软操作，不影响已存在会话；删除（`DELETE`）为硬操作，不可恢复。
  - Skill 版本挂载后，后续上传新版本不影响已挂载 Agent 行为；但旧版本若被 `DELETE`，已挂载 Agent 将无法加载该技能。
- **版本一致性**：Agent 更新采用全量替换 + 乐观锁，请求体必须包含当前 `version`；Environment 更新同理，缺省字段视为清空。
- **事件语义**：`POST /sessions/{session_id}/events` 仅用于注入事件（用户消息、中断、工具回填等），不触发状态变更；状态流转由平台内部驱动并通过 SSE 推送。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


