# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的智能体托管运行时服务，由平台统一管理会话生命周期、执行沙箱、工具调用与事件流。开发者通过 REST API 或官方 SDK 创建 Agent、Environment、Session 等资源，并以事件驱动方式与智能体交互。所有请求需通过 API Key 鉴权，基地址按工作空间与地域动态生成。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-plus` 等百炼已开放的推理模型（详见 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)），模型 ID 通过 `model.id` 字段指定。
- **核心资源**：
  - `Agent`：封装模型、系统提示词、技能（Skill）与工具配置；每次更新自动递增 `version`，会话创建时锁定快照版本。
  - `Environment`：定义执行沙箱类型（如 `"type": "cloud"`）及预装依赖，可被多个 Session 复用。
  - `Session`：绑定 Agent 快照与 Environment 的运行实例，状态机为 `idle` → `running` → `idle`/`terminated`。
  - `Skill`：以 ZIP 包封装的工具组合，上传后需通过安全扫描（状态为 `active` 才可挂载），挂载时必须显式指定 `version`。
  - `File`：支持上传至工作空间（最大 20 MB），经审核为 `available` 后可用于消息内容或挂载至 Session 沙箱。

> **注意**：文档 2 的快速开始示例中使用 `model: "qwen-plus"`（字符串），而文档 1 的 API 总览中明确要求 `model` 为对象结构 `{"id": "qwen-plus"}`。实际请求体必须遵循文档 1 的格式，否则返回 400 错误 —— 请以 [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中的字段定义为准。

## 关键参数

| 资源 | 关键字段 | 说明 |
|------|----------|------|
| `Agent` | `model.id`, `system`, `skills: [{skill_id, version}]` | `model` 必须为对象；`skills` 中每个技能需指定 `version`（不支持 `latest`） |
| `Environment` | `config.type` | 当前仅支持 `"cloud"`；更新为全量替换，缺省字段将被清空 |
| `Session` | `agent`, `environment_id` | 创建时即绑定 Agent 快照与 Environment 快照，不可变更 |
| `Event`（发送） | `input: [{role, type, content}]` | `content` 支持文本、图像等多模态；`role` 仅支持 `"user"`（工具回执由平台自动注入） |
| `File` | 上传使用 `multipart/form-data` | 不支持 JSON body；响应返回 `file_id` 用于后续 Skill 创建或消息引用 |

## 使用方式

1. **前置准备**：开通百炼、创建 API Key 并设置环境变量 `DASHSCOPE_API_KEY`，获取工作空间 ID（如 `ws_xxxxxxxxxxxx`）和地域（当前仅 `cn-beijing`）[API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。
2. **端点构造**：基地址为 `https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`。
3. **典型流程**（参考 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)）：
   - 创建 Agent（含模型与系统提示）
   - 创建 Environment（定义沙箱）
   - 创建 Session（绑定二者）
   - `POST /sessions/{session_id}/events` 提交用户消息
   - `GET /sessions/{session_id}/events/stream` 订阅 SSE 流接收 `session_status` 及执行结果
4. **SDK 要求**：Python SDK ≥ v1.26.2，Java SDK ≥ v2.22.24；旧版本需强制重装升级。

## 限制和注意事项

- **配额限制**：单文件 ≤ 20 MB，工作空间总容量 ≤ 100 GB，文件保留期 30 天（超期可能被清理）[File](../../raw/application-api-reference/managed-agents-api/files-api.md)。
- **状态语义**：
  - `archive` 为软操作（归档后仍可查，已绑定资源不受影响），`delete` 为硬删除（不可恢复）。
  - Environment 更新不影响已绑定的运行中 Session（使用创建时的快照）；Agent 更新后新 Session 自动使用新版，旧 Session 保持原版。
- **安全约束**：
  - Skill 和 File 均需通过安全扫描，状态非 `active` 或 `available` 时不可使用。
  - Skill 挂载必须指定具体 `version`，上传新版本不影响已挂载的 Agent。
- **事件流**：SSE 响应头需包含 `Accept: text/event-stream`；客户端应监听 `session_status` 字段判断会话终态（`idle` 或 `terminated`）。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)
- [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)
- [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md)
- [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)
- [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)
- [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md)
- [File](../../raw/application-api-reference/managed-agents-api/files-api.md)


