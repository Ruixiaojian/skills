# application call

阿里云百炼平台支持通过 API 调用已创建的**智能体**和**工作流**应用。平台提供两套调用接口：**DashScope API** 和 **OpenAI 兼容的 Responses API**，开发者可根据场景选择同步或异步调用方式。调用前需获取 API Key 和应用 ID 等凭证。

## 前置准备

调用应用前，需完成以下准备：

1. **创建应用**：在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面创建百炼应用（智能体或工作流），获取应用 ID。
2. **获取 API Key**：通过 [密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key) 获取，并配置到环境变量。
3. **获取 Workspace ID**（按需）：若应用位于**子业务空间**，还需提供 Workspace ID。详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
4. **安装 SDK**（可选）：根据所选接口安装 DashScope SDK 或 OpenAI SDK。

> **注意**：目前只能通过控制台手动获取 APP ID 和 Workspace ID，不支持通过 API 或 CLI 查询。

## 两套调用接口

### DashScope API

适用于需要更全面功能和更高性能的场景。支持**智能体**（含新版 Agent 2.0）和**工作流**应用。

- **Endpoint**：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
- **SDK 支持**：Python、Java（DashScope SDK 版本建议 ≥ 2.12.0）
- **HTTP 支持**：curl、PHP、Node.js、C#、Go
- **多轮对话**：通过 `session_id` 维护会话上下文（首次无需传入，响应返回后续使用的 `session_id`，有效期为最后一次请求后 1 小时）

详细参数和用法参见 [应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。

### OpenAI 兼容 Responses API

适合已有 OpenAI 代码库或需要快速集成 OpenAI 生态工具的场景。

- **Endpoint**：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
- **SDK**：使用 OpenAI Python/Java SDK
- **`base_url`**：`https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/`
- **多轮对话**：当前需在每次请求时传递完整的对话历史（`pre_response_id` 和 `conversation_id` 功能后续支持）

> **注意**：DashScope API 通过 `session_id` 实现多轮对话（服务端维护上下文），而 Responses API 目前需要客户端在 `input` 中传递完整的消息历史。两种方式的多轮对话机制不同，迁移时需注意。

## 关键参数

| 参数 | 类型 | 必选 | 说明 | 适用接口 |
|------|------|------|------|----------|
| `app_id` | string | 是 | 应用 ID，在应用管理页面获取 | 两者 |
| `prompt` | string | 是 | 用户输入的文本 | DashScope API |
| `input` | string/array | 是 | 请求输入，支持字符串或消息数组（含多模态） | Responses API |
| `session_id` | string | 否 | 多轮对话的会话 ID | DashScope API |
| `stream` | boolean | 否 | 是否[流式输出](../concepts/streaming.md)，默认 `false` | 两者 |
| `background` | boolean | 否 | 是否异步执行，默认 `false` | Responses API |
| `biz_params` | object | 否 | 自定义业务参数（如工作流参数） | Responses API |
| `workspace_id` | string | 条件 | 子业务空间下的应用必须提供 | 两者 |

## 调用方式

### 同步调用

适用于需要即时获取结果的实时交互场景。

**DashScope API 示例（Python）：**

```python
import os
from dashscope import Application

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='你是谁？'
)
print(response.output.text)
```

**Responses API 示例（Python）：**

```python
from openai import OpenAI
import os

app_id = 'YOUR_APP_ID'
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'
)
response = client.responses.create(input="你是谁？")
print(response.model_dump_json(indent=2))
```

### [流式输出](../concepts/streaming.md)

设置 `stream=True` 实现边生成边输出。若应用类型为**工作流**，需在结束节点或流程输出节点中启用**[流式输出](../concepts/streaming.md)**开关并重新发布应用。

### 异步调用

适用于耗时较长的任务（如报告生成、多步骤工具调用），通过设置 `background=True` 开启。API 立即返回任务 ID，后续通过 `retrieve` 接口轮询状态。详见 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。

核心流程：
1. **创建任务**：调用 `create` 方法并设置 `background=True`，获取任务 ID
2. **轮询状态**：定期调用 `retrieve` 方法查询任务状态
3. **处理结果**：任务状态为 `completed`、`failed` 或 `cancelled` 时获取结果

## 支持的输入类型

| 输入类型 | 智能体 | 工作流 | 说明 |
|----------|--------|--------|------|
| 文本 | ✅ | ✅ | 基础文本对话 |
| 图像 | ✅ | ✅ | 需使用通义千问 VL 系列模型 |
| 文件 | ✅ | ❌ | 仅智能体支持，需配置文件处理方式（全文引用/切片检索） |

## 限制和注意事项

- 所有文档中的 API 仅适用于**中国大陆版（北京地域）**。
- 异步调用**不支持**流式输出（`stream=true` 与 `background=true` 不可同时使用）。
- `session_id` 在最后一次请求后 **1 小时**内有效。
- 不建议在生产环境中将 API Key 硬编码到代码中，应通过环境变量 `DASHSCOPE_API_KEY` 配置。
- 使用图像输入时，智能体应用需将文件处理方式选为**自定义处理**；工作流应用需将模型节点的模型入参变量填为 `imageList`。
- RAM 子账号访问"业务空间管理"页面需具备超级管理员权限或已授予 `AliyunBailianFullAccess` / `AliyunBailianControlFullAccess` 权限。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)

