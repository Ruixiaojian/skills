# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者可使用 DashScope 原生 API 或 OpenAI 兼容的 Responses API 发起请求，支持文本、图像、文件等[多模态](../concepts/multi-modal.md)输入，并可通过 `session_id` 或完整消息历史维护多轮对话上下文。所有调用均需提供有效的 `APP ID` 和 `API Key`，部分场景还需 `Workspace ID`。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)。
- **调用模式**：
  - **同步调用**：适用于实时交互场景，立即返回结果；支持[流式输出](../concepts/streaming-output.md)（`stream=true`），但工作流应用需在结束节点启用流式开关并重新发布 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
  - **异步调用**：适用于耗时较长任务（如复杂报告生成），设置 `background=true` 后立即返回任务 ID，后续通过轮询查询结果；**异步模式不支持[流式输出](../concepts/streaming-output.md)** [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **[多模态](../concepts/multi-modal.md)输入**：
  - 图像：需选用通义千问 VL 系列模型，并在应用中配置为“自定义处理”（智能体）或模型入参变量设为 `imageList`（工作流）。
  - 文件：仅智能体应用支持，需配置文件处理方式为“全文引用”或“切片检索”。
- **会话管理**：
  - DashScope API 使用 `session_id` 维护上下文（有效期 1 小时）；
  - Responses API 要求每次请求传递完整消息历史（`input` 为 messages 数组），`pre_response_id` 和 `conversation_id` 功能暂未支持。

> **注意**：文档 2（[新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)）和文档 4（[应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)）均描述了 `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion` 接口，但前者明确限定“仅适用于华北2（北京）地域”，后者同样标注相同限制，二者无实质矛盾；但文档 3 和 5 中 Responses API 的 endpoint 为 `/api/v2/...`，与 v1 接口属于不同协议栈，开发者应根据 SDK 或兼容性需求选择对应路径。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面复制。若应用位于子业务空间或德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域，还需提供 `workspace_id` [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` | string \| array | 是 | 核心输入内容：<br>- 字符串：单轮纯文本（如 `"你好"`）；<br>- 消息数组：支持多轮对话及[多模态](../concepts/multi-modal.md)（`input_text`/`input_image`/`input_file`）。`input_file` 仅智能体应用支持。 |
| `stream` | boolean | 否 | 默认 `false`。设为 `true` 启用流式响应（仅同步调用支持）。 |
| `background` | boolean | 否 | 默认 `false`。设为 `true` 启用异步调用，返回任务 ID。 |
| `biz_params` | object | 否 | 用于向工作流或智能体应用传递自定义参数（如 `{"city": "北京"}`），参数名须与应用内定义一致。 |

## 使用方式

### 1. 凭证准备
- 获取 `APP ID` 和（如需）`Workspace ID`：通过百炼控制台手动复制，[不支持 API 或 CLI 查询](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- 获取 `DASHSCOPE_API_KEY`：在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建并配置到环境变量。

### 2. 接口选择与调用
- **DashScope 原生 API**（推荐用于高性能/全功能场景）：
  - Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
  - 请求体示例（HTTP）：
    ```json
    {
      "input": { "prompt": "你是谁？" },
      "parameters": {},
      "debug": {}
    }
    ```
- **OpenAI 兼容 Responses API**（便于迁移现有 OpenAI 代码）：
  - 同步 Endpoint：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
  - 异步 Endpoint：同上，但请求体中添加 `"background": true`
  - Python SDK 示例（同步）：
    ```python
    from openai import OpenAI
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/"
    )
    response = client.responses.create(input="你是谁？")
    ```

### 3. 多轮对话实现
- **DashScope API**：首请求不带 `session_id`，响应中返回 `session_id`；后续请求携带该值即可延续会话。
- **Responses API**：每次请求的 `input` 必须包含完整对话历史（system/user/assistant 消息数组），不可依赖服务端状态。

## 限制和注意事项

- **地域限制**：所有文档（文档 2、3、4、5）均明确标注“仅适用于华北2（北京）地域”，其他地域暂不支持 `application call` 功能。
- **Workspace ID 使用场景**：当应用位于子业务空间，或部署在德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域时，API 请求必须包含 `workspace_id`；其值是 Base URL 的组成部分，且只能通过控制台手动获取 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **权限要求**：查询所有业务空间 ID 需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号；普通 RAM 子账号仅能查看已加入的业务空间 ID。
- **异步与流式互斥**：`background=true` 时 `stream` 参数无效，且会被忽略；若同时设置将导致行为未定义。
- **SDK 版本要求**：Java SDK 调用 DashScope API 时，建议版本 ≥ 2.12.0；OpenAI SDK 调用 Responses API 时需安装对应语言的 `openai` 客户端库。
- **安全实践**：禁止在代码中硬编码 `API Key`，应始终通过环境变量（如 `DASHSCOPE_API_KEY`）注入。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


