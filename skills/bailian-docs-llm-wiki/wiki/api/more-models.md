# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，覆盖法律、意图理解、机器翻译、深度研究、OCR图文识别和GUI自动化等方向。这些模型在通用大模型基础上进行了领域精调或架构增强，支持通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，适用于高精度、低延迟、[多模态](../concepts/multi-modal.md)等特定业务需求。

## 支持的模型与功能

| 模型名称 | 用途 | 关键能力 | 文档引用 |
|----------|------|-----------|-----------|
| `farui-plus` | 法律行业大模型 | 法律问答、案情分析、文书生成、合同审查、RAG检索增强 | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 意图理解 | 百毫秒级意图识别、工具调用解析（INTENT_MODE）、单标签分类 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-mt-plus` | 机器翻译 | 多语言互译、术语干预、翻译记忆（TM）、领域提示 | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `qwen-deep-research` | 深度研究 | 两阶段交互式研究（反问确认 + 网络搜索 + 报告生成）、带引用溯源的结构化输出 | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `qwen3.5-ocr` | 图文识别 | 多格式图像文字提取、结构化信息抽取（如车票字段）、支持 Prompt 控制输出格式 | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `gui-plus-2026-02-26` | GUI 自动化 | 基于截图的桌面操作（鼠标/键盘/等待/终止）、[函数调用](../concepts/function-calling.md)驱动界面交互 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |

> **注意**：文档 4 明确指出 `qwen-deep-research` “仅支持华北2（北京）地域”且“暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)”，而其他模型（如 `farui-plus`、`qwen-mt-plus`）均明确支持 Python/Java SDK 及 OpenAI 兼容模式。该限制需在集成时严格遵守，否则将导致调用失败。

## 关键参数

所有模型均遵循统一参数范式，但部分模型支持扩展参数：

- **通用必选参数**：`model`（字符串，如 `"farui-plus"`）、`messages`（消息数组，含 `role` 和 `content`）
- **扩展参数（按模型）**：
  - `qwen-mt-plus`：通过 `extra_body.translation_options` 传入 `source_lang`、`target_lang`、`terms`（术语表）、`tm_list`（翻译记忆）；
  - `qwen3.5-ocr`：`messages.content` 支持 `image_url` + `text` 混合输入，可指定 `min_pixels` / `max_pixels` 控制图像缩放；
  - `gui-plus-2026-02-26`：需在 `extra_body` 中设置 `vl_high_resolution_images: true` 以启用高分辨率截图处理；
  - `qwen-deep-research`：支持 `output_format` 参数，取值为 `model_detailed_report`（默认，约6000 [Token](../concepts/token.md)）或 `model_summary_report`（约1500–2000 [Token](../concepts/token.md)）；
  - `tongyi-intent-detect-v3`：依赖 `system` 消息中显式声明 `Response in INTENT_MODE.` 或意图字典格式，否则无法触发对应模式。

## 使用方式

### 域名与认证
- **强制使用业务空间专属域名**：华北2（北京）和新加坡地域必须使用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，旧域名 `dashscope.aliyuncs.com` 已不推荐（见[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)和[Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)中的迁移说明）。
- **API Key 配置**：必须通过环境变量 `DASHSCOPE_API_KEY` 设置，禁止硬编码；Java SDK 要求复用 `Generation` 对象并注意线程安全（见[通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)）。

### 调用示例共性
- 所有模型均支持[流式输出](../concepts/streaming-output.md)（`stream=True` / `X-DashScope-SSE: enable`），但 `qwen-deep-research` 必须分两步调用（先反问确认，再深入研究）；
- `tongyi-intent-detect-v3` 的 `INTENT_MODE` 响应需用正则解析 `<tags>` / `<tool_call>` / `<content>` 三段式结构（见[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）；
- `qwen3.5-ocr` 和 `gui-plus-2026-02-26` 均要求 `messages.content` 为数组，包含 `image_url` 和 `text` 对象，不可仅传纯文本。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅限华北2（北京）地域，其他地域调用将失败；`qwen-mt-plus` 和 `qwen3.5-ocr` 支持北京、新加坡、美国（弗吉尼亚）三地，但各地区 API Key 不互通。
- **SDK 限制**：`qwen-deep-research` 当前仅支持 Python DashScope SDK，不支持 Java SDK 和 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（见[Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)）。
- **成本与配额**：`tongyi-intent-detect-v3` 提供 100 万 [Token](../concepts/token.md) 免费额度（开通后 90 天内有效），其余模型按实际 [Token](../concepts/token.md) 数计费；`farui-plus` 输入/输出成本分别为 20 元/百万 [Token](../concepts/token.md)（见[通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)）。
- **流式响应解析**：`qwen-deep-research` 的流式响应包含 `phase` 字段（如 `"ResearchPlanning"`、`"WebResearch"`、`"answer"`），需据此区分阶段并处理 `extra.deep_research.references` 等结构化数据。
- **图像处理约束**：`qwen3.5-ocr` 和 `gui-plus-2026-02-26` 对输入图像有像素阈值（`min_pixels`/`max_pixels`），超出范围将自动缩放，需在请求中显式配置以避免失真。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)




