# 多轮对话

多轮对话是指用户与大模型应用在同一会话中进行多次连续交互，系统在每次响应时能够理解并引用之前的对话内容，从而实现上下文连贯的自然语言交互。在百炼平台中，多轮对话是智能体应用、工作流应用和 Assistant API 的核心能力之一。

## 在百炼平台中的使用场景

### 智能体与工作流应用调用

通过 `Application.call` 接口调用智能体或工作流应用时，多轮对话支持两种实现模式：

- **`session_id` 模式**：由服务端自动维护对话历史。首次调用无需传入 `session_id`，系统在响应中返回一个会话 ID，后续请求携带该 ID 即可自动加载上下文。有效期为最后一次请求后 **1 小时**，最多支持 **50 轮**对话。
- **`messages` 模式（推荐）**：由客户端自行维护对话历史数组，每次请求传入完整的消息列表。控制更灵活，不受有效期限制。工作流应用使用此模式时，需在大模型节点配置提示词变量 `historyList` 并发布应用。

> **注意**：若请求中同时包含 `session_id` 和 `messages`，系统将优先使用 `messages`。

### OpenAI 兼容 Responses API

使用 Responses API 调用百炼应用时，当前需要在每次请求的 `input` 中传递完整的对话历史（`pre_response_id` 和 `conversation_id` 功能后续支持）。这与 DashScope API 的 `session_id` 服务端托管机制不同，迁移时需注意。

### Assistant API（已下线）

Assistant API 通过 Thread 机制自动维护对话历史。Thread 记录用户和 Assistant 之间的所有消息，开发者无需手动管理上下文。该 API 已下线，建议迁移至 Responses API。

### 智能体应用配置

在百炼控制台创建智能体应用时，可通过**短期记忆**参数配置多轮对话的上下文轮数，支持 **0–30 轮**。该参数决定每次模型推理时携带的历史对话轮数。

### 与长期记忆的关系

多轮对话属于会话内的短期上下文管理，会话结束后上下文即失效。如需跨会话持久化用户信息，可结合记忆库实现长期记忆——每轮对话结束后调用 `AddMemory` 接口将对话写入记忆库，下次会话时通过 `SearchMemory` 检索历史记忆并注入 Prompt。

## 关键参数与配置

### DashScope API 参数

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `session_id` | string | 否 | 多轮对话会话 ID，首次调用不传，后续使用响应返回的值 |
| `messages` | array | 否 | 自行维护的对话历史数组，每个元素包含 `role` 和 `content` |

### 智能体应用控制台配置

| 配置项 | 说明 |
|--------|------|
| 短期记忆轮数 | 0–30 轮，控制模型可见的历史对话深度 |

## 代码示例

### 使用 session_id 实现多轮对话（Python）

```python
import os
from dashscope import Application

# 第一轮对话
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='我想去杭州旅游'
)
session_id = response.output.session_id

# 第二轮对话，携带 session_id
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='帮我推荐几个景点',
    session_id=session_id
)
print(response.output.text)
```

### 使用 messages 实现多轮对话（Python）

```python
import os
from dashscope import Application

messages = []

# 第一轮
messages.append({"role": "user", "content": "我想去杭州旅游"})
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='我想去杭州旅游'
)
messages.append({"role": "assistant", "content": response.output.text})

# 第二轮
messages.append({"role": "user", "content": "帮我推荐几个景点"})
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='帮我推荐几个景点',
    messages=messages
)
print(response.output.text)
```

## 注意事项

- `session_id` 的有效期为最后一次请求后 1 小时，超时后上下文将被清除。
- 对话历史会占用模型的上下文窗口，轮数过多可能导致输入 Token 超限，建议根据业务需要合理设置短期记忆轮数。
- DashScope API 与 Responses API 的多轮对话机制不同：前者支持服务端托管（`session_id`），后者目前需客户端传递完整历史。
- 如需超出会话生命周期的记忆能力，应结合记忆库功能实现长期记忆。

## 关联主题页

- [assistant api](../guides/assistant-api.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [memory library overview](../guides/memory-library-overview.md)
- [llm application](../guides/llm-application.md)
- [application call](../api/application-call.md)
- [long term memory new](../api/long-term-memory-new.md)

