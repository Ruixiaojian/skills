# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖法律、意图理解、机器翻译、深度研究、OCR和GUI自动化等能力。这些模型均基于通义千问基座，通过领域精调、RAG增强或[多模态](../concepts/multi-modal.md)架构优化，在特定任务上具备更强的专业性和实用性。开发者可通过DashScope SDK或OpenAI兼容接口调用，支持[流式输出](../concepts/streaming-output.md)、多轮对话及结构化参数配置。

## 支持的模型与功能

当前支持以下专用模型：

- **通义法睿（`farui-plus`）**：法律行业大模型，支持法律咨询、文书生成、案情分析、合同审查等，详见[通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。
- **意图理解模型（`tongyi-intent-detect-v3`）**：毫秒级意图识别，支持[函数调用](../concepts/function-calling.md)解析与纯标签分类两种模式，适用于智能助手、对话路由等场景。
- **Qwen-MT（`qwen-mt-plus`）**：专业机器翻译模型，支持术语干预、翻译记忆（TM）和领域提示，可显著提升技术文档、合同等专业文本的译文一致性与准确性。
- **Qwen-Deep-Research（`qwen-deep-research`）**：支持两阶段交互式深度研究，自动规划研究路径、执行网络搜索并生成带参考文献的详尽报告；**仅支持华北2（北京）地域及Python DashScope SDK**，不支持Java SDK或OpenAI兼容接口 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **Qwen-OCR（`qwen3.5-ocr`）**：[多模态](../concepts/multi-modal.md)OCR模型，支持图像输入+文本Prompt联合推理，可精准提取票据、证件等复杂版式中的结构化信息。
- **GUI-Plus（`gui-plus-2026-02-26`）**：界面交互专用模型，通过截图理解GUI状态并生成鼠标/键盘操作指令，适用于自动化测试与RPA场景。

> **注意**：文档 3 中对美国（弗吉尼亚）地域的 `qwen-mt` 接口描述重复出现两次，且未明确说明该地域是否支持所有功能（如术语干预、TM），实际调用前请以控制台最新文档为准；文档 5 和文档 6 均强调北京/新加坡地域专属域名优势，但文档 4 明确指出 `qwen-deep-research` **仅支持华北2（北京）地域**，此限制未在其他文档中体现，应以文档 4 为准。

## 关键参数

| 参数 | 说明 | 示例值 | 备注 |
|------|------|--------|------|
| `model` | 模型标识符 | `"farui-plus"`, `"tongyi-intent-detect-v3"` | 必填，不同模型不可混用 |
| `messages` | 对话历史数组 | `[{"role":"user","content":"..."}]` | `qwen-deep-research` 要求两阶段构造（反问确认 + 深入研究）；`qwen-ocr` 和 `gui-plus` 支持 `image_url` 类型内容 |
| `result_format` / `output_format` | 输出格式 | `"message"`（默认）、`"model_detailed_report"` | `qwen-deep-research` 支持 `model_detailed_report`（约6000 [Token](../concepts/token.md)）和 `model_summary_report`（约1500–2000 [Token](../concepts/token.md)） |
| `translation_options` | Qwen-MT专用参数 | `{"source_lang":"Chinese","target_lang":"English","terms":[...]}` | 仅 `qwen-mt-plus` 有效，含 `source_lang`、`target_lang`、`terms`（术语干预）、`tm_list`（翻译记忆） |
| `extra_body` | OpenAI兼容接口扩展字段 | `{"vl_high_resolution_images": true}` | `gui-plus` 需启用高清图像处理；`qwen-mt-plus` 使用 `translation_options` |

## 使用方式

### 通用前提
- 获取并配置API Key：推荐设为环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄露 [获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
- 安装SDK：Python 或 Java 版 DashScope SDK，或 OpenAI SDK（v1.0+）。
- **强制使用业务空间专属域名**：华北2（北京）和新加坡地域必须使用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，旧域名已不推荐 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。

### 调用示例要点
- **[流式输出](../concepts/streaming-output.md)**：设置 `stream=True`（Python）或 `streamCall()`（Java），配合 `incremental_output=True` 获取实时token；`qwen-deep-research` 默认流式，需循环读取 `response.output.message.content`。
- **[多模态](../concepts/multi-modal.md)输入**：`qwen-ocr` 和 `gui-plus` 的 `messages.content` 为数组，包含 `image_url` 和 `text` 对象，`image_url` 可选配 `min_pixels`/`max_pixels` 控制图像缩放。
- **意图识别模式**：需严格按格式构造 `system` 消息——`Response in INTENT_MODE.` 触发工具调用解析；`just reply with the chosen tag.` 触发纯标签分类。
- **深度研究流程**：必须分两步调用：第一步传入初始主题获取模型反问；第二步将反问结果作为 `assistant` 消息，连同用户澄清一并提交。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他模型虽支持多地域，但**强烈建议迁移至业务空间专属域名**以获得更高稳定性与性能 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)。
- **SDK支持差异**：
  - `qwen-deep-research` 仅支持 Python DashScope SDK，Java SDK 和 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)暂不支持；
  - `gui-plus` 和 `qwen-ocr` 在 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)中需通过 `extra_body` 传递扩展参数（如 `vl_high_resolution_images`），DashScope SDK 不支持 `gui-plus`。
- **[Token](../concepts/token.md)成本与限流**：各模型输入/输出成本不同（如 `farui-plus` 输入20元/百万Token），具体见各模型文档；全局限流策略参见[限流](https://help.aliyun.com/zh/model-studio/rate-limit)。
- **安全实践**：避免在代码中明文写入API Key；Java SDK中 `Generation` 对象非线程安全，需复用并自行管理同步 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。
- **响应解析**：`tongyi-intent-detect-v3` 返回含 `<tags>`、<tool_call>、`<content>` 的特殊格式，需用正则+JSON解析提取 `tool_call` 数组；`qwen-deep-research` 响应含 `phase` 字段（如 `WebResearch`、`answer`），需按阶段处理 `extra.deep_research.references` 等结构化数据。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


