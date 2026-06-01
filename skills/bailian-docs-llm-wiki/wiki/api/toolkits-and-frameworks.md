# toolkits and frameworks

阿里云百炼平台提供一系列与 OpenAI 兼容的 API 接口，开发者只需调整 API Key、BASE_URL 和模型名称，即可将现有 OpenAI 生态代码快速迁移至百炼服务。同时，百炼也支持通过 LangChain 等主流开发框架进行集成，覆盖文本生成、视觉理解、文本向量化、文件管理、批量推理等多种场景。

## 兼容接口总览

百炼平台提供以下 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，各接口适用于不同场景：

| 接口类型 | 适用场景 | 详细文档 |
|---------|---------|---------|
| Chat Completions | 文本对话、多轮会话 | [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) |
| Responses | 智能体原生功能，内置工具调用 | [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) |
| Completions | 代码补全、内容续写 | [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md) |
| Vision | 图像/视频理解 | [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md) |
| Embedding | 文本向量化 | [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md) |
| Files | 文件上传/管理 | [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md) |
| Batch (文件输入) | 大批量异步推理 | [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) |
| Batch Chat | 同步批量推理（限时5折） | [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md) |
| Conversations | 跨设备对话上下文管理 | [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md) |

## 服务地址（BASE_URL）

根据调用方式和地域选择对应的 BASE_URL：

| 地域 | SDK 调用 base_url | HTTP 请求端点 |
|------|-------------------|--------------|
| 北京 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions` |
| 弗吉尼亚 | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` | `POST https://dashscope-us.aliyuncs.com/compatible-mode/v1/chat/completions` |
| 新加坡 | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` | `POST https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions` |

Batch Chat 使用独立端点：`https://batch.dashscope.aliyuncs.com/compatible-mode/v1`

> **注意**：中国香港地域的旧版 URL `https://cn-hongkong.dashscope.aliyuncs.com/compatible-mode/v1` 即将下线，请迁移至新版路径 `https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/compatible-mode/v1`。Responses API 和 Conversations API 的旧版路径（含 `/api/v2/apps/protocols/`）也即将停止维护。

## 支持的模型

### 文本生成模型（Chat Completions / Responses）

根据 [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md) 文档，中国内地支持的主要模型系列包括：

- **商业版**：千问 Max（qwen3.7-max、qwen3-max 等）、Plus（qwen3.6-plus、qwen-plus 等）、Flash（qwen3.6-flash、qwen-flash 等）、Turbo、Coder、Long、QwQ、数学模型
- **开源版**：qwen3.6-35b-a3b、qwen3.5-397b-a17b、qwen3-235b-a22b、qwen3-32b、qwq-32b 等

Responses API 支持的模型范围较小，主要包括 `qwen3.7-max`、`qwen3.6-plus`、`qwen3.6-flash`、`qwen3.5-plus`、`qwen3.5-flash` 以及部分开源模型和 Coder 系列。

### 视觉模型（Vision）

包括 Qwen3-VL 系列（qwen3-vl-plus、qwen3-vl-flash 等）、QVQ 系列（qvq-max、qvq-plus）以及 OCR 系列（qwen-vl-ocr）。

### 文本向量模型（Embedding）

| 模型 | 向量维度 | 单行最大 [Token](../concepts/token.md) 数 |
|------|---------|-----------------|
| text-embedding-v4 | 64~2048（默认1024） | 8,192 |
| text-embedding-v3 | 64~1024（默认1024） | 8,192 |
| text-embedding-v2 | 1,536（固定） | 2,048 |
| text-embedding-v1 | 1,536（固定） | 2,048 |

### 代码补全模型（Completions）

仅支持 Qwen Coder 部分模型：qwen2.5-coder-7b/14b/32b-instruct、qwen-coder-turbo 系列。该接口仅适用于中国内地（北京地域）。

## 快速开始

### 前提条件

1. 开通阿里云百炼服务并获取 API Key
2. 将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`（推荐）
3. 安装对应 SDK（如 `pip install -U openai`）

### 基础调用示例（Chat Completions）

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '你是谁？'}
    ]
)
print(completion.model_dump_json())
```

### Responses API 调用示例

Responses API 是 Chat Completions 的演进版本，支持内置工具、更灵活的输入和简化的上下文管理（通过 `previous_response_id`）。详见 [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

response = client.responses.create(
    model="qwen3.6-plus",
    input="你能做些什么？"
)
print(response.output_text)
```

## LangChain 集成

根据 [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)，百炼支持两种 LangChain 集成方式：

### 通过 OpenAI 兼容模式

仅支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)覆盖的模型。安装 `langchain_openai` 后：

```python
from langchain_openai import ChatOpenAI

chatLLM = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-plus",
)
```

### 通过 DashScope 原生模式

支持百炼所有文本生成模型（包括部署后的模型）。安装 `langchain-community` 和 `dashscope` 后：

```python
from langchain_community.chat_models.tongyi import ChatTongyi

chatLLM = ChatTongyi(
    model="qwen-plus",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"),
)
```

Java 开发者可通过 LangChain4j（需 Java 17+）使用 Plain Java 或 Spring Boot 方式集成。

## 批量推理

百炼提供两种批量推理方式，均享受 **50% 费用折扣**：

| 方式 | 特点 | base_url |
|------|------|----------|
| **Batch Chat**（同步） | 保持同步调用方式，请求排队后返回结果，默认超时 3600 秒 | `https://batch.dashscope.aliyuncs.com/compatible-mode/v1` |
| **Batch File**（异步） | 通过 JSONL 文件批量提交，异步处理后下载结果 | 同标准 base_url |

> **注意**：在 Batch 场景下，`qwen3.7-max`、`qwen3.6` 和 `qwen3.5` 系列模型默认开启思考模式，会产生额外思考 tokens 导致成本增加。建议显式设置 `enable_thinking` 参数。

## 文件管理

通过 OpenAI 兼容的 Files API 上传文件，可用于：

- **Qwen-Long** 长文档问答（purpose 设为 `file-extract`，单文件最大 150 MB）
- **Batch 推理**任务输入（purpose 设为 `batch`，单文件最大 500 MB）

存储限制：最多 10,000 个文件，总大小不超过 100 GB。

## 关键限制与注意事项

- **不同地域的 API Key 不通用**，北京、新加坡、弗吉尼亚等地域需分别获取。
- Completions 接口**仅支持北京地域**和 Qwen Coder 部分模型。
- QVQ 模型**仅支持[流式输出](../concepts/streaming.md)**。
- 多模态 Embedding 模型（如 qwen3-vl-embedding）**不支持** [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，需使用原生 API。
- Responses API 的 `previous_response_id` 有效期为 **7 天**。
- Conversations API 删除会话后，会话中的消息项**不会被删除**。
- LangChain4j 1.0.0-beta3 需要 **Java 17** 及以上版本。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)

