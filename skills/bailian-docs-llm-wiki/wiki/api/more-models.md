# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，覆盖法律、翻译、意图理解、深度研究、GUI自动化和OCR等能力。这些模型在通用大模型基础上进行了领域精调或架构优化，支持通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，适用于需要高精度、低延迟或特定模态处理的生产场景。

## 支持的模型/功能

| 模型名称 | 类型 | 核心能力 | 适用场景 | 文档引用 |
|----------|------|-----------|------------|-----------|
| `farui-plus` | 法律大模型 | 法律问答、案情分析、文书生成、合同审查、RAG检索增强 | 律所、司法机关、法务部门 | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `qwen-mt-plus` | 机器翻译模型 | 多语言翻译、术语干预、翻译记忆（TM）、领域提示 | 技术文档本地化、多语种内容分发 | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `tongyi-intent-detect-v3` | 意图理解模型 | 百毫秒级意图识别、工具调用决策、单标签/多标签分类 | 智能客服、语音助手、任务编排系统 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-deep-research` | 深度研究模型 | 自动规划研究路径、网络搜索、多轮反问确认、结构化报告生成 | 行业分析、竞品调研、学术辅助 | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `gui-plus-2026-02-26` | GUI交互模型 | 基于截图的桌面操作（鼠标/键盘/等待/终止）、多步自动化执行 | RPA流程自动化、UI测试、无障碍辅助 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |
| `qwen3.5-ocr` | 多模态OCR模型 | 图像文字提取、结构化信息抽取（如车票、发票）、支持自定义Prompt | 单据识别、证照处理、文档数字化 | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |

> **注意**：文档 2 中重复列出了北京、新加坡、美国地域的配置说明（两次“北京地域”、两次“新加坡地域”、两次“美国（弗吉尼亚）地域”），属冗余排版，实际配置以首次出现为准。开发者应仅保留一份地域配置示例，避免混淆。

## 关键参数

所有模型均遵循统一参数框架，但关键字段存在差异：

- **`model`**（必选）：严格区分大小写与版本后缀，例如 `qwen3.5-ocr` 不可写作 `qwen-ocr`；`gui-plus-2026-02-26` 中日期为模型标识一部分，不可省略。
- **`messages`**（必选）：  
  - 法律/意图/翻译模型支持标准 `role`（`system`/`user`/`assistant`）+ `content` 结构；  
  - OCR 和 GUI 模型要求 `content` 为数组，含 `image_url` 和 `text` 元素（[Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)）；  
  - 深度研究模型需按两阶段构造 `messages`：第一阶段仅含用户初始请求，第二阶段需拼接模型反问与用户澄清（[Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)）。
- **`extra_body` / `translation_options` / `vl_high_resolution_images`**：模型特有扩展参数：  
  - `qwen-mt-plus` 使用 `translation_options` 控制源/目标语言、术语表、翻译记忆；  
  - `gui-plus-*` 需设置 `vl_high_resolution_images: true` 保障截图精度；  
  - `qwen3.5-ocr` 支持 `min_pixels`/`max_pixels` 调整图像预处理分辨率。
- **`output_format`**（`qwen-deep-research` 专属）：可选 `model_detailed_report`（默认，~6000 [Token](../concepts/token.md)）或 `model_summary_report`（~1500–2000 [Token](../concepts/token.md)）。

## 使用方式

### 接口协议
- **DashScope SDK**：Python（全模型支持）、Java（`farui-plus` 等文本模型支持，但 `qwen-deep-research` 明确不支持 Java SDK）；  
- **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**：Python/Node.js/curl 均适用，但需注意：  
  - `qwen-deep-research` **不支持** [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)）；  
  - 所有 OpenAI 兼容调用必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），旧域名 `dashscope.aliyuncs.com` 已不推荐。

### 认证与配置
- API Key 必须通过环境变量 `DASHSCOPE_API_KEY` 注入，禁止硬编码；  
- 地域与 WorkspaceId 绑定：华北2（北京）模型必须使用北京地域 API Key 和对应 WorkspaceId；新加坡/美国地域同理；  
- `qwen-deep-research` 仅支持华北2（北京）地域，其他地域调用将失败。

### 调用模式
- **非流式**：适用于结果确定性高、长度可控的场景（如 OCR 提取、意图单标签输出）；  
- **流式**（`stream=True`）：必需用于 `farui-plus` 多轮对话、`qwen-deep-research` 全流程、`gui-plus-*` 多步操作，响应中需解析 `phase` 字段（如 `"phase": "answer"`）判断当前阶段；  
- **特殊响应解析**：`tongyi-intent-detect-v3` 返回 `<tags>...</tags>` 和 `<tool_call>...<tool_call>` 包裹的 JSON，需用正则提取（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 示例）。

## 限制和注意事项

- **限流策略**：所有模型均受百炼平台统一限流控制，具体配额请参阅 [限流](https://help.aliyun.com/zh/model-studio/rate-limit)；`tongyi-intent-detect-v3` 提供 100 万 [Token](../concepts/token.md) 免费额度（开通后 90 天有效）；  
- **输入长度约束**：`farui-plus` 最大输入 12k Token，`tongyi-intent-detect-v3` 为 8,192 Token，超长输入将被截断或报错；  
- **地域隔离**：`qwen-deep-research` 仅在北京地域可用；`qwen-mt-plus` 在北京/新加坡/美国三地部署，但各地区 API Key 不互通；  
- **SDK 版本要求**：`farui-plus` Java SDK 需 ≥ 2.12.0；OpenAI SDK 需 v18+（Node.js）；  
- **安全实践**：DashScope Java SDK 中 `Generation` 对象非线程安全，多线程场景需自行管理同步或复用实例（见 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) 说明）；  
- **图像处理**：OCR 和 GUI 模型对输入图像尺寸敏感，务必设置 `min_pixels`/`max_pixels` 防止失真或超限；未设置时可能触发默认降级策略导致识别率下降。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)


