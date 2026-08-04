# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者只需提供应用凭证（APP ID 和可选的 Workspace ID）、API Key 及输入数据，即可触发应用执行并获取结构化响应。该机制支持文本、图像、文件等多模态输入，并兼容 OpenAI 生态工具链。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **多模态能力**：
  - 文本输入：单轮/多轮对话（需完整传递历史消息）；
  - 图像输入：需选用通义千问 VL 系列模型，并在应用中配置为“自定义处理”（智能体）或模型入参变量设为 `imageList`（工作流）；
  - 文件输入：仅智能体应用支持，需启用“全文引用”或“切片检索”[文件处理](../concepts/file-processing.md)方式；
- **输出模式**：同步调用支持非流式与[流式输出](../concepts/streaming-output.md)；异步调用不支持流式（`stream=true` 会被忽略），详见 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。

> **注意**：文档 2（`new-agent-application-api-reference.md`）和文档 4（`agent-and-workflow-application-api-reference.md`）均声明“仅适用于华北2（北京）地域”，但文档 1 明确指出：在德国（法兰克福）、华北2（北京）、新加坡、日本（东京）等地域调用子业务空间下的应用时，`Workspace ID` 是 Base URL 的组成部分。这意味着跨地域调用能力实际存在，但文档未统一说明地域覆盖范围，建议以控制台实际可用地域为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面复制。若应用位于子业务空间，还需配合 `workspace_id` 使用 —— 具体获取方式见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` | string / array | 是 | 核心输入内容：<br>• 字符串：单轮纯文本（如 `"你好"`）；<br>• 消息数组：支持多轮对话、图像（`type: "input_image"`）、文件（`type: "input_file"`，仅智能体）等多模态输入。 |
| `stream` | boolean | 否 | 默认 `false`。设为 `true` 启用[流式输出](../concepts/streaming-output.md)（仅同步调用有效）。工作流应用需在结束节点启用“[流式输出](../concepts/streaming-output.md)”开关并重新发布。 |
| `background` | boolean | 否 | 默认 `false`。设为 `true` 切换为异步调用，立即返回任务 ID，后续通过 `retrieve` 查询结果。 |
| `biz_params` | object | 否 | 用于向工作流或智能体传递自定义参数（如城市名、索引值等），参数名与应用内定义必须一致。 |

## 使用方式

### 接口地址
- **DashScope SDK/API**：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
- **OpenAI 兼容 Responses API（同步）**：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
- **OpenAI 兼容 Responses API（异步）**：同上，但请求体中需含 `"background": true`  

### 调用示例（Python）
```python
# 同步调用（DashScope SDK）
from dashscope import Application
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？"
)

# 同步调用（OpenAI SDK，流式）
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/YOUR_APP_ID/compatible-mode/v1/"
)
stream = client.responses.create(input=[{"role": "user", "content": "你好"}], stream=True)
for chunk in stream:
    if hasattr(chunk, 'delta') and chunk.delta:
        print(chunk.delta, end='', flush=True)

# 异步调用（OpenAI SDK）
async_response = await client.responses.create(
    input="生成一份技术方案",
    background=True
)
task_id = async_response.id
# 后续调用 client.responses.retrieve(task_id) 查询状态
```

## 限制和注意事项

- **地域与凭证约束**：调用子业务空间应用或特定地域（德国、北京、新加坡、东京）模型时，必须提供 `workspace_id`，且其值需作为 Base URL 的一部分或独立 Header 传入 —— 具体规则请严格参照 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 中的说明。
- **会话管理**：
  - DashScope API 通过 `session_id` 维护多轮对话上下文，有效期为最后一次请求后 1 小时；
  - OpenAI Responses API 不支持 `pre_response_id` 或 `conversation_id`，当前必须在每次请求中显式传递完整消息历史。
- **权限要求**：RAM 子账号默认无法查看全部业务空间 ID，仅能访问已加入的空间；查询所有 Workspace ID 需主账号或具备 `AliyunBailianFullAccess` 权限的超级管理员操作。
- **安全实践**：严禁在代码中硬编码 `DASHSCOPE_API_KEY`，应始终通过环境变量（如 `os.getenv("DASHSCOPE_API_KEY")`）注入。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


