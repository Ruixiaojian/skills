# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者可使用 DashScope 原生 API 或 OpenAI 兼容的 Responses API 发起请求，支持文本、图像、文件等[多模态](../concepts/multi-modal.md)输入，并可通过 `session_id` 或完整消息历史维护多轮对话上下文。所有调用均需提供有效的 APP ID 和 API Key，部分场景还需 Workspace ID。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)。
- **[多模态](../concepts/multi-modal.md)能力**：
  - 图像输入：需选用通义千问 VL 系列模型，并在应用中配置为“自定义处理”（智能体）或模型入参变量设为 `imageList`（工作流）[同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
  - 文件输入：仅智能体应用支持，需在应用内选择“全文引用”或“切片检索”文件处理方式。
- **交互模式**：
  - 单轮/多轮对话：DashScope API 通过 `session_id` 维护会话；Responses API 则需在每次请求中传入完整 `input` 消息数组。
  - [流式输出](../concepts/streaming-output.md)：仅同步调用支持，且工作流应用需在结束节点启用“[流式输出](../concepts/streaming-output.md)”开关并重新发布。
- **[异步任务](../concepts/asynchronous-task.md)**：适用于耗时较长的场景（如报告生成），通过设置 `background=true` 立即返回任务 ID，后续轮询查询结果 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。

> **注意**：文档 2（新版智能体 API）和文档 4（通用 DashScope API）均声明“仅适用于华北2（北京）地域”，但文档 1 明确指出 Workspace ID 在德国（法兰克福）、华北2（北京）、新加坡、日本（东京）等地域为必需参数，且是 Base URL 的组成部分。这意味着跨地域调用实际可行，但需显式指定对应地域的 endpoint —— 文档 2 和 4 的“仅适用北京”属表述过窄，应以文档 1 的地域支持范围为准。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面获取。 |
| `workspace_id` | string | 条件必选 | 子业务空间或特定地域（德、京、新、日）下必须提供，用于路由请求。详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` | string / array | 是 | 核心输入：<br>- 字符串：单轮纯文本（如 `"你好"`）；<br>- 消息数组：支持多轮对话及[多模态](../concepts/multi-modal.md)（`input_text`/`input_image`/`input_file`）。 |
| `stream` | boolean | 否 | 默认 `false`。设为 `true` 启用[流式输出](../concepts/streaming-output.md)（仅同步调用支持）。 |
| `background` | boolean | 否 | 默认 `false`。设为 `true` 启用异步调用，立即返回任务 ID。 |
| `biz_params` | object | 否 | 用于传递应用内定义的自定义参数（如城市名、索引值等），需与应用配置严格一致。 |

## 使用方式

### 1. 准备工作
- 获取 `APP ID` 和（如需）`Workspace ID`：通过控制台手动复制，[不支持 API 查询](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- 获取并安全配置 `DASHSCOPE_API_KEY`（推荐环境变量）。
- （可选）安装对应 SDK：[DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk) 或 [OpenAI Python SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

### 2. 调用入口
- **DashScope API（原生）**  
  Endpoint: `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  请求体结构：`{"input": {"prompt": "..."}, "parameters": {}, "debug": {}}`
- **Responses API（OpenAI 兼容）**  
  - 同步：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  - 异步：同上，但请求体含 `"background": true`  
  - SDK 配置 `base_url = "https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/"`

### 3. 示例代码（Python）
```python
# DashScope 同步调用（单轮）
from dashscope import Application
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？"
)

# Responses 同步调用（多轮+图像）
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/api/v2/apps/agent/YOUR_APP_ID/compatible-mode/v1/"
)
response = client.responses.create(
    input=[
        {"role": "user", "content": [
            {"type": "input_text", "text": "这是什么"},
            {"type": "input_image", "image_url": "https://example.com/dog.jpg"}
        ]}
    ]
)

# Responses 异步调用
response = client.responses.create(
    input="生成一份北京旅游攻略",
    background=True
)
task_id = response.id  # 后续用此 ID 轮询
```

## 限制和注意事项

- **地域与 Workspace ID**：调用子业务空间应用，或位于德国（法兰克福）、华北2（北京）、新加坡、日本（东京）的应用时，**必须**在请求中提供 `workspace_id`，且其值需与目标地域匹配 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **权限要求**：RAM 子账号需被授予 `AliyunBailianFullAccess` 或 `AliyunBailianControlFullAccess` 权限才能查看所有业务空间 ID；普通子账号仅能查看已加入的业务空间。
- **异步限制**：异步调用不支持 `stream=true`，且 `background=true` 与流式输出互斥。
- **会话有效期**：DashScope API 的 `session_id` 在最后一次请求后 1 小时内有效；Responses API 不维护服务端会话，需自行传递完整历史消息。
- **参数一致性**：通过 `biz_params` 传递的自定义参数，其名称、类型必须与应用内配置完全一致，否则将被忽略或报错。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


