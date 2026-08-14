# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，覆盖法律、翻译、意图理解、深度研究、OCR图文识别及GUI自动化等能力。这些模型均基于通义千问基座，通过领域精调、RAG增强、多阶段推理等技术优化，在特定任务上具备更高精度与效率。开发者可通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，需注意地域、域名、参数格式及模型专属约束。

## 支持的模型/功能

- **通义法睿（`farui-plus`）**：法律行业专用模型，支持法律咨询、案情分析、文书生成、合同审查等，上下文长度 12k [Token](../concepts/token.md) [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。  
- **Qwen-MT（`qwen-mt-plus`）**：机器翻译模型，支持术语干预、翻译记忆、领域提示等高级功能，适用于技术文档、本地化等高精度翻译场景 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)。  
- **意图理解（`tongyi-intent-detect-v3`）**：毫秒级意图识别模型，支持双模式输出——带[函数调用](../concepts/function-calling.md)的结构化意图（`INTENT_MODE`）或纯标签分类，免费额度 100 万 [Token](../concepts/token.md)/90 天 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。  
- **Qwen-Deep-Research（`qwen-deep-research`）**：两阶段深度研究模型，先反问澄清需求，再联网检索并生成结构化报告，仅支持华北2（北京）地域及 Python SDK [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。  
- **Qwen-OCR（`qwen3.5-ocr`）**：多模态图文识别模型，支持图像输入（含 `min_pixels`/`max_pixels` 自适应缩放）、Prompt 引导的结构化信息抽取（如车票字段），兼容 OpenAI 和 DashScope 接口 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。  
- **GUI-Plus（`gui-plus-2026-02-26`）**：界面交互专用模型，接收截图+指令，输出 GUI 操作动作（如 `left_click`, `type`, `terminate`），需严格遵循 `<tools>` + `<tool_call>` XML 格式响应 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

> **注意**：文档 2 中重复列出了北京、新加坡、美国地域的配置说明（同一段落出现两次），属冗余内容；文档 4 明确声明 Qwen-Deep-Research “暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)”，而其他模型（如法睿、Qwen-MT）均支持多 SDK，此为关键差异点，非矛盾。

## 关键参数

| 参数 | 说明 | 示例值 | 所属模型 |
|------|------|--------|----------|
| `model` | 模型标识符，必填 | `"farui-plus"`, `"qwen-mt-plus"` | 全部 |
| `messages` | 对话历史数组，含 `role`（`user`/`system`/`assistant`）和 `content` | `[{"role":"user","content":"生成起诉书"}]` | 法睿、意图、Qwen-MT、OCR、GUI-Plus |
| `translation_options` | Qwen-MT 专用，含 `source_lang`, `target_lang`, `terms`, `tm_list` | `{"source_lang":"Chinese","target_lang":"English"}` | Qwen-MT |
| `output_format` | Qwen-Deep-Research 专用，控制报告详略 | `"model_detailed_report"`（默认）或 `"model_summary_report"` | Qwen-Deep-Research |
| `extra_body` | [OpenAI 兼容接口](../concepts/openai-compatible-api.md)扩展字段 | `{"vl_high_resolution_images": true}`（OCR/GUI-Plus）、`{"translation_options": {...}}`（Qwen-MT） | Qwen-MT、OCR、GUI-Plus |
| `stream` / `stream_options` | 控制[流式输出](../concepts/streaming-output.md)，OCR 和法睿支持 `stream=True`，Qwen-MT 需显式传 `stream_options={"include_usage": true}` | `True`, `{"include_usage": true}` | 法睿、Qwen-MT、OCR |

## 使用方式

1. **环境准备**：  
   - 获取并配置 `DASHSCOPE_API_KEY` 到环境变量（推荐）或代码中；  
   - 安装对应 SDK：`pip install dashscope openai`（Python），或 Java SDK（法睿、意图支持）；  
   - **必须使用业务空间专属域名**：华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，详见各文档强调项。

2. **调用示例**：  
   - **单轮对话（法睿）**：`Generation.call(model="farui-plus", messages=[...])`；  
   - **翻译（Qwen-MT）**：OpenAI SDK 中 `client.chat.completions.create(model="qwen-mt-plus", extra_body={"translation_options": {...}})`；  
   - **意图识别（双模式）**：系统提示词需明确包含 `Response in INTENT_MODE.`（结构化）或 `just reply with the chosen tag.`（纯标签）；  
   - **深度研究（Qwen-Deep-Research）**：分两步调用，第一步获取反问内容，第二步将用户回答拼入 `messages` 继续请求；  
   - **OCR（Qwen-OCR）**：`content` 为图像 URL + 文本 Prompt 的数组，支持 `image_url` 字段内嵌 `min_pixels`/`max_pixels`；  
   - **GUI 自动化（GUI-Plus）**：`system` 消息必须完整定义 `<tools>` 和 `<tool_call>` 响应格式，`user` 消息含截图 URL 和文本指令。

3. **流式处理**：  
   - 法睿、Qwen-Deep-Research、Qwen-OCR、Qwen-MT 均支持[流式输出](../concepts/streaming-output.md)，需设置 `stream=True`（Python）或 `stream: true`（Node.js），并按 chunk 解析 `content` 或 `delta.content`。

## 限制和注意事项

- **地域限制**：Qwen-Deep-Research 仅支持华北2（北京）地域；其他模型在华北2、新加坡、美国（弗吉尼亚）三地可用，但 API Key 和 `base_url` 必须匹配地域。  
- **SDK 限制**：Qwen-Deep-Research 仅支持 Python DashScope SDK；法睿、意图识别支持 Python/Java SDK；Qwen-MT、OCR、GUI-Plus 主推 OpenAI 兼容接口（亦支持 DashScope）。  
- **输入格式**：OCR 和 GUI-Plus 要求 `messages[0].content` 为数组（含 `image_url` 和 `text` 对象）；法睿、意图、Qwen-MT 的 `content` 为字符串。  
- **成本与限流**：法睿输入/输出成本分别为 20 元/百万 [Token](../concepts/token.md)；意图识别有免费额度；所有模型均受 [限流策略](https://help.aliyun.com/zh/model-studio/rate-limit) 约束，需关注 `X-RateLimit-Remaining` 响应头。  
- **安全实践**：API Key 务必配置至环境变量，避免硬编码；Java SDK 中 `Generation` 对象非线程安全，需复用或加锁 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。  
- **响应解析**：意图识别返回含 `<tags>`/`<tool_call>`/`<content>` 的特殊格式，需正则提取；Qwen-Deep-Research 响应含 `phase` 字段（如 `answer`, `WebResearch`），需按阶段处理。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


