# application call

`application call` 是指通过 API 调用阿里云百炼平台已发布的应用（包括新版智能体、旧版智能体、工作流等），向其提交输入并获取模型或流程处理后的输出。调用需提供有效的 `APP ID` 和可选的 `Workspace ID`，支持同步、异步、流式等多种模式，并兼容 DashScope SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)。核心能力覆盖单轮/多轮对话、多模态输入（文本、图像、文件）及自定义参数传递。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体、工作流三类应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **调用协议**：提供两种主流接口：
  - **DashScope 原生 API**：路径为 `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`，适用于对性能和控制力要求较高的场景；
  - **OpenAI 兼容 Responses API**：路径为 `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`，支持复用 OpenAI 生态代码，详见 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md) 和 [异步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **多模态能力**：
  - 文本输入（必选）；
  - 图像输入：需选用通义千问 VL 系列模型，并在应用中配置“自定义处理”（智能体）或 `imageList` 入参（工作流）；
  - 文件输入：仅智能体应用支持，需配置“全文引用”或“切片检索”；
- **会话管理**：
  - DashScope API 通过 `session_id` 维持多轮上下文（有效期 1 小时）；
  - Responses API 通过传入完整 `messages` 数组实现多轮对话，当前不支持基于 `pre_response_id` 或 `conversation_id` 的自动上下文延续。

> **注意**：文档 3 和文档 2 均声明“仅适用于华北2（北京）地域”，但文档 1 明确指出在德国（法兰克福）、新加坡、日本（东京）等地域调用子业务空间下的应用时也必须提供 `Workspace ID`，且该 ID 是对应地域 [Base URL](https://help.aliyun.com/zh/model-studio/regions/) 的组成部分。因此，地域限制实际取决于所选 API 路径与业务空间归属，而非绝对限定于北京。

## 关键参数

| 参数名 | 类型 | 是否必选 | 说明 |
|--------|------|----------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面复制获取；HTTP 调用时需嵌入 URL 路径。 |
| `workspace_id` | string | 条件必选 | 仅当应用位于**子业务空间**，或部署在**德国（法兰克福）、华北2（北京）、新加坡、日本（东京）** 地域时必需；获取方式见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` | string \| array | 是 | 核心输入内容：<br>- 字符串：单轮纯文本（如 `"你是谁？"`）；<br>- 数组：多轮消息或含多模态内容（`input_text`/`input_image`/`input_file`）。 |
| `stream` | boolean | 否（默认 `false`） | 仅 Responses API 支持；设为 `true` 启用[流式输出](../concepts/streaming-output.md)，**工作流应用需在结束节点启用“[流式输出](../concepts/streaming-output.md)”开关并重新发布**。 |
| `background` | boolean | 否（默认 `false`） | 仅 Responses API 支持；设为 `true` 切换为异步模式，立即返回任务 ID；**异步调用不支持 `stream=true`**。 |
| `biz_params` | object | 否 | 仅 Responses API 支持；用于传递应用内预定义的**自定义参数**（如 `{"city": "北京"}`），参数名与类型须与应用配置严格一致。 |

## 使用方式

### 1. 凭证准备
- 获取 `APP ID` 和（如需）`Workspace ID`：参考 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)；
- 获取并安全配置 `DASHSCOPE_API_KEY`：推荐通过环境变量（如 `DASHSCOPE_API_KEY`）注入，**禁止硬编码到生产代码中**。

### 2. 调用示例（任选一种）
- **DashScope SDK（推荐）**：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？"
  )
  ```
- **Responses API（OpenAI 兼容）**：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/YOUR_APP_ID/compatible-mode/v1/"
  )
  response = client.responses.create(input="你是谁？")
  ```
- **HTTP/curl**：
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"input": {"prompt": "你是谁？"}}'
  ```

### 3. 多轮与异步处理
- **多轮对话（DashScope）**：首次调用不传 `session_id`，响应中提取 `response.output.session_id`，后续请求携带该值；
- **异步任务（Responses API）**：设置 `background=True` 创建任务，获 `task_id` 后轮询 `client.responses.retrieve(task_id)` 直至状态为 `completed`/`failed`/`cancelled`。

## 限制和注意事项

- **地域与权限限制**：
  - `Workspace ID` 仅在子业务空间及特定地域（法兰克福、北京、新加坡、东京）下强制要求；
  - 查询所有 `Workspace ID` 需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号，普通子账号仅可见已加入的空间 —— 详情见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **功能约束**：
  - 异步调用（`background=true`）**不支持[流式输出](../concepts/streaming-output.md)（`stream=true`）**；
  - 文件输入（`input_file`）**仅智能体应用支持**，工作流暂不支持；
  - 响应中的 `usage` 字段（token 统计）在部分场景下可能为空，不应作为计费依据。
- **安全与最佳实践**：
  - `API Key` 必须通过环境变量或密钥管理服务注入，严禁明文写入代码或日志；
  - 生产环境应实现重试、超时、错误码分类（参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)）等健壮性逻辑；
  - 多轮对话时，若使用 Responses API，务必每次传递完整历史 `messages`，因上下文自动延续功能尚未上线。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)


