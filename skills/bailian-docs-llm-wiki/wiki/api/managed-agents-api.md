# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、执行沙箱、工具调用与事件流。开发者通过 REST 或 SDK 创建 Agent（智能体配置）、Environment（运行环境）、Session（运行实例）并驱动任务执行，所有资源均按工作空间隔离。该 API 适用于构建可复用、可审计、可扩展的智能体应用。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼托管大模型（详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)），模型 ID 通过 `model.id` 字段指定，不支持自定义模型或外部模型接入。
- **核心功能模块**：
  - `Agent`：封装模型、系统提示词、工具集与技能（Skill），支持版本化管理与软归档；
  - `Environment`：定义沙箱类型（如 `"cloud"`）与预装依赖，独立于 Agent 生命周期，可被多 Session 复用；
  - `Session`：绑定 Agent 快照与 Environment 快照的运行实例，状态机驱动（`idle` → `running` → `idle`/`terminated`）；
  - `Event`：支持同步发送（用户消息、中断、工具回填）与 SSE 流式订阅，含 `session_status` 状态变更通知；
  - `Skill`：以 ZIP 包形式上传工具组合，需经安全扫描后方可挂载，挂载时必须指定具体版本号（不支持 `latest`）；
  - `File`：支持上传至工作空间（上限 20 MB/文件，100 GB/空间），审核通过（`status: available`）后可用于消息内容或挂载至沙箱。

> **注意**：文档 2 的快速开始示例中使用 `model: "qwen-plus"` 为字符串简写，而文档 1 的 API 总览明确要求 `model` 为对象结构 `{"id": "qwen-plus"}`。实际请求体必须遵循 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中定义的 JSON Schema，否则返回 400 错误。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，从控制台获取并配置为环境变量（见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)） |
| `workspace_id` | Endpoint path | string | 是 | 工作空间 ID（如 `ws_xxxxxxxxxxxx`），与地域拼接构成 base URL |
| `region` | Endpoint path | string | 是 | 当前仅支持 `cn-beijing` |
| `agent.id` | Session 创建体 | string | 是 | Agent 唯一标识，创建 Session 时锁定其当前版本快照 |
| `environment_id` | Session 创建体 | string | 是 | Environment 唯一标识，创建 Session 时绑定其当前配置快照 |
| `input` | Event 发送体 | array | 是 | 消息数组，每项含 `role`（`user`/`assistant`）、`type`（`message`）、`content`（含 `text`/`image_url` 等） |

## 使用方式

1. **初始化**：设置 `DASHSCOPE_API_KEY` 与 `AGENTSTUDIO_URL`（形如 `https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`）；
2. **资源准备**：
   - 创建 Agent（`POST /agents`），指定 `model.id`、`system` 提示词等；
   - 创建 Environment（`POST /environments`），配置 `config.type`（如 `"cloud"`）；
3. **启动会话**：
   - 创建 Session（`POST /sessions`），传入 `agent` 和 `environment_id`；
   - 发送用户消息（`POST /sessions/{session_id}/events`），`input` 格式需严格符合 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md) 规范；
4. **接收结果**：
   - 订阅 SSE 流（`GET /sessions/{session_id}/events/stream`），监听 `session_status` 变更及 `message` 事件；
   - 或轮询事件历史（`GET /sessions/{session_id}/events`）；

SDK 调用需确保版本兼容：Python SDK ≥ v1.26.2，Java SDK ≥ v2.22.24（见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）。

## 限制和注意事项

- **配额限制**：单文件上传上限 20 MB，工作空间总存储上限 100 GB，文件保留期 30 天（见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)）；
- **版本与更新语义**：
  - Agent 更新为**全量替换 + 乐观锁**：请求体必须包含当前 `version`，不一致返回 409；成功后 `version` 自动递增；
  - Environment 更新也为**全量替换**，但已绑定的运行中 Session 仍使用创建时的快照，不受影响；
- **归档与删除**：
  - 归档（`archive`）均为软操作，资源仍可查询，已绑定 Session 不受影响；
  - 删除（`DELETE`）为硬操作，不可恢复（如 `DELETE /environments/{env_id}` 清除全部配置）；
- **安全约束**：
  - Skill 与 File 上传后需通过安全扫描，仅 `status: active` 或 `available` 状态才可使用；
  - Skill 挂载到 Agent 时必须指定具体 `version`，后续上传新版本不影响已挂载的 Agent；
- **状态机约束**：Session 仅在 `idle` 状态下可接收新消息；`running` 状态下仅支持中断、工具审批等特定操作（见 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)）。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)


