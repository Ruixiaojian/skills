# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、沙箱环境、工具执行与事件流。开发者通过 REST 或 SDK 调用，可快速创建、部署和运行具备多步推理与[工具调用](../concepts/tool-use.md)能力的智能体。所有资源均按工作空间隔离，需通过 API Key 鉴权访问。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼托管模型，如 `qwen-plus`（见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 示例），不支持自定义模型或外部模型接入。
- **核心功能模块**：
  - **Agent**：定义模型、系统提示词、工具集与技能挂载；支持版本化管理与软归档（详见 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)）。
  - **Environment**：配置执行沙箱类型（如 `"type": "cloud"`）与预装依赖，独立于 Agent 管理，可被多个 Session 复用。
  - **Session**：绑定 Agent 版本与 Environment 快照的一次运行实例，状态机驱动（`idle` → `running` → `idle`/`terminated`）。
  - **Event**：支持同步发送用户消息、中断指令、工具回填结果，并通过 SSE 流式接收执行过程事件（含 `session_status` 变更）。
  - **File**：上传后经安全审核（状态为 `available` 才可用），可用于消息内容（图像/音频）或挂载至沙箱供工具读写。
  - **Skill**：以 zip 包封装工具组合，上传后需通过安全扫描（状态 `active` 后方可挂载），挂载时必须指定具体版本号（不支持 `latest`）。

> **注意**：文档 1 中列出的 `/skills/{skill_id}/versions/{version}/download` 端点返回的是 OSS 预签名 URL，而文档 7 描述其路径为 `/skills/{skill_id}/versions/{version}/content`；实际应以文档 7 的路径为准，文档 1 的路径已过时。

## 关键参数

- **Endpoint**：`https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`，其中 `workspace_id`（如 `ws_xxxxxxxxxxxx`）和 `region`（当前仅支持 `cn-beijing`）需拼接生成。
- **鉴权**：所有请求必须携带 `Authorization: Bearer <your-api-key>` Header。
- **Agent 创建参数**：必需字段包括 `name`、`model.id`（字符串，如 `"qwen-plus"`）、`system`（系统提示词）；可选 `skills`（技能版本列表，格式为 `[{ "id": "sk_xxx", "version": 1 }]`）。
- **Session 创建参数**：必需 `agent`（Agent ID）与 `environment_id`（Environment ID）。
- **Event 发送参数**：`input` 字段为消息数组，每条消息需含 `role`（`user`/`assistant`/`tool`）、`type`（`message`/`tool_result`）及 `content`（文本或富媒体数组）。
- **分页参数**：列表接口支持 `limit`（默认 20，最大 100）与 `page`（或使用响应中的 `next_page`）。

## 使用方式

1. **准备环境**：开通百炼、创建 API Key 并导出为 `DASHSCOPE_API_KEY`，获取工作空间 ID（见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）。
2. **创建基础资源**：
   - 调用 `POST /agents` 创建 Agent（建议复用）；
   - 调用 `POST /environments` 创建 Environment（建议复用）；
   - 调用 `POST /sessions` 绑定二者，获得 Session ID。
3. **触发执行**：向 `POST /sessions/{session_id}/events` 提交用户消息事件。
4. **接收结果**：通过 `GET /sessions/{session_id}/events/stream` 建立 SSE 连接，监听 `session_status` 和 `content` 类型事件，直至状态变为 `idle` 或 `terminated`。
5. **SDK 推荐**：Python 使用 `dashscope>=1.26.2`，Java 使用 `dashscope-sdk-java>=2.22.24`（见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)）。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，其他 region 不可用。
- **文件限制**：单文件直传上限 20 MB，工作空间总容量上限 100 GB，保留期 30 天（超期可能自动清理）。
- **版本锁定**：Session 创建时即锁定 Agent 和 Environment 的快照；后续更新不影响已有 Session，但新 Session 将使用最新版本。
- **技能挂载**：必须指定 Skill 的具体 `version`，挂载后即使上传新版本也不会自动生效。
- **归档语义**：Agent、Environment、Session 的归档均为软操作（`archived_at` 字段标记），不影响已运行中的实例，但禁止用于新建 Session。
- **删除语义**：Environment 和 File 的删除为硬删除（不可恢复）；Skill 删除将清除其全部版本，但已挂载该 Skill 旧版本的 Agent 不受影响（见 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)）。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


