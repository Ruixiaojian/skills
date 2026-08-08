# [more](more.md) models

百炼平台提供一系列面向垂直场景和特定任务的专用模型，覆盖法律、深度研究、OCR、GUI自动化、意图理解与机器翻译等方向。这些模型在通用大模型基础上进行了领域精调或架构增强，支持通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用。所有模型均需配置业务空间专属域名以获得最佳性能。

## 支持的模型与功能

- **通义法睿（`farui-plus`）**：法律行业专用模型，支持法律咨询、文书生成、案情分析、合同审查等功能，基于千问基座并融合RAG、法律Agent等技术 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。
- **Qwen-Deep-Research（`qwen-deep-research`）**：支持两阶段交互式深度研究，包含反问确认、网络搜索、结构化报告生成，当前**仅支持华北2（北京）地域及 Python SDK**，不支持 Java SDK 和 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **Qwen-OCR（`qwen3.5-ocr`）**：多模态OCR模型，支持图像中文字提取与结构化输出，兼容 OpenAI 接口，支持北京、新加坡、美国（弗吉尼亚）三地调用 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **GUI-Plus（`gui-plus-2026-02-26`）**：界面交互专用模型，可解析截图并执行鼠标/键盘操作，依赖工具调用协议，目前仅公开北京地域接入点。
- **意图理解（`tongyi-intent-detect-v3`）**：毫秒级意图识别模型，支持两种模式：`INTENT_MODE`（输出工具调用JSON）与纯标签分类（如 `alarm_set`），适用于对话系统路由 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **Qwen-MT（`qwen-mt-plus`）**：专业机器翻译模型，支持术语干预、翻译记忆（TM）、领域提示等高级功能，覆盖多地域部署。

> **注意**：文档 6 中对新加坡和美国地域的 `base_url` 描述存在重复（两次列出同一地域），且未明确说明 `qwen-mt-plus` 是否支持所有地域的完整功能（如 TM 在非北京地域是否可用）。实际使用请以控制台最新文档为准。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `model` | 必选，模型标识符 | `"farui-plus"`, `"qwen-deep-research"`, `"qwen3.5-ocr"`, `"gui-plus-2026-02-26"`, `"tongyi-intent-detect-v3"`, `"qwen-mt-plus"` |
| `messages` | 必选，对话消息数组，含 `role`（`user`/`system`/`assistant`）与 `content`；OCR 和 GUI-Plus 支持 `image_url` 类型内容 | `[{"role":"user","content":"起诉书生成"}]` |
| `result_format`（DashScope） | 指定响应格式，常用 `"message"` | `"message"` |
| `stream` | 控制是否启用[流式输出](../concepts/streaming-output.md) | `True`（Python）或 `stream=true`（curl） |
| `translation_options`（Qwen-MT） | 包含 `source_lang`, `target_lang`, `terms`, `tm_list` 等 | `{"source_lang":"Chinese","target_lang":"English"}` |
| `extra_body`（OpenAI 兼容） | 扩展参数载体，如 OCR 的 `{"vl_high_resolution_images": true}` 或 MT 的 `{"translation_options": {...}}` | `{"vl_high_resolution_images": true}` |

## 使用方式

1. **环境准备**  
   - 获取 API Key 并配置至环境变量 `DASHSCOPE_API_KEY`（推荐）或代码内显式传入。  
   - 安装对应 SDK：[DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)（Python/Java）或 [OpenAI SDK](https://help.aliyun.com/zh/model-studio/install-sdk)（Python/Node.js）。  
   - **必须配置业务空间专属域名**：将 `base_url` 或 `dashscope.base_http_api_url` 替换为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/...`，其中 `{WorkspaceId}` 从控制台获取。旧域名（如 `dashscope.aliyuncs.com`）仍可用但不推荐。

2. **调用示例**  
   - **单模型单次调用（法睿）**：  
     ```python
     from dashscope import Generation
     response = Generation.call(model="farui-plus", messages=[{"role":"user","content":"生成离婚协议书"}])
     ```
   - **OCR 图文混合输入（OpenAI 兼容）**：  
     ```python
     client.chat.completions.create(
         model="qwen3.5-ocr",
         messages=[{"role":"user","content":[{"type":"image_url","image_url":{"url":"..."}},{"type":"text","text":"提取发票信息"}]}]
     )
     ```
   - **意图识别（INTENT_MODE）**：  
     System Message 需包含 `Response in INTENT_MODE.` 与工具定义 JSON，响应需用正则解析 `<tags>` / `<tool_call>` / `<content>` 结构。

3. **[流式输出](../concepts/streaming-output.md)**  
   - DashScope：设置 `stream=True`（Python）或调用 `streamCall()`（Java）。  
   - OpenAI 兼容：设置 `stream=True` 并迭代 `completion` 对象，注意 `stream_options={"include_usage": True}` 可返回 token 统计。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；其他模型（OCR、MT、GUI-Plus、意图）虽支持多地域，但各区域 API Key 不互通，需按地域分别申请。
- **SDK 限制**：`qwen-deep-research` 当前**不支持 Java SDK 和 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**，仅限 Python DashScope SDK [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **输入格式**：GUI-Plus 和 OCR 要求 `messages` 中 `user` 角色内容为列表（含 `image_url` + `text`），不可为纯字符串；意图模型对 System Message 格式敏感，缺失 `INTENT_MODE` 或标签列表将导致解析失败。
- **成本与限流**：`farui-plus` 输入/输出成本分别为 20 元/百万 [Token](../concepts/token.md)；`tongyi-intent-detect-v3` 提供 90 天内 100 万 [Token](../concepts/token.md) 免费额度；所有模型均受平台[限流策略](https://help.aliyun.com/zh/model-studio/rate-limit)约束。
- **稳定性建议**：务必迁移至业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名已逐步降级支持。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)


