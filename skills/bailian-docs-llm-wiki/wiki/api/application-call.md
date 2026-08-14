# application call

`application call` 是指通过 API 调用阿里云百炼平台已发布的应用（包括新版智能体、旧版智能体、工作流等）的核心能力。开发者可使用 DashScope SDK、OpenAI 兼容 SDK 或原生 HTTP 请求，向指定应用发送输入并获取结构化响应。调用需提供有效的 `APP ID` 和（在必要时）`Workspace ID`，并遵循对应协议的参数规范与地域限制。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体、工作流三类应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **调用模式**：
  - **同步调用**：适用于实时交互场景，API 阻塞等待结果返回，支持[流式输出](../concepts/streaming-output.md)（`stream=true`），但仅限工作流应用在发布时启用流式开关后生效 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
  - **异步调用**：适用于耗时较长任务（如多步骤工具链执行），立即返回任务 ID，后续通过轮询查询状态；**异步模式不支持[流式输出](../concepts/streaming-output.md)**。
- **输入模态**：支持纯文本、多轮对话消息数组、图像（`input_image`）、音频/文档等文件（`input_file`，仅智能体应用支持）。

> **注意**：文档 2 和文档 3 均声明“本文档仅适用于华北2（北京）地域”，但文档 1 明确指出在德国（法兰克福）、新加坡、日本（东京）等非北京地域调用子业务空间下的应用时，`Workspace ID` 是 Base URL 的组成部分。这意味着跨地域调用能力实际存在，但部分 API 文档未完整覆盖地域适配说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)中获取。 |
| `workspace_id` | string | 条件必填 | 仅当应用位于**子业务空间**，或部署在**德国（法兰克福）、华北2（北京）、新加坡、日本（东京）** 地域时必需，用于构造请求 URL 或作为 Header。详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` | string \| array | 是 | 核心输入内容：<br>• 字符串：单轮文本（如 `"你是谁？"`）；<br>• 消息数组：支持 `system`/`user`/`assistant` 角色，含 `input_text`/`input_image`/`input_file` 等多模态内容。 |
| `stream` | boolean | 否（默认 false） | 同步调用下启用流式响应；工作流应用需在发布前于结束节点开启流式开关。 |
| `background` | boolean | 否（默认 false） | 设为 `true` 启用异步调用，返回任务 ID；与 `stream=true` 互斥。 |
| `biz_params` | object | 否 | 用于传递应用内定义的**自定义参数**（如城市名、索引值），需与应用配置的参数名和类型严格一致。 |

## 使用方式

### 1. 凭证准备
- 获取 `APP ID` 和（如需）`Workspace ID`：通过控制台手动复制，**不支持 API 或 CLI 查询** [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- 获取 `DASHSCOPE_API_KEY`：在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)中创建并配置到环境变量（推荐）或代码中（不建议生产环境硬编码）。

### 2. 接口选择与调用
- **DashScope SDK（推荐）**：  
  Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  示例（Python）：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？"
  )
  ```

- **OpenAI 兼容 SDK（Responses API）**：  
  - 同步：`base_url = "https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/"`  
  - 异步：同 base_url，但 `create` 时设 `background=True`。  
  示例（Python 同步）：
  ```python
  from openai import OpenAI
  client = OpenAI(base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/YOUR_APP_ID/compatible-mode/v1/", api_key=api_key)
  response = client.responses.create(input="你是谁？")
  ```

- **HTTP 原生调用**：  
  - DashScope：`curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  - Responses API：`curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`

### 3. 多轮对话
- **DashScope 方式**：通过 `session_id` 维护会话，首次响应返回 `session_id`，后续请求携带该值即可延续上下文（有效期 1 小时）。
- **Responses API 方式**：直接在 `input` 中传入完整消息历史数组（`messages`），无需显式管理 session。

## 限制和注意事项

- **地域限制**：DashScope API（`/v1/apps/...`）和 Responses API（`/v2/apps/...`）当前均**仅支持华北2（北京）地域**，其他地域暂不可用。
- **Workspace ID 使用场景**：当应用位于子业务空间，或部署在德国（法兰克福）、新加坡、日本（东京）时，`Workspace ID` 为必需参数，且是 Base URL 的一部分；默认业务空间下的北京地域应用可省略 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **权限要求**：查询所有业务空间 ID 需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号；普通子账号仅能查看已加入的业务空间。
- **异步限制**：[异步任务](../concepts/async-task.md)不支持 `stream=true`，且需自行实现轮询逻辑（如每 2 秒调用 `retrieve`）。
- **参数一致性**：`biz_params` 中的键名必须与应用内「开始」节点定义的自定义参数名完全一致，否则参数将被忽略。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)


