# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 API 协议层，严格遵循 OpenAI REST API 的路径、请求体结构、响应格式与错误码规范，使开发者能复用现有 OpenAI SDK（如 `openai>=1.0`）、LangChain 集成、Cursor/Cherry Studio 等工具链，零代码或极小改动即可接入 Qwen 及第三方大模型服务。

## 在百炼平台的不同场景中如何使用

- **快速迁移已有项目**：若应用已基于 OpenAI SDK 开发（如 `client.chat.completions.create()`），只需替换 `api_key` 和 `base_url`，无需修改业务逻辑即可调用 `qwen3.8-max`、`deepseek-v4-flash` 等模型。  
- **[多模态](multimodal.md)能力扩展**：通过 OpenAI Vision 接口（`/v1/chat/completions` + `image_url`）调用 `qwen3-vl-plus`、`QVQ` 等视觉模型，支持图文理解与生成。  
- **智能体与工作流集成**：使用 OpenAI 兼容的 Responses API（`/v1/responses`）调用已发布的智能体应用，自动处理联网搜索、网页提取等内置工具，并通过 `previous_response_id` 实现多轮上下文延续。  
- **嵌入向量服务**：调用 `/v1/embeddings` 接口使用 `text-embedding-v3`/`v4` 模型，支持 `dimensions` 参数动态控制向量维度。  
- **批量与文件处理**：结合 Files API（`/v1/files`）上传文档用于问答，或通过 Batch Chat / Batch File（JSONL）接口实现低成本批量推理。

> ⚠️ 注意：OpenAI 兼容接口**不支持音频模型（如 Qwen-Audio）**、**不支持 `logprobs` 与 `n > 1` 并行采样**，且部分高级能力（如细粒度流式 chunk 控制、`incremental_output`）需切换至 DashScope 原生接口。

## 关键参数和配置

| 参数 | 类型 | 说明 | 是否必需 | 备注 |
|------|------|------|----------|------|
| `base_url` | string | 接入端点，必须为 `compatible-mode/v1` 路径 | 是 | 推荐使用业务空间专属域名：<br>`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`；<br>旧域名（如 `dashscope.aliyuncs.com`）兼容但不推荐。 |
| `model` | string | 模型 ID，需与控制台开通列表一致 | 是 | 如 `qwen3.8-max`、`qwen3-vl-plus`、`text-embedding-v3`；<br>三方模型（如 `deepseek-v4-flash`）仅限中国内地地域。 |
| `messages` | array | 对话历史，格式 `[{"role": "user", "content": "..."}]` | 是（Chat/Vision/Responses） | `system` 角色中禁止注入指令性内容，否则触发安全拦截。 |
| `stream` | boolean | 启用流式响应 | 否（默认 `false`） | 流式响应中需显式设置 `stream_options={"include_usage": true}` 才返回 token 统计。 |
| `enable_thinking` | boolean | 启用混合思考模式（Qwen3.5+ 系列） | 否（默认关闭） | 需置于 `extra_body` 中（如 `extra_body={"enable_thinking": true}`），非顶层参数。 |
| `previous_response_id` | string | 上一轮 Responses API 返回的顶层 `id` | 否（仅 Responses API） | 用于自动注入上下文，**不是 `output` 内消息的 `id`**。 |
| `dimensions` | integer | 向量维度（仅 embedding v3/v4） | 否（默认 1024） | `v1`/`v2` 不支持该参数。 |

## 面向开发者的实用提示

- ✅ **首选 SDK 初始化方式**（推荐）：
  ```python
  from openai import OpenAI
  import os

  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),  # 环境变量管理密钥
      base_url="https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为实际 WorkspaceId
  )
  ```

- ✅ **Chat 调用示例**：
  ```python
  response = client.chat.completions.create(
      model="qwen3.8-max",
      messages=[{"role": "user", "content": "用 Python 写一个斐波那契数列生成器"}],
      stream=True
  )
  for chunk in response:
      if chunk.choices[0].delta.content:
          print(chunk.choices[0].delta.content, end="", flush=True)
  ```

- ✅ **Vision 调用示例**（需模型支持）：
  ```python
  response = client.chat.completions.create(
      model="qwen3-vl-plus",
      messages=[
          {
              "role": "user",
              "content": [
                  {"type": "text", "text": "图中有什么？"},
                  {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,..."}}
              ]
          }
      ]
  )
  ```

- ❌ **避免常见错误**：
  - 混用不同地域的 API Key 与 Base URL（如北京 Key + 新加坡 URL）；
  - 在 `system` 消息中写 `"你必须回答..."` 等强制指令；
  - 对 `qwen-coder-turbo` 使用 `/chat/completions`（应改用 `/completions`）；
  - 期望 OpenAI 兼容接口返回 `logprobs` 或多候选（`n=2`）——请改用 DashScope 原生接口。

如需更高控制力（如自定义 stop tokens、细粒度流式解析、工具调用增强），建议直接选用 DashScope 原生接口。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [get started with models](../guides/get-started-with-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [application call](../api/application-call.md)


