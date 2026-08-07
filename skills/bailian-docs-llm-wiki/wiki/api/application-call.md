# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者只需提供应用凭证（APP ID 及可选的 Workspace ID）、API Key 和输入内容，即可触发应用执行并获取结构化响应。该机制支持单轮/多轮对话、[多模态](../concepts/multi-modal.md)输入（文本、图像、文件）及[流式输出](../concepts/streaming-output.md)，适用于从轻量级问答到复杂任务编排的各类场景。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **调用模式**：
  - **同步调用**：适用于实时交互，立即返回结果；支持[流式输出](../concepts/streaming-output.md)（`stream=true`），但工作流应用需在结束节点启用流式开关 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
  - **异步调用**：适用于耗时任务（如报告生成、多步骤工具调用），返回任务 ID 后轮询状态；**不支持[流式输出](../concepts/streaming-output.md)** [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **输入能力**：
  - 文本：单轮字符串或符合 OpenAI Messages 格式的多轮数组。
  - 图像：需选用通义千问 VL 系列模型，并在应用中配置为“自定义处理”（智能体）或模型入参变量设为 `imageList`（工作流）。
  - 文件：仅智能体应用支持，需配置文件处理方式为“全文引用”或“切片检索”。

> **注意**：文档 2 和文档 3 均声明“仅适用于华北2（北京）地域”，但文档 1 明确指出德国（法兰克福）、新加坡、日本（东京）等地域调用子业务空间下的应用时也必须传 `Workspace ID`，且其 Base URL 已适配对应地域。因此，`application call` 实际支持多地域，但 DashScope API 的默认 endpoint 仅覆盖北京，其他地域需按文档 1 的 Base URL 规则构造请求地址。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面获取。若应用位于子业务空间或特定地域（如德国、新加坡），还需配合 `workspace_id` 使用 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` | string / array | 是 | 核心输入内容：<br>- 字符串：单轮文本，如 `"你好"`；<br>- 数组：OpenAI Messages 格式，支持 `system`/`user`/`assistant` 角色，`user` 消息的 `content` 可为纯文本或含 `input_text`/`input_image`/`input_file` 的数组。 |
| `session_id` | string | 否（多轮必需） | 用于维护会话上下文。首次调用不传，响应中返回；后续请求携带该值即可延续对话，有效期为最后一次请求后 1 小时。 |
| `stream` | boolean | 否 | 是否流式输出，默认 `false`。设为 `true` 时需客户端支持 SSE 解析；**异步调用不支持此参数**。 |
| `background` | boolean | 否 | 是否异步执行，默认 `false`。设为 `true` 时立即返回任务 ID，需后续调用 `retrieve` 查询结果。 |
| `biz_params` | object | 否 | 传递应用内定义的自定义参数（如城市名、索引值），键名与应用配置严格一致。 |

## 使用方式

### 1. 凭证准备
- 获取 `APP ID`：在[应用管理](https://bailian.console.aliyun.com/#/app-center)列表中复制目标应用 ID。
- 获取 `Workspace ID`（如需）：若应用位于子业务空间，或部署在德国、新加坡等非北京地域，需通过控制台右上角业务空间图标或[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)页面获取 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- 获取 `DASHSCOPE_API_KEY`：通过[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建并配置至环境变量。

### 2. 接口调用
- **DashScope API（推荐）**  
  Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  请求头：`Authorization: Bearer {DASHSCOPE_API_KEY}`  
  请求体示例（单轮）：
  ```json
  {
    "input": {"prompt": "你是谁？"},
    "parameters": {},
    "debug": {}
  }
  ```

- **OpenAI 兼容 Responses API（同步）**  
  Endpoint：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  请求头同上，`input` 为 Messages 数组或字符串。

- **OpenAI 兼容 Responses API（异步）**  
  在同步请求体中添加 `"background": true`，后续通过 `GET /responses/{task_id}` 查询状态。

### 3. SDK 调用
- Python：使用 `dashscope.Application.call()`（DashScope）或 `openai.OpenAI().responses.create()`（Responses API）。
- Java/Node.js/Go/C#/PHP：各语言 SDK 均提供封装方法，详见对应文档示例。

## 限制和注意事项

- **地域与 Workspace ID**：调用子业务空间应用或德国、新加坡等非北京地域模型时，`Workspace ID` 为必填项，且需作为 Base URL 的一部分 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **权限要求**：RAM 子账号需被授予 `AliyunBailianFullAccess` 或 `AliyunBailianControlFullAccess` 权限才能查询所有业务空间 ID；普通子账号仅能查看已加入的业务空间。
- **会话管理**：`session_id` 由服务端生成并返回，客户端需自行存储和传递；超时（1 小时无新请求）后失效，需重新开始会话。
- **异步限制**：`background=true` 与 `stream=true` 互斥，异步任务不支持流式输出。
- **文件与图像**：文件输入仅限智能体应用；图像输入需模型支持 VL 能力且应用已正确配置，否则返回错误。
- **凭证获取**：`APP ID` 和 `Workspace ID` **仅支持控制台手动获取**，不提供 API 或 CLI 查询接口 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


