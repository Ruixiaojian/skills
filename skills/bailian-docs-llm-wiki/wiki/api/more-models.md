# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，覆盖法律、意图理解、机器翻译、深度研究、GUI自动化和OCR等能力。这些模型在通用大模型基础上进行了领域精调或架构优化，支持通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，适用于需要高精度、低延迟或特定模态处理的生产场景。

## 支持的模型/功能

当前支持以下专用模型：

- **通义法睿（`farui-plus`）**：法律行业大模型，支持法律咨询、文书生成、案情分析、合同审查等 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)  
- **意图理解模型（`tongyi-intent-detect-v3`）**：毫秒级意图识别与工具调用决策，支持 `INTENT_MODE` 输出格式 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)  
- **Qwen-MT（`qwen-mt-plus`）**：多语言机器翻译模型，支持术语干预、翻译记忆、领域提示等高级功能 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)  
- **Qwen-Deep-Research（`qwen-deep-research`）**：支持两阶段交互式深度研究（反问确认 + 网络检索 + 报告生成），仅限华北2（北京）地域 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)  
- **GUI-Plus（`gui-plus-2026-02-26`）**：桌面GUI自动化模型，支持图像输入+工具调用，执行鼠标键盘操作 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)  
- **Qwen-OCR（`qwen3.5-ocr`）**：多模态OCR模型，支持结构化文本提取与自定义Prompt指令 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)  

> **注意**：文档 3 和文档 6 均提及美国（弗吉尼亚）地域支持 `qwen-mt-plus` 和 `qwen3.5-ocr`，但文档 4 明确指出 `qwen-deep-research` **仅支持华北2（北京）地域**。跨地域可用性需以各模型独立文档为准，不建议默认假设所有模型全域可用。

## 关键参数

| 模型 | 上下文长度 | 最大输入 | 最大输出 | 输入成本（/百万[Token](../concepts/token.md)） | 输出成本（/百万[Token](../concepts/token.md)） | 免费额度 |
|------|------------|----------|----------|------------------------|------------------------|----------|
| `farui-plus` | 12k | 12k | 2k | 20元 | — | 无 |
| `tongyi-intent-detect-v3` | 8,192 | 8,192 | 1,024 | 0.4元 | 1元 | 100万[Token](../concepts/token.md)（开通后90天） |
| `qwen-mt-plus` | — | — | — | 未明确 | 未明确 | 未明确 |
| `qwen-deep-research` | — | — | — | 未明确 | 未明确 | 未明确 |
| `gui-plus-2026-02-26` | — | — | — | — | — | — |
| `qwen3.5-ocr` | — | — | — | — | — | — |

- 所有模型均需显式指定 `model` 参数（字符串，如 `"farui-plus"`）。
- 多模态模型（`gui-plus-2026-02-26`, `qwen3.5-ocr`）要求 `messages` 中 `content` 为数组，含 `image_url` 和 `text` 类型项。
- `qwen-mt-plus` 必须通过 `extra_body.translation_options` 传入 `source_lang`/`target_lang`；`qwen-deep-research` 支持 `output_format`（`model_detailed_report` 或 `model_summary_report`）；`qwen3.5-ocr` 支持 `min_pixels`/`max_pixels` 图像预处理参数。
- `tongyi-intent-detect-v3` 的行为由 `system` message 决定：`Response in INTENT_MODE.` 启用工具调用，`just reply with the chosen tag.` 启用纯意图分类。

## 使用方式

### 通用前提
- 获取并配置 API Key（推荐设为环境变量 `DASHSCOPE_API_KEY`）[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)  
- 安装对应 SDK：[DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk) 或 [OpenAI SDK](https://help.aliyun.com/zh/model-studio/install-sdk)  
- **强烈建议使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com`，以获得更高性能和稳定性 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)

### 调用示例（核心模式）
- **单轮对话（法睿）**：直接传入 `messages` 数组，`role` 为 `user`/`system`，`result_format='message'`  
- **多轮对话（法睿）**：将上一轮 `response.output.choices[0].message` 追加至 `messages` 后续调用  
- **[流式输出](../concepts/streaming-output.md)（所有支持模型）**：DashScope SDK 设置 `stream=True`，OpenAI SDK 设置 `stream=True` 并迭代 `completion`  
- **工具调用（意图模型）**：`system` message 中声明 `Response in INTENT_MODE.` 并嵌入工具 JSON Schema  
- **图像理解（OCR/GUI）**：`messages.content` 为对象数组，包含 `{"type": "image_url", "image_url": {"url": "..."} }` 和 `{"type": "text", "text": "..."}`  

> **注意**：文档 4 明确说明 `qwen-deep-research` **暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**，仅可通过 Python DashScope SDK 调用，与其他模型的多SDK支持存在差异。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，调用时必须使用该地域的 API Key 和 endpoint；其他模型（如 `qwen-mt-plus`, `qwen3.5-ocr`）在美东、新加坡等地域亦可用，但需匹配对应 `base_url` [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)  
- **限流策略**：所有模型受百炼平台统一限流控制，详情见 [限流文档](https://help.aliyun.com/zh/model-studio/rate-limit)  
- **线程安全**：DashScope Java SDK 中 `Generation` 等对象**非线程安全**，需复用实例并自行管理同步 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)  
- **输入格式**：`gui-plus-2026-02-26` 和 `qwen3.5-ocr` 要求 `messages` 中 `content` 为数组，且 `image_url` 对象需包含 `min_pixels`/`max_pixels`（OCR）或 `vl_high_resolution_images=True`（GUI）等特定字段  
- **响应解析**：`tongyi-intent-detect-v3` 在 `INTENT_MODE` 下返回 `<tags>...</tags>` 和 `<tool_call>...<tool_call>` 包裹的 JSON，需正则解析；`qwen-deep-research` 返回多阶段 `phase` 字段（`ResearchPlanning`, `WebResearch`, `answer`），需按阶段处理流式响应  
- **免费额度**：`tongyi-intent-detect-v3` 提供 100 万 Token 免费额度（开通后 90 天内），其余模型未在原始文档中声明免费额度

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)


