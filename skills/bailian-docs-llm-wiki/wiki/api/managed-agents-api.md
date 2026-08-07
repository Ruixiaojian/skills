# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、沙箱执行环境、工具调用与事件流。开发者通过 REST 或 SDK 调用，可快速构建具备[长期记忆](../concepts/long-term-memory.md)、多步推理与工具调用能力的智能体应用。所有资源（Agent、Environment、Session 等）均按工作空间隔离，支持版本控制与软归档。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼平台已接入的大模型（详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)），模型 ID 通过 `model.id` 字段指定。
- **核心功能模块**：
  - **Agent**：封装模型、系统提示词、工具列表与 Skill 挂载配置；支持版本化更新与软归档 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)。
  - **Environment**：定义沙箱类型（如 `"cloud"`）、预装依赖与网络策略；独立于 Agent 管理，可被多个 Session 复用 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)。
  - **Skill**：以 ZIP 包形式封装工具组合，上传后需通过安全扫描（状态为 `active` 才可挂载）；挂载时必须指定具体版本号，不支持 `latest` [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)。
  - **File**：支持 ≤20 MB 的文件直传，用于消息内容（图像/音频）或挂载至沙箱；审核状态为 `available` 后方可使用 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)。
  - **Session & Event**：Session 是绑定 Agent 快照与 Environment 的运行实例，状态机包括 `idle` → `running` → `idle`/`terminated`；Event 支持同步写入与 SSE 流式订阅 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)。

> **注意**：文档 1 中列出的 `/skills/{skill_id}/versions/{version}/download` 端点返回 OSS 预签名 URL，但文档 5 明确说明该 URL 有效期为 2 小时；而文档 2 的 Python 示例中未处理下载超时逻辑，实际集成时需自行缓存或重试。

## 关键参数

| 参数 | 位置 | 说明 | 示例 |
|------|------|------|------|
| `Authorization` | Header | API Key 鉴权，格式 `Bearer <your-api-key>` | `Bearer sk-xxx` |
| `workspace_id` | Endpoint path | 工作空间 ID，从控制台获取 | `ws_xxxxxxxxxxxx` |
| `region` | Endpoint path | 当前仅支持 `cn-beijing` | `cn-beijing` |
| `model.id` | Agent 创建请求体 | 必填，指定模型 ID | `"qwen-plus"` |
| `config.type` | Environment 创建请求体 | 沙箱类型，目前仅支持 `"cloud"` | `{"type": "cloud"}` |
| `input` | `/sessions/{id}/events` 请求体 | 用户消息数组，每项含 `role`、`type`、`content` | `[{"role":"user","type":"message","content":[{"type":"text","text":"..."}]}]` |
| `limit` / `page` | 列表端点查询参数 | 分页控制，默认 `limit=20`，最大 `100` | `?limit=50&page=2` |

## 使用方式

1. **准备环境**：开通百炼，创建 API Key 并导出为 `DASHSCOPE_API_KEY`；获取工作空间 ID 和地域（固定 `cn-beijing`）[API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。
2. **创建基础资源**：
   - 调用 `POST /agents` 定义 Agent（含模型、system [prompt](../guides/prompt.md)、[skill](../guides/skill.md)s）；
   - 调用 `POST /environments` 定义 Environment（沙箱配置）；
   - （可选）上传 File 并等待 `status=available`，再用于消息或沙箱挂载。
3. **启动会话**：
   - 调用 `POST /sessions` 绑定 Agent 与 Environment，获得 `session_id`；
   - 调用 `POST /sessions/{id}/events` 提交用户输入；
   - 调用 `GET /sessions/{id}/events/stream` 建立 SSE 连接，实时接收 `session_status` 与 `message` 事件。
4. **SDK 推荐**：Python 使用 `dashscope>=1.26.2`，Java 使用 `dashscope-sdk-java>=2.22.24`，避免旧版兼容问题（见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)）。

## 限制和注意事项

- **配额限制**：单文件 ≤20 MB；工作空间总存储 ≤100 GB；文件保留期 30 天，超期可能被自动清理 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)。
- **版本与快照**：
  - Agent 更新采用乐观锁（需传 `version`），成功后 `version` 自增；Session 创建时锁定 Agent 当前版本，后续更新不影响已有会话 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)。
  - Environment 更新为全量替换，已绑定的运行中 Session 仍使用绑定时的快照 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)。
- **安全约束**：
  - Skill 与 File 上传后需通过安全扫描，仅 `active` 或 `available` 状态才可使用；`rejected` 状态需根据 `error_info` 修正后重传。
- **状态管理**：
  - Session 为终态设计：`terminated` 后不可恢复；`DELETE /sessions/{id}` 为硬删除，事件历史不可恢复 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)。
- **错误排查**：所有响应携带 `x-request-id`，提工单时务必提供此 ID。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)


