# [more](more.md) models

百炼平台提供一系列面向特定任务的专用模型，覆盖意图理解、法律推理、机器翻译、OCR文字提取、深度研究和GUI自动化等场景。这些模型在各自领域具备更强的专业能力与优化性能，开发者可根据业务需求选择合适的模型并集成到应用中。

## 支持的模型/功能

当前支持的专用模型包括：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持两种模式——同时输出意图与[函数调用](../concepts/function-calling.md)信息（需 `Response in INTENT_MODE.` 系统提示），或仅输出预定义意图标签（[原文标题](../../raw/model-api-reference/more-models/intent-detect-capability.md)）。
- **法律大模型**：`farui-plus`，专为法律场景优化，支持法律咨询、文书生成、案情分析、合同审查等功能（[原文标题](../../raw/model-api-reference/more-models/tongyi-farui-api.md)）。
- **机器翻译模型**：`qwen-mt-plus`，支持多语言互译、术语干预、翻译记忆及领域提示（[原文标题](../../raw/model-api-reference/more-models/qwen-mt-api.md)）。
- **OCR模型**：`qwen3.5-ocr`，支持图文混合输入，可结合自定义 Prompt 提取结构化文本（如车票信息），支持流式与非[流式输出](../concepts/streaming-output.md)。
- **深度研究模型**：`qwen-deep-research`，仅支持华北2（北京）地域，通过两阶段交互（反问确认 + 深入研究）完成网络检索增强型分析，**不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**（> **注意**：文档5明确说明“模型当前仅支持通过 Python DashScope SDK 调用，暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)”，而文档3和文档4均提供了 OpenAI 兼容示例，此处存在明确约束差异，开发者须严格遵循文档5要求）。
- **GUI自动化模型**：`gui-plus-2026-02-26`，接收截图与指令，输出 GUI 操作动作（如 `left_click`, `type`, `terminate`），需严格按 `<tools>` 和 `<tool_call>` 格式组织系统提示与响应。

## 关键参数

| 参数 | 说明 | 示例/约束 |
|------|------|-----------|
| `model` | 必选字符串，指定模型名称 | `tongyi-intent-detect-v3`, `farui-plus`, `qwen-mt-plus`, `qwen3.5-ocr`, `qwen-deep-research`, `gui-plus-2026-02-26` |
| `messages` | 必选数组，按对话顺序排列 | `role` 仅支持 `system`/`user`/`assistant`；`content` 可为纯文本或含 `image_url` 的数组（OCR/GUI-Plus） |
| `translation_options` | `qwen-mt-plus` 专用，含 `source_lang`, `target_lang`, `terms`, `tm_list` | `source_lang: "auto"` 或 `"Chinese"`；`terms` 用于术语强制对齐 |
| `extra_body` | [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)扩展字段 | OCR/GUI-Plus 中需传 `{"vl_high_resolution_images": true}`；MT 中传 `{"translation_options": {...}}` |
| `output_format` | `qwen-deep-research` 专用，控制报告详略 | `model_detailed_report`（默认，~6000 [Token](../concepts/token.md)）或 `model_summary_report`（~1500–2000 [Token](../concepts/token.md)） |

## 使用方式

- **域名迁移**：华北2（北京）和新加坡地域用户**强烈建议**迁移到业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性（[原文标题](../../raw/model-api-reference/more-models/intent-detect-capability.md)）。
- **SDK 配置**：
  - OpenAI 兼容：设置 `base_url` 为对应地域的兼容模式地址（如 `.../compatible-mode/v1`），并传入 `DASHSCOPE_API_KEY`。
  - DashScope SDK：Python 中需显式设置 `dashscope.base_http_api_url`；Java 中需配置 `Constants.baseHttpApiUrl`。
- **调用模式**：
  - 非流式：直接获取完整响应（适用于意图识别、法律文书生成等确定性任务）。
  - 流式：设置 `stream=True`（Python）或 `stream: true`（Node.js），适用于 OCR 结果逐步返回、GUI 操作分步执行、Deep-Research 多阶段响应等场景。
- **特殊输入格式**：
  - OCR/GUI-Plus：`messages[0].content` 必须为数组，包含 `image_url` 和 `text` 对象。
  - Intent Detect：系统提示必须包含 `Response in INTENT_MODE.` 或明确的意图字典。
  - GUI-Plus：系统提示必须包含 `<tools>` 定义与 `<tool_call>` 响应格式规则。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` **仅支持华北2（北京）地域**，且不支持 OpenAI 兼容接口（见上文 > **注意**）；`qwen-mt-plus` 和 `qwen3.5-ocr` 支持北京、新加坡、美国（弗吉尼亚）三地，但各地区 API Key 不互通。
- **[Token](../concepts/token.md) 成本与配额**：`tongyi-intent-detect-v3` 提供开通后90天内100万 Token 免费额度；`farui-plus` 输入成本为20元/百万 Token（文档2未列输出成本，需以控制台实时计费为准）；其他模型成本请参考控制台定价页。
- **图像处理约束**：OCR 模型对输入图像有像素阈值（`min_pixels`/`max_pixels`），默认值见示例代码，超限将自动缩放。
- **流式响应解析**：`qwen-deep-research` 的流式响应包含多个 `phase`（如 `ResearchPlanning`, `WebResearch`, `answer`），需根据 `output.message.phase` 和 `output.message.status` 判断当前阶段与进度；`gui-plus-2026-02-26` 的响应必须严格解析 `<tool_call>` 块内的 JSON 执行动作。
- **工具调用解析**：`tongyi-intent-detect-v3` 的 `INTENT_MODE` 响应需用正则提取 `<tags>`、<tool_call>、`<content>` 三段内容（[原文标题](../../raw/model-api-reference/more-models/intent-detect-capability.md)）。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


