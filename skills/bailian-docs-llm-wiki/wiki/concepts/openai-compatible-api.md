# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组遵循 OpenAI API 规范的服务端点，开发者可直接使用 OpenAI 官方 SDK 或任何兼容 OpenAI 协议的工具，仅需替换 API Key、Base URL 和模型名称，即可调用百炼平台上的千问（Qwen）系列及其他模型，实现零成本或低成本迁移。

## 核心价值

- **迁移成本最低**：已有 OpenAI 代码的项目只需修改三个配置项即可切换到百炼服务。
- **生态兼容广泛**：凡是支持 OpenAI 协议的第三方客户端、IDE 插件、Agent 框架（如 Cursor、Claude Code、Dify、Cherry Studio、LangChain 等）均可直接接入。
- **覆盖多种能力**：不仅限于文本对话，还扩展至视觉理解、向量化、文件管理、批量推理、语音翻译等场景。

## 支持的接口类型

百炼通过 OpenAI 兼容接口暴露了以下能力：

| 接口 | 用途 | 说明 |
|------|------|------|
| Chat Completions | 文本对话、多轮会话 | 最常用的接口，兼容性最广 |
| Responses | 内置工具调用的智能体场景 | 内置联网搜索、代码解释器，自动管理对话历史 |
| Completions | 代码补全、内容续写 | 非对话式的文本生成 |
| Vision | 图像/视频理解 | 通过多模态消息格式传入图像 |
| Embedding | 文本向量化 | 用于检索增强等场景 |
| Files | 文件上传与管理 | 配合批量推理等功能使用 |
| Batch | 大批量异步推理 | 文件输入模式和 Batch Chat 模式 |
| Conversations | 跨设备对话上下文管理 | 服务端维护对话状态 |

此外，百炼的**应用调用**（智能体和工作流）也提供了基于 Responses API 的 OpenAI 兼容入口，以及**专用模型**（机器翻译、OCR、语音翻译等）也大多支持 OpenAI 兼容接口。

## 关键配置

### 三要素

使用 OpenAI 兼容接口只需配置三项：

| 配置项 | 说明 |
|--------|------|
| `api_key` | 百炼平台的 API Key，建议存入环境变量 `DASHSCOPE_API_KEY` |
| `base_url` | 按地域和计费方案选择对应的服务地址 |
| `model` | 百炼平台上的模型名称，如 `qwen3.6-plus`、`qwen3.7-max` |

### 服务地址（Base URL）

不同地域的 Base URL **不可混用**，API Key 也需与地域对应：

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

如果使用 [Token](token.md) Plan 团队版或 Coding Plan 等订阅方案，Base URL 有所不同，需使用对应方案的专属地址和 API Key。

Batch Chat 使用独立端点：`https://batch.dashscope.aliyuncs.com/compatible-mode/v1`

## 快速示例

### Python

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.6-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"}
    ]
)
print(completion.choices[0].message.content)
```

### Node.js

```javascript
import OpenAI from "openai";

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
});

const completion = await client.chat.completions.create({
    model: "qwen3.6-plus",
    messages: [{ role: "user", content: "你是谁？" }],
});
console.log(completion.choices[0].message.content);
```

## 在不同场景中的使用

### 文本生成模型调用

最典型的使用场景。通过 Chat Completions 接口调用千问系列模型（qwen3.7-max、qwen3.6-plus、qwen3.6-flash 等）以及 DeepSeek、Kimi、GLM 等第三方模型，API 格式完全一致。

### 专用模型调用

机器翻译（qwen-mt-plus）、OCR 文字提取（qwen-vl-ocr-latest）、GUI 自动化（gui-plus）、语音翻译（qwen3-livetranslate-flash）等专用模型均通过 OpenAI 兼容接口调用。部分模型使用非标准参数（如 `translation_options`），需通过 `extra_body` 传入：

```python
completion = client.chat.completions.create(
    model="qwen-mt-plus",
    messages=[{"role": "user", "content": "待翻

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [get started with models](../guides/get-started-with-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [specialized model](../api/specialized-model.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)
- [application call](../api/application-call.md)

