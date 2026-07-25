# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者只需提供应用凭证（APP ID 和可选的 Workspace ID）、API Key 及输入内容，即可触发应用执行并获取结构化响应。该机制支持文本、图像、文件等[多模态输入](../concepts/multimodal-input.md)，并兼容 OpenAI 接口风格，便于快速迁移现有代码。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **调用模式**：
  - **同步调用**：适用于实时交互场景，立即返回完整结果；支持[流式输出](../concepts/streaming-output.md)（`stream=true`），但工作流应用需在结束节点启用流式开关并重新发布。
  - **异步调用**：适用于耗时任务（如长文本生成、多步骤工具调用），立即返回任务 ID，后续通过 `retrieve` 查询状态；> **注意**：异步调用不支持[流式输出](../concepts/streaming-output.md)，且 `background=true` 与 `stream=true` 互斥 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **多模态能力**：
  - 图像输入：仅限选用通义千问 VL 系列模型的智能体或工作流应用，且需按文档配置文件处理方式或模型入参变量 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
  - 文件输入：仅智能体应用支持，需在应用内选择“全文引用”或“切片检索”文件处理方式。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面获取。若应用位于子业务空间或特定地域（如德国法兰克福、华北2北京、新加坡、日本东京），还需传入 `workspace_id` [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` | string 或 array | 是 | 核心输入内容：<br>- 字符串：单轮纯文本对话；<br>- 消息数组：支持多轮对话、图像（`input_image`）、文件（`input_file`）等[多模态输入](../concepts/multimodal-input.md)。消息对象中 `role` 必须为 `user`（或 `system`），`content` 为字符串或含 `type`/`text`/`image_url`/`file_url` 的结构体。 |
| `stream` | boolean | 否 | 默认 `false`。设为 `true` 启用流式响应，适用于实时渲染场景。> **注意**：工作流应用需在流程中显式启用[流式输出](../concepts/streaming-output.md)开关并重新发布，否则将忽略该参数 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。 |
| `background` | boolean | 否 | 默认 `false`。设为 `true` 切换为异步调用，立即返回任务 ID。该参数与 `stream` 不可同时为 `true`。 |
| `biz_params` | object | 否 | 仅异步调用支持，用于传递应用内定义的自定义参数（如城市名、索引值等），键名需与应用配置完全一致 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。 |

## 使用方式

### 1. 凭证准备
- 获取 `APP ID`：在控制台 [应用管理](https://bailian.console.aliyun.com/#/app-center) 页面复制目标应用 ID。
- 获取 `Workspace ID`（如需）：若应用位于子业务空间或指定地域，需通过控制台右上角业务空间图标或 [业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 页面获取 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- 获取 `API Key`：在 [密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key) 页面创建并配置到环境变量 `DASHSCOPE_API_KEY`。

### 2. 接口调用
- **DashScope API（推荐）**  
  Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  请求体示例（JSON）：
  ```json
  {
    "input": { "prompt": "你是谁？" },
    "parameters": {},
    "debug": {}
  }
  ```

- **OpenAI 兼容 Responses API**  
  - 同步：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  - 异步：同上，但请求体中添加 `"background": true`  
  SDK 初始化示例（Python）：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/"
  )
  ```

### 3. 多轮对话管理
- **DashScope API**：使用 `session_id` 维护上下文。首次调用不传，响应中返回 `session_id`；后续请求携带该 ID 即可延续会话，有效期为最后一次请求后 1 小时。
- **Responses API**：不支持 `session_id`，需在每次请求的 `input` 数组中显式传递完整对话历史（含 `role: user/assistant` 消息）。

## 限制和注意事项

- **地域限制**：所有文档均明确标注“本文档仅适用于华北2（北京）地域”，其他地域（如德国法兰克福、新加坡）的调用需确认 Workspace ID 是否已正确嵌入 Base URL [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **权限要求**：RAM 子账号需被授予 `AliyunBailianFullAccess` 或 `AliyunBailianControlFullAccess` 权限才能查询所有业务空间 ID；普通子账号仅能查看已加入的业务空间 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **凭证获取方式**：APP ID 和 Workspace ID **仅支持控制台手动获取**，不提供 API 或 CLI 查询接口 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **SDK 版本**：Java SDK 调用 DashScope API 时，建议版本 ≥ 2.12.0；OpenAI SDK 调用 Responses API 时，需安装对应语言的官方 SDK 并正确配置 `base_url`。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


