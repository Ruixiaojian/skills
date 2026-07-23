# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖法律、翻译、深度研究、OCR、GUI自动化和意图理解等能力。这些模型基于通义千问系列基座模型精调或增强，支持通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用。所有模型均需配置业务空间专属域名以获得最佳性能与稳定性。

## 支持的模型/功能

- **通义法睿（`farui-plus`）**：法律行业专用大模型，支持法律咨询、文书生成、案情分析、合同审查等，详见 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。
- **Qwen-MT（`qwen-mt-plus`）**：机器翻译模型，支持术语干预、翻译记忆、领域提示等高级功能，兼容 OpenAI 接口，详见 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)。
- **Qwen-Deep-Research（`qwen-deep-research`）**：支持两阶段交互式深度研究（反问确认 + 网络检索增强），**仅限华北2（北京）地域且仅支持 Python DashScope SDK**，不支持 Java SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，详见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **Qwen-OCR（`qwen3.5-ocr`）**：[多模态](../concepts/multi-modal.md) OCR 模型，支持图像输入与结构化文本提取（如车票信息），支持流式与非[流式输出](../concepts/streaming-output.md)，详见 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **GUI-Plus（`gui-plus-2026-02-26`）**：界面交互专用模型，可调用 `computer_use` 工具执行鼠标/键盘操作并解析截图，适用于自动化 GUI 测试与桌面任务，详见 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。
- **意图理解（`tongyi-intent-detect-v3`）**：毫秒级意图识别模型，支持两种模式：① 输出结构化工具调用（需 `INTENT_MODE` system [prompt](../guides/prompt.md)）；② 仅输出预定义意图标签（支持单 [Token](../concepts/token.md) 响应优化），详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。

> **注意**：文档 2 和文档 4 均重复列出新加坡/美国地域的 `base_url` 配置两次，属冗余描述，实际使用时按地域选择唯一正确地址即可；文档 5 中 GUI-Plus 的 `vl_high_resolution_images` 参数在文档 4（Qwen-OCR）中亦有相同用法，但未在文档 5 明确说明其作用，建议开发者参考 Qwen-OCR 文档中关于 `min_pixels`/`max_pixels` 的图像预处理逻辑进行适配。

## 关键参数

| 参数 | 类型 | 说明 | 必填 |
|------|------|------|------|
| `model` | string | 模型名称，如 `"farui-plus"`、`"qwen-mt-plus"` 等 | ✅ |
| `messages` | array | 对话消息列表，含 `role`（`user`/`system`/`assistant`）与 `content`；OCR/GUI-Plus 支持 `image_url` 类型内容 | ✅ |
| `result_format` / `response_format` | string | DashScope SDK 使用 `result_format='message'`；[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)默认为 `chat.completions` 格式 | ❌（默认） |
| `stream` | boolean | 启用[流式输出](../concepts/streaming-output.md)（需配合 `stream_options={"include_usage": true}` 获取 token 统计） | ❌（默认 false） |
| `extra_body` | object | OpenAI 兼容接口扩展字段：<br>• `qwen-mt-plus`: `{"translation_options": {...}}`<br>• `gui-plus-*`: `{"vl_high_resolution_images": true}`<br>• `tongyi-intent-detect-v3`: 无特殊字段，依赖 system [prompt](../guides/prompt.md) 控制行为 | ❌（按需） |
| `output_format` | string | 仅 `qwen-deep-research` 支持：`"model_detailed_report"`（默认）或 `"model_summary_report"` | ❌（默认） |

## 使用方式

1. **环境准备**  
   - 获取并配置 API Key 到环境变量 `DASHSCOPE_API_KEY`（[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）；
   - 安装对应 SDK：`pip install dashscope`（DashScope）或 `pip install openai`（OpenAI 兼容）；
   - **必须配置业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低。

2. **调用示例（通用流程）**  
   ```python
   # DashScope SDK（以 farui-plus 为例）
   import dashscope
   dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
   response = dashscope.Generation.call(
       model="farui-plus",
       messages=[{"role": "user", "content": "生成一份离婚协议书"}],
       result_format="message"
   )
   ```

   ```python
   # OpenAI 兼容接口（以 qwen-mt-plus 为例）
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
   )
   completion = client.chat.completions.create(
       model="qwen-mt-plus",
       messages=[{"role": "user", "content": "我看到这个视频后没有笑"}],
       extra_body={"translation_options": {"source_lang": "Chinese", "target_lang": "English"}}
   )
   ```

3. **特殊模型注意事项**  
   - `qwen-deep-research`：必须分两步调用（先反问确认，再传入 assistant 回复 + user 补充指令）；
   - `gui-plus-*`：system [prompt](../guides/prompt.md) 必须包含完整 `<tools>` 定义与 `Response format` 规则；
   - `tongyi-intent-detect-v3`：意图识别模式由 system prompt 决定——含 `INTENT_MODE` 则输出 `<tags>`/<tool_call> 块；否则仅输出纯标签字符串。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；其他模型（如 `qwen-mt-plus`、`qwen3.5-ocr`、`gui-plus-*`）在华北2、新加坡、美国（弗吉尼亚）三地均可用，但需使用对应地域的 `base_url` 和独立 API Key。
- **SDK 支持差异**：`qwen-deep-research` **不支持 Java SDK 与 OpenAI 兼容接口**（文档明确说明），仅支持 Python DashScope SDK；其余模型均支持两种调用方式。
- **输入格式约束**：OCR 与 GUI-Plus 模型要求 `messages[0].content` 为数组，内含 `image_url` 和 `text` 对象；普通文本模型（如 `farui-plus`、`tongyi-intent-detect-v3`）则接受字符串 `content`。
- **成本与限流**：各模型按输入/输出 token 计费（如 `farui-plus` 输入 20元/百万 token），具体见各模型文档表格；全局限流策略参见 [限流](https://help.aliyun.com/zh/model-studio/rate-limit)，未在原始文档中统一说明。
- **安全实践**：强烈建议将 `DASHSCOPE_API_KEY` 配置为环境变量，避免硬编码或日志泄露（[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)）。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)


