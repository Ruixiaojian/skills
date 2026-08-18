# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖法律、意图理解、机器翻译、深度研究、OCR识别和GUI自动化等能力。这些模型均基于通义千问系列基座模型深度优化，支持通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，适用于对领域精度、响应结构或多模态交互有明确要求的生产场景。

## 支持的模型/功能

当前 `more models` 类别下已开放以下专用模型：

- **通义法睿（`farui-plus`）**：法律行业大模型，支持法律咨询、案情分析、文书生成、合同审查等，详见 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。
- **意图理解模型（`tongyi-intent-detect-v3`）**：毫秒级意图识别与工具调用决策，支持 `INTENT_MODE` 输出格式，适用于智能助手、对话路由等场景。
- **Qwen-MT（`qwen-mt-plus`）**：专业机器翻译模型，支持术语干预、翻译记忆（TM）、领域提示等高级功能，适用于技术文档、本地化等高保真翻译需求。
- **Qwen-Deep-Research（`qwen-deep-research`）**：支持两阶段交互式深度研究，自动规划、网络检索并生成带引用的研究报告，**仅支持华北2（北京）地域及 Python DashScope SDK**，详见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **Qwen-OCR（`qwen3.5-ocr`）**：多模态图文理解模型，支持图像中文字提取与结构化信息抽取（如车票、发票），兼容 OpenAI 多模态消息格式。
- **GUI-Plus（`gui-plus-2026-02-26`）**：界面交互专用模型，可解析桌面截图并生成鼠标/键盘操作指令，用于自动化 GUI 测试或远程桌面任务。

> **注意**：文档 3（Qwen-MT API参考）中重复列出了新加坡和美国地域的配置说明，且存在冗余段落；实际使用时请以各节标题下的唯一配置为准。文档 4 明确指出 Qwen-Deep-Research **不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)**，而文档 1 和文档 2 的示例代码中 Java SDK 调用方式与此矛盾，开发者应以文档 4 的限制为准。

## 关键参数

所有模型均遵循统一的核心参数规范，但部分模型支持扩展参数：

| 参数 | 类型 | 是否必选 | 说明 |
|------|------|----------|------|
| `model` | string | 是 | 模型标识符，如 `"farui-plus"`、`"qwen-deep-research"` 等 |
| `messages` | array | 是 | 对话消息列表，每条消息含 `role`（`user`/`system`/`assistant`）和 `content`；OCR 与 GUI-Plus 支持 `image_url` 类型内容 |
| `result_format` / `response_format` | string | 否 | 默认为 `"message"`；OCR 和 GUI-Plus 场景下通常无需显式设置 |
| `stream` | boolean | 否 | 启用[流式输出](../concepts/streaming-output.md)（如 `farui-plus`、`qwen-deep-research`） |
| `extra_body` | object | 否 | [OpenAI 兼容接口](../concepts/openai-compatible-api.md)专用，用于传递模型特有参数：<br>• `qwen-mt-plus`: `translation_options`（含 `source_lang`, `target_lang`, `terms`, `tm_list`）<br>• `gui-plus-2026-02-26`: `vl_high_resolution_images: true`<br>• `qwen3.5-ocr`: 无额外字段，图像缩放由 `min_pixels`/`max_pixels` 控制 |
| `output_format` | string | 否 | 仅 `qwen-deep-research` 支持：`"model_detailed_report"`（默认）或 `"model_summary_report"` |

## 使用方式

### 基础调用流程
1. **获取并配置 API Key**：在百炼控制台开通服务后[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，并**强烈建议配置至环境变量 `DASHSCOPE_API_KEY`** 以规避密钥泄露风险。
2. **选择接入方式**：
   - 推荐使用 **DashScope Python SDK**（v2.12.0+），覆盖全部模型；
   - OpenAI 兼容接口适用于 `qwen-mt-plus`、`qwen3.5-ocr`、`gui-plus-2026-02-26` 等模型，需正确设置 `base_url`。
3. **配置业务空间专属域名**：为获得最佳性能与稳定性，**必须**将请求地址迁移至业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 文档中的迁移指引。

### 示例：OCR 结构化提取（OpenAI 兼容）
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
completion = client.chat.completions.create(
    model="qwen3.5-ocr",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": "https://example.com/ticket.jpg"}},
            {"type": "text", "text": "提取发票号码、起始站、终点站...（JSON格式）"}
        ]
    }]
)
```

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；其他模型（如 `qwen-mt-plus`, `qwen3.5-ocr`）支持北京、新加坡、美国（弗吉尼亚）三地，但各区域 API Key 不互通。
- **SDK 限制**：`qwen-deep-research` **仅支持 Python DashScope SDK**，Java SDK 与 OpenAI 兼容接口调用将失败；其余模型均支持 Python/Java SDK 及 OpenAI 兼容方式。
- **[流式输出](../concepts/streaming-output.md)兼容性**：`farui-plus`、`qwen-deep-research`、`qwen3.5-ocr` 支持流式响应；`tongyi-intent-detect-v3` 和 `gui-plus-2026-02-26` 当前仅支持非[流式输出](../concepts/streaming-output.md)。
- **输入格式约束**：
  - OCR 模型要求 `messages[0].content` 为包含 `image_url` 和 `text` 的数组，不可仅传文本；
  - GUI-Plus 模型的 `system` message 必须严格包含 `<tools>` 定义与 `<tool_call>` 分隔符规则，否则无法解析操作指令。
- **限流与配额**：所有模型均受百炼平台通用限流策略约束，具体阈值参见 [限流文档](https://help.aliyun.com/zh/model-studio/rate-limit)；`tongyi-intent-detect-v3` 提供 90 天内 100 万 Token 免费额度。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


