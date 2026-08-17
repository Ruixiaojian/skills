# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者可选择 OpenAI 兼容的 Responses API 或原生 DashScope API 两种方式发起同步或异步请求，支持文本、图像、文件等[多模态](../concepts/multi-modal.md)输入，并可通过会话 ID 或完整历史消息维护上下文。所有调用均需提供有效的 APP ID 和认证凭证。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流三类应用，具体能力因应用配置而异。
- **[多模态](../concepts/multi-modal.md)输入**：
  - 文本：所有应用均支持；
  - 图像：需选用通义千问 VL 系列模型，并在应用中启用「自定义处理」（智能体）或配置 `imageList` 入参（工作流），详见 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)；
  - 文件：仅智能体应用支持，且文件处理方式须设为「全文引用」或「切片检索」；
- **会话管理**：
  - Responses API：不支持 `pre_response_id` 或 `conversation_id`，需显式传递完整对话历史；
  - DashScope API：支持 `session_id` 维护上下文，有效期为最后一次请求后 1 小时；
- **异步任务**：适用于耗时较长的场景（如报告生成、多步骤工具调用），通过 `background=true` 触发，返回任务 ID 后可轮询查询结果。

> **注意**：文档 4（[新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)）与文档 5（[应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)）均描述 `/api/v1/apps/{APP_ID}/completion` 接口，但文档 4 明确限定为「新版智能体应用」，而文档 5 声明支持「智能体、工作流」两类应用。实际调用中，工作流应用应优先参考文档 5；若使用新版智能体，两个文档均可参考，但需以文档 5 的通用性为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面获取。详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) |
| `input` | string / array | 是 | 核心输入内容：<br>• 字符串：单轮纯文本（如 `"你好"`）；<br>• 消息数组：支持多轮对话及[多模态](../concepts/multi-modal.md)（含 `input_text`/`input_image`/`input_file`）；<br>• 注意：Responses API 不支持隐式上下文，必须传全量历史 |
| `stream` | boolean | 否 | 是否[流式输出](../concepts/streaming-output.md)，默认 `false`；工作流应用需在结束节点启用「[流式输出](../concepts/streaming-output.md)」开关并重新发布 |
| `background` | boolean | 否 | 是否异步执行，默认 `false`；异步模式下不支持 `stream=true` |
| `biz_params` | object | 否 | 仅 Responses API 异步调用支持，用于向工作流或智能体传递自定义参数（如 `{"city": "北京"}`），参数名须与应用内配置一致 |
| `session_id` | string | 否 | 仅 DashScope API 多轮对话使用，首次调用不需传入，后续请求携带上一轮响应中的 `output.session_id` |

## 使用方式

### 1. 凭证准备
- 获取 `APP ID`：通过控制台「应用管理」页面复制；
- 获取 `Workspace ID`（如需）：当应用位于子业务空间，或部署在德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域时必需，通过控制台右上角「业务空间」图标查看；
- 配置 `DASHSCOPE_API_KEY`：通过「密钥管理」获取，并推荐配置为环境变量。

### 2. API 选型与端点
- **Responses API（OpenAI 兼容）**  
  - 同步：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  - 异步：同上，仅需添加 `"background": true`  
  - 适用场景：快速迁移 OpenAI 生态代码，或需复用现有 SDK
- **DashScope API（原生）**  
  - 统一端点：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  - 适用场景：需要更细粒度控制（如 `session_id`）、或调用工作流应用

### 3. 示例调用（Python）
```python
# Responses API 同步调用（多轮+图像）
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/"
)
response = client.responses.create(
    input=[
        {"role": "user", "content": [{"type": "input_text", "text": "这是什么？"},
                                      {"type": "input_image", "image_url": "https://example.com/dog.jpg"}]}
    ]
)

# DashScope API 多轮对话
from dashscope import Application
response1 = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id=app_id,
    prompt="你是谁？"
)
response2 = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id=app_id,
    prompt="你有什么技能？",
    session_id=response1.output.session_id
)
```

## 限制和注意事项

- **地域限制**：所有文档均明确指出「本文档仅适用于华北2（北京）地域」，其他地域（如德国、新加坡）调用需确认 Workspace ID 是否已正确嵌入 Base URL；
- **权限要求**：获取 Workspace ID 需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号，普通子账号仅能查看已加入的业务空间；
- **异步约束**：异步任务不支持[流式输出](../concepts/streaming-output.md)（`stream=true` 会被忽略），且必须通过 `retrieve` 接口轮询状态，无 Webhook 回调机制；
- **凭证时效性**：APP ID 和 Workspace ID 为静态标识，长期有效；API Key 可随时在控制台禁用或轮换；
- **调试建议**：控制台「应用卡片 → 发布 → API 调试」提供可视化调试入口，推荐首次集成时使用。

> **注意**：文档 1 明确说明「目前只能通过控制台手动获取APP ID和Workspace ID，不支持通过 API 或 CLI 查询」，而文档 2/3/4/5 均未提及该限制，开发者应以文档 1 的权威说明为准，避免尝试自动化获取。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)


