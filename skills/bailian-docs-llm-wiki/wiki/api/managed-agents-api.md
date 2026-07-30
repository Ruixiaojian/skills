# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、沙箱执行环境、工具调用与事件流。开发者通过 REST 或 SDK 创建 Agent、Environment、Session 等资源，并以事件驱动方式与智能体交互。所有请求需通过 API Key 鉴权，且严格绑定工作空间与地域。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼托管大模型（见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 示例），不支持自定义模型或外部模型接入。
- **核心功能模块**：
  - `Agent`：封装模型、系统提示词、工具列表与技能挂载配置，支持版本化管理与软归档；
  - `Environment`：定义沙箱类型（如 `"type": "cloud"`）与预装依赖，独立于 Agent 生命周期，可被多 Session 复用；
  - `Session`：绑定 Agent 版本快照与 Environment 快照的运行实例，状态机驱动（`idle` → `running` → `idle`/`terminated`）；
  - `Event`：支持用户消息、工具调用审批、函数结果回填等原子事件，提供 SSE 流式订阅；
  - `File`：作为独立资源上传（上限 20 MB），经安全审核后可用于消息内容或挂载至沙箱；
  - `Skill`：以 ZIP 包形式封装工具组合，上传后需通过安全扫描（状态为 `active` 才可挂载），挂载时必须指定具体版本号（不支持 `latest`）。

> **注意**：文档 1 中列出的 `/skills/{skill_id}/versions/{version}/download` 端点返回的是 OSS 预签名 URL，而文档 7 明确说明该 URL 有效期为 2 小时；但文档 1 的表格中未标注此时效限制，实际使用应以 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md) 文档为准。

## 关键参数

- **Endpoint 格式**：`https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`，其中 `region` 当前**仅支持 `cn-beijing`**（见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）。
- **鉴权方式**：HTTP Header `Authorization: Bearer <your-api-key>`，一个 API Key 仅限访问其归属工作空间内资源。
- **分页参数**：列表接口（如 `/agents`, `/sessions`）支持 `limit`（默认 20，最大 100）和 `page`（首次不传，后续传 `next_page`）。
- **Agent 版本控制**：更新 Agent 时请求体必须包含当前 `version` 字段用于乐观锁校验，失败返回 409；历史版本可通过 `GET /agents/{id}?version=N` 查询。
- **File 审核状态**：上传后 `status` 为 `checking`，仅当变为 `available` 后才可被引用或挂载（见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)）。

## 使用方式

1. **前置准备**：开通百炼服务，创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`；获取工作空间 ID（形如 `ws_xxxxxxxxxxxx`）。
2. **资源创建顺序**（推荐复用）：
   - 创建 `Agent`（含模型、system [prompt](../guides/prompt.md)、[skill](../guides/skill.md)s 列表）；
   - 创建 `Environment`（指定沙箱类型及依赖）；
   - 创建 `Session`（绑定 agent_id 和 environment_id）；
3. **任务执行**：
   - 调用 `POST /sessions/{session_id}/events` 提交用户消息（格式为 `input: [{"role":"user","type":"message","content":[...]}`）；
   - 通过 `GET /sessions/{session_id}/events/stream` 建立 SSE 连接，监听 `session_status` 变更及 `message` 类型事件；
4. **SDK 接入**：Python SDK 要求 v1.26.2+，Java SDK 要求 v2.22.24+；初始化 Client 时需显式传入 `workspace` 和 `region`（见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)）。

## 限制和注意事项

- **地域限制**：API 仅在 `cn-beijing` 地域可用，其他 region 不支持（文档 1 与文档 2 均明确限定）。
- **配额限制**：
  - 单文件上传上限 20 MB，工作空间总容量上限 100 GB，文件保留期 30 天（见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)）；
  - Skill ZIP 包无明确大小限制，但需通过安全扫描，`rejected` 状态会附带详细错误路径。
- **状态与生命周期**：
  - `Environment` 删除为硬删除（不可恢复），而归档为软操作（已绑定会话仍可用）；
  - `Session` 归档即进入 `terminated` 终态，不可再发送事件；删除则清除全部事件历史。
- **版本一致性**：Agent 更新后新会话自动使用最新版，但已有会话始终锁定创建时的版本；Skill 挂载后不受新版本上传影响，必须显式更新 Agent 配置才能切换版本。
- **SSE 连接**：客户端需主动处理连接中断并重试；事件流中 `session_status` 字段是判断会话是否结束的唯一可靠依据（非 HTTP 响应码）。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


