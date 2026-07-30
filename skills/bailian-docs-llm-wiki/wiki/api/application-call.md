# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者可选择 DashScope 原生协议或 OpenAI 兼容模式（Responses API）发起同步或异步请求，支持单轮/多轮对话、[多模态](../concepts/multi-modal.md)输入及自定义参数传递。所有调用均需提供有效的 `APP ID` 和（在特定地域或子业务空间下）`Workspace ID`。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **调用模式**：
  - **同步调用**：适用于实时交互场景，立即返回结果；支持[流式输出](../concepts/streaming-output.md)（`stream=true`），但仅限工作流应用在发布时启用流式开关 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
  - **异步调用**：适用于耗时任务（如复杂工具链执行），返回任务 ID 后可轮询状态；**不支持[流式输出](../concepts/streaming-output.md)** [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **输入类型**：
  - 纯文本（`input: string` 或 `input: messages[]`）
  - [多模态](../concepts/multi-modal.md)：图像（`input_image`）、音频/文档等文件（`input_file`，仅智能体应用支持）[同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
- **会话管理**：
  - DashScope API 使用 `session_id` 维持上下文，有效期为最后一次请求后 1 小时；
  - Responses API 需显式传递完整 `messages` 数组，当前**不支持**基于 `pre_response_id` 或 `conversation_id` 的自动上下文续写。

> **注意**：文档 2 和文档 3 均声明“仅适用于华北2（北京）地域”，但文档 1 明确指出德国（法兰克福）、新加坡、日本（东京）等地域调用子业务空间应用时也必须传入 `Workspace ID`，且其 Base URL 已包含地域信息。因此，“仅适用北京”是接口 endpoint 的限制，而非地域能力限制；跨地域调用需使用对应地域的 endpoint 并确保 `Workspace ID` 正确。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)中获取。 |
| `workspace_id` | string | 条件必填 | 子业务空间或德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域下必需，见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` | string \| array | 是 | 核心输入：<br>- 字符串：单轮文本；<br>- `messages[]`：多轮对话或含图片/文件的[多模态](../concepts/multi-modal.md)输入（`type: input_text`/`input_image`/`input_file`）。 |
| `stream` | boolean | 否（默认 false） | 是否[流式输出](../concepts/streaming-output.md)；**工作流应用需在发布时启用流式开关**。 |
| `background` | boolean | 否（默认 false） | 是否异步执行；设为 `true` 时返回任务 ID，**与 `stream=true` 冲突，不可同时设置**。 |
| `biz_params` | object | 否 | 传递应用内配置的自定义参数（如城市名、索引值），需与应用参数定义严格一致 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。 |

## 使用方式

### 协议选择
- **DashScope 原生协议**（推荐）：Endpoint 为 `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`，SDK 封装简洁，支持 `session_id` 会话管理。
- **OpenAI 兼容模式（Responses API）**：Endpoint 为 `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`，便于复用现有 OpenAI 生态代码，但需注意 `input` 结构差异。

### 调用示例（DashScope SDK - Python）
```python
from dashscope import Application
import os

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="your_app_id",  # 替换为实际 APP ID
    prompt="你是谁？"
)
if response.status_code == 200:
    print(response.output.text)
```

### 多轮对话（DashScope）
首次调用不传 `session_id`，响应中返回 `session_id`；后续请求携带该 ID 即可延续上下文：
```python
# 第一轮
resp1 = Application.call(app_id="...", prompt="你好")
# 第二轮（携带 session_id）
resp2 = Application.call(
    app_id="...",
    prompt="刚才说了什么？",
    session_id=resp1.output.session_id
)
```

### 异步调用（Responses API - Python）
```python
from openai import AsyncOpenAI
client = AsyncOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/"
)

# 创建异步任务
create_resp = await client.responses.create(input="生成报告", background=True)
task_id = create_resp.id

# 轮询结果
while True:
    retrieve_resp = await client.responses.retrieve(task_id)
    if retrieve_resp.status in ["completed", "failed", "cancelled"]:
        break
    await asyncio.sleep(2)
```

## 限制和注意事项

- **地域与 Workspace ID**：调用位于子业务空间的应用，或德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域的应用时，**必须提供 `Workspace ID`**，且需使用对应地域的 Base URL [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **凭证获取**：`APP ID` 和 `Workspace ID` **仅支持控制台手动获取**，不提供 API 或 CLI 查询接口 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **权限要求**：RAM 子账号查询所有业务空间 ID 需具备 `AliyunBailianFullAccess` 或 `AliyunBailianControlFullAccess` 权限，否则仅能查看已加入的业务空间 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **参数冲突**：`stream=true` 与 `background=true` **不可共存**；异步调用强制禁用流式输出 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **会话生命周期**：DashScope 的 `session_id` 在最后一次请求后 **1 小时过期**，超时后需新建会话。
- **多模态支持**：文件输入（`input_file`）**仅智能体应用支持**，且需在应用配置中选择“全文引用”或“切片检索” [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)


