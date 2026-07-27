# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖法律、意图理解、机器翻译、深度研究、OCR 和 GUI 自动化等能力。这些模型均基于通义千问基座，通过领域精调、RAG、Agent 或多模态技术增强，支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与 DashScope SDK 调用。开发者需根据模型特性选择合适参数、输入格式及地域 endpoint。

## 支持的模型/功能

| 模型名称 | 用途 | 输入类型 | 关键能力 | 文档引用 |
|----------|------|----------|----------|----------|
| `farui-plus` | 法律行业大模型 | 文本（单/多轮对话） | 法律问答、文书生成、案情分析、合同审查、RAG 增强检索 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 意图识别与工具调用 | 文本（带结构化 System Prompt） | 百毫秒级意图分类、[函数调用](../concepts/function-calling.md)解析（INTENT_MODE）、支持标签映射优化响应速度 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-mt-plus` | 专业机器翻译 | 文本（含 source_lang/target_lang） | 支持术语干预、翻译记忆（TM）、领域提示，适用于技术文档等高精度场景 | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `qwen-deep-research` | 深度研究分析 | 文本（两阶段交互式输入） | 自动规划研究路径、联网搜索、引用溯源、生成详尽或摘要式报告；**仅支持华北2（北京）地域及 Python SDK** | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `qwen3.5-ocr` | 多模态文字提取 | 图文混合（image_url + text [prompt](../guides/prompt.md)） | 支持高分辨率图像处理、自定义 OCR 提取规则、[流式输出](../concepts/streaming-output.md)结构化 JSON | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `gui-plus-2026-02-26` | GUI 自动化操作 | 图文混合（截图 + 指令） | 通过工具调用模拟鼠标键盘操作，支持 wait、click、type 等动作链，分辨率固定为 1000×1000 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |

> **注意**：文档 4 明确指出 `qwen-deep-research` “仅支持通过 Python DashScope SDK 调用，暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)”，而文档 1 中 `farui-plus` 的 Java SDK 示例代码存在截断（末尾为 `System.out.println(JsonUtil`），且未说明是否完全支持该模型。实际开发中应以文档 4 的限制为准，避免在 Java 环境中尝试调用 `qwen-deep-research`。

## 关键参数

- **`model`**：必填字符串，值为上述任一模型名称（如 `"farui-plus"`、`"qwen3.5-ocr"`）。
- **`messages`**：必填数组，按角色（`system`/`user`/`assistant`）和内容组织。OCR 与 GUI 模型支持 `image_url` 类型 content（需配合 `min_pixels`/`max_pixels` 控制图像尺寸）。
- **`result_format` / `response_format`**：DashScope 使用 `result_format='message'`（默认），[OpenAI 兼容接口](../concepts/openai-compatible-api.md)无需显式指定。
- **`stream`**：布尔值，启用[流式输出](../concepts/streaming-output.md)（如 `qwen-deep-research`、`qwen3.5-ocr`）。OCR 流式需额外设置 `stream_options={"include_usage": true}`。
- **模型专属参数**：
  - `qwen-mt-plus`：通过 `extra_body` 或顶层字段传入 `translation_options`（含 `source_lang`, `target_lang`, `terms`, `tm_list`）。
  - `tongyi-intent-detect-v3`：依赖特定 System Prompt 格式（`Response in INTENT_MODE.` 或 `just reply with the chosen tag`）。
  - `qwen-deep-research`：支持 `output_format`（`model_detailed_report` 或 `model_summary_report`）控制报告长度。
  - `gui-plus-*`：需 `extra_body={"vl_high_resolution_images": true}` 启用高分辨率图像处理。

## 使用方式

1. **环境准备**  
   - 获取并配置 API Key 到环境变量 `DASHSCOPE_API_KEY`（[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。
   - 安装 SDK：Python 推荐 `dashscope>=2.12.0` 或 `openai>=1.0.0`；Java 需 `dashscope>=2.12.0`（但注意 `qwen-deep-research` 不支持 Java）。

2. **Endpoint 配置**  
   - **强烈推荐使用业务空间专属域名**（性能与稳定性更优）：
     - 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
     - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
     - 美国（弗吉尼亚）：`https://dashscope-us.aliyuncs.com`
   - WorkspaceId 在百炼控制台「业务空间详情」页获取。旧域名（如 `dashscope.aliyuncs.com`）仍可用，但不推荐。

3. **调用示例（核心模式）**  
   - **单轮文本生成**（`farui-plus`）：直接传入 `messages`，无需特殊 System Prompt。
   - **意图识别**（`tongyi-intent-detect-v3`）：System Prompt 必须包含 `Response in INTENT_MODE.` 或明确的标签列表。
   - **图文任务**（`qwen3.5-ocr`, `gui-plus-*`）：`messages[0].content` 为数组，含 `{"type": "image_url", ...}` 和 `{"type": "text", ...}` 对象。
   - **深度研究**（`qwen-deep-research`）：严格遵循两阶段流程——先发起研究请求获取反问，再将反问+用户回答组合为第二轮输入。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他模型虽多地可用，但需匹配对应地域的 API Key 和 endpoint。
- **SDK 限制**：`qwen-deep-research` 不支持 Java SDK 和 OpenAI 兼容接口，仅限 Python DashScope SDK（见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)）。
- **[流式输出](../concepts/streaming-output.md)兼容性**：`farui-plus` 支持 `stream=True`（Python）或 `streamCall`（Java）；`qwen-deep-research` 必须启用 `stream=True`；`qwen3.5-ocr` 流式需 `stream_options`。
- **成本与限流**：各模型有独立计费（如 `farui-plus` 输入 20 元/百万 [Token](../concepts/token.md)），且受平台限流策略约束（参见 [限流](https://help.aliyun.com/zh/model-studio/rate-limit)）。
- **安全实践**：API Key 务必配置至环境变量，避免硬编码；Java SDK 中 `Generation` 对象非线程安全，需复用或同步管理（见 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)）。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


