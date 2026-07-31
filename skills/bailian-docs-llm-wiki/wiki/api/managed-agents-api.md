# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，负责会话生命周期管理、沙箱环境调度、工具执行协调及事件流分发。开发者通过 REST 或 SDK 创建 Agent（配置模型与系统提示）、Environment（定义执行沙箱）、Session（绑定二者并启动运行实例），再以事件驱动方式与 Agent 交互。所有资源均归属工作空间，支持版本控制、归档与分页查询。

## 支持的模型/功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼托管大模型（详见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 中的端到端示例）；不支持自定义模型 ID 或外部模型接入。
- **核心功能模块**：
  - **Agent**：封装模型、系统提示词、工具包与 Skill 列表；每次更新生成新版本，会话创建时锁定快照（[Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)）。
  - **Environment**：定义沙箱类型（如 `"cloud"`）与预装依赖；独立于 Agent 管理，可被多 Session 复用（[Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)）。
  - **Skill**：以 ZIP 包封装工具组合，上传后需通过安全扫描（状态为 `active` 才可挂载），挂载时必须指定具体 `version`（不支持 `latest`）（[Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)）。
  - **File**：支持上传图像、音频、文本等文件（单文件 ≤20 MB），审核通过（`status: "available"`）后可用于消息内容或挂载至沙箱（[File](../../raw/application-api-reference/managed-agents-api/files-api.md)）。

> **注意**：文档 2 中“可用 API”表格将 `/skills` 归类为独立资源，但实际 Skill 必须通过 Agent 的 `skills` 字段挂载才生效；直接调用 Skill API 仅完成注册与版本管理，不触发工具调用能力。

## 关键参数

- **认证与 Endpoint**：必须设置 `Authorization: Bearer <API_KEY>` 请求头；Endpoint 格式为 `https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`，其中 `region` 当前仅支持 `cn-beijing`（[API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）。
- **Agent 创建参数**：`model.id`（必填，如 `"qwen-plus"`）、`system`（系统提示词）、`skills`（Skill 版本数组，格式为 `[{"id": "skl_xxx", "version": "1"}]`）。
- **Environment 创建参数**：`config.type`（必填，目前仅 `"cloud"` 有效）；其他字段如 `config.dependencies` 尚未开放配置。
- **Session 创建参数**：`agent`（Agent ID）、`environment_id`（Environment ID）；创建后会话初始状态为 `idle`。
- **Event 发送参数**：`input` 为消息数组，每条消息含 `role`（`"user"` 或 `"assistant"`）、`type`（`"message"`）、`content`（文本或文件引用）；文件需先上传并传入 `file_id`。

## 使用方式

1. **初始化**：导出 `DASHSCOPE_API_KEY` 和 `AGENTSTUDIO_URL` 环境变量（[快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)）。
2. **资源创建**（建议复用）：
   - 调用 `POST /agents` 创建 Agent；
   - 调用 `POST /environments` 创建 Environment；
   - 调用 `POST /sessions` 绑定二者，获取 `session_id`。
3. **任务执行**：
   - 调用 `POST /sessions/{session_id}/events` 提交用户消息；
   - 调用 `GET /sessions/{session_id}/events/stream` 建立 SSE 长连接，监听 `session_status`（`running` → `idle`/`terminated`）及 `content` 事件。
4. **SDK 接入**：Python SDK ≥ v1.26.2，Java SDK ≥ v2.22.24；SDK 封装了认证、重试与流式解析逻辑（[API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）。

## 限制和注意事项

- **配额限制**：单文件上传上限 20 MB；工作空间总文件容量上限 100 GB；文件保留期 30 天（[File](../../raw/application-api-reference/managed-agents-api/files-api.md)）。
- **状态机约束**：Session 状态流转严格受限——仅 `idle` 状态可接收新消息；`running` 状态不可手动中断，需等待 Agent 自行完成或失败；`terminated` 为终态（[Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)）。
- **版本与归档语义**：
  - Agent/Environment 更新均为**全量替换**，缺省字段视为清空；已绑定的运行中 Session 使用创建时的快照，不受影响（[Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)、[Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)）。
  - 归档（`archive`）是软操作，资源仍可查询且已绑定 Session 继续运行；删除（`DELETE`）是硬操作，不可恢复。
- **安全审核**：File 与 Skill 上传后均需异步安全扫描，仅 `available`/`active` 状态才可使用；`rejected` 状态需根据 `error_info` 修正后重传。

## 来源文档

- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)


