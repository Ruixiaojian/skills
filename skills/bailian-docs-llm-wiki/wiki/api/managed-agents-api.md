# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、沙箱执行环境、工具调用与事件流。开发者通过 REST 接口或 SDK 创建 Agent、Environment、Session 等资源，并以事件驱动方式与智能体交互。所有操作均基于工作空间隔离，需通过 API Key 鉴权。

## 支持的模型与功能

- **模型支持**：Agent 创建时通过 `model.id` 指定模型，当前支持 `qwen-plus` 等百炼已开通的推理模型（详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）。
- **核心功能模块**：
  - `Agent`：定义智能体配置（模型、系统提示词、技能、工具），支持版本化与软归档；
  - `Environment`：定义沙箱类型（如 `"cloud"`）与预装依赖，独立于 Agent 管理，可被多会话复用；
  - `Session`：绑定 Agent 版本与 Environment 快照的一次运行实例，状态机驱动（`idle` → `running` → `idle`/`terminated`）；
  - `Event`：会话内原子操作载体，支持用户消息、工具回填、中断等，可通过 SSE 流式订阅；
  - `File`：独立文件资源，用于消息内容（图像/音频）或挂载至沙箱供工具读写；
  - `Skill`：zip 包封装的工具组合，需经安全扫描后按具体版本号挂载到 Agent。

> **注意**：文档 3 的 Bash 示例中使用 `model: {"id": "qwen-plus"}`（对象格式），而文档 2 和文档 3 的 Python SDK 示例中直接传入字符串 `"qwen-plus"`。实际 REST API 要求 `model` 字段为对象（含 `id` 字段），SDK 封装层做了简化。请以 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中的接口定义为准。

## 关键参数

- **Endpoint**：`https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`，其中 `region` 当前仅支持 `cn-beijing`；
- **鉴权**：`Authorization: Bearer <your-api-key>`，API Key 需在百炼控制台创建并配置为环境变量；
- **Agent 创建关键字段**：
  - `name`: 必填，智能体名称；
  - `model.id`: 必填，模型 ID（如 `"qwen-plus"`）；
  - `system`: 可选，系统提示词；
  - `skills`: 数组，每个元素为 `{skill_id: "...", version: N}`，**必须指定整数版本号，不支持 `"latest"`**（见 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)）；
- **Session 创建关键字段**：
  - `agent`: Agent ID（会自动锁定当前最新版本）；
  - `environment_id`: Environment ID；
- **Event 发送关键字段**：
  - `input`: 消息数组，每条消息含 `role`（`user`/`assistant`）、`type`（`message`）、`content`（文本或文件引用）；
- **分页参数**：`limit`（默认 20，最大 100）、`page`（首次省略，后续传 `next_page`）。

## 使用方式

完整调用流程为五步（参考 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)）：

1. **创建 Agent**：定义模型与行为逻辑，获得 `agent_xxx`；
2. **创建 Environment**：定义沙箱类型（如 `{"type": "cloud"}`），获得 `env_xxx`；
3. **创建 Session**：绑定 Agent 与 Environment，获得 `sesn_xxx`，初始状态为 `idle`；
4. **发送 Event**：向 Session 提交用户消息（`POST /sessions/{session_id}/events`）；
5. **订阅 SSE 事件流**：`GET /sessions/{session_id}/events/stream`，监听 `session_status` 变更及工具调用、响应等事件，直至状态变为 `idle` 或 `terminated`。

SDK 推荐使用：Python SDK ≥ v1.26.2，Java SDK ≥ v2.22.24。旧版本需重新安装升级（见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）。

## 限制和注意事项

- **配额限制**：
  - 单文件上传上限 **20 MB**，工作空间总容量 **100 GB**，文件保留期 **30 天**（见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)）；
  - 分页 `limit` 最大值为 **100**；
- **版本与快照**：
  - Agent 更新为全量替换 + 乐观锁（需携带当前 `version`），成功后 `version` 自动 +1；会话创建时锁定 Agent 版本，后续更新不影响已有会话；
  - Environment 更新同样为全量替换，已绑定会话继续使用创建时的快照；
- **归档与删除**：
  - Agent、Environment、Session 的 `archive` 均为软操作（保留数据，不可新建会话），而 `DELETE` 为硬删除（不可恢复）；
- **安全约束**：
  - File 上传后需通过安全审核（`status` 为 `available` 才可用）；
  - Skill 上传新版本后需等待扫描状态变为 `active` 方可挂载，`rejected` 状态需根据 `error_info` 修复后重传；
- **事件语义**：`POST /sessions/{session_id}/events` 仅用于注入事件（如用户输入、工具结果回填），**不触发执行**；执行由平台在收到用户消息后自动启动。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


