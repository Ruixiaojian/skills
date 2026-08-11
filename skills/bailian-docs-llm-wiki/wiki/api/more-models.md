# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖法律、意图理解、机器翻译、OCR、GUI自动化和深度研究等能力。这些模型均基于通义千问基座，通过领域精调、RAG增强、[多模态](../concepts/multi-modal.md)对齐或工具链集成实现专业化输出，开发者可通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用。

## 支持的模型/功能

| 模型名称 | 用途 | 输入类型 | 关键能力 | 文档引用 |
|----------|------|----------|----------|----------|
| `farui-plus` | 法律行业大模型 | 文本 | 法律问答、案情分析、文书生成、合同审查、司法知识检索 | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 意图识别与[函数调用](../concepts/function-calling.md)解析 | 文本 | 百毫秒级意图分类、结构化工具调用参数提取（支持 `INTENT_MODE`）、单 [Token](../concepts/token.md) 标签输出优化 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-mt-plus` | 专业机器翻译 | 文本 | 多语言互译、术语干预、翻译记忆（TM）、领域提示（如技术文档、金融） | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `qwen3.5-ocr` | [多模态](../concepts/multi-modal.md)文字提取 | 图像+文本 | 高精度 OCR、结构化信息抽取（如车票、发票）、支持自定义 Prompt 和图像分辨率控制 | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `gui-plus-2026-02-26` | GUI 自动化交互 | 图像+文本 | 基于截图的桌面操作（鼠标/键盘模拟）、应用启动、界面状态感知与反馈闭环 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |
| `qwen-deep-research` | 深度研究代理 | 文本（两阶段） | 主动反问澄清、网络搜索、多源信息整合、带引用的结构化研究报告生成（支持 `model_detailed_report` / `model_summary_report`） | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |

> **注意**：文档 3 和文档 4 中均重复列出“新加坡地域”和“美国（弗吉尼亚）地域”的配置说明，但文档 5 仅明确支持华北2（北京）地域；文档 6 明确声明 `qwen-deep-research` **仅支持华北2（北京）地域**且**不支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)**，与文档 2、3、4 的通用多地域描述存在矛盾，应以文档 6 的限制为准。

## 关键参数

- **`model`**：必填字符串，指定模型标识符（如 `"farui-plus"`、`"qwen3.5-ocr"`），不同模型不可混用。
- **`messages`**：必填数组，按对话顺序组织消息对象。需严格遵循角色规范：
  - `role: "user"`：用户输入（文本或含 `image_url` 的[多模态](../concepts/multi-modal.md)内容）；
  - `role: "system"`：用于注入模型行为约束（如 `Response in INTENT_MODE.` 或工具定义）；
  - `role: "assistant"`：仅在 `qwen-deep-research` 第二步调用中作为历史回复传入。
- **`result_format` / `output_format`**：
  - DashScope 接口使用 `result_format="message"`（默认）；
  - `qwen-deep-research` 使用 `output_format="model_summary_report"` 等可选值控制报告粒度。
- **`extra_body`（OpenAI 兼容）**：用于传递模型特有参数，例如：
  - `qwen-mt-plus`：`{"translation_options": {"source_lang": "Chinese", "target_lang": "English", "terms": [...]}}`；
  - `gui-plus-*`：`{"vl_high_resolution_images": true}` 启用高分辨率图像处理。
- **`stream`**：布尔值，启用[流式输出](../concepts/streaming-output.md)（`True`/`True`），配合 `stream_options={"include_usage": true}` 获取实时 token 统计。

## 使用方式

1. **环境准备**：
   - 获取并配置 `DASHSCOPE_API_KEY` 到环境变量（推荐）或代码内显式传入；
   - 安装对应 SDK：`pip install dashscope openai`（Python）或 `npm install openai`（Node.js）；
   - 设置业务空间专属域名：`base_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"`（北京）或 `/api/v1`（DashScope 原生）。

2. **调用示例（核心模式）**：
   - **单轮文本生成**（如 `farui-plus`）：直接传入 `messages` 调用 `Generation.call()` 或 `client.chat.completions.create()`；
   - **多轮对话**：将上一轮 `response.output.choices[0].message` 追加至 `messages` 数组后再次调用；
   - **流式响应**：设置 `stream=True`，迭代处理 `response` 流（DashScope）或 `chunk`（OpenAI）；
   - **多模态输入**（如 `qwen3.5-ocr`, `gui-plus-*`）：`messages[0].content` 为对象数组，包含 `{"type": "image_url", "image_url": {"url": "..."}}` 和 `{"type": "text", "text": "..."}`；
   - **两阶段流程**（`qwen-deep-research`）：先流式获取反问内容，再将其作为 `assistant` 消息与用户新输入组合发起第二步调用。

3. **SDK 差异注意事项**：
   - `qwen-deep-research` 仅支持 Python DashScope SDK，**不支持 Java SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)**（见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)）；
   - DashScope Java SDK 中 `Generation` 对象非线程安全，需复用并管理同步（见 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)）。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；其他模型虽文档提及多地域，但实际可用性需以控制台开通情况为准。
- **限流策略**：所有模型受百炼平台统一限流控制，详情参见 [限流](https://help.aliyun.com/zh/model-studio/rate-limit)（见 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)）。
- **成本与配额**：`tongyi-intent-detect-v3` 提供 90 天内 100 万 [Token](../concepts/token.md) 免费额度；其余模型按输入/输出 [Token](../concepts/token.md) 数计费（如 `farui-plus` 输入 20 元/百万 Token）。
- **API Key 隔离**：北京、新加坡、弗吉尼亚地域的 API Key **不互通**，跨地域调用需分别申请并配置（见 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) 和 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)）。
- **图像处理约束**：`qwen3.5-ocr` 和 `gui-plus-*` 支持 `min_pixels` / `max_pixels` 参数控制图像缩放，避免因分辨率异常导致解析失败。
- **响应解析**：`tongyi-intent-detect-v3` 在 `INTENT_MODE` 下返回 `<tags>` / `<tool_call>` / `<content>` 三段式结构，需自行正则解析（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)


