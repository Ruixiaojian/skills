# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者可选择 DashScope 原生协议或 OpenAI 兼容的 Responses API 两种方式发起请求，支持同步、异步及[流式输出](../concepts/streaming-output.md)等多种交互模式。所有调用均需提供有效的 APP ID 和 API Key，并根据应用部署位置决定是否携带 Workspace ID。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流三类应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **输入模态**：
  - 文本（单轮/多轮对话）
  - 图像（需选用通义千问 VL 系列模型并配置自定义处理或 `imageList` 入参）
  - 文件（仅智能体应用支持，需配置为“全文引用”或“切片检索”）
- **输出模式**：
  - 同步响应（默认）
  - [流式输出](../concepts/streaming-output.md)（`stream=true`，仅同步调用支持，且工作流应用需在结束节点启用流式开关）
  - 异步任务（`background=true`，返回任务 ID 后轮询结果，[异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)）

> **注意**：文档 2 和文档 5 均描述了 `/api/v1/apps/{APP_ID}/completion` 接口，但文档 2 明确限定“仅适用于华北2（北京）地域”，而文档 5 未声明地域限制，实际生产中应以文档 2 的约束为准，避免跨地域调用失败。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)中获取。若应用位于子业务空间或德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域，还需传入 `workspace_id`（见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)） |
| `input` | string / array | 是 | 核心输入内容：<br>• 字符串：单轮文本，如 `"你好"`<br>• 消息数组：支持多轮对话、图像（`input_image`）、文件（`input_file`）等多模态输入；**注意**：基于 `pre_response_id` 或 `conversation_id` 的上下文功能暂不支持，需显式传递完整历史 |
| `stream` | boolean | 否 | 是否[流式输出](../concepts/streaming-output.md)，默认 `false`；设为 `true` 时需配合 SDK 的 chunk 迭代处理 |
| `background` | boolean | 否 | 是否异步执行，默认 `false`；设为 `true` 时立即返回任务 ID，不可与 `stream=true` 同时使用 |

- **DashScope SDK 方式**（如 Python）：使用 `prompt` 字段传递文本输入，`session_id` 维持会话状态。
- **Responses API 方式**（OpenAI 兼容）：统一使用 `input` 字段，结构更灵活，支持多模态。

## 使用方式

### 1. DashScope 原生接口（推荐用于新应用）
- **Endpoint**：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
- **认证**：`Authorization: Bearer {DASHSCOPE_API_KEY}`
- **示例（Python SDK）**：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="your-app-id",
      prompt="你是谁？"
  )
  ```

### 2. OpenAI 兼容 Responses API（适合迁移现有代码）
- **同步 Endpoint**：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
- **异步 Endpoint**：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`（请求体含 `"background": true`）
- **认证**：同上，`base_url` 需拼接 `{APP_ID}`

### 3. 多轮对话
- **DashScope 方式**：首次调用不传 `session_id`，响应中返回 `session_id`；后续请求携带该值即可延续上下文。
- **Responses API 方式**：将完整消息历史数组（含 `role: "user"/"assistant"`）传入 `input`，无需维护 `session_id`。

## 限制和注意事项

- **地域限制**：DashScope 原生接口（文档 2、5）和 Responses API（文档 3、4）均明确标注“仅适用于华北2（北京）地域”，其他地域需确认控制台 Base URL 是否适配。
- **Workspace ID 规则**：调用子业务空间下的应用，或德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域的模型时，必须提供 `workspace_id`；默认业务空间下仅需 `app_id`（见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)）。
- **权限要求**：RAM 子账号查询所有业务空间 ID 需具备 `AliyunBailianFullAccess` 或 `AliyunBailianControlFullAccess` 权限，否则仅能查看当前登录空间 ID。
- **异步限制**：异步任务不支持流式输出（`stream=true` 与 `background=true` 互斥），且暂无内置取消接口，需依赖轮询状态后手动处理。
- **凭证安全**：API Key **严禁硬编码**，务必通过环境变量（如 `DASHSCOPE_API_KEY`）注入，避免泄露风险。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)


