# application call

`application call` 是指通过 API 调用阿里云百炼平台已发布的应用（包括新版智能体、旧版智能体、工作流等）的核心交互方式。它支持同步与异步两种执行模式，兼容 DashScope 原生接口和 OpenAI 兼容的 Responses API，适用于实时对话、长任务处理、多模态输入等多种场景。调用前需明确目标应用身份（APP ID）、运行环境（Workspace ID，如适用）及认证凭证（API Key）。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体、工作流三类应用；其中文件输入仅限智能体应用，图像输入需选用通义千问VL系列模型并完成对应配置 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
- **交互模式**：
  - 同步调用：即时返回结果，适用于低延迟交互（如单轮问答、短流程）；
  - 异步调用：返回任务 ID 后后台执行，适用于耗时任务（如报告生成、多步骤工具链），但**不支持[流式输出](../concepts/streaming-output.md)** [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **多模态能力**：
  - 图像输入：需在应用中启用通义千问VL模型，并将文件处理方式设为“自定义处理”（智能体）或模型入参变量设为 `imageList`（工作流）；
  - 文件输入：仅智能体应用支持，需配置文件处理方式为“全文引用”或“切片检索”。

> **注意**：文档 2（[新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)）声明“仅适用于华北2（北京）地域”，而文档 4（[应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)）同样标注相同地域限制，但文档 1 明确指出 Workspace ID 在德国（法兰克福）、新加坡、日本（东京）等非北京地域为必需字段且构成 Base URL 一部分。这表明 DashScope API 实际支持多地域，但部分文档未及时更新地域说明，开发者应以控制台实际可用地域和 [Base URL 文档](https://help.aliyun.com/zh/model-studio/regions/) 为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面获取。 |
| `workspace_id` | string | 条件必填 | 仅当应用位于子业务空间，或部署在德国（法兰克福）、华北2（北京）、新加坡、日本（东京）等特定地域时必需；其值是 Base URL 的组成部分 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` | string / array | 是 | 核心输入内容：<br>• 字符串：单轮纯文本（如 `"你好"`）；<br>• 消息数组：支持多轮对话、图像（`input_image`）、文件（`input_file`）等多模态输入。 |
| `stream` | boolean | 否（默认 `false`） | 是否启用[流式输出](../concepts/streaming-output.md)。仅同步调用支持；工作流应用需在结束节点启用“[流式输出](../concepts/streaming-output.md)”开关并重新发布。 |
| `background` | boolean | 否（默认 `false`） | 是否启用异步模式。设为 `true` 时立即返回任务 ID，后续通过 `retrieve` 查询结果。 |
| `session_id` | string | 否（多轮对话必需） | 用于维护会话上下文，首次调用不传，响应中返回；后续请求携带该值即可延续对话，有效期为最后一次请求后 1 小时。 |
| `biz_params` | object | 否 | 传递工作流或智能体应用内定义的自定义参数（如 `{"city": "北京"}`），需与应用内参数名和类型严格一致。 |

## 使用方式

### 接口地址
- **DashScope API（原生）**：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
- **Responses API（OpenAI 兼容）**：  
  - 同步：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  - 异步：同上，但请求体中 `background=true`

### 调用示例（Python）
```python
# DashScope SDK 方式（推荐）
from dashscope import Application
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？"
)

# Responses API + OpenAI SDK 方式（同步）
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/YOUR_APP_ID/compatible-mode/v1/"
)
response = client.responses.create(input="你是谁？")

# Responses API + OpenAI SDK 方式（异步）
response = client.responses.create(input="生成一份周报", background=True)
task_id = response.id
# 后续调用 client.responses.retrieve(task_id) 查询状态
```

### 认证与凭证
- 所有调用均需在 `Authorization` 请求头中携带 `Bearer <API_KEY>`；
- APP ID 和 Workspace ID 必须通过控制台手动获取，**不支持 API 或 CLI 查询** [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

## 限制和注意事项

- **地域限制**：所有文档均注明“仅适用于华北2（北京）地域”，但实际支持多地域（如文档 1 所述），开发者需根据部署地域选择对应 Base URL 并显式传入 `workspace_id`（如适用）。
- **会话管理**：DashScope API 的 `session_id` 机制仅适用于新版智能体；工作流应用的多轮对话依赖 `messages` 数组传递完整历史，不支持 `session_id` [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **异步约束**：异步调用不支持 `stream=true`，且 `background=true` 与 `stream=true` 互斥。
- **参数传递**：`biz_params` 仅在 Responses API 中生效；DashScope API 需通过 `input` 或 `parameters` 字段传递业务参数，具体取决于应用配置。
- **安全实践**：严禁在代码中硬编码 `DASHSCOPE_API_KEY`，应始终通过环境变量（如 `os.getenv("DASHSCOPE_API_KEY")`）注入。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


