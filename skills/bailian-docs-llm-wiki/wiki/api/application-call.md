# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者无需自行部署模型与编排逻辑，只需提供应用凭证与输入数据，即可获得结构化响应。该能力支持同步、异步及流式三种调用模式，适配实时交互、长耗时任务和渐进式输出等不同场景。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **调用协议**：
  - **DashScope 原生协议**：适用于高性能、低延迟场景，Endpoint 为 `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`。
  - **OpenAI 兼容协议（Responses API）**：便于复用现有 OpenAI 生态代码，分为同步（`/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`）与异步（`/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` + `background=true`）两种路径。
- **多模态输入**：支持文本、图像（需选用通义千问 VL 系列模型并配置自定义处理）、音频/文档文件（仅智能体应用，需配置全文引用或切片检索），具体参见 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。

> **注意**：文档 2 和文档 3 均声明“本文档仅适用于华北2（北京）地域”，但文档 1 明确指出在德国（法兰克福）、新加坡、日本（东京）等地域调用子业务空间下的应用时，`Workspace ID` 是 Base URL 的组成部分。这意味着跨地域调用能力存在，但 DashScope 原生 API 的地域限制需以最新控制台文档为准，建议优先参考 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 中的地域说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)中获取。 |
| `workspace_id` | string | 条件必填 | 子业务空间或特定地域（如法兰克福、北京、新加坡、东京）下应用的业务空间 ID，详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` | string 或 array | 是 | 核心输入内容：<br>- 字符串：单轮纯文本对话；<br>- 消息数组：支持多轮对话、图像（`input_image`）、文件（`input_file`，仅智能体）等多模态输入。 |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming-output.md)（默认 `false`）。工作流应用需在结束节点启用“[流式输出](../concepts/streaming-output.md)”开关后方可生效。 |
| `background` | boolean | 否 | 是否启用异步模式（默认 `false`）。设为 `true` 时立即返回任务 ID，后续需轮询查询结果；**异步模式不支持 `stream=true`**。 |
| `session_id` | string | 否（多轮对话） | DashScope 原生协议中用于维护会话上下文的 ID，首次请求不传，后续请求携带上一轮响应中的 `output.session_id` 即可延续对话，有效期为最后一次请求后 1 小时。 |
| `biz_params` | object | 否（自定义参数） | 用于传递工作流或智能体中预设的自定义参数（如 `{"city": "北京"}`），需与应用内参数配置严格一致。 |

## 使用方式

### 1. 凭证准备
- 获取 `APP ID` 和（如需）`Workspace ID`：通过百炼控制台 [应用管理](https://bailian.console.aliyun.com/#/app-center) 和 [业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 页面手动复制，**不支持 API 查询**（见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)）。
- 获取 `DASHSCOPE_API_KEY`：通过 [密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key) 获取，并推荐配置为环境变量 `DASHSCOPE_API_KEY`。

### 2. 调用示例
- **DashScope 同步调用（Python SDK）**：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="your_app_id",
      prompt="你是谁？"
  )
  print(response.output.text)
  ```

- **OpenAI 兼容同步调用（Python）**：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/your_app_id/compatible-mode/v1/"
  )
  response = client.responses.create(input="你是谁？")
  print(response.output[0].content[0].text)
  ```

- **OpenAI 兼容异步调用（Python）**：
  ```python
  response = await client.responses.create(
      input="请规划三天北京行程",
      background=True
  )
  task_id = response.id
  # 后续轮询 retrieve(task_id)
  ```

### 3. 在线调试
所有应用均支持在控制台 **应用卡片 → 发布 → API 调试** 页面进行可视化参数填写与即时运行，无需编码。

## 限制和注意事项

- **地域与权限**：DashScope 原生 API（`/v1/apps/...`）和 Responses API（`/v2/apps/...`）当前均明确标注“仅适用于华北2（北京）地域”。跨地域调用必须使用对应地域的 Base URL 并传入 `workspace_id`，且需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号才能查询所有业务空间 ID（见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)）。
- **异步限制**：异步调用（`background=true`）不支持[流式输出](../concepts/streaming-output.md)（`stream=true`），且任务状态需主动轮询 `retrieve` 接口获取。
- **会话管理**：DashScope 原生协议的 `session_id` 由服务端生成并返回，有效期 1 小时；OpenAI 兼容协议不提供内置会话管理，需在每次请求的 `input` 中显式传递完整消息历史。
- **参数兼容性**：`biz_params` 仅在 OpenAI 兼容协议中通过 `extra_body={"biz_params": {...}}` 传递；DashScope SDK 不直接支持该参数，需通过 `parameters` 字段或应用内配置间接实现。
- **安全实践**：生产环境中严禁硬编码 `API Key`，务必使用环境变量或密钥管理服务。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)


