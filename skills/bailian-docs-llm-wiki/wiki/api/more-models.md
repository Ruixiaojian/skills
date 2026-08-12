# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖法律、意图理解、机器翻译、OCR、GUI自动化和深度研究等方向。这些模型在通用大模型基础上进行了领域精调或架构增强，具备更强的专业能力与任务适配性。所有模型均通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，支持流式/非[流式输出](../concepts/streaming-output.md)，并需配置业务空间专属域名以获得最佳性能。

## 支持的模型/功能

| 模型名称 | 用途 | 关键能力 | 文档引用 |
|----------|------|-----------|-----------|
| `farui-plus` | 法律行业大模型 | 法律问答、案情分析、文书生成、合同审查、RAG检索增强、法律Agent [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 意图理解 | 百毫秒级意图识别、[函数调用](../concepts/function-calling.md)解析（INTENT_MODE）、多意图分类与单[Token](../concepts/token.md)极简响应 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-mt-plus` | 机器翻译 | 多语言互译、术语干预、翻译记忆（TM）、领域提示 | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `qwen3.5-ocr` | 图像文字提取 | 高精度OCR、结构化信息抽取（如车票字段）、支持图文混合Prompt | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `gui-plus-2026-02-26` | GUI自动化 | 基于截图的桌面交互（鼠标/键盘操作）、多步任务编排、阻塞窗口处理 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |
| `qwen-deep-research` | 深度研究 | 两阶段工作流（反问确认 → 网络搜索 → 报告生成）、自动引用溯源、支持`model_detailed_report`/`model_summary_report`输出格式 | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |

> **注意**：文档 3 和文档 4 中对新加坡/美国地域的 base_url 描述存在重复（两次列出同一地域），且文档 5 未明确说明 GUI-Plus 是否支持除北京外的其他地域；实际调用时请以控制台中业务空间详情页显示的 WorkspaceId 和对应地域为准，避免硬编码错误地址。

## 关键参数

所有模型共用以下核心参数（部分模型有扩展）：

- **`model`**：必填，模型标识符（如 `"farui-plus"`、`"qwen3.5-ocr"`）。
- **`messages`**：必填，对话消息数组，每项含 `role`（`user`/`system`/`assistant`）和 `content`；OCR 和 GUI-Plus 支持 `content` 为图文混合列表（含 `image_url` 和 `text`）。
- **`result_format` / `response_format`**：推荐设为 `"message"`（DashScope）或使用 OpenAI 兼容的 `response_format={"type": "json_object"}`（若需结构化输出）。
- **`stream`**：布尔值，启用[流式输出](../concepts/streaming-output.md)（`True`/`true`），配合 `stream_options={"include_usage": true}` 获取实时 token 统计。
- **模型特有参数**：
  - `qwen-mt-plus`：通过 `extra_body={"translation_options": {...}}` 或直接传入 `translation_options` 字段指定 `source_lang`、`target_lang`、`terms`、`tm_list`。
  - `qwen-deep-research`：通过 `output_format` 控制报告粒度（`"model_detailed_report"` 或 `"model_summary_report"`）。
  - `gui-plus-2026-02-26`：需设置 `extra_body={"vl_high_resolution_images": true}` 以启用高分辨率图像处理。
  - `tongyi-intent-detect-v3`：依赖 `system` message 中的 `Response in INTENT_MODE.` 或 `just reply with the chosen tag.` 指令触发对应模式。

## 使用方式

1. **环境准备**  
   - 获取并配置 API Key 到环境变量 `DASHSCOPE_API_KEY`（[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）；
   - 安装 SDK：`pip install dashscope openai`（Python）或对应 Java/Node.js 版本；
   - **必须配置业务空间专属域名**：华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`（详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 和 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)）。

2. **调用示例（通用流程）**  
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # OpenAI 兼容
   )
   response = client.chat.completions.create(
       model="qwen3.5-ocr",
       messages=[{
           "role": "user",
           "content": [
               {"type": "image_url", "image_url": {"url": "https://..."}},
               {"type": "text", "text": "提取发票号码和金额"}
           ]
       }],
       stream=True
   )
   ```

3. **特殊流程说明**  
   - `qwen-deep-research` 必须分两步调用：先发送初始主题获取反问，再将反问+用户澄清作为上下文发起第二轮请求；
   - `tongyi-intent-detect-v3` 的响应需用正则解析 `<tags>`/<tool_call>/`<content>` 三段式结构（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）；
   - OCR 和 GUI-Plus 模型要求 `image_url` 指向可公开访问的 HTTPS 图片，且建议设置 `min_pixels`/`max_pixels` 控制图像分辨率。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他模型虽支持多地域，但业务空间专属域名需与 API Key 所属地域严格匹配。
- **输入限制**：各模型有最大上下文长度（如 `farui-plus` 为 12k tokens，`tongyi-intent-detect-v3` 为 8,192 tokens），超长输入将被截断，不报错。
- **输出格式兼容性**：`qwen-deep-research` 仅支持 DashScope Python SDK，**不支持 Java SDK 和 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**（见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)）。
- **流式响应解析**：DashScope 流式返回为 `GenerationResponse` 对象流，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)返回 `ChatCompletionChunk`，二者 `content` 字段位置不同（前者在 `response.output.choices[0].message.content`，后者在 `chunk.choices[0].delta.content`）。
- **成本与限流**：模型按输入/输出 token 计费（如 `farui-plus` 输入 20元/百万token），具体费率见各模型文档；全局限流策略参见 [限流](https://help.aliyun.com/zh/model-studio/rate-limit)。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)


