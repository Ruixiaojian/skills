# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者可使用 DashScope 原生 API 或 OpenAI 兼容的 Responses API 发起请求，支持文本、图像、文件等[多模态输入](../concepts/multimodal-input.md)，并可通过 `session_id` 维持多轮对话状态。所有调用均需提供有效的 `APP ID` 和 `DASHSCOPE_API_KEY`，部分场景还需 `Workspace ID`。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **多模态能力**：
  - 图像输入：需选用通义千问 VL 系列模型，并在应用中配置为“自定义处理”（智能体）或设置模型入参为 `imageList`（工作流）[同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
  - 文件输入：仅智能体应用支持，需将文件处理方式设为“全文引用”或“切片检索”。
- **交互模式**：
  - 单轮/多轮对话：DashScope API 通过 `session_id` 实现会话延续；Responses API 则需在每次请求中显式传递完整 `input` 消息数组。
  - [流式输出](../concepts/streaming-output.md)：仅同步调用支持，且工作流应用需在结束节点启用“[流式输出](../concepts/streaming-output.md)”开关并重新发布。

> **注意**：文档 2 和文档 4 均描述了 `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion` 接口，但文档 2 明确标注“仅适用于华北2（北京）地域”，而文档 4 未声明地域限制，存在潜在不一致。实际部署时请以控制台所选地域为准，并参考 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 中关于 Workspace ID 的地域要求。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在 [应用管理](https://bailian.console.aliyun.com/#/app-center) 页面复制。 |
| `input` | string / array | 是 | 核心输入内容：<br>- 字符串：单轮纯文本（如 `"你好"`）；<br>- 消息数组：支持多轮对话及多模态（`input_text`/`input_image`/`input_file`）。 |
| `session_id` | string | 否（多轮必需） | DashScope API 中用于维持会话上下文，首次调用不传，后续请求携带上一轮响应中的 `output.session_id`。 |
| `stream` | boolean | 否 | 仅同步调用支持。`true` 启用[流式输出](../concepts/streaming-output.md)；`false`（默认）返回完整结果。 |
| `background` | boolean | 否 | `true` 表示异步调用，API 立即返回任务 ID；`false`（默认）为同步调用。 |
| `biz_params` | object | 否 | 用于传递工作流或智能体中预定义的自定义参数（如 `{"city": "北京"}`），需与应用内参数名严格一致。 |

## 使用方式

### 1. DashScope 原生 API（推荐用于高性能/全功能场景）
- **Endpoint**：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
- **认证**：Header 中携带 `Authorization: Bearer {DASHSCOPE_API_KEY}`
- **SDK 调用**：Python 示例中直接使用 `Application.call(app_id=..., prompt=...)`；Java 需构造 `ApplicationParam` 对象。
- **HTTP 示例**：
  ```json
  {
    "input": { "prompt": "你是谁？" },
    "parameters": {},
    "debug": {}
  }
  ```

### 2. OpenAI 兼容 Responses API（适合复用现有 OpenAI 代码）
- **同步 Endpoint**：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
- **异步 Endpoint**：同上，但请求体中添加 `"background": true`
- **认证**：Header 中携带 `Authorization: Bearer {DASHSCOPE_API_KEY}`
- **SDK 调用**：初始化 `OpenAI(base_url=...)` 后调用 `client.responses.create(input=..., stream=..., background=...)`

### 3. 在线调试
所有应用均支持在控制台 **应用卡片 → 发布 → API 调试** 页面进行实时参数填写与执行，无需编码即可验证逻辑。

## 限制和注意事项

- **地域限制**：DashScope API（文档 2、4）和 Responses API（文档 3、5）均明确标注“仅适用于华北2（北京）地域”。若应用部署在德国（法兰克福）、新加坡等其他地域，必须提供 `Workspace ID` 且 Base URL 不同，详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **凭证获取**：`APP ID` 和 `Workspace ID` **仅支持控制台手动获取**，不提供 API 或 CLI 查询接口。
- **权限要求**：查询所有业务空间 ID 需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号；普通子账号仅能查看已加入的业务空间。
- **异步限制**：异步调用（`background=true`）**不支持流式输出**（`stream=true`），二者互斥。
- **上下文管理**：Responses API 当前不支持 `pre_response_id` 或 `conversation_id`，必须在每次请求中传递完整对话历史。
- **安全实践**：生产环境严禁硬编码 `DASHSCOPE_API_KEY`，应通过环境变量或密钥管理服务注入。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


