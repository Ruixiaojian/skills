# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖法律、意图理解、机器翻译、深度研究、OCR和GUI自动化等能力。这些模型在通用大模型基础上进行了领域精调或架构增强，支持通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，适用于需要高精度、低延迟或特定模态处理的生产场景。

## 支持的模型与功能

| 模型名称 | 用途 | 关键特性 | 文档引用 |
|----------|------|-----------|-----------|
| `farui-plus` | 法律行业问答与文书生成 | 基于千问基座，融合RAG、法律Agent及司法小模型；支持单轮/多轮对话、[流式输出](../concepts/streaming-output.md) | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 用户意图识别与工具路由 | 百毫秒级响应；支持 `INTENT_MODE` 输出结构化工具调用，或纯标签分类；可配置简写标签提升性能 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-mt-plus` | 多语言机器翻译 | 支持术语干预、翻译记忆（TM）、领域提示；自动语言检测（`source_lang: "auto"`） | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `qwen-deep-research` | 自动化深度研究报告生成 | 两阶段流程（反问确认 → 深入研究）；集成网络搜索与引用溯源；仅支持华北2（北京）地域 | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `qwen3.5-ocr` | 图像文字提取与结构化解析 | 支持图文混合输入（`image_url` + `text` [prompt](../guides/prompt.md)）；可指定 `min_pixels`/`max_pixels` 控制图像分辨率 | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `gui-plus-2026-02-26` | GUI界面自动化操作 | 接收截图输入，输出鼠标/键盘动作指令；需严格遵循 `<tools>` 和 `<tool_call>...<tool_call>` 响应格式 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |

> **注意**：文档 3 中重复列出了北京、新加坡、美国地域的 endpoint 配置（各出现两次），属冗余信息，实际使用请以首次出现的配置为准；文档 4 明确说明 `qwen-deep-research` **暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**，与文档 1、2、3、5、6 中普遍支持 OpenAI 接口的表述存在矛盾，开发者应以文档 4 的限制为准。

## 关键参数

所有模型均需通过 `model` 参数指定名称，并遵循以下通用参数规范：

- **`messages`**（必选）：按对话顺序排列的消息数组，每条消息含 `role`（`user`/`system`/`assistant`）和 `content`。OCR 与 GUI-Plus 模型支持 `content` 为图文混合数组（含 `image_url` 和 `text` 类型项）。
- **`result_format` / `response_format`**：DashScope SDK 使用 `result_format='message'`（默认），[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)无需显式设置。
- **`stream`**：设为 `True` 启用[流式输出](../concepts/streaming-output.md)（如 `farui-plus`、`qwen-deep-research`、`qwen3.5-ocr`）；GUI-Plus 和意图识别模型暂未提及流式支持。
- **模型专属参数**：
  - `qwen-mt-plus`：通过 `extra_body={"translation_options": {...}}` 或直接传参（如 `translation_options`）指定 `source_lang`、`target_lang`、`terms`、`tm_list`。
  - `qwen-deep-research`：支持 `output_format`（`model_detailed_report` 或 `model_summary_report`）控制报告长度。
  - `qwen3.5-ocr`：`image_url` 对象可包含 `min_pixels` 和 `max_pixels` 字段调节图像预处理。
  - `gui-plus-2026-02-26`：需在 `extra_body` 中设置 `{"vl_high_resolution_images": True}` 以启用高分辨率图像处理。

## 使用方式

### 域名与认证
- **推荐域名**：华北2（北京）和新加坡地域必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），详见[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)和[Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)中的迁移说明。
- **API Key**：必须通过环境变量 `DASHSCOPE_API_KEY` 配置，避免硬编码；不同地域需使用对应地域的 API Key（如 `qwen-deep-research` 仅支持华北2地域 Key）。

### SDK 调用示例（核心模式）
- **单轮对话**（`farui-plus`）：构造 `system` + `user` 消息，调用 `dashscope.Generation.call(model="farui-plus", messages=...)`。
- **意图识别**（`tongyi-intent-detect-v3`）：`system` 消息中必须包含 `Response in INTENT_MODE.`（工具调用）或 `just reply with the chosen tag.`（纯标签分类）。
- **OCR 结构化提取**（`qwen3.5-ocr`）：`messages[0].content` 为图像 URL 与文本 Prompt 的数组，Prompt 应明确指定输出 JSON 格式。
- **GUI 自动化**（`gui-plus-2026-02-26`）：`system` 消息需完整嵌入 `<tools>` 定义和响应规则，`user` 消息含截图与自然语言指令。

### HTTP 直接调用
- OpenAI 兼容接口：`POST {base_url}/chat/completions`，请求体含 `model`、`messages` 及模型专属字段（如 `translation_options`）。
- DashScope 原生接口：`POST {base_url}/api/v1/services/aigc/text-generation/generation`（如 `qwen-deep-research`），请求体需包裹在 `input` 对象内。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他模型在华北2、新加坡、美国（弗吉尼亚）地域均有部署，但 API Key 不互通。
- **SDK 支持差异**：
  - `qwen-deep-research` 仅支持 Python DashScope SDK，**不支持 Java SDK 和 OpenAI 兼容接口**（见[Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)）。
  - `farui-plus` Java SDK 示例中 `Constants.baseHttpApiUrl` 配置方式与 Python 不同，且强调对象非线程安全，需自行管理同步。
- **[流式输出](../concepts/streaming-output.md)兼容性**：`farui-plus`、`qwen-deep-research`、`qwen3.5-ocr` 明确支持流式；`tongyi-intent-detect-v3` 和 `gui-plus-2026-02-26` 文档未说明流式能力，建议默认按非流式调用。
- **成本与限流**：`farui-plus` 输入/输出成本分别为 20 元/百万 [Token](../concepts/token.md)；`tongyi-intent-detect-v3` 提供 100 万 [Token](../concepts/token.md) 免费额度（90 天有效期）。所有模型均受平台[限流策略](https://help.aliyun.com/zh/model-studio/rate-limit)约束。
- **输入约束**：OCR 模型对图像尺寸有 `min_pixels`/`max_pixels` 限制；GUI-Plus 模型要求 `system` 消息严格遵循工具定义与响应格式，否则将导致解析失败。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


