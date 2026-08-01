# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、执行沙箱、工具调用与事件流。开发者通过 REST API 或官方 SDK 创建 Agent、Environment、Session 等资源，并以事件驱动方式与智能体交互。所有请求需通过 API Key 鉴权，Endpoint 按工作空间与地域动态拼装。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼托管大模型（详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)），不支持自定义模型或外部模型接入。
- **核心功能模块**：
  - `Agent`：封装模型、系统提示词、技能（Skill）与工具配置；每次更新自动递增版本号，会话创建时锁定快照 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)。
  - `Environment`：定义执行沙箱类型（如 `"type": "cloud"`）与预装依赖，可被多个 Session 复用 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)。
  - `Skill`：以 ZIP 包形式上传工具组合，经安全扫描后挂载至 Agent；挂载时必须指定具体版本号（不支持 `latest`）[Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)。
  - `File`：支持上传 ≤20 MB 的文件，用于消息内容（图像/音频）或挂载至沙箱供工具读写；上传后需通过安全审核（状态为 `available` 才可用）[File](../../raw/application-api-reference/managed-agents-api/files-api.md)。

> **注意**：文档 2 的快速开始示例中使用 `model="qwen-plus"` 作为字符串传入，而文档 1 的 `POST /agents` 请求体示例中使用嵌套对象 `{"id": "qwen-plus"}`。实际接口要求为 **嵌套对象格式**（即 `"model": {"id": "qwen-plus"}`），文档 2 的 Python SDK 示例因封装层简化了参数，但原始 REST 接口必须遵循文档 1 的结构。

## 关键参数

| 资源 | 关键字段 | 说明 |
|------|----------|------|
| `Agent` | `model.id`, `system`, `skills` | `model.id` 必填；`system` 为系统提示词；`skills` 为技能 ID 列表，每个技能需已通过安全扫描且指定 `version` |
| `Environment` | `config.type` | 当前仅支持 `"cloud"`；其他值将导致 400 错误 |
| `Session` | `agent`, `environment_id` | 创建时必须同时指定 Agent ID 和 Environment ID；绑定后不可更改 |
| `Event`（发送） | `input[].role`, `input[].content` | `role` 仅支持 `"user"`；`content` 为消息数组，支持 `text`/`image_url`/`file_id` 类型（见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)） |
| 分页通用 | `limit`, `page`, `next_page` | `limit` 默认 20，最大 100；响应中 `next_page` 字段指示下一页，为空表示末页 |

## 使用方式

1. **准备环境**：开通百炼、创建 API Key 并导出为 `DASHSCOPE_API_KEY`，获取工作空间 ID（`ws_xxx`）和地域（当前仅 `cn-beijing`）。
2. **构建 Endpoint**：`https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`。
3. **按顺序创建资源**：
   - 创建 `Agent` → 创建 `Environment` → 创建 `Session`（绑定二者）→ 发送 `Event` 触发执行 → 订阅 `/sessions/{session_id}/events/stream` 获取 SSE 流式响应。
4. **SDK 推荐**：Python 使用 `dashscope>=1.26.2`，Java 使用 `dashscope-sdk-java>=2.22.24`；SDK 封装了鉴权、重试与流式解析逻辑，优于裸 HTTP 调用。

## 限制和注意事项

- **配额限制**：单文件 ≤20 MB；工作空间总存储 ≤100 GB；文件保留期 30 天，超期可能被自动清理 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)。
- **状态与生命周期**：
  - `Agent`/`Environment`/`Session` 的“归档”均为软操作（保留数据，不可新建会话/环境/任务），而“删除”为硬操作（不可恢复）。
  - `Environment` 更新采用全量替换，缺省字段视为清空；已绑定的运行中 Session 仍使用旧快照。
  - `Agent` 更新需携带当前 `version` 值作乐观锁，否则返回 409；历史版本可通过 `GET /agents/{id}?version=N` 查询。
- **安全约束**：
  - `Skill` 和 `File` 上传后均需通过安全扫描，状态为 `active` 或 `available` 方可使用；`rejected` 状态需根据 `error_info` 修正后重新上传。
  - `Session` 状态机严格受控：仅 `idle` 状态可接收新消息；`running` 中不可修改绑定关系；`terminated` 为终态。
- **错误处理**：所有响应含 `x-request-id` 头，提工单时必须提供该 ID 以加速问题定位。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)


