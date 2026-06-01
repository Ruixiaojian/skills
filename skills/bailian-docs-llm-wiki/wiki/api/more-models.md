# [more](more.md) models

百炼平台除了通用大语言模型和 Embedding 模型外，还提供了多种专用模型，包括文本排序（Rerank）、意图理解和法律行业大模型等。这些模型面向特定场景优化，可与通用模型配合使用，构建更完整的 AI 应用流水线。

## 支持的模型

### 文本排序模型（Rerank）

文本排序模型用于对检索召回的文档进行二次精排，提升 RAG 等应用的准确率。详见 [文本排序](../../raw/model-api-reference/more-models/text-rerank-api.md)。

> **注意**：gte-rerank 模型将于 2026 年 05 月 30 日下线，推荐使用 qwen3-rerank 替代。

| 模型名称 | 最大文档数 | 单条最大 Token | 请求最大 Token | 主要场景 |
|---|---|---|---|---|
| qwen3-rerank | 500 | 4,000 | — | 文本语义检索、RAG |
| qwen3-vl-rerank | 文本100/图片40/视频4 | 8,000 | 120,000 | 跨模态搜索、图片检索 |
| gte-rerank-v2 | — | — | 30,000 | 多语种文本排序 |

- **qwen3-vl-rerank** 支持文本、图片（JPEG/PNG/WEBP 等）、视频（MP4/AVI/MOV）多模态输入
- **qwen3-rerank** 支持 `instruct` 参数自定义排序策略（如问答检索、语义相似度排序）

### 意图理解模型

意图理解模型能在百毫秒级时间内解析用户意图并选择合适工具。详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。

| 模型名称 | 上下文长度 | 最大输入 | 最大输出 | 输入成本（每百万 Token） | 输出成本（每百万 Token） |
|---|---|---|---|---|---|
| tongyi-intent-detect-v3 | 8,192 | 8,192 | 1,024 | 0.4 元 | 1 元 |

### 法律行业模型

通义法睿基于千问微调，专注法律场景。详见 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。

| 模型名称 | 上下文长度 | 最大输出 | 输入成本（每百万 Token） |
|---|---|---|---|
| farui-plus | 12k | 2k | 20 元 |

## 使用方式

### 前提条件

所有模型均需要：
1. 获取 API Key 并配置到环境变量 `DASHSCOPE_API_KEY`
2. 如使用 SDK 调用，需安装对应的 DashScope SDK 或 OpenAI SDK

### 文本排序模型

不同排序模型使用**不同的 API 端点**：

- **qwen3-rerank**：`POST https://dashscope.aliyuncs.com/compatible-api/v1/reranks`
- **qwen3-vl-rerank / gte-rerank-v2**：`POST https://dashscope.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank`

> **注意**：两种接口的请求体结构不同。`qwen3-rerank` 的 `query`、`documents` 参数位于顶层，而其他模型需嵌套在 `input` 对象内。响应格式也有差异：`qwen3-rerank` 的 `results` 位于顶层，其他模型嵌套在 `output` 中。

SDK 调用示例（Python）：

```python
import dashscope

resp = dashscope.TextReRank.call(
    model="qwen3-rerank",
    query="什么是文本排序模型",
    documents=["文档1", "文档2", "文档3"],
    top_n=2,
    return_documents=True,
    instruct="Given a web search query, retrieve relevant passages that answer the query."
)
```

### 意图理解模型

通过 System Message 控制输出模式：

| 模式 | System Message 关键指令 | 输出内容 |
|---|---|---|
| 意图 + 函数调用 | `Response in INTENT_MODE.` + 工具定义 | `<tags>` + `<tool_call>` + `<content>` |
| 仅意图分类 | `Just reply with the chosen tag.` + 意图列表 | 意图标签字符串 |
| 仅函数调用 | 标准 tool calling 格式 | 工具调用信息 |

响应需使用正则解析 `<tags>`、`<tool_call>`、`<content>` 标签结构，原文档提供了 `parse_text` 函数示例。

**性能优化技巧**：将意图分类用大写字母（A/B/C...）指代，可使响应始终为单 Token，显著降低延迟。

### 法律行业模型

farui-plus 使用标准的 `Generation.call` 接口，兼容 DashScope SDK 的对话格式，支持单轮对话、多轮对话和[流式输出](../concepts/streaming.md)。

```python
import dashscope

response = dashscope.Generation.call(
    model="farui-plus",
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '我哥欠我10000块钱，给我生成起诉书。'}
    ],
    result_format='message'
)
```

## 关键参数说明

### 排序模型特有参数

| 参数 | 类型 | 说明 |
|---|---|---|
| `top_n` | int | 返回排序后前 N 个文档，默认返回全部 |
| `return_documents` | bool | 是否返回文档原文，默认 `false`（仅 gte-rerank-v2、qwen3-vl-rerank） |
| `instruct` | string | 自定义排序策略说明，建议英文（仅 qwen3-rerank、qwen3-vl-rerank） |
| `fps` | float | 视频帧采样率，范围 [0,1]，默认 1.0（仅 qwen3-vl-rerank） |

### 排序相关性得分

`relevance_score` 取值 0.0~1.0，为**当前请求内的相对分数**，不可用于跨请求比较。

## 限制和注意事项

- **排序模型输入截断**：超过单条最大 Token 限制的内容会被截断，截断后可能导致排序结果不准确
- **请求最大 Token 计算**：公式为 `Query Tokens × Document 数量 + Document Tokens 总和`
- **qwen3-vl-rerank 视频输入**：仅支持 URL 方式，不支持 Base64
- **意图理解模型**：响应为自定义标签格式（非标准 JSON），需自行解析
- **farui-plus**：仅标注了输入成本（20 元/百万 Token），文档未明确输出成本；Java SDK 中 `Generation` 对象非线程安全，需注意并发场景下的使用
- 所有模型均受限流策略约束，具体条件参见平台限流文档

## 来源文档

- [文本排序](../../raw/model-api-reference/more-models/text-rerank-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)

