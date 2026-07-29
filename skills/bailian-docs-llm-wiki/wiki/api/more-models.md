# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，覆盖意图理解、法律服务、多模态OCR、机器翻译和深度研究等能力。这些模型在通用大模型基础上进行了领域精调与架构优化，支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)和 DashScope 原生 SDK 调用，适用于高精度、低延迟、强可控性的生产级任务。

## 支持的模型/功能

| 模型名称 | 主要能力 | 适用场景 | 文档来源 |
|----------|-----------|------------|-----------|
| `tongyi-intent-detect-v3` | 意图识别与[函数调用](../concepts/function-calling.md)解析（INTENT_MODE）或纯标签分类 | 对话路由、Agent 工具选择、业务指令归一化 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `farui-plus` | 法律问答、文书生成、案情分析、合同审查 | 法律咨询、司法辅助、合规自动化 | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `qwen3.5-ocr` | 图像中文字提取与结构化信息抽取（支持图文混合 Prompt） | 票据识别、证件解析、报表 OCR、多语言文档处理 | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `qwen-mt-plus` | 高质量机器翻译，支持术语干预、翻译记忆（TM）、领域提示 | 技术文档本地化、多语种客服、专业内容翻译 | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `qwen-deep-research` | 多阶段自主研究：反问确认 → 网络搜索 → 综合分析 → 引用报告生成 | 行业调研、竞品分析、学术预研、政策解读 | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |

> **注意**：`qwen-deep-research` **仅支持华北2（北京）地域**，且**不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 Java SDK**，必须使用 Python DashScope SDK 调用；而其他模型（如 `qwen3.5-ocr`、`qwen-mt-plus`）在文档中均明确声明支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，该差异为模型设计约束，非文档错误。

## 关键参数

- **`model`**（必填）：模型标识符，如 `"tongyi-intent-detect-v3"`、`"qwen-mt-plus"`。所有模型均需显式指定。
- **`messages`**（必填）：对话消息数组，格式为 `[{ "role": "user", "content": ... }]`。部分模型有特殊要求：
  - `tongyi-intent-detect-v3` 要求 `system` 消息中包含 `Response in INTENT_MODE.` 或明确的意图字典；
  - `qwen3.5-ocr` 支持 `content` 数组内混合 `image_url` 与 `text` 类型项，并可配置 `min_pixels` / `max_pixels`；
  - `qwen-deep-research` 采用两阶段调用，第二步 `messages` 必须包含第一步的 `assistant` 反问内容。
- **`translation_options`**（`qwen-mt-plus` 专用）：JSON 对象，含 `source_lang`、`target_lang`、`terms`（术语表）、`tm_list`（翻译记忆库）等字段。
- **`output_format`**（`qwen-deep-research` 专用）：可选 `"model_detailed_report"`（默认，~6000 [Token](../concepts/token.md)）或 `"model_summary_report"`（~1500–2000 [Token](../concepts/token.md)）。
- **`stream`**：所有模型均支持流式响应（`True`/`true`），但 `qwen-deep-research` **必须启用流式**以获取中间阶段状态（如 `phase: "WebResearch"`）。

## 使用方式

### 基础调用前提
- 已获取对应地域的 API Key（[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）；
- 推荐将 API Key 配置至环境变量 `DASHSCOPE_API_KEY`（[配置指南](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)）；
- 安装 SDK：Python 用户安装 `dashscope` 或 `openai`（>=1.0），Java 用户安装 `dashscope-java-sdk`（>=2.12.0）。

### 域名与 endpoint
- **强烈推荐使用业务空间专属域名**（性能与稳定性更优）：
  - 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
  - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
  - 美国（弗吉尼亚）：`https://dashscope-us.aliyuncs.com`
- OpenAI 兼容接口 endpoint 为 `/compatible-mode/v1/chat/completions`；
- DashScope 原生接口 endpoint 为 `/api/v1/services/aigc/text-generation/generation`（`qwen-deep-research` 除外，其路径同上）。

### 示例模式
- **意图识别（[函数调用](../concepts/function-calling.md)）**：见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 中 `INTENT_MODE` 的 System Message 构造与 `parse_text` 解析逻辑；
- **OCR 结构化提取**：见 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 中 `image_url` + `text` Prompt 组合用法；
- **术语干预翻译**：见 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) 中 `terms` 字段定义；
- **深度研究两阶段**：见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) 中 `step1_content` 提取与第二步 `messages` 构造。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；`qwen3.5-ocr` 和 `qwen-mt-plus` 在美东、新加坡、北京三地均可用，但 API Key 需匹配地域。
- **SDK 限制**：`qwen-deep-research` **不支持 OpenAI 兼容接口**，仅支持 Python DashScope SDK（[Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) 明确说明）；而 `farui-plus`、`qwen3.5-ocr` 等模型在各自文档中均提供 OpenAI 和 DashScope 双示例。
- **输入格式**：`qwen3.5-ocr` 的 `content` 字段必须为数组（含 `image_url` 和 `text`），不可为纯字符串；违反将返回 400 错误。
- **免费额度**：`tongyi-intent-detect-v3` 提供开通后 90 天内 100 万 [Token](../concepts/token.md) 免费额度（[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）；其他模型未在原始文档中声明免费额度。
- **流式必选**：`qwen-deep-research` 的完整工作流（含 ResearchPlanning、WebResearch 等阶段）**仅通过流式响应暴露**，非流式调用将无法获取中间状态或引用信息。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)


