# application call

`application call` 是指通过 API 调用阿里云百炼平台已发布的应用（包括新版智能体、旧版智能体及工作流），向其提交输入并获取模型推理或编排执行结果的核心交互方式。该能力支持同步与异步两种模式，兼容 DashScope 原生协议和 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，适用于实时对话、长耗时任务、多模态交互等多种场景。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体、工作流三类应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **调用协议**：
  - DashScope 原生协议（推荐用于高性能、低延迟场景）；
  - OpenAI 兼容 Responses API（便于复用现有 OpenAI 生态代码）。
- **输入模态**：
  - 文本（单轮/多轮对话）；
  - 图像（需选用通义千问 VL 系列模型，并在应用中配置自定义处理）；
  - 文件（仅智能体应用支持，需配置为“全文引用”或“切片检索”）；
  - 自定义参数（通过 `biz_params` 传递，需与应用内定义的参数名和类型一致）。
- **输出模式**：
  - 同步阻塞式响应（默认）；
  - [流式输出](../concepts/streaming-output.md)（`stream=true`，需工作流应用在结束节点启用流式开关）；
  - 异步任务（`background=true`，立即返回任务 ID，后续轮询查询结果）。

> **注意**：文档 4 和文档 5 均声明“本文档仅适用于华北2（北京）地域”，但文档 1 明确指出在德国（法兰克福）、华北2（北京）、新加坡、日本（东京）等地域调用子业务空间下的应用时，`Workspace ID` 是 Base URL 的组成部分。这意味着 `application call` 实际支持多地域，但部分 API 文档未完整覆盖地域适配说明，开发者应以 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 中的地域列表为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面获取。 |
| `workspace_id` | string | 条件必填 | 子业务空间或特定地域（德/京/新/东京）下必须提供，用于构造 Base URL 或作为请求头。详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` | string \| array | 是 | 核心输入内容：<br>- 字符串：单轮文本；<br>- 消息数组：支持 `system`/`user`/`assistant` 角色，含 `input_text`/`input_image`/`input_file` 多模态类型。 |
| `session_id` | string | 可选（多轮对话） | 用于维护会话上下文，由首次响应返回，有效期为最后一次请求后 1 小时。 |
| `stream` | boolean | 否（默认 false） | 启用[流式输出](../concepts/streaming-output.md)，仅同步调用支持。工作流应用需在发布前启用流式开关。 |
| `background` | boolean | 否（默认 false） | 启用异步模式，立即返回任务 ID；**异步调用不支持 `stream=true`**。 |
| `biz_params` | object | 否 | 传递应用内定义的自定义参数（如 `{"city": "北京"}`），仅 Responses API 支持。 |

## 使用方式

### 1. 准备工作
- 创建应用并获取 `app_id`（必要）；
- 获取 `workspace_id`（若应用位于子业务空间或德/京/新/东京地域）；
- 获取并安全配置 `DASHSCOPE_API_KEY`（环境变量优先，禁止硬编码）；
- （可选）安装对应 SDK：[DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk) 或 [OpenAI Python SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

### 2. 接口地址
- **DashScope 协议**（同步）：  
  `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  （`{APP_ID}` 替换为实际值；`workspace_id` 需拼入 Base URL 或作为请求头）
- **Responses API**（同步）：  
  `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
- **Responses API**（异步）：  
  `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`（带 `background=true`）

### 3. 示例调用
- **DashScope SDK（Python）单轮**：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="your_app_id",
      prompt="你是谁？"
  )
  ```
- **Responses API（curl）多轮+图像**：
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/api/v2/apps/agent/APP_ID/compatible-mode/v1/responses" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "这是什么？"},
                    {"type": "input_image", "image_url": "https://example.com/image.jpg"}
                ]
            }
        ]
      }'
  ```

## 限制和注意事项

- **地域与 Workspace ID**：调用子业务空间应用，或在德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域调用时，**必须提供 `workspace_id`**，否则请求失败。该要求在 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 中明确说明。
- **API Key 安全**：所有示例均强调“不建议在生产环境中直接将 API Key 硬编码到代码中”，应优先使用环境变量或密钥管理服务。
- **异步限制**：异步调用（`background=true`）**不支持[流式输出](../concepts/streaming-output.md)（`stream=true`）**，且暂无回调机制，需主动轮询任务状态。
- **多轮对话**：DashScope 协议依赖 `session_id`；Responses API 则需在每次请求中传递完整 `messages` 数组，因 `pre_response_id`/`conversation_id` 上下文功能尚未上线。
- **凭证获取方式**：`app_id` 和 `workspace_id` **仅支持控制台手动获取**，不支持 API 或 CLI 查询，详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)


