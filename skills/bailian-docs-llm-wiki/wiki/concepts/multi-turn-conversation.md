# 多轮对话

多轮对话是指用户与大模型应用在同一会话中进行多次交互时，模型能够理解并引用先前对话内容的能力。百炼平台通过不同机制实现多轮对话的上下文管理，使应用能够在连续交互中保持语义连贯。

## 在百炼平台中的使用场景

### 智能体与工作流应用调用

通过 `Application.call` 接口调用智能体或工作流应用时，多轮对话支持两种实现方式：

- **`session_id` 模式**：由服务端自动维护对话历史。首次请求无需传入，系统在响应中返回 `session_id`，后续请求携带该值即可延续对话。有效期为最后一次请求后 **1 小时**，最多支持 **50 轮**。
- **`messages` 模式（推荐）**：由客户端自行维护对话历史数组，每次请求时传入完整的消息列表，控制更灵活。工作流应用使用此模式时，需在大模型节点中配置提示词变量 `historyList` 并重新发布应用。

> 若请求中同时包含 `session_id` 和 `messages`，系统将优先使用 `messages`。

### DashScope API 与 Responses API 的差异

百炼平台提供两套应用调用接口，它们的多轮对话机制有所不同：

| 接口 | 多轮对话机制 | 说明 |
|------|------------|------|
| DashScope API | `session_id` 或 `messages` | 服务端可维护上下文，也支持客户端自管理 |
| OpenAI 兼容 Responses API | 客户端传递完整消息历史 | `pre_response_id` 和 `conversation_id` 功能计划后续支持 |

迁移时需注意两者的上下文管理方式不同。

### Assistant API（已下线）

Assistant API 通过 **Thread** 机制实现多轮对话管理。Thread 自动记录用户和 Assistant 之间的所有消息，开发者无需手动维护上下文。该 API 目前处于下线状态，建议迁移至 Responses API。

### 智能体应用中的短期记忆

在百炼控制台配置智能体应用时，多轮对话上下文作为**短期记忆**存在，支持配置 **0–30 轮**的会话历史保留。轮次越多，模型可参考的上下文越丰富，但也会占用更多的上下文窗口和输入 [Token](token.md)。

### 与长期记忆的配合

多轮对话的上下文属于会话级别的短期记忆，会话结束后即失效。若需跨会话持续记住用户偏好或历史信息，可结合**记忆库**实现长期记忆。记忆库通过 `AddMemory` 接口将对话内容中的关键信息自动提取为记忆片段，在后续会话中通过 `SearchMemory` 检索并注入 Prompt，实现个性化回复。

## 关键参数与配置

| 参数 | 类型 | 说明 |
|------|------|------|
| `session_id` | string | 会话 ID，用于服务端维护对话历史。首次请求不传，后续从响应中获取并回传 |
| `messages` | array | 对话历史数组，每条消息包含 `role`（`user` / `assistant`）和 `content` 字段 |
| 短期记忆轮次 | 0–30 | 在控制台智能体配置中设置，控制模型可参考的历史对话轮数 |

### 基本示例（`session_id` 模式）

```python
import os
from dashscope import Application

# 第一轮对话
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='我叫小明'
)
session_id = response.output.session_id

# 第二轮对话，携带 session_id
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='我叫什么？',
    session_id=session_id
)
print(response.output.text)  # 模型将回答"小明"
```

### 基本示例（`messages` 模式）

```python
import os
from dashscope import Application

messages = [
    {"role": "user", "content": "我叫小明"},
    {"role": "assistant", "content": "你好，小明！"},
    {"role": "user", "content": "我叫什么？"}
]

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    messages=messages
)
print(response.output.text)
```

## 注意事项

- `session_id` 的有效期为最后一次请求后 1 小时，超时后对话历史将丢失。
- `messages` 模式下，开发者需自行管理消息数组的长度，避免超出模型的上下文窗口限制。
- 工作流应用使用 `messages` 模式时，必须在大模型节点的提示词中配置 `historyList` 变量并重新发布，否则历史消息不会生效。
- 多轮对话的历史消息会占用输入 [Token](token.md)，轮次越多成本越高，建议根据业务需要合理控制保留轮数。

## 关联主题页

- [assistant api](../guides/assistant-api.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [llm application](../guides/llm-application.md)
- [application call](../api/application-call.md)

