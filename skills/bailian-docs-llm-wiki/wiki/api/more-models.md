# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，覆盖法律、意图理解、机器翻译、深度研究、GUI自动化和OCR等能力。这些模型均基于通义千问基座，通过领域精调、RAG增强、多模态融合或工具链集成实现专业化输出。开发者可通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，需注意地域限制、域名迁移要求及参数差异。

## 支持的模型/功能

当前支持以下专用模型：

- **通义法睿（`farui-plus`）**：法律行业大模型，支持法律咨询、文书生成、案情分析、合同审查等功能，详见 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。
- **意图理解模型（`tongyi-intent-detect-v3`）**：毫秒级意图识别与[函数调用](../concepts/function-calling.md)决策，支持 `INTENT_MODE` 输出结构化工具调用指令，或仅返回标签化意图结果。
- **Qwen-MT（`qwen-mt-plus`）**：机器翻译模型，支持术语干预、翻译记忆（TM）、领域提示等高级功能，适用于技术文档、本地化等高精度场景。
- **Qwen-Deep-Research（`qwen-deep-research`）**：支持两阶段交互式深度研究（反问确认 + 网络搜索 + 报告生成），**仅限华北2（北京）地域且仅支持 Python DashScope SDK**，不支持 Java SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **GUI-Plus（`gui-plus-2026-02-26`）**：界面交互专用模型，接受截图输入并输出 GUI 操作指令（如 `left_click`, `type`, `wait`），需严格遵循 `<tools>` 和 `<tool_call>...<tool_call>` 响应格式。
- **Qwen-OCR（`qwen3.5-ocr`）**：多模态 OCR 模型，支持图像中文字提取与结构化信息抽取（如车票字段），支持 `min_pixels` / `max_pixels` 图像分辨率控制。

> **注意**：文档 3 中重复列出了北京、新加坡、美国地域的配置说明（两次“北京地域”、两次“新加坡地域”、两次“美国地域”），属冗余内容；实际使用时请按地域选择唯一对应的 `base_url`，避免混淆。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `model` | string | 是 | 模型标识符 | `"farui-plus"`, `"tongyi-intent-detect-v3"`, `"qwen-mt-plus"` |
| `messages` | array | 是 | 对话消息列表，含 `role`（`user`/`system`/`assistant`）和 `content` | `[{"role":"user","content":"起诉书生成"}]` |
| `result_format` / `response_format` | string | 否 | 输出格式，`"message"`（推荐）或 `"text"` | `"message"` |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming-output.md) | `True` |
| `translation_options` | object | 否 | Qwen-MT 专用，含 `source_lang`, `target_lang`, `terms`, `tm_list` | `{"source_lang":"Chinese","target_lang":"English"}` |
| `extra_body` | object | 否 | [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)扩展参数，如 `vl_high_resolution_images: true`（GUI-Plus）、`translation_options`（Qwen-MT） | `{"vl_high_resolution_images": true}` |
| `output_format` | string | 否 | Qwen-Deep-Research 专用，`"model_detailed_report"`（默认）或 `"model_summary_report"` | `"model_summary_report"` |

## 使用方式

### 通用前提
- 获取并配置 API Key：建议设为环境变量 `DASHSCOPE_API_KEY`，降低泄露风险 [获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
- 安装 SDK：Python 或 Java 版 DashScope SDK，或 OpenAI SDK（v1.0+）[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。
- **强制域名迁移**：华北2（北京）和新加坡地域必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名 `dashscope.aliyuncs.com` 已不推荐 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。

### 调用示例（核心模式）
- **单轮对话（法睿）**：直接传入 `messages`，指定 `model="farui-plus"`。
- **多轮对话（法睿）**：将上一轮 `response.output.choices[0].message` 追加至 `messages` 后续调用。
- **[流式输出](../concepts/streaming-output.md)（所有支持模型）**：设置 `stream=True`（Python）或 `streamCall()`（Java），逐块消费响应。
- **意图识别（INTENT_MODE）**：`system` 消息中必须包含 `Response in INTENT_MODE.` 及工具定义 JSON。
- **OCR 结构化提取**：`messages.content` 为 `[{ "type": "image_url", ... }, { "type": "text", "text": PROMPT }]`，PROMPT 明确指定字段与输出格式。
- **深度研究（两阶段）**：第一阶段仅传初始 `user` 消息获取反问；第二阶段将反问 `assistant` 消息与用户回答一并传入。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他模型在多地域可用，但 API Key 需匹配对应地域 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **SDK 限制**：`qwen-deep-research` **暂不支持 Java SDK 与 OpenAI 兼容接口**，仅 Python DashScope SDK 可用。
- **[Token](../concepts/token.md) 成本与限流**：各模型输入/输出 [Token](../concepts/token.md) 成本不同（如 `farui-plus` 输入 20元/百万 [Token](../concepts/token.md)），具体见各模型文档；全局限流策略参见 [限流](https://help.aliyun.com/zh/model-studio/rate-limit)。
- **图像处理参数**：Qwen-OCR 和 GUI-Plus 支持 `min_pixels` / `max_pixels` 控制图像缩放，单位为像素总数（宽×高），默认值需显式设置以避免失真。
- **响应解析**：意图识别返回含 `<tags>` / `<tool_call>` / `<content>` 的混合文本，需用正则解析；Qwen-Deep-Research 返回含 `phase` 字段的多阶段响应，需按 `phase` 区分处理逻辑。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)


