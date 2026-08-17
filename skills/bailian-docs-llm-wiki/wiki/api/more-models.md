# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖法律、意图理解、机器翻译、深度研究、GUI自动化和OCR等能力。这些模型在通用大模型基础上进行了领域精调或架构优化，支持通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，适用于对专业性、响应速度或[多模态](../concepts/multi-modal.md)处理有明确要求的生产场景。

## 支持的模型/功能

| 模型名称 | 用途 | 关键特性 | 文档引用 |
|----------|------|-----------|-----------|
| `farui-plus` | 法律行业大模型 | 基于千问基座，融合法律精调、RAG、法律Agent及司法小模型；支持文书生成、案情分析、合同审查等 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 意图识别与工具调用 | 百毫秒级响应，支持 `INTENT_MODE` 输出结构化工具调用指令或纯意图标签；需严格按 System Prompt 格式配置 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-mt-plus` | 专业机器翻译 | 支持术语干预（`terms`）、翻译记忆（`tm_list`）和领域提示；覆盖中英等多语种 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `qwen-deep-research` | 深度研究分析 | 两阶段工作流（反问确认 → 深入研究），自动执行网络搜索、内容聚合与引用标注；**仅支持华北2（北京）地域及 Python DashScope SDK** | > **注意**：文档明确说明“暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)”，与其它模型的多 SDK 支持存在矛盾，开发者应以该限制为准。 |
| `gui-plus-2026-02-26` | GUI 自动化交互 | 接收截图输入，输出鼠标/键盘操作指令（如 `left_click`, `type`, `wait`）；需在 System Prompt 中声明 `<tools>` 和响应格式规范 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |
| `qwen3.5-ocr` | 多场景文字提取 | 支持图像输入（含 `min_pixels`/`max_pixels` 调优参数）与自定义 Prompt；可精准提取票据、证件等结构化文本 | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |

## 关键参数

- **地域与 endpoint**：所有模型均推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com`。华北2（北京）和新加坡地域已强制启用新域名以保障性能与稳定性，详见[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)与[Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)。
- **身份认证**：必须配置有效的 `DASHSCOPE_API_KEY`，建议通过环境变量（如 `os.getenv("DASHSCOPE_API_KEY")`）注入，避免硬编码泄露。
- **模型特有参数**：
  - `qwen-mt-plus`：通过 `extra_body={"translation_options": {...}}`（OpenAI）或 `translation_options={...}`（DashScope）传入 `source_lang`、`target_lang`、`terms`、`tm_list`。
  - `qwen-deep-research`：支持 `output_format` 参数，取值 `model_detailed_report`（默认，~6000 [Token](../concepts/token.md)）或 `model_summary_report`（~1500–2000 [Token](../concepts/token.md)）。
  - `qwen3.5-ocr` 与 `gui-plus-2026-02-26`：`messages` 中 `content` 为数组，需同时包含 `image_url` 和 `text` 类型元素；`image_url` 对象可选 `min_pixels`/`max_pixels` 控制图像预处理。
- **[流式输出](../concepts/streaming-output.md)**：`farui-plus`、`qwen-deep-research`、`qwen3.5-ocr` 均支持流式（`stream=True`），但协议细节不同：`farui-plus` 需设 `incremental_output=True`；`qwen-deep-research` 使用 `X-DashScope-SSE: enable` header；`qwen3.5-ocr` 的 OpenAI 接口需 `stream_options={"include_usage": True}`。

## 使用方式

1. **SDK 选择**：
   - 通用推荐：DashScope Python SDK（全模型支持）或 OpenAI SDK（除 `qwen-deep-research` 外均兼容）。
   - **关键限制**：`qwen-deep-research` 仅支持 DashScope Python SDK，不支持 Java SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) —— 此为硬性约束，不可绕过。

2. **基础调用流程**（以 Python 为例）：
   ```python
   import dashscope  # 或 from openai import OpenAI
   # 1. 配置地域 endpoint（必需）
   dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
   # 2. 构造 messages（role/content 必填，部分模型需 system prompt 特定格式）
   messages = [{"role": "user", "content": "你的请求"}]
   # 3. 调用 Generation.call() 或 client.chat.completions.create()
   response = dashscope.Generation.call(model="farui-plus", messages=messages, ...)
   ```

3. **特殊模式配置**：
   - 意图识别：System message 必须包含 `Response in INTENT_MODE.`（工具调用）或 `just reply with the chosen tag.`（纯意图）。
   - GUI 自动化：System message 必须完整声明 `<tools>` XML 块及 `<tool_call>...</tool_call>` 响应格式规则。
   - OCR：`content` 字段必须为列表，内含 `{"type": "image_url", ...}` 和 `{"type": "text", "text": "prompt"}`。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他地域调用将失败；其余模型在华北2、新加坡、美国（弗吉尼亚）三地均可用，但需匹配对应地域的 `base_url` 和 API Key。
- **SDK 限制**：`qwen-deep-research` 不支持 Java SDK 和 OpenAI 兼容接口，此限制在[Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)中明确声明，开发者务必遵守。
- **成本与限流**：各模型计费标准独立（如 `farui-plus` 输入 20元/百万 [Token](../concepts/token.md)），且受全局限流策略约束。具体配额与限流规则请参见[限流](https://help.aliyun.com/zh/model-studio/rate-limit)，该链接在[通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)中被直接引用。
- **安全实践**：API Key 必须通过环境变量配置，禁止明文写入代码或日志；`Generation` 等非线程安全对象在 Java SDK 中需手动管理生命周期。
- **响应解析**：`tongyi-intent-detect-v3` 的 `INTENT_MODE` 响应需用正则解析 `<tags>`/<tool_call>/`<content>` 三段式结构；`qwen-deep-research` 的流式响应需按 `phase`（如 `"answer"`、`"WebResearch"`）和 `status`（如 `"typing"`、`"streamingQueries"`）状态机处理。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)


