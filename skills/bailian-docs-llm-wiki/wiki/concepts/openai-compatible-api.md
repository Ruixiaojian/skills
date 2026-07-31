# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 API 协议，完全遵循 OpenAI REST API 的路径、请求格式、响应结构与参数命名规范（如 `/v1/chat/completions`），使开发者无需修改业务代码即可将现有基于 OpenAI SDK 的应用无缝迁移到百炼，调用千问（Qwen）及第三方大模型。

## 在百炼平台的不同场景中如何使用

OpenAI 兼容接口是百炼面向开发者最主流的接入方式，覆盖以下核心场景：

- **通用文本生成**：通过 `chat/completions` 接口调用 `qwen3.7-plus`、`qwen3.7-max` 等模型，支持多轮对话、system [prompt](../guides/prompt.md)、流式响应（`stream=true`）和 [Token](token.md) 统计（`stream_options={"include_usage": true}`）。
- **智能体（Agent）交互**：使用 `responses` 子路径（如 `/compatible-mode/v1/responses`）调用已发布的智能体应用，自动注入上下文、[工具调用](tool-use.md)结果与联网能力，支持 `previous_response_id` 实现多轮状态追踪。
- **向量嵌入（Embedding）**：调用 `/v1/embeddings` 接口，兼容 `text-embedding-v3`/`v4` 系列模型，支持多语种、可选维度（`dimensions=1024`），但不支持[多模态](multi-modal.md) Embedding 模型。
- **视觉理解（Vision）**：通过 `chat/completions` 传入含 `image_url` 或 Base64 图像的结构化 `content`，调用 `qwen3-vl-plus`、`qwen3-vl-flash` 等模型；注意 QVQ 等模型仅支持[流式输出](streaming-output.md)。
- **批量处理（Batch）**：提供两种模式——**文件输入模式**（异步 JSONL 处理，成本降低 50%）和 **单请求同步模式**（Batch Chat），均需显式指定 `enable_thinking` 控制推理深度。
- **代码补全（Completions）**：专用于前缀/中缀生成任务，当前仅支持 `qwen-coder-turbo` 模型，限北京地域。

> ⚠️ 注意：并非所有模型和能力都支持 OpenAI 兼容协议。例如：
> - `Qwen-Audio`、`Qwen-Omni`（语音）、`Qwen-OCR`（纯 OCR）仅支持 DashScope 原生协议；
> - [工具调用](tool-use.md)（function calling）在 OpenAI 兼容接口中**暂不支持结构化工具定义**，需改用 DashScope 或 Anthropic 兼容接口；
> - [多模态](multi-modal.md) Embedding（如 `qwen3-vl-embedding`）不可通过 `/v1/embeddings` 调用。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `base_url` | string | ✅ | **必须配置为业务空间专属域名**，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`。旧域名（如 `dashscope.aliyuncs.com`）兼容但不推荐。各地域域名不同，不可混用。 | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | string | ✅ | 百炼控制台生成的 API Key，**必须与 `base_url` 所属地域和计费方案严格匹配**。建议通过环境变量 `DASHSCOPE_API_KEY` 配置。 | `sk-xxx` |
| `model` | string | ✅ | 模型 ID，需严格匹配[支持列表](https://help.aliyun.com/zh/model-studio/developer-reference/openai-compatible-api-reference)，区分大小写与版本号。 | `"qwen3.7-plus"`、`"text-embedding-v4"`、`"qwen3-vl-plus"` |
| `messages` | array | ✅（Chat） | 对话历史数组，格式为 `[{ "role": "user", "content": "..." }]`；支持 `system`、`user`、`assistant` 角色；`content` 可为字符串或含 `text`/`image_url`/`image_url.url` 的对象（Vision 场景）。 | `[{"role":"user","content":"你好"}]` |
| `stream` | boolean | ❌（默认 `false`） | 启用流式响应。返回 `text/event-stream`，每 chunk 包含 `delta.content` 和 `finish_reason`。流式结尾可含 [Token](token.md) 统计（需 `stream_options={"include_usage":true}`）。 | `true` |
| `temperature` | number | ❌（默认 `1.0`） | 控制输出随机性（0.0–2.0）。部分模型（如 `qwen3.8-max-preview`）会强制修正低于阈值的值（如 `<0.6` → `0.6`）。 | `0.7` |
| `max_tokens` | integer | ❌（建议设置） | 限制响应最大 token 数，防止超限或耗尽配额。 | `1024` |
| `enable_thinking` | boolean | ⚠️（Batch/Responses 场景必填） | 控制是否启用深度推理模式。`qwen3.7`/`qwen3.6`/`qwen3.5` 系列默认开启，**必须作为 body 顶层参数传入，不可置于 `extra_body`**。 | `true` |
| `previous_response_id` | string | ⚠️（Responses 多轮场景） | 上一轮响应的顶层 `id`（UUID 格式），用于自动恢复上下文。非 `output.msg_xxx` 中的 ID。 | `"resp_abc123..."` |

## 面向开发者：简洁实用指南

✅ **快速上手（Python + OpenAI SDK）**  
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://ws-xxx.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为你的 WorkspaceId + 地域
)

# 文本生成
resp = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "用 Python 写一个斐波那契函数"}]
)
print(resp.choices[0].message.content)

# 流式响应
for chunk in client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你好"}],
    stream=True,
    stream_options={"include_usage": True}
):
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

✅ **关键检查清单**  
- ✅ `base_url`、`api_key`、`model` 三者必须属于**同一地域 + 同一计费方案**（[Token](token.md) Plan / Coding Plan / 按量）；  
- ✅ 使用业务空间专属域名（含 `WorkspaceId`），避免跨地域调用失败；  
- ✅ 流式响应需客户端正确解析 `text/event-stream`，非 JSON；  
- ✅ `enable_thinking`、`previous_response_id` 等场景特定参数务必放在请求体顶层；  
- ✅ 查看[模型兼容性矩阵](https://help.aliyun.com/zh/model-studio/developer-reference/openai-compatible-api-reference)确认目标模型是否支持所需能力（如 Vision、Embedding、Batch）。

❌ **常见错误规避**  
- 不要将 `top_p` 依赖默认值（OpenAI 兼容接口默认 `1.0`，DashScope 原生默认 `0.8`）→ 显式指定；  
- 不要在 `extra_body` 中传 `enable_thinking` → 放入主 request body；  
- 不要混用 OpenAI 和 Anthropic 的 `base_url` → 协议栈隔离，参数行为不同；  
- 不要对 `qwen3.8-max-preview` 尝试关闭 `thinking` → 服务端强制启用，客户端设置无效。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [get started with models](../guides/get-started-with-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [application call](../api/application-call.md)


