# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，覆盖意图理解、深度研究、OCR识别、GUI自动化、机器翻译和法律推理等能力。这些模型均基于通义千问基座，通过领域数据精调与架构优化，在特定任务上显著优于通用模型。开发者可通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 调用，支持多地域部署与业务空间专属域名接入。

## 支持的模型/功能

当前 `more models` 类别下已开放以下专用模型：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持毫秒级意图识别与[函数调用](../concepts/function-calling.md)生成，适用于对话路由、智能助手等场景。详情见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **深度研究模型**：`qwen-deep-research`，支持两阶段交互式研究（反问确认 + 网络检索增强分析），仅限华北2（北京）地域调用，暂不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **OCR识别模型**：`qwen3.5-ocr`，支持图文混合输入与结构化文本提取，兼容 OpenAI 多模态格式（含 `image_url` + `min_pixels`/`max_pixels` 参数）[Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **GUI自动化模型**：`gui-plus-2026-02-26`，专用于桌面界面操作，需配合 `computer_use` 工具调用及高分辨率图像输入（通过 `extra_body={"vl_high_resolution_images": true}` 启用）。
- **机器翻译模型**：`qwen-mt-plus`，支持源/目标语言指定、术语干预、翻译记忆（TM）及领域提示，所有参数均通过 `extra_body.translation_options` 传递。
- **法律推理模型**：`farui-plus`，上下文长度 12K，具备法律文书生成、案情分析、合同审查等能力，支持单轮/多轮对话与[流式输出](../concepts/streaming-output.md)。

> **注意**：文档 5 中重复列出了新加坡与美国地域的配置说明（两次“新加坡地域”、两次“美国（弗吉尼亚）地域”），属冗余内容，实际配置请以首次出现的条目为准。

## 关键参数

| 参数 | 类型 | 说明 | 所属模型 |
|------|------|------|----------|
| `model` | string | 必选。模型名称，如 `tongyi-intent-detect-v3`、`qwen3.5-ocr` 等 | 全部 |
| `messages` | array | 必选。按角色（`system`/`user`/`assistant`）组织的对话历史，支持 `text` 和 `image_url` 类型内容 | `qwen3.5-ocr`, `gui-plus-2026-02-26`, `qwen-mt-plus`, `farui-plus` |
| `system` message 内容 | string | 控制行为模式的关键指令。例如：<br>- `tongyi-intent-detect-v3` 需包含 `Response in INTENT_MODE.` 或明确意图字典<br>- `gui-plus-2026-02-26` 需声明 `<tools>` 与 `<tool_call>` 响应格式 | `tongyi-intent-detect-v3`, `gui-plus-2026-02-26` |
| `extra_body.translation_options` | object | `qwen-mt-plus` 专用，包含 `source_lang`, `target_lang`, `terms`, `tm_list` 等字段 | `qwen-mt-plus` |
| `result_format="message"` | string | DashScope SDK 中必需显式设置，否则默认返回 `text` 格式（无 `choices` 结构） | `farui-plus`, `qwen-deep-research` |
| `stream=True` + `incremental_output=True` | boolean | [流式输出](../concepts/streaming-output.md)必需组合，尤其 `farui-plus` 的 Java SDK 需使用 `streamCall` 接口 | `farui-plus` |

## 使用方式

### 域名与认证
- **强烈推荐迁移至业务空间专属域名**：华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 和 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 中的迁移说明。
- 所有模型均需有效 `DASHSCOPE_API_KEY`，建议配置至环境变量而非硬编码。

### 调用协议选择
- **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**：适用于 `tongyi-intent-detect-v3`, `qwen3.5-ocr`, `gui-plus-2026-02-26`, `qwen-mt-plus`，需设置 `base_url` 并使用 `chat.completions.create`。
- **DashScope SDK**：适用于 `qwen-deep-research`（强制）、`farui-plus`（推荐）、`tongyi-intent-detect-v3`（可选），需设置 `dashscope.base_http_api_url`（北京/新加坡）或 `Constants.baseHttpApiUrl`（Java）。

### 输入构造要点
- **意图识别**：`system` 消息必须明确指示 `INTENT_MODE` 或意图字典；工具定义需 JSON 序列化后嵌入 [prompt](../guides/prompt.md)。
- **OCR 与 GUI**：`user` 消息中 `content` 为数组，含 `{"type": "image_url", "image_url": {"url": "..."}, "min_pixels": ..., "max_pixels": ...}` 与 `{"type": "text", "text": "prompt"}`。
- **翻译**：`translation_options` 必须置于 `extra_body`（Python/Node.js）或顶层请求体（curl）。
- **深度研究**：严格遵循两阶段流程——先发起研究主题（无 `assistant` 消息），再将模型反问结果作为 `assistant` 消息传入第二轮请求。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；`farui-plus` 未明确地域限制，但示例代码均使用北京专属域名，建议优先选用北京地域。
- **SDK 支持差异**：
  - `qwen-deep-research` **不支持 OpenAI 兼容接口**，仅 DashScope Python SDK 可用 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
  - `farui-plus` 的 Java SDK 需版本 ≥ 2.12.0，且 `Generation` 对象非线程安全。
- **成本与配额**：`tongyi-intent-detect-v3` 提供开通后90天内100万 [Token](../concepts/token.md) 免费额度；`farui-plus` 输入成本为20元/百万 [Token](../concepts/token.md)，具体计费规则需查阅控制台限流文档。
- **响应解析**：`tongyi-intent-detect-v3` 的 `INTENT_MODE` 输出需用正则解析 `<tags>`/<tool_call>/`<content>` 三段式结构；`qwen-deep-research` 响应含 `phase` 字段（如 `answer`, `WebResearch`），需按阶段处理 `extra.deep_research.references` 等字段。
- **图像预处理**：`qwen3.5-ocr` 与 `gui-plus-2026-02-26` 均支持 `min_pixels`/`max_pixels` 自动缩放，但 `gui-plus` 必须启用 `vl_high_resolution_images` 才能正确解析桌面截图细节。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)


