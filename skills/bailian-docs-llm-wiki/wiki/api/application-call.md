# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者可通过 OpenAI 兼容的 Responses API 或原生 DashScope API 两种方式发起同步或异步请求，支持文本、图像、文件等[多模态](../concepts/multimodal.md)输入，并可复用现有 SDK 生态快速集成。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流三类应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **调用模式**：提供同步调用（即时响应）与异步调用（长任务提交+轮询）两种模式，分别适用于实时交互和耗时任务场景。
- **[多模态](../concepts/multimodal.md)能力**：
  - 文本输入：单轮/多轮对话；
  - 图像输入：需选用通义千问 VL 系列模型，并在应用中配置为“自定义处理”（智能体）或 `imageList` 入参（工作流）；
  - 文件输入：仅智能体应用支持，需启用“全文引用”或“切片检索”文件处理方式；
  - [流式输出](../concepts/streaming-output.md)：仅同步调用支持，且工作流应用需在结束节点启用流式开关并重新发布。

> **注意**：文档 4 和文档 5 均描述了 `/api/v1/apps/{APP_ID}/completion` 接口，但文档 4 明确限定为“新版智能体应用”，而文档 5 未作此限定且标题为“智能体**与**工作流”，二者适用范围存在不一致。实际使用中，请以应用创建类型为准，并参考 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 中的明确约束。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，从控制台[应用管理](https://bailian.console.aliyun.com/#/app-center)页面获取；若应用位于子业务空间，还需传入 `workspace_id`（见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)） |
| `input` / `prompt` | string 或 array | 是 | 同步调用（Responses API）使用 `input`，支持字符串（单轮）或消息数组（多轮/[多模态](../concepts/multimodal.md)）；DashScope API 使用 `prompt` 字符串（单轮）或 `messages` 数组（多轮） |
| `stream` | boolean | 否 | 仅同步调用支持，设为 `true` 启用[流式输出](../concepts/streaming-output.md)；异步调用不支持该参数（见 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)） |
| `background` | boolean | 否 | 设为 `true` 则转为异步调用，立即返回任务 ID；默认 `false`（同步） |
| `biz_params` | object | 否 | 用于向工作流或智能体传递自定义参数（如城市名、索引值），需与应用内定义的参数名和类型严格一致 |
| `session_id` | string | 否 | DashScope API 多轮对话必需，首次调用不传，后续请求携带上一轮响应中的 `session_id` 即可延续上下文 |

## 使用方式

- **同步调用（Responses API）**  
  Endpoint：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  适用于低延迟场景，如聊天界面。示例（Python）：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/"
  )
  response = client.responses.create(input="你好")
  ```

- **异步调用（Responses API）**  
  在同步请求基础上增加 `background=True`，再通过 `retrieve(task_id)` 查询结果。适用于报告生成、批量处理等长耗时任务（见 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)）。

- **DashScope API（HTTP/SDK）**  
  Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  提供更底层控制，支持 `session_id` 管理多轮会话，推荐用于需要精细状态管理的场景。

## 限制和注意事项

- **地域限制**：所有文档均明确指出当前仅支持华北2（北京）地域，其他地域（如德国法兰克福、新加坡）调用需额外传入 `workspace_id`，且其 Base URL 不同（见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)）。
- **凭证获取**：`APP ID` 和 `Workspace ID` **仅支持控制台手动获取**，不支持 API 或 CLI 查询。
- **权限要求**：查询全部业务空间需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号；普通子账号仅能查看已加入的业务空间。
- **上下文管理**：Responses API 当前**不支持**基于 `pre_response_id` 或 `conversation_id` 的上下文自动续接，必须显式传递完整历史消息数组；DashScope API 则通过 `session_id` 实现。
- **流式与异步互斥**：`stream=true` 与 `background=true` **不可同时设置**，否则将报错（见 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)）。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)


