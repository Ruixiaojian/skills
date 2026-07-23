# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，覆盖意图理解、机器翻译、深度研究、GUI自动化和法律推理等任务。这些模型在特定领域经过强化训练或架构优化，相比通用模型具备更高的准确率、更优的响应结构和更强的领域适配能力。开发者可通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope SDK 调用，需注意地域限制、域名迁移要求及模型特有的输入格式约束。

## 支持的模型/功能

当前 `more models` 类别下支持以下专用模型：

- **`tongyi-intent-detect-v3`**：意图理解模型，支持两种模式：  
  - `INTENT_MODE`：输出结构化[函数调用](../concepts/function-calling.md)（含工具名与参数），适用于 Agent 场景；  
  - 纯标签模式：从预定义意图字典中返回单个语义标签（如 `alarm_set`），支持单 Token 输出以提升延迟敏感型场景性能。详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。  
- **`qwen-mt-plus`**：专业级机器翻译模型，支持源/目标语言自动识别、术语干预（`terms`）、翻译记忆（`tm_list`）和领域提示，适用于技术文档、合同等高保真翻译场景。  
- **`qwen-deep-research`**：深度研究模型，采用两阶段工作流（反问确认 → 深入研究），支持联网搜索、引用溯源与多粒度报告生成（`model_detailed_report` / `model_summary_report`）。**注意**：该模型[仅支持华北2（北京）地域且不支持 OpenAI 兼容接口](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)，必须使用 DashScope Python SDK 调用。  
- **`gui-plus-2026-02-26`**：GUI 自动化模型，专为桌面界面交互设计，接受截图（`image_url`）与自然语言指令，输出鼠标/键盘操作指令（如 `left_click`, `type`），需严格遵循 `<tools>` + `<tool_call>...<tool_call>` 响应格式。  
- **`farui-plus`**：法律行业大模型，集成 RAG、法律 Agent 和司法小模型，支持法律咨询、文书生成（如起诉书）、案情分析与合同审查。其上下文长度达 12k Token，但输出成本显著高于通用模型（20元/百万 Token）。

> **注意**：文档 2 中重复列出了北京、新加坡、美国地域的配置说明，且对新加坡和美国地域的 `base_url` 描述存在冗余与不一致（如美国地域未提供 WorkspaceId 占位符），实际应以 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) 中“重要”区块的迁移指引为准，即仅北京与新加坡地域启用 WorkspaceId 专属域名，美国地域仍使用 `dashscope-us.aliyuncs.com`。

## 关键参数

| 参数 | 说明 | 示例值 | 文档依据 |
|------|------|--------|----------|
| `model` | 必选，模型标识符 | `"tongyi-intent-detect-v3"`, `"qwen-mt-plus"` | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md), [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `translation_options` | `qwen-mt-plus` 专用，包含 `source_lang`, `target_lang`, `terms`, `tm_list` | `{"source_lang": "Chinese", "target_lang": "English", "terms": [...]}` | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `output_format` | `qwen-deep-research` 专用，控制报告粒度 | `"model_detailed_report"` (默认), `"model_summary_report"` | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `extra_body` | [OpenAI 兼容接口](../concepts/openai-compatible-api.md)中传递非标准字段（如 `vl_high_resolution_images`, `translation_options`） | `{"vl_high_resolution_images": true}` | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md), [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `stream` & `incremental_output` | 控制[流式输出](../concepts/streaming-output.md)行为（`qwen-deep-research`, `farui-plus` 等支持） | `True`, `True` | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md), [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |

## 使用方式

1. **环境准备**：  
   - 获取并配置 API Key（推荐设为环境变量 `DASHSCOPE_API_KEY`）；  
   - 安装对应 SDK（DashScope SDK 或 OpenAI SDK）；  
   - **强制迁移域名**：北京/新加坡地域必须使用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，`{WorkspaceId}` 在控制台业务空间详情页获取。  

2. **请求构造**：  
   - `tongyi-intent-detect-v3`：System Message 必须显式声明 `Response in INTENT_MODE.`（[函数调用](../concepts/function-calling.md)）或 `just reply with the chosen tag.`（纯标签）；  
   - `qwen-mt-plus`：将 `translation_options` 作为 `extra_body`（OpenAI）或顶层字段（DashScope）传入；  
   - `gui-plus-2026-02-26`：`messages[0].content` 需为含 `image_url` 的数组，且 System Prompt 必须包含 `<tools>` 定义与 `<tool_call>` 格式规范；  
   - `qwen-deep-research`：严格按两阶段调用——首请求仅含用户初始问题，第二请求需拼接 `user → assistant → user` 三元组；  
   - `farui-plus`：支持标准单轮/多轮对话及[流式输出](../concepts/streaming-output.md)（设置 `stream=True` 与 `incremental_output=True`）。

3. **响应解析**：  
   - `tongyi-intent-detect-v3`（INTENT_MODE）：需用正则提取 `<tags>`, `<tool_call>`, `<content>` 三段内容，并 `json.loads()` 解析 `tool_call` 字段；  
   - `qwen-deep-research`：响应含 `phase` 字段（如 `answer`, `WebResearch`），需按阶段处理 `extra.deep_research.references` 等结构化数据；  
   - 其他模型：遵循标准 OpenAI/DashScope 响应格式，`choices[0].message.content` 为文本结果。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他模型（如 `qwen-mt-plus`）在美国（弗吉尼亚）地域使用公共域名 `dashscope-us.aliyuncs.com`，不支持 WorkspaceId。  
- **接口限制**：`qwen-deep-research` 不支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，仅 DashScope Python SDK 可用；`gui-plus-2026-02-26` 要求输入图像 URL 可公开访问，且 `extra_body={"vl_high_resolution_images": True}` 为必需项。  
- **成本与限流**：`farui-plus` 输入成本为 20元/百万 Token，显著高于其他模型；所有模型的限流策略详见 [限流](https://help.aliyun.com/zh/model-studio/rate-limit)，需在生产环境做好熔断与重试。  
- **稳定性建议**：北京/新加坡地域务必迁移至 WorkspaceId 专属域名，[原文标题](../../raw/model-api-reference/more-models/intent-detect-capability.md) 明确指出其“能够为推理请求提供卓越的性能和更高的稳定性”。  
- **安全实践**：API Key 绝不可硬编码，必须通过环境变量注入；DashScope Java SDK 对象非线程安全，需自行管理同步机制。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)


