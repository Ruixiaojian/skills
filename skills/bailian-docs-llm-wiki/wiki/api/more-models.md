# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖法律、意图理解、机器翻译、深度研究、OCR 和 GUI 自动化等能力。这些模型均基于通义千问基座，通过领域精调、RAG、Agent 等技术增强，支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与 DashScope SDK 调用。开发者需关注地域限制、域名迁移要求及模型特有的输入格式约束。

## 支持的模型/功能

| 模型名称 | 主要能力 | 适用场景 | 文档来源 |
|----------|----------|----------|----------|
| `farui-plus` | 法律问答、文书生成、案情分析、合同审查 | 法律咨询、司法辅助 | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 意图识别、工具调用决策（INTENT_MODE）、标签分类 | 对话系统路由、智能助手前置理解 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-mt-plus` | 多语种机器翻译，支持术语干预、翻译记忆、领域提示 | 技术文档本地化、跨语言内容处理 | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `qwen-deep-research` | 多阶段网络搜索+深度报告生成（含引用溯源） | 学术研究、竞品分析、政策解读 | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `qwen3.5-ocr` | 图像文字提取与结构化解析（支持多图、Prompt 控制输出格式） | 票据识别、证件信息抽取、表单自动化 | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `gui-plus-2026-02-26` | 基于截图的 GUI 操作自动化（鼠标/键盘/等待/终止） | 桌面应用自动化测试、RPA 流程编排 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |

> **注意**：`qwen-deep-research` 明确声明“仅支持华北2（北京）地域”，且“暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)”；而其他模型（如 `qwen-mt-plus`、`qwen3.5-ocr`、`gui-plus-2026-02-26`）在文档中均明确列出 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)用法。该差异需在集成时严格遵循，避免跨地域或跨 SDK 调用失败。

## 关键参数

- **通用参数**  
  - `model`: 必填，模型名称（如 `"farui-plus"`），见上表。  
  - `messages`: 必填，对话消息数组，每项含 `role`（`user`/`system`/`assistant`）和 `content`（字符串或含 `image_url` 的对象数组）。  
  - `result_format` / `response_format`: 非 OpenAI 接口需显式设为 `"message"`；OpenAI 接口默认兼容。  

- **模型特有参数**  
  - `qwen-mt-plus`: 通过 `extra_body.translation_options` 或直接传参 `translation_options` 指定 `source_lang`、`target_lang`、`terms`（术语表）、`tm_list`（翻译记忆）。  
  - `qwen-deep-research`: 支持 `output_format`（`model_detailed_report` 或 `model_summary_report`），控制报告长度。  
  - `qwen3.5-ocr` / `gui-plus-2026-02-26`: `content` 中 `image_url` 对象可带 `min_pixels` 和 `max_pixels` 控制图像缩放；`gui-plus` 还需 `extra_body.vl_high_resolution_images=true` 启用高分辨率处理。  
  - `tongyi-intent-detect-v3`: `system` 消息必须包含 `Response in INTENT_MODE.`（工具调用）或 `just reply with the chosen tag.`（纯标签分类）。

## 使用方式

1. **环境准备**  
   - 获取并配置 API Key 到环境变量 `DASHSCOPE_API_KEY`（[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。  
   - 安装 SDK：Python 推荐 `dashscope>=2.12.0` 或 `openai>=1.0.0`；Java 仅 `dashscope` 支持部分模型（见[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)）。  

2. **域名迁移（强制推荐）**  
   华北2（北京）和新加坡地域用户**必须**使用业务空间专属域名，而非旧版 `dashscope.aliyuncs.com`：  
   - 北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`（DashScope API）或 `/compatible-mode/v1`（OpenAI 兼容）  
   - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`  
   `{WorkspaceId}` 在百炼控制台「业务空间详情」中查看。该要求在 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)、[Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)、[Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 和 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) 中均被强调。

3. **调用示例（核心模式）**  
   - **单轮对话**（如 `farui-plus`）：构造 `messages` 后直接 `Generation.call()` 或 `client.chat.completions.create()`。  
   - **多轮对话**：将上一轮 `response.output.choices[0].message` 追加至 `messages` 数组再调用。  
   - **[流式输出](../concepts/streaming-output.md)**：DashScope SDK 设 `stream=True`；OpenAI SDK 设 `stream=True` 并迭代 `completion`。  
   - **两阶段流程**（如 `qwen-deep-research`）：先调用获取反问内容，再将该内容作为 `assistant` 消息与新 `user` 消息组合发起第二轮调用。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他地域调用将失败；其余模型支持北京、新加坡、美国（弗吉尼亚）三地，但 API Key 和域名需匹配。  
- **限流策略**：所有模型均受百炼平台统一限流控制，具体配额请参见 [限流](https://help.aliyun.com/zh/model-studio/rate-limit)。  
- **成本与免费额度**：`tongyi-intent-detect-v3` 提供开通后90天内100万 [Token](../concepts/token.md) 免费额度；`farui-plus` 等按输入/输出 [Token](../concepts/token.md) 计费（单位：元/百万 [Token](../concepts/token.md)），详见各模型文档中的价格表格。  
- **SDK 线程安全**：DashScope Java SDK 中 `Generation` 等对象非线程安全，需复用实例并自行管理同步（见 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) 说明）。  
- **响应解析**：`tongyi-intent-detect-v3` 的 `INTENT_MODE` 输出需用正则 + JSON 解析 `<tags>`、<tool_call>、`<content>` 三段式结构；`qwen-deep-research` 响应含 `phase` 字段标识当前执行阶段（如 `WebResearch`），需按阶段处理。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


