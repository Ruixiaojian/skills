# [more](more.md) models

百炼平台提供一系列面向特定任务的专用模型，覆盖法律、意图理解、深度研究、OCR、机器翻译和GUI自动化等场景。这些模型在通用大模型基础上进行了领域精调或架构优化，具备更强的专业能力与推理效率。开发者可通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，需注意地域、域名及参数格式差异。

## 支持的模型/功能

| 模型名称 | 用途 | 关键特性 | 文档来源 |
|----------|------|-----------|-----------|
| `farui-plus` | 法律行业问答与文书生成 | 基于千问基座，融合RAG、法律Agent、司法小模型；支持单轮/多轮对话、[流式输出](../concepts/streaming-output.md) | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 用户意图识别与[工具调用](../concepts/tool-use.md) | 百毫秒级响应；支持 `INTENT_MODE`（结构化[工具调用](../concepts/tool-use.md)）与纯标签分类两种模式 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-deep-research` | 多阶段深度研究 | 两阶段流程（反问确认 → 深入研究），自动执行网络搜索、引用溯源；仅支持华北2（北京）地域及 Python SDK | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `qwen3.5-ocr` | 图像文字提取与结构化解析 | 支持图文混合输入（`image_url` + `text` [prompt](../guides/prompt.md)），可定制字段提取逻辑 | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `qwen-mt-plus` | 领域适配机器翻译 | 支持术语干预（`terms`）、翻译记忆（`tm_list`）、领域提示（`domain`）；[OpenAI 兼容接口](../concepts/openai-compatible-api.md)需通过 `extra_body` 传参 | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `gui-plus-2026-02-26` | GUI界面自动化交互 | 接收截图输入，输出鼠标/键盘操作指令（如 `left_click`, `type`, `wait`）；需严格遵循 `<tools>` 和 `<tool_call>` 标签格式 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |

> **注意**：文档 5 中重复列出了“新加坡地域”和“美国（弗吉尼亚）地域”的配置说明两次，属冗余内容，实际使用时按地域选择唯一对应配置即可。

## 关键参数

- **`model`**（必选）：字符串，指定模型名称（如 `"farui-plus"`、`"qwen3.5-ocr"`），不区分大小写但需与文档一致。
- **`messages`**（必选）：消息数组，每项含 `role`（`user`/`system`/`assistant`）和 `content`。OCR 与 GUI-Plus 模型支持 `content` 为图文混合数组（含 `image_url` 和 `text` 子项）。
- **`result_format` / `response_format`**：DashScope SDK 使用 `result_format='message'`；[OpenAI 兼容接口](../concepts/openai-compatible-api.md)默认返回 `message` 格式，无需显式设置。
- **`stream`**：布尔值，启用[流式输出](../concepts/streaming-output.md)（如 `qwen-deep-research`、`qwen3.5-ocr`）。DashScope 需配合 `incremental_output=True`；OpenAI 需设 `stream_options={"include_usage": True}` 获取 token 统计。
- **领域/任务专用参数**：
  - 意图识别：`system` 消息中必须包含 `Response in INTENT_MODE.` 或明确的 tag 列表。
  - OCR：`image_url` 对象可带 `min_pixels`/`max_pixels` 控制图像缩放。
  - 翻译：通过 `extra_body={"translation_options": {...}}`（OpenAI）或 `translation_options={...}`（Node.js）传递 `source_lang`、`target_lang`、`terms`、`tm_list`。
  - GUI-Plus：必须启用 `vl_high_resolution_images: true`（OpenAI）或 `vl_high_resolution_images=True`（DashScope）以保障截图精度。

## 使用方式

1. **环境准备**  
   - 获取并配置 API Key 到环境变量 `DASHSCOPE_API_KEY`（[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。
   - 安装 SDK：`pip install dashscope openai`（Python）或对应 Node.js 包。
   - **强制使用业务空间专属域名**：华北2（北京）地域为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`（详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 和 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)）。

2. **调用示例（通用流程）**  
   ```python
   # DashScope SDK（推荐用于 farui-plus, qwen-deep-research）
   import dashscope
   dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
   response = dashscope.Generation.call(
       model="farui-plus",
       messages=[{"role": "user", "content": "生成起诉书"}],
       result_format="message"
   )

   # OpenAI 兼容接口（推荐用于 qwen3.5-ocr, qwen-mt-plus, gui-plus）
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
   )
   completion = client.chat.completions.create(
       model="qwen3.5-ocr",
       messages=[{"role": "user", "content": [{"type": "image_url", "image_url": {"url": "..."}}, {"type": "text", "text": "提取发票号码"}]}]
   )
   ```

3. **特殊流程处理**  
   - `qwen-deep-research`：必须分两步调用——先发送初始请求获取反问，再将用户回答与反问一并提交进行深入研究（见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)）。
   - `tongyi-intent-detect-v3`：`system` 消息需严格按模板构造，含工具定义或意图字典，并声明 `Response in INTENT_MODE.` 或 `just reply with the chosen tag.`。
   - `gui-plus-*`：`system` 消息必须完整嵌入 `<tools>` XML 块及 `<tool_call>` 标签规则，输出必须为 `Action: ...` + `<tool_call>{...}<tool_call>` 格式。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；其他模型在华北2、新加坡、美国（弗吉尼亚）均可用，但 API Key 和 endpoint 必须匹配（见 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)）。
- **SDK 限制**：`qwen-deep-research` 当前**仅支持 Python DashScope SDK**，Java SDK 与 OpenAI 兼容接口不可用（见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)）。
- **限流与成本**：所有模型均受百炼平台统一限流策略约束（参见 [限流](https://help.aliyun.com/zh/model-studio/rate-limit)）；`farui-plus` 输入/输出成本分别为 20 元/百万 [Token](../concepts/token.md)（见 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)）。
- **安全实践**：API Key **严禁硬编码**，必须通过环境变量注入；DashScope Java SDK 中 `Generation` 对象非线程安全，需复用并自行管理同步（见 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)）。
- **响应解析**：意图识别模型返回含 `<tags>`、`<tool_call>`、`<content>` 的特殊格式，需用正则+JSON 解析（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）；GUI-Plus 输出必须严格校验 `<tool_call>` 标签完整性，否则会导致自动化失败。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


