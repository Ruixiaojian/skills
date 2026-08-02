# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 API 协议，严格遵循 OpenAI REST API 的路径、请求/响应格式、字段命名与语义约定（如 `/v1/chat/completions`、`messages` 数组、`delta.content` 流式结构等），使开发者能复用现有 OpenAI SDK（如 `openai>=1.0`）、LangChain、Dify 等生态工具，零代码改造即可接入千问（Qwen）及第三方模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移存量应用**：已有基于 OpenAI SDK 的 Python/Node.js 项目，只需替换 `base_url` 和 `api_key`，即可调用 `qwen3.7-plus`、`qwen-vl-plus`（多模态）、`text-embedding-v3`（向量）等模型，无需重写业务逻辑。
- **多模态统一接入**：图像理解（Qwen-VL）、文本生成（Qwen3）、嵌入（text-embedding）均通过同一套 `/compatible-mode/v1` 路径提供，仅需切换 `model` 参数，客户端保持协议一致。
- **增强型对话能力**：选择 `OpenAI 兼容 Responses` 接口（而非基础 `chat/completions`），可自动启用联网搜索、代码解释器、网页提取等工具链，同时保留标准 OpenAI 消息格式，支持 `previous_response_id` 实现多轮上下文锚定。
- **批量与异步任务**：通过 `batch.dashscope.aliyuncs.com/compatible-mode/v1` 调用 Batch Chat，或结合 `/files` + `/batches` 实现 JSONL 批处理，均复用 OpenAI 文件与批处理语义。
- **开发工具无缝集成**：Cursor、Cherry Studio、Hermes Agent、Dify 等工具原生支持 OpenAI 协议，配置百炼的 `base_url` 后即可直接选用 `qwen3.8-max-preview` 等模型，思考模式（`enable_thinking`）等高级能力亦可通过标准参数透传。

## 关键参数和配置

| 参数 | 类型 | 说明 | 注意事项 |
|------|------|------|----------|
| `base_url` | string | 必填服务端点，决定协议兼容性与地域/计费方案 | 生产推荐使用业务空间专属域名：<br>`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`；<br>试用环境用 `https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；<br>Batch Chat 固定为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1` |
| `model` | string | 模型 ID，必须与文档所列完全一致 | `qwen3.7-plus`、`qwen-vl-flash`、`text-embedding-v3` 等均需精确匹配；带时间后缀的版本（如 `qwen3.7-plus-2026-05-26`）不可省略 |
| `messages` | array | OpenAI 标准消息数组，含 `role`（`system`/`user`/`assistant`）和 `content` | `system` 消息在部分模型（如 `qwen3.7-plus`）中生效；多模态需在 `content` 中嵌入 `{"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}` |
| `enable_thinking` | boolean | 控制是否启用思考链（R1 messages format） | 仅 `qwen3.5/3.6/3.7/3.8` 系列支持；必须作为请求 body 顶层参数传入，不可置于 `extra_body` |
| `previous_response_id` | string | Responses API 多轮对话上下文锚点 | 必须传入上一轮响应的顶层 `id`（如 `"resp_abc123"`），非 `output` 内部消息 ID |
| `stream` | boolean | 是否启用流式响应 | `true` 时返回 `text/event-stream`，客户端需按 SSE 解析 `data: {...}`；注意：Batch Chat 不支持 `stream=true` |

> ⚠️ 重要差异提醒：  
> - `max_tokens` 在 `OpenAI 兼容 Responses` 中限制**总输出长度**（含工具调用结果），而 DashScope 原生接口仅限制模型生成部分；  
> - `qwen-vl-plus` 等多模态模型不可用于纯文本 `chat/completions`，需使用 `/v1/chat/completions` 并传入图像内容；  
> - 第三方模型（如 DeepSeek、Kimi）仅在中国内地地域可用，且部分不支持 `enable_thinking`。

## 面向开发者，简洁实用

- ✅ **三步启动**：  
  1. 在 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建密钥（按地域独立）；  
  2. 设置环境变量 `DASHSCOPE_API_KEY=sk-xxx`；  
  3. 用 OpenAI SDK 发起请求（示例见下），无需安装额外依赖。

- ✅ **推荐调用方式（Python）**：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  
  # 标准对话
  response = client.chat.completions.create(
      model="qwen3.7-plus",
      messages=[{"role": "user", "content": "你好"}],
      stream=False
  )
  print(response.choices[0].message.content)
  
  # 启用思考模式（若模型支持）
  response = client.chat.completions.create(
      model="qwen3.7-plus",
      messages=[{"role": "user", "content": "分析这段代码"}],
      enable_thinking=True  # 顶层参数，非 extra_body
  )
  ```

- ✅ **调试技巧**：  
  - 用 `curl` 快速验证：确保 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 和 `Content-Type: application/json` 正确；  
  - 查看响应头 `x-dashscope-usage` 获取实际 token 消耗；  
  - 遇到 `401` 检查 `api_key` 与 `base_url` 是否属同一地域/计费方案；`400` 则检查 `model` 名称拼写与功能支持性。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [get started with models](../guides/get-started-with-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [model deployment 1](../guides/model-deployment-1.md)


