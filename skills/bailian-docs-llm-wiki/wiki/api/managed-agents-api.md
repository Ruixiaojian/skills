# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、执行沙箱、工具调用与事件流。开发者通过 RESTful 接口或 SDK 创建 Agent、Environment、Session 等资源，并以事件驱动方式与智能体交互。所有操作均基于工作空间隔离，需通过 API Key 鉴权。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼托管大模型（详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)），模型 ID 通过 `model.id` 字段指定，不支持自定义模型接入。
- **核心功能模块**：
  - `Agent`：封装模型、系统提示词、技能（Skill）与工具配置；支持版本化管理与软归档；
  - `Environment`：定义沙箱类型（如 `"type": "cloud"`）与预装依赖，可被多 Session 复用；
  - `Session`：绑定 Agent 版本与 Environment 快照的运行实例，状态机驱动（`idle` → `running` → `idle`/`terminated`）；
  - `File`：作为消息内容（图像/音频）或挂载至沙箱供工具读写，上传后需审核通过（`status: available`）方可使用；
  - `Skill`：以 zip 包封装工具组合，上传后经安全扫描，挂载到 Agent 时必须显式指定 `version`（不支持 `latest`）。

> **注意**：文档 2 的快速开始示例中将 `system` 字段用于创建 Agent，而文档 4 的 Agent API 规范明确要求字段名为 `system_prompt`（Python SDK）或 `instructions`（Java SDK）。实际 REST 接口接受 `system`（兼容旧版），但 SDK 调用应严格遵循各自参数命名，避免混淆 —— 此差异已在 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 和 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 中分别体现。

## 关键参数

| 资源 | 关键字段 | 说明 |
|------|----------|------|
| **全局** | `workspace_id`, `region` | Endpoint 拼接必需；当前 `region` 仅支持 `cn-beijing`（见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)） |
| **Agent** | `model.id`, `system_prompt`（REST 为 `system`）, `skills` | `skills` 为 Skill 版本数组，格式：`[{"skill_id": "sk_xxx", "version": 1}]` |
| **Environment** | `config.type` | 取值为 `"cloud"`（默认）或 `"local"`（受限可用），更新为全量替换语义 |
| **Session** | `agent`, `environment_id` | 创建时锁定 Agent 当前 `version` 与 Environment 快照；`agent` 值为 `agent_id` 字符串 |
| **Event** | `input` 数组 | 消息结构需符合 `role`/`type`/`content` 标准（如 `user_message`），`content` 支持文本、文件引用等 |

## 使用方式

1. **认证与初始化**：设置 `DASHSCOPE_API_KEY` 环境变量，并构造 Endpoint：`https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`；
2. **资源创建顺序**（不可逆依赖）：
   - 先创建 `Skill`（若需工具能力）→ 上传 `File`（若需挂载或传入内容）→ 创建 `Agent`（引用 Skill 与 File）→ 创建 `Environment` → 创建 `Session`；
3. **任务执行流程**：
   - `POST /sessions/{session_id}/events` 提交用户消息；
   - `GET /sessions/{session_id}/events/stream` 建立 SSE 长连接，监听 `session_status` 与 `message` 事件；
   - 会话状态变更（如 `running` → `idle`）通过 `session_status` 字段推送；
4. **SDK 推荐**：Python 使用 `dashscope>=1.26.2`，Java 使用 `dashscope-sdk-java>=2.22.24`，避免因版本过低导致 `AgentStudioClient` 初始化失败（参见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)）。

## 限制和注意事项

- **配额限制**：单文件上传上限 20 MB，工作空间总容量 100 GB，文件保留期 30 天（见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)）；
- **版本与快照**：Agent 更新自动递增 `version` 并需乐观锁校验；Environment 更新为全量替换，已绑定 Session 仍使用创建时的快照；
- **状态与清理**：
  - `archive` 为软操作（`archived_at` 记录时间），归档后资源仍可查询，但不可新建 Session；
  - `delete` 为硬操作（如 `DELETE /environments/{id}`），不可恢复；
- **安全约束**：Skill 上传后必须通过安全扫描（`status: active`）才可挂载；File 须为 `available` 状态才可挂载或作为消息内容；
- **事件流可靠性**：SSE 连接中断后需客户端自行重连并从断点续订（服务端不保证事件重放），建议结合 `x-request-id` 定位问题。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


