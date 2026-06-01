# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组遵循 OpenAI API 协议规范的服务端点，开发者只需将 `api_key`、`base_url` 和 `model` 替换为百炼平台的对应值，即可使用 OpenAI 官方 SDK 和生态工具直接调用百炼上的模型与应用，无需更改业务代码逻辑。

## 核心价值

- **零成本迁移**：已有基于 OpenAI SDK 的项目，改动三个参数即可切换到百炼服务。
- **生态兼容**：支持 Cursor、Claude Code、Cline、Cherry Studio、Dify 等主流第三方工具通过该接口接入百炼模型。
- **多场景覆盖**：从文本对话、视觉理解到批量推理、应用调用，提供完整的兼容接口矩阵。

## 支持的接口类型

百炼平台提供以下 OpenAI 兼容接口，覆盖不同能力场景：

| 接口类型 | 适用场景 | 说明 |
|---------|---------|------|
| Chat Completions | 文本对话、多轮会话 | 最常用的接口，与 OpenAI Chat API 完全兼容 |
| Responses | 智能体、内置工具调用 | 内置联网搜索、代码解释器等工具，自动管理对话历史 |
| Completions | 代码补全、内容续写 | 适用于非对话式的文本生成 |
| Vision | 图像/视频理解 | 多模态输入，调用视觉模型 |
| Embedding | 文本向量化 | 用于语义检索和 RAG 场景 |
| Files | 文件上传与管理 | 管理用于批量推理等场景的文件 |
| Batch（文件输入） | 大批量异步推理 | 提交文件进行离线批量处理 |
| Batch Chat | 同步批量推理 | 批量发送对话请求 |
| Conversations | 对话上下文管理 | 跨设备维护对话历史 |

## 服务地址（Base URL）

不同地域使用不同的 Base URL，API Key 与地域绑定，不可跨地域混用。

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

Batch Chat 使用独立端点：`https://batch.dashscope.aliyuncs.com/compatible-mode/v1`

> **注意**：德国（法兰克福）地域需先创建业务空间并获取 WorkspaceId 替换占位符。中国香港地域的旧版 URL 即将下线，请关注官方迁移通知。

## 关键配置参数

使用 OpenAI 兼容接口时，需要配置以下三个核心参数：

| 参数 | 说明 | 示例 |
|------|------|------|
| `api_key` | 百炼平台的 API Key，在控制台的密钥管理页面获取 | 通过环境变量 `DASHSCOPE_API_KEY` 传入 |
| `base_url` | 百炼平台对应地域的兼容模式端点 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| `model` | 百炼平台上的模型名称 | `qwen3.6-plus`、`qwen3.7-max` 等 |

认证方式与 OpenAI 一致，通过 HTTP Header `Authorization: Bearer <API_KEY>` 传递。

## 使用场景

### 模型直接调用

最典型的使用方式，通过 OpenAI SDK 调用百炼上的千问系列及第三方模型：

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.6-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你好"}
    ]
)
print(completion.choices[0].message.content)
```

### 应用调用（Responses API）

调用百炼上创建的智能体或工作流应用时，通过 OpenAI 兼容的 Responses API 接入，`base_url` 中需包含应用 ID：

```python
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/"
)
response = client.responses.create(input="你好")
```

### 专用模型调用

机器翻译（qwen-mt）、OCR（qwen-vl-ocr）、离线音视频翻译（qwen3-livetranslate-flash）等专用模型均支持通过 OpenAI 兼容接口调用。部分模型需要通过 `extra_body` 传入非标准参数，例如：

```python
extra_body={"translation_options": {"source_lang": "zh", "target_lang": "en"}}
```

### 第三方工具接入

支持 OpenAI 兼容协议的客户端和开发工具（如 Cursor、Cline、Cherry Studio、Codex、Dify 等）均可通过配置 Base URL 和 API Key 接入百炼。不同计费方

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [get started with models](../guides/get-started-with-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [specialized model](../api/specialized-model.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)
- [application call](../api/application-call.md)

