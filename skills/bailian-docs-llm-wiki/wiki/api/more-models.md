# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，覆盖法律、意图理解、机器翻译、深度研究、OCR图文识别和GUI自动化等方向。这些模型均基于通义千问基座，通过领域数据精调与能力增强，具备更强的专业性与实用性。开发者可通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，支持流式/非[流式输出](../concepts/streaming-output.md)、多轮对话及结构化参数配置。

## 支持的模型/功能

当前 `more models` 类别下支持以下专业模型：

- **通义法睿（`farui-plus`）**：法律行业专用模型，支持法律咨询、文书生成、案情分析、合同审查等功能，上下文长度 12k [Token](../concepts/token.md) [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)  
- **意图理解模型（`tongyi-intent-detect-v3`）**：毫秒级意图识别，支持[函数调用](../concepts/function-calling.md)（INTENT_MODE）或纯标签分类两种模式，上下文长度 8,192 [Token](../concepts/token.md) [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)  
- **Qwen-MT（`qwen-mt-plus`）**：高质量机器翻译模型，支持术语干预、翻译记忆（TM）、领域提示等高级能力 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)  
- **Qwen-Deep-Research（`qwen-deep-research`）**：支持两阶段交互式深度研究（反问确认 + 网络检索分析），仅限华北2（北京）地域，**暂不支持 Java SDK 和 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)** [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)  
- **Qwen-OCR（`qwen3.5-ocr`）**：多模态 OCR 模型，支持图像+文本 Prompt 联合输入，可提取结构化票据、文档等信息 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)  
- **GUI-Plus（`gui-plus-2026-02-26`）**：桌面 GUI 自动化模型，通过截图理解界面并执行鼠标/键盘操作，需传入高分辨率图像 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)  

> **注意**：文档 4 明确指出 Qwen-Deep-Research “仅支持通过 Python DashScope SDK 调用，暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)”，而文档 1 中 Java SDK 示例代码存在语法截断（`System.out.println(JsonUtil` 未闭合），且文档 2 的 Java 示例中 `JsonUtils.toJson()` 调用方式与文档 1 不一致，表明 Java SDK 支持存在版本兼容性风险，建议优先使用 Python SDK。

## 关键参数

| 参数 | 说明 | 示例值/约束 |
|------|------|-------------|
| `model` | 必选，模型唯一标识符 | `"farui-plus"`, `"tongyi-intent-detect-v3"`, `"qwen-mt-plus"` 等 |
| `messages` | 必选，对话消息数组，含 `role`（`user`/`system`/`assistant`）和 `content` | `[{ "role": "user", "content": "..." }]`；OCR/GUI-Plus 支持 `content` 为图像 URL 数组 |
| `result_format` / `response_format` | 输出格式控制（DashScope/OpenAI） | `"message"`（推荐），`"text"`（已弃用） |
| `stream` | 是否启用[流式输出](../concepts/streaming-output.md) | `True`（Python），`true`（JSON/curl） |
| `extra_body`（OpenAI） / `generation_params`（DashScope） | 模型专属参数载体 | OCR 使用 `"vl_high_resolution_images": true`；Qwen-MT 使用 `"translation_options"` 对象；意图模型需在 `system` message 中声明 `Response in INTENT_MODE.` |

## 使用方式

### 基础调用流程
1. **准备环境**：获取 API Key 并配置至环境变量 `DASHSCOPE_API_KEY`；安装对应 SDK（[DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk) 或 [OpenAI SDK](https://help.aliyun.com/zh/model-studio/install-sdk)）  
2. **选择域名**：强烈建议使用业务空间专属域名提升稳定性与性能（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 和 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) 中的迁移说明  
3. **构造请求**：按模型要求组织 `messages`，必要时添加 `system` 角色指令（如意图模型的 `INTENT_MODE`、GUI-Plus 的工具定义）  
4. **处理响应**：解析 `output.choices[0].message.content`（非流式）或迭代 `stream` 响应（流式）；Qwen-Deep-Research 需按 `phase` 字段区分研究阶段  

### 特殊能力调用示例
- **术语干预（Qwen-MT）**：在 `translation_options` 中传入 `terms` 数组，强制指定专有名词译法  
- **OCR 结构化提取**：`messages.content` 包含 `image_url` 和 `text` [prompt](../guides/prompt.md)，[prompt](../guides/prompt.md) 应明确要求 JSON 格式输出  
- **GUI 自动化**：`system` message 必须完整嵌入 `<tools>` 定义，并严格遵循 `Action` + `<tool_call>...<tool_call>` 响应格式  

## 限制和注意事项

- **地域限制**：Qwen-Deep-Research 仅支持华北2（北京）地域；Qwen-MT 和 Qwen-OCR 在美东、新加坡等地域有独立 endpoint，需匹配对应 API Key [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)  
- **SDK 限制**：Qwen-Deep-Research 明确不支持 Java SDK 和 OpenAI 兼容接口；通义法睿 Java SDK 示例存在代码截断，实际使用需验证 SDK 版本（≥2.12.0）与线程安全机制  
- **[流式输出](../concepts/streaming-output.md)差异**：DashScope Python SDK 需设置 `stream=True` 和 `incremental_output=True`；Java SDK 需调用 `streamCall()` 方法；OpenAI SDK 统一使用 `stream=True`  
- **成本与限流**：各模型按输入/输出 [Token](../concepts/token.md) 计费（如 `farui-plus` 输入 20 元/百万 Token），具体见各模型文档；全局限流策略参见 [限流](https://help.aliyun.com/zh/model-studio/rate-limit)  
- **安全实践**：API Key **必须**配置到环境变量，禁止硬编码；DashScope Java SDK 对象（如 `Generation`）非线程安全，需自行管理同步或复用策略 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


