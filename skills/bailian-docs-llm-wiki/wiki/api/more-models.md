# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖法律、意图理解、深度研究、机器翻译、OCR图文识别及GUI自动化等能力。这些模型均基于通义千问系列基座模型优化，支持通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，适用于对领域精度、响应结构或[多模态](../concepts/multi-modal.md)交互有明确要求的生产场景。

## 支持的模型/功能

| 模型名称 | 主要能力 | 适用场景 | 文档引用 |
|----------|----------|----------|----------|
| `farui-plus` | 法律问答、文书生成、合同审查、案情推理 | 法律咨询、司法辅助、律所SaaS集成 | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 百毫秒级意图识别与工具调用决策（支持 `INTENT_MODE`） | 智能客服路由、语音助手指令解析、Agent 工具选择 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-deep-research` | 多阶段网络搜索+研究规划+报告生成（含参考文献溯源） | 行业分析、竞品调研、学术预研 | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `qwen-mt-plus` | 领域自适应机器翻译（支持术语干预、翻译记忆、领域提示） | 技术文档本地化、多语种客服、合规材料翻译 | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `qwen3.5-ocr` | 图文混合输入下的高精度文本提取与结构化输出 | 车票/发票/证件识别、表单信息抽取、文档数字化 | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `gui-plus-2026-02-26` | 基于截图的 GUI 自动化操作（鼠标/键盘/等待/终止） | 桌面应用RPA、无障碍辅助、UI测试脚本生成 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |

> **注意**：`qwen-deep-research` 明确声明“仅支持华北2（北京）地域”且“暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)”，而其他模型（如 `qwen-mt-plus`、`qwen3.5-ocr`、`gui-plus-2026-02-26`）均明确支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)。该差异需在技术选型时重点确认。

## 关键参数

所有模型共性参数（见各文档 `model` 和 `messages` 字段定义）：
- `model`: 必填字符串，值为上表所列模型名；
- `messages`: 必填数组，按对话顺序排列，每项含 `role`（`user`/`system`/`assistant`）和 `content`；  
- `result_format` / `output_format`: 控制响应结构（如 `message`、`model_detailed_report`）；
- `stream`: 布尔值，启用[流式输出](../concepts/streaming-output.md)（部分模型需配合 `incremental_output=True` 或 `stream_options={"include_usage": true}`）。

模型特有参数：
- `tongyi-intent-detect-v3`: 依赖 `system` message 中的 `Response in INTENT_MODE.` 指令及工具/意图 JSON 定义；
- `qwen-mt-plus`: 通过 `extra_body.translation_options` 传入 `source_lang`、`target_lang`、`terms`、`tm_list` 等翻译控制参数；
- `qwen3.5-ocr` / `gui-plus-2026-02-26`: `content` 支持 `image_url` + `text` 混合类型，可指定 `min_pixels`/`max_pixels` 或 `vl_high_resolution_images`；
- `qwen-deep-research`: 两阶段调用必需——第一阶段仅 `user` message 发起研究请求，第二阶段需拼接 `user`→`assistant`（反问）→`user`（澄清）完整上下文。

## 使用方式

### 域名与认证
- **强制使用业务空间专属域名**：华北2（北京）和新加坡地域必须使用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，旧域名 `dashscope.aliyuncs.com` 已不推荐（[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)、[Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)、[Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)、[GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) 均强调此迁移要求）；
- **API Key 管理**：必须通过环境变量 `DASHSCOPE_API_KEY` 配置，禁止硬编码（[通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) 明确警示泄露风险）。

### SDK 选择
- Python：全模型支持 DashScope SDK 和 OpenAI SDK；
- Java：仅 `farui-plus` 明确提供 Java 示例；`qwen-deep-research` 明确声明**不支持 Java SDK**；
- Node.js：`qwen-mt-plus`、`qwen3.5-ocr`、`gui-plus-2026-02-26` 提供 Node.js 示例，`tongyi-intent-detect-v3` 未提供。

### 调用模式
- **单轮对话**：适用于一次性任务（如文书生成、翻译）；
- **多轮对话**：需手动维护 `messages` 列表并追加历史 `assistant` 和新 `user` 消息（[通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) 提供完整示例）；
- **[流式输出](../concepts/streaming-output.md)**：`farui-plus`、`qwen-deep-research`、`qwen3.5-ocr` 均支持，但参数细节不同（如 `incremental_output` 仅见于 `farui-plus` 示例）。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅限华北2（北京）地域，其他模型虽支持多地域，但 API Key 需与地域匹配（[Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) 多次强调“各地域的 API Key 不同”）；
- **SDK 兼容性**：`qwen-deep-research` 不支持 Java SDK 和 OpenAI 兼容接口，与其余模型形成明显断层；
- **输入格式约束**：
  - `tongyi-intent-detect-v3` 的 `system` message 必须包含精确字符串 `Response in INTENT_MODE.`（注意末尾句点），否则无法触发意图模式；
  - `qwen3.5-ocr` 和 `gui-plus-2026-02-26` 的 `image_url` 输入需符合像素阈值（`min_pixels`/`max_pixels`），否则可能被缩放导致识别失真；
- **成本与限流**：`farui-plus` 的计费单位为“每百万 [Token](../concepts/token.md)”，且需查阅独立限流文档（[通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) 引用限流链接）；`tongyi-intent-detect-v3` 提供 100 万 [Token](../concepts/token.md) 免费额度（90 天有效期），该策略与其他模型不同；
- **响应解析复杂度**：`tongyi-intent-detect-v3` 的 `INTENT_MODE` 响应需正则解析 `<tags>`/<tool_call>/`<content>` 三段式结构（[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 提供 `parse_text` 函数）；`qwen-deep-research` 响应含 `phase` 字段（如 `WebResearch`、`answer`），需按阶段处理 `extra.deep_research.references` 等嵌套数据。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


