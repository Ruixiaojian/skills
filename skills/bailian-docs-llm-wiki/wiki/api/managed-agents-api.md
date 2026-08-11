# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、执行沙箱、工具调用与事件流。开发者通过 RESTful 接口或 SDK 创建 Agent、Environment、Session 等资源，并以事件驱动方式与智能体交互。所有请求需通过 API Key 鉴权，且严格绑定至指定工作空间与地域。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼托管的 Qwen 系列模型（如 `qwen-plus`），模型 ID 通过 `model.id` 字段在创建 Agent 时指定（见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)）。
- **核心功能模块**：
  - **Agent**：定义智能体配置（模型、系统提示词、技能列表），支持版本化管理与软归档；
  - **Environment**：定义执行沙箱（如 `"type": "cloud"`），支持预装依赖，可被多 Session 复用；
  - **Session**：一次运行实例，绑定 Agent 版本快照与 Environment，状态机驱动（`idle` → `running` → `idle`/`terminated`）；
  - **Event**：支持同步发送用户消息、中断指令、工具回填等，并通过 SSE 流式接收执行过程与状态变更；
  - **File**：独立文件资源，用于消息内容（图像/音频）或挂载至沙箱供工具读写；
  - **Skill**：zip 包封装的工具组合，上传后需通过安全扫描（`checking` → `active`），挂载时必须显式指定版本号。

> **注意**：文档 2 的快速开始示例中使用 `model: "qwen-plus"` 作为字符串传入 Python SDK 的 `create()` 方法，而文档 1 的 REST 示例中使用嵌套对象 `{"id": "qwen-plus"}`。实际 REST 接口要求 `model` 字段为对象格式（含 `id` 键），SDK 封装已做适配；若直接调用 REST，请严格遵循 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中的 JSON 结构。

## 关键参数

| 资源 | 关键字段 | 说明 |
|------|----------|------|
| **Agent** | `model.id`, `system`, `skills` | `model.id` 必填；`system` 为系统提示词；`skills` 是 Skill 版本 ID 列表（如 `["skl_xxx:v1"]`） |
| **Environment** | `config.type`, `config.dependencies` | `config.type` 当前仅支持 `"cloud"`；`dependencies` 可指定 pip 包列表（如 `["pandas==2.0.3"]`） |
| **Session** | `agent`, `environment_id` | 创建时必须同时指定 Agent ID 与 Environment ID；会话锁定 Agent 当前版本快照 |
| **Event（发送）** | `input[].role`, `input[].content` | `role` 为 `"user"` 或 `"assistant"`；`content` 是消息内容数组，支持 `text`/`image_url`/`file_id` 类型 |
| **File** | `file`（multipart）、`scope`（挂载时） | 直传上限 20 MB；挂载到 Session 沙箱时生成作用域限定副本（见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)） |

## 使用方式

1. **环境准备**：开通百炼、创建 API Key 并导出为 `DASHSCOPE_API_KEY`；获取工作空间 ID（`ws_xxxxxxxxxxxx`）与地域（当前仅 `cn-beijing`）；
2. **构建 Endpoint**：拼接为 `https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`；
3. **资源创建顺序**（推荐复用）：
   - 创建 Agent（`POST /agents`）→ 获取 `agent_id`
   - 创建 Environment（`POST /environments`）→ 获取 `environment_id`
   - 创建 Session（`POST /sessions`，传 `agent` 和 `environment_id`）→ 获取 `session_id`
4. **任务执行**：
   - 发送用户消息：`POST /sessions/{session_id}/events`，携带 `input` 数组；
   - 订阅结果流：`GET /sessions/{session_id}/events/stream`（SSE，响应头 `Content-Type: text/event-stream`）；
5. **SDK 快速接入**：Python 使用 `dashscope>=1.26.2`，Java 使用 `dashscope-sdk-java>=2.22.24`，详见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 中的端到端示例。

## 限制和注意事项

- **地域与模型限制**：Endpoint 中 `region` 仅支持 `cn-beijing`；模型仅限百炼平台托管的 Qwen 系列，不支持自定义模型部署；
- **配额约束**：
  - 单文件直传 ≤ 20 MB，工作空间总容量 ≤ 100 GB，文件保留期 30 天（见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)）；
  - 分页接口 `limit` 最大为 100，`page` 默认从 1 开始；
- **状态与生命周期**：
  - Agent/Environment/Session 的“归档”均为软操作（保留数据、不可新建但已有会话仍可用）；“删除”为硬操作（不可恢复）；
  - Agent 更新需提供当前 `version` 值作乐观锁，失败返回 409；Environment 更新为全量替换，缺省字段视为清空；
- **安全与审核**：
  - 文件上传后进入 `checking` 状态，仅 `available` 状态方可引用；
  - Skill 上传后需通过安全扫描，`rejected` 状态版本不可挂载，错误详情见 `additional_properties.error_info`；
- **事件语义**：`POST /sessions/{session_id}/events` 仅注入事件，不触发执行；执行由平台在收到用户消息后自动启动；SSE 流中 `session_status` 字段反映会话状态变更（如 `"idle"` → `"running"`）。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)


