# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接口，支持文本生成、多轮对话、[工具调用](../concepts/tool-use.md)等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过百炼平台鉴权访问，并遵循统一的计费与配额规则。

## 支持的模型与功能

当前 Qwen 系列支持以下主流接口协议：

- **OpenAI 兼容 Chat Completions**：适用于已有 OpenAI 客户端（如 `openai==1.0+`）的快速迁移，支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等模型，但不支持原生[工具调用](../concepts/tool-use.md)（需依赖 [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference.md) 的增强能力）。  
- **OpenAI兼容-Responses**：在 Chat Completions 基础上扩展了联网搜索、代码解释器、网页内容提取等内置工具，自动维护对话历史，适合需要轻量级智能体能力的场景。详见 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)。  
- **Anthropic兼容-Messages**：支持 `tool_use`、`thinking` 等结构化输出，适用于需显式控制推理链路的高级用例；注意其 `max_tokens` 语义与 OpenAI 接口不同（指输出 token 上限，不含输入）。  
- **DashScope 原生接口**：提供最完整的参数控制（如 `enable_search`、`incremental_output`）、细粒度流式响应及模型专属能力（如 Qwen-VL 多模态支持），是功能完备性的首选。该接口文档见 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)。

> **注意**：原始文档中提及的“[DashScope](https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope)”链接已更新为新域名 `dashscope.aliyuncs.com`，旧文档未同步；实际请求应使用新版 endpoint，参见最新 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中的示例配置。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-max`、`qwen-plus`；不同接口对取值范围有差异（DashScope 支持全部，OpenAI 接口仅支持部分别名） |
| `messages` | array | 是（Chat Completions / Anthropic） | 对话消息列表，格式为 `{"role": "user/system/assistant", "content": "..."}`；Anthropic 接口还支持 `tool_result` 角色 |
| `temperature` | number | 否 | 默认 `0.8`，控制输出随机性；DashScope 接口额外支持 `top_p`、`frequency_penalty` 等高级采样参数 |
| `stream` | boolean | 否 | 是否启用流式响应；OpenAI 和 DashScope 接口均支持，但 Anthropic 接口需显式设置 `stream: true` 并处理 `event: message_start` 等事件 |

## 使用方式

1. **认证**：所有请求需携带 `Authorization: Bearer <api_key>`，API Key 在百炼控制台「API 密钥管理」中获取。  
2. **Endpoint 示例**：
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/v1/chat/completions`  
   - DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`  
3. **SDK 调用**：推荐使用官方 SDK（如 `dashscope` Python 包或 `@aliyun/dashscope` Node.js 包），可自动处理重试、鉴权与错误解析。基础调用示例见 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)。

## 限制和注意事项

- 单次请求最大 `input_tokens + output_tokens` 不超过 32768（Qwen-Max）或 8192（Qwen-Turbo），超出将返回 `400 Bad Request`。  
- [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)默认禁用[工具调用](../concepts/tool-use.md)；如需搜索或代码执行，请改用 OpenAI兼容-Responses 或 DashScope 接口。  
- 所有接口均按实际 token 数计费，`system` 消息内容计入输入 token；DashScope 接口支持 `incremental_output: true` 以降低首 token 延迟，但需客户端适配分块解析逻辑。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


