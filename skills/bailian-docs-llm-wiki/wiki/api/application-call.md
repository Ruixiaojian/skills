# application call

`application call` 是指通过 API 调用阿里云百炼平台已发布的应用（包括新版智能体、旧版智能体和工作流），向其提交输入并获取模型推理或流程执行结果的核心交互方式。它支持同步与异步两种模式，适配 DashScope 原生协议和 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，是集成百炼能力至自有系统的关键技术路径。开发者需正确配置凭证、选择调用方式，并遵循对应参数规范。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流三类应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **输入模态**：
  - 纯文本（单轮/多轮对话）
  - 图像（需选用通义千问 VL 系列模型，并在应用中配置为“自定义处理”或“模型节点入参变量为 `imageList`”）
  - 文件（仅智能体应用支持，需配置文件处理方式为“全文引用”或“切片检索”）
- **输出模式**：
  - 同步阻塞式响应（默认）
  - [流式输出](../concepts/streaming-output.md)（`stream=true`，仅同步调用支持，且工作流应用需在结束节点启用“[流式输出](../concepts/streaming-output.md)”开关）
  - 异步任务（`background=true`，立即返回任务 ID，后续轮询查询结果）

> **注意**：文档 4 明确指出“异步任务暂不支持[流式输出](../concepts/streaming-output.md)（stream=true）”，而文档 5 在 `background` 参数说明中也强调“异步调用暂不支持流式输出”。二者一致，无矛盾。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，从[应用管理](https://bailian.console.aliyun.com/#/app-center)页面复制。若应用位于子业务空间或特定地域（如德国法兰克福、华北2北京、新加坡、日本东京），还需配合 `workspace_id` 使用 —— 获取方式见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` | string \| array | 是 | 核心输入内容：<br>• 字符串：用于单轮文本对话；<br>• 消息数组：支持多轮对话、图像（`type: "input_image"`）、文件（`type: "input_file"`，仅智能体）等多模态输入。消息对象需包含 `role`（`user`/`system`/`assistant`）和 `content`。 |
| `session_id` | string | 否（多轮对话必需） | 用于维护会话上下文。首次调用不传，响应中返回；后续请求携带该值即可延续对话，有效期为最后一次请求后 1 小时。 |
| `stream` | boolean | 否 | 是否启用流式输出。默认 `false`；设为 `true` 时需配合同步调用使用。 |
| `background` | boolean | 否 | 是否启用异步模式。设为 `true` 时，API 立即返回任务 ID，适用于耗时较长的任务。 |

## 使用方式

### 1. 接口地址与认证
- **DashScope 原生接口**（推荐用于高性能场景）：  
  `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  Header：`Authorization: Bearer {DASHSCOPE_API_KEY}`  
- **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**（便于复用现有生态）：  
  同步：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  异步：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`（需 `background=true`）  
  Header：`Authorization: Bearer {DASHSCOPE_API_KEY}`  

### 2. SDK 调用示例（Python）
```python
# DashScope SDK（同步）
from dashscope import Application
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？"
)

# OpenAI SDK（同步 + 流式）
from openai import OpenAI
client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/YOUR_APP_ID/compatible-mode/v1/")
stream = client.responses.create(input=[{"role": "user", "content": "你好"}], stream=True)
for chunk in stream:
    if hasattr(chunk, 'delta') and chunk.delta:
        print(chunk.delta, end='', flush=True)
```

### 3. HTTP 调用（curl）
```bash
# DashScope 同步
curl -X POST "https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"prompt": "你是谁？"}}'

# OpenAI 兼容异步
curl -X POST "https://dashscope.aliyuncs.com/api/v2/apps/agent/YOUR_APP_ID/compatible-mode/v1/responses" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": "请规划三天北京行程", "background": true}'
```

## 限制和注意事项

- **地域限制**：所有文档（文档 2、3、4、5）均明确标注“本文档仅适用于华北2（北京）地域”。其他地域（如德国法兰克福、新加坡）调用时，必须显式提供 `workspace_id`，且 Base URL 可能不同 —— 具体请参考 [Base URL 文档](https://help.aliyun.com/zh/model-studio/regions/)。
- **凭证获取**：`APP ID` 和 `Workspace ID` **仅支持控制台手动获取**，不支持通过 API 或 CLI 查询 —— 此限制在 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 中明确说明。
- **权限要求**：查询所有业务空间 ID 需主账号或具备 `AliyunBailianFullAccess` / `AliyunBailianControlFullAccess` 权限的 RAM 子账号；普通 RAM 子账号仅能查看其已加入的业务空间 ID。
- **多轮对话兼容性**：DashScope SDK 使用 `session_id`；[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)则需在 `input` 中传递完整消息历史数组（`messages`），当前不支持基于 `pre_response_id` 或 `conversation_id` 的上下文自动管理。
- **异步任务生命周期**：异步任务创建后，需主动轮询 `retrieve` 接口检查状态（`completed`/`failed`/`cancelled`），无自动回调机制。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)


