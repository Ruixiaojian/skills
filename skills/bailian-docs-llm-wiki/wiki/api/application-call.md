# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者可选择 OpenAI 兼容的 Responses API 或原生 DashScope API 两种方式发起同步或异步请求，支持文本、图像、文件等[多模态](../concepts/multi-modal.md)输入，并可通过 `session_id` 或完整消息历史维护对话上下文。所有调用均需提供有效的 APP ID 及认证凭证。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流应用；其中文件输入仅限智能体应用，且需在应用配置中启用“全文引用”或“切片检索”[新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)。
- **[多模态](../concepts/multi-modal.md)能力**：
  - 图像输入：需选用通义千问 VL 系列模型，并在应用中正确配置图像处理方式 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)；
  - 文件输入：仅智能体应用支持，依赖应用内文件处理方式配置；
  - [流式输出](../concepts/streaming-output.md)：仅同步调用支持，且工作流应用需在结束节点启用“[流式输出](../concepts/streaming-output.md)”开关并重新发布 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
- **会话管理**：
  - DashScope API 通过 `session_id` 维护上下文，有效期为最后一次请求后 1 小时；
  - Responses API 当前不支持 `pre_response_id` 或 `conversation_id`，需在每次请求中传递完整消息历史 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。

> **注意**：文档 4 和文档 5 均描述了 `/api/v1/apps/{APP_ID}/completion` 接口，但文档 4 明确限定为“新版智能体应用”，而文档 5 泛指“智能体、工作流应用”。实际调用时，该接口对两类应用均有效，但功能支持（如 `session_id` 行为、参数结构）以应用类型和发布配置为准，建议优先参考 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面获取。若应用位于子业务空间，还需传入 `workspace_id` [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` / `prompt` | string 或 array | 是 | 核心输入内容：<br>- DashScope API 使用 `prompt` 字符串；<br>- Responses API 支持字符串（单轮）或消息数组（多轮/[多模态](../concepts/multi-modal.md)），数组元素含 `role`（`user`/`system`/`assistant`）与 `content`（支持 `input_text`/`input_image`/`input_file`）[同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。 |
| `stream` | boolean | 否 | 仅 Responses API 支持。设为 `true` 启用[流式输出](../concepts/streaming-output.md)，需应用端配合启用流式开关 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。 |
| `background` | boolean | 否 | 仅 Responses API 支持。设为 `true` 进入异步模式，立即返回任务 ID，后续通过 `retrieve` 查询结果 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。 |
| `biz_params` | object | 否 | Responses API 中用于传递工作流或智能体应用内定义的自定义参数，键名需与应用配置完全一致 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。 |
| `session_id` | string | 否 | DashScope API 多轮对话必需。首次调用不传，响应中返回；后续调用需携带上一轮返回的 `session_id` [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)。 |

## 使用方式

### 1. 认证与端点
- **API Key**：通过[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)获取，并推荐配置为环境变量 `DASHSCOPE_API_KEY`。
- **Base URL / Endpoint**：
  - Responses API（OpenAI 兼容）：`https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/`（同步/异步共用）；
  - DashScope API（原生）：`https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`。

### 2. 调用示例
- **同步调用（Responses API）**：  
  ```python
  from openai import OpenAI
  client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), 
                  base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/")
  response = client.responses.create(input="你好")
  ```
- **异步调用（Responses API）**：  
  设置 `background=True`，获取 `task_id` 后轮询 `retrieve` 接口 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **DashScope SDK 调用**：  
  ```python
  from dashscope import Application
  response = Application.call(api_key=..., app_id=..., prompt="你好")
  ```

## 限制和注意事项

- **地域限制**：Responses API（同步/异步）与 DashScope API 均**仅支持华北2（北京）地域**，其他地域（如德国法兰克福、新加坡）调用需显式传入 `workspace_id` 并确认 Base URL [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **异步限制**：异步调用不支持 `stream=true`，且暂无流式输出能力 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **凭证获取**：APP ID 和 Workspace ID **仅支持控制台手动获取**，不提供 API 或 CLI 查询接口 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **权限要求**：查询所有业务空间 ID 需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号，普通子账号仅能查看已加入的业务空间 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **参数兼容性**：`biz_params` 仅在 Responses API 中生效；DashScope API 的自定义参数需通过 `parameters` 字段传递（文档未明确示例，以 SDK 实际行为为准）。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)


