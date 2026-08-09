# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、执行沙箱、工具调用与事件流。开发者通过 REST 或 SDK 创建 Agent（智能体配置）、Environment（运行环境）、Session（运行实例），并以事件驱动方式与智能体交互。所有请求需通过 API Key 鉴权，且必须指定工作空间 ID 与地域。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼托管大模型（详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中的 `model.id` 字段示例）；不支持自定义模型或外部模型端点。
- **核心功能模块**：
  - `Agent`：封装模型、系统提示词、工具列表与 Skill（技能包），支持版本化与软归档；
  - `Environment`：定义沙箱类型（如 `"type": "cloud"`）及预装依赖，独立于 Agent 生命周期；
  - `Session`：绑定 Agent 版本与 Environment 快照，驱动状态机（`idle` → `running` → `terminated`）；
  - `Event`：支持同步发送用户消息、中断指令、工具审批结果，并通过 SSE 流式接收执行事件；
  - `File`：上传后经安全审核（状态为 `available` 才可用），可挂载至沙箱或作为消息内容；
  - `Skill`：zip 包形式封装工具组合，需通过安全扫描（状态 `active` 后方可挂载），挂载时必须显式指定 `version`。

> **注意**：文档 2 的快速开始示例中使用 `model: "qwen-plus"` 作为字符串，而文档 1 的 API 总览中 `model` 字段结构为 `{"id": "qwen-plus"}`。实际请求体应严格遵循 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 定义的 JSON Schema，即 `model` 必须为对象而非字符串，否则返回 400 错误。

## 关键参数

| 参数 | 位置 | 说明 | 示例 |
|------|------|------|------|
| `Authorization` | Header | API Key 鉴权，格式为 `Bearer <your-api-key>` | `Bearer sk-xxx` |
| `workspace_id` | Endpoint 路径 | 工作空间 ID，从控制台获取，形如 `ws_xxxxxxxxxxxx` | `ws_abc123` |
| `region` | Endpoint 路径 | 当前仅支持 `cn-beijing` | `cn-beijing` |
| `agent.id` & `version` | Agent 更新请求体 | 更新 Agent 时需携带当前 `version` 值用于乐观锁校验 | `"version": 3` |
| `environment.config.type` | Environment 创建请求体 | 沙箱类型，目前仅支持 `"cloud"` | `{"type": "cloud"}` |
| `session_status` | SSE 事件字段 | Session 状态变更事件的关键字段，用于判断流程终止 | `"idle"` 或 `"terminated"` |
| `file_id` | File 相关操作路径 | 文件唯一标识，上传成功后返回；挂载到 Session 时服务端生成新副本 ID | `file_xxx` |

## 使用方式

1. **准备环境**：开通百炼，创建 API Key 并导出为 `DASHSCOPE_API_KEY`；获取工作空间 ID 和地域（固定为 `cn-beijing`），拼接 Endpoint：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio`。
2. **创建资源**（建议复用）：
   - 调用 `POST /agents` 创建 Agent，指定 `model.id`、`system` 提示词等；
   - 调用 `POST /environments` 创建 Environment，配置 `config.type`；
   - （可选）上传文件 `POST /files`，待状态变为 `available` 后使用；
   - （可选）创建 Skill 并上传版本，待扫描状态为 `active` 后挂载到 Agent。
3. **启动会话**：
   - 调用 `POST /sessions` 绑定 `agent.id` 与 `environment_id`，获得 `session_id`；
   - 调用 `POST /sessions/{session_id}/events` 发送用户消息（`input` 数组含 `role: "user"` 消息）；
4. **流式消费结果**：
   - 调用 `GET /sessions/{session_id}/events/stream` 建立 SSE 连接，监听 `session_status` 字段变化；
   - 当收到 `session_status: "idle"` 或 `"terminated"` 时，可安全结束流式读取。

SDK 使用请参考 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)，Python SDK 要求 v1.26.2+，Java SDK 要求 v2.22.24+。

## 限制和注意事项

- **配额限制**：单文件直传上限 **20 MB**，工作空间总存储上限 **100 GB**，文件保留期 **30 天**（超期可能被自动清理）[见 File 文档](../../raw/application-api-reference/managed-agents-api/files-api.md)。
- **版本锁定**：Session 创建时锁定 Agent 的 `version` 和 Environment 的快照，后续更新不影响已运行会话；Skill 挂载也必须指定具体 `version`，不支持 `latest`。
- **状态机约束**：Session 仅在 `idle` 状态下可接收新事件；`running` 状态下不可直接删除，需先归档或等待自然结束。
- **归档 vs 删除**：Agent、Environment、Session 的 `archive` 为软操作（保留历史、不影响已有会话），而 `DELETE /environments/{id}` 和 `DELETE /sessions/{id}` 为硬删除（不可恢复）。
- **安全性要求**：Skill zip 包必须通过安全扫描（状态 `active`）才可挂载；File 上传后需等待 `status: "available"` 才能引用，否则返回 400。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


