# qwen api reference

Qwen 系列大模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过阿里云认证（AccessKey 或 Bearer [Token](../concepts/token.md)）调用。

## 支持的模型与功能

当前支持的 Qwen 模型包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 及 `qwen-vl`（多模态），具体能力因模型而异：  
- `qwen-max` 适用于复杂推理与长上下文任务；  
- `qwen-plus` 在成本与性能间取得平衡，适合通用场景；  
- `qwen-turbo` 面向低延迟、高吞吐场景；  
- `qwen-vl` 支持图像理解与图文生成（需使用 DashScope 接口）。  
详细模型能力与适用场景见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

## 关键参数

通用关键参数（以 DashScope 为例）：
- `model`: 必填，如 `"qwen-max"`；  
- `input.messages`: 对话消息数组，格式为 `[{ "role": "user", "content": "..." }]`；  
- `parameters.temperature`: 控制输出随机性（0.0–1.0，默认 0.8）；  
- `parameters.max_tokens`: 最大生成 token 数（默认 2048，上限依模型而定）；  
- `parameters.tools`: 启用工具调用时声明可用工具列表（仅 DashScope 和 Anthropic Messages 支持）。  
完整参数说明请参考 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

## 使用方式

推荐按以下优先级选择接入方式：  
1. **已有 OpenAI 生态**：直接复用 `openai` 官方 SDK，替换 base URL 为百炼 OpenAI 兼容端点（`https://dashscope.aliyuncs.com/v1`），详见 [OpenAI 兼容 Chat Completions](../../raw/model-api-reference/qwen-api-reference.md)；  
2. **需自动工具调用与联网能力**：选用 OpenAI 兼容-Responses 接口，其内置搜索、代码解释器等插件，无需手动维护 history；  
3. **追求最大灵活性与最新特性**：使用原生 DashScope 接口，支持流式响应、自定义 stop tokens、多模态输入等高级能力。

## 限制和注意事项

- 所有接口均受阿里云配额系统约束，包括 QPS、TPM（[Token](../concepts/token.md) Per Minute）及单次请求最大 token 数，具体限额请在控制台查看；  
- [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)不支持 `response_format`（JSON Schema）等部分 OpenAI v1.0+ 新增字段；  
- Anthropic Messages 接口的 `system` 字段行为与 Anthropic 官方略有差异：百炼中 `system` 内容会被合并至首条 user message 的 `content` 中（而非独立角色），此行为已在 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中明确说明；  
> **注意**：DashScope 接口的 `stream_options.include_usage` 参数在 v1.12+ SDK 中才生效，旧版 SDK 可能忽略该配置，请确保使用最新 `dashscope` Python 包（≥1.25.0）。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


