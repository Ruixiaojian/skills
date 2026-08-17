# application call

`application call` 是指通过 API 调用阿里云百炼平台已发布的应用（包括新版智能体、旧版智能体、工作流等）的能力。开发者可使用 DashScope 原生 API 或 OpenAI 兼容的 Responses API 发起同步或异步请求，支持单轮/多轮对话、多模态输入（文本、图像、文件）及自定义参数传递。调用需提供有效的 `APP ID` 和（必要时）`Workspace ID`，并配合正确的认证凭证与 endpoint。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体、工作流三类应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **调用模式**：
  - **同步调用**：适用于实时交互场景，API 阻塞等待结果返回；支持[流式输出](../concepts/streaming-output.md)（`stream=true`），但仅对配置了流式开关的工作流应用生效 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
  - **异步调用**：适用于耗时较长任务（如复杂工具链执行），立即返回任务 ID，后续通过轮询查询状态；**不支持[流式输出](../concepts/streaming-output.md)**。
- **输入能力**：
  - 文本：单字符串或标准 OpenAI Messages 数组（含 `system`/`user`/`assistant` 角色）；
  - 图像：需选用通义千问 VL 系列模型，并在应用中配置为“自定义处理”（智能体）或 `imageList` 入参（工作流）；
  - 文件：仅智能体应用支持，需配置[文件处理](../concepts/file-processing.md)方式为“全文引用”或“切片检索”。

> **注意**：文档 4 明确指出“[异步任务](../concepts/asynchronous-task.md)暂不支持[流式输出](../concepts/streaming-output.md)（stream=true）”，而文档 5 的同步调用说明中允许 `stream=true`。二者逻辑一致，无矛盾；但需注意异步调用下显式设置 `stream=true` 将被忽略或报错。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，从[应用管理](https://bailian.console.aliyun.com/#/app-center)页面复制。 |
| `workspace_id` | string | 条件必填 | 子业务空间或德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域下的应用必需；获取方式见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` | string / array | 是 | 核心输入：<br>- 字符串：`"你是谁？"`；<br>- Messages 数组：支持多轮对话与多模态（`input_text`/`input_image`/`input_file`）。 |
| `stream` | boolean | 否（默认 false） | 仅同步调用有效；设为 `true` 启用流式响应。 |
| `background` | boolean | 否（默认 false） | 设为 `true` 切换为异步调用模式，返回任务 ID。 |
| `biz_params` | object | 否 | 用于传递应用内定义的**自定义参数**（如城市名、索引值等），需与应用配置严格一致。 |

## 使用方式

### 1. Endpoint 与认证
- **DashScope API（推荐）**：  
  `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  Header：`Authorization: Bearer {DASHSCOPE_API_KEY}`  
  （注：该接口仅支持华北2（北京）地域，见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)）

- **OpenAI Responses API（兼容模式）**：  
  `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  Header：`Authorization: Bearer {DASHSCOPE_API_KEY}`  
  （同步/异步均适用，但异步需设 `background=true`）

### 2. 多轮对话
- **DashScope SDK**：通过 `session_id` 维护会话，首次响应返回 `session_id`，后续请求携带该值即可延续上下文。
- **Responses API**：直接在 `input` 中传入完整 Messages 数组（含历史 `user`/`assistant` 消息），**不依赖 `pre_response_id` 或 `conversation_id`**（当前未支持）。

### 3. 示例代码（Python）
```python
# DashScope 同步调用（单轮）
from dashscope import Application
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？"
)

# Responses API 同步流式调用
from openai import OpenAI
client = OpenAI(base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/YOUR_APP_ID/compatible-mode/v1/", 
                api_key=os.getenv("DASHSCOPE_API_KEY"))
stream = client.responses.create(input=[{"role":"user","content":"你好"}], stream=True)
for chunk in stream:
    print(chunk.delta.text, end="", flush=True)
```

## 限制和注意事项

- **地域限制**：DashScope API（`/v1/apps/...`）和 Responses API（`/v2/apps/...`）当前**仅支持华北2（北京）地域**，其他地域需使用对应 Base URL（见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)）。
- **凭证获取**：`APP ID` 和 `Workspace ID` **仅可通过控制台手动获取**，不支持 API 或 CLI 查询。
- **权限要求**：查询所有业务空间需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号；普通子账号仅可见已加入的空间。
- **[异步任务](../concepts/asynchronous-task.md)生命周期**：创建后需主动轮询 `retrieve` 接口检查状态（`completed`/`failed`/`cancelled`），无自动回调机制。
- **参数一致性**：`biz_params` 中的键名、类型必须与应用内自定义参数配置完全一致，否则将被忽略或导致调用失败。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)


