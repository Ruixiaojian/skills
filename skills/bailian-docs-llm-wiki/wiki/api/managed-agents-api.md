# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，负责会话生命周期管理、沙箱环境调度、工具执行与事件流编排。开发者通过 REST 或 SDK 调用，可快速构建具备[长期记忆](../concepts/long-term-memory.md)、多步推理与工具调用能力的智能体应用。所有资源均按工作空间隔离，需通过 API Key 鉴权。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼托管模型，如 `qwen-plus`、`qwen-max` 等（具体列表以控制台为准）。模型 ID 在创建 Agent 时通过 `model.id` 字段指定，详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。
- **核心功能模块**：
  - **Agent**：定义模型、系统提示词、技能（Skill）与工具配置；支持版本化管理与软归档。
  - **Environment**：声明运行沙箱类型（如 `"cloud"`）、预装依赖与安全策略；可被多个 Session 复用。
  - **Session**：绑定 Agent 快照与 Environment 快照的一次运行实例，状态机驱动（`idle` → `running` → `idle`/`terminated`）。
  - **Event**：支持同步发送用户消息、中断指令、工具审批回执，并通过 SSE 流式接收执行过程事件（含 `session_status` 变更）。
  - **Skill**：以 ZIP 包封装的工具组合，上传后需通过安全扫描（`checking` → `active`/`rejected`），挂载时必须指定精确版本号。
  - **File**：支持上传 ≤20 MB 文件，用于消息内容（图像/音频）或挂载至 Session 沙箱；审核通过后状态为 `available` 才可使用。

> **注意**：文档 2 的 Bash 示例中 `config: {"type": "cloud"}` 与文档 4 中 Environment 的 `config` 字段描述一致，但文档 4 未明确列出其他合法 `type` 值（如 `local`、`docker`）。实际可用类型请以 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md) 文档最新说明为准，避免硬编码未声明类型。

## 关键参数

| 参数 | 位置 | 说明 | 示例 |
|------|------|------|------|
| `Authorization` | Header | API Key 鉴权凭证 | `Bearer sk-xxx` |
| `workspace_id` | Endpoint 路径 | 工作空间 ID，从控制台获取 | `ws_xxxxxxxxxxxx` |
| `region` | Endpoint 路径 | 当前仅支持 `cn-beijing` | `cn-beijing` |
| `agent.id` & `environment_id` | `/sessions` 请求体 | 创建 Session 时必需，绑定快照 | `"agent_xxx"`, `"env_xxx"` |
| `version` | `/agents/{id}` 查询参数 或 `/agents/{id}` 更新请求体 | Agent 版本号，用于乐观锁与历史版本查询 | `?version=2`, `"version": 3` |
| `file_id` | `/skills` 或 `/sessions/events` 请求体 | 审核通过（`available`）的文件 ID，用于技能上传或消息附件 | `"file_xxx"` |

## 使用方式

1. **准备环境**：开通百炼，[创建 API Key](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)，获取 `workspace_id`，并设置 `DASHSCOPE_API_KEY` 环境变量。
2. **创建基础资源**：
   - 调用 `POST /agents` 创建 Agent（指定 `model.id`、`system` 等）；
   - 调用 `POST /environments` 创建 Environment（指定 `config.type`）；
   - 调用 `POST /sessions` 绑定二者，获得 `session_id`。
3. **交互与流式消费**：
   - 向 `POST /sessions/{session_id}/events` 发送用户消息（`input` 字段为消息数组）；
   - 通过 `GET /sessions/{session_id}/events/stream` 建立 SSE 连接，实时接收 `session_status` 和执行结果事件。
4. **SDK 推荐**：Python 使用 `dashscope>=1.26.2`，Java 使用 `dashscope-sdk-java>=2.22.24`，详见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 中的端到端示例。

## 限制和注意事项

- **配额限制**：单文件 ≤20 MB；工作空间总存储 ≤100 GB；文件保留期 30 天，超期可能被自动清理（见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)）。
- **状态一致性**：
  - Agent/Environment 更新均为**全量替换**，更新请求体必须包含当前 `version` 作为乐观锁，否则返回 409。
  - Session 创建时锁定 Agent 与 Environment 的**当时快照**，后续更新不影响已运行会话。
- **安全约束**：
  - Skill 与 File 上传后需经安全扫描，仅 `active` 或 `available` 状态才可挂载或引用。
  - Skill 挂载到 Agent 时必须指定精确 `version`，不支持 `latest` 别名。
- **删除行为**：
  - `archive` 为软操作（保留数据，不可新建会话），`delete` 为硬操作（不可恢复）。
  - 删除 Environment 或 Skill 不影响已绑定的运行中 Session 或已挂载的 Agent。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)


