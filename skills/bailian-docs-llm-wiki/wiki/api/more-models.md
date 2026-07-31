# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖法律、意图理解、OCR、深度研究、GUI自动化和机器翻译等能力。这些模型均基于通义千问系列基座模型优化，支持通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，适用于需要高精度、低延迟或领域适配的生产场景。

## 支持的模型与功能

| 模型名称 | 用途 | 关键特性 | 文档来源 |
|----------|------|-----------|-----------|
| `farui-plus` | 法律行业大模型 | 支持法律文书生成、案情分析、合同审查、RAG检索增强及司法专属小模型协同 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 意图识别与工具调用 | 百毫秒级响应，支持 `INTENT_MODE` 输出结构化工具调用指令，或纯标签式意图分类 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen3.5-ocr` | 多模态OCR | 支持图像输入（含 `min_pixels`/`max_pixels` 调优）、Prompt引导的结构化文本提取（如车票信息） | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `qwen-deep-research` | 深度研究分析 | 两阶段流程（反问确认 → 深入研究），自动执行网络搜索、引用溯源，输出详尽/摘要报告 | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `gui-plus-2026-02-26` | GUI自动化交互 | 基于截图理解与鼠标键盘操作模拟，需传入系统提示词定义 `computer_use` 工具规范 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |
| `qwen-mt-plus` | 专业机器翻译 | 支持术语干预（`terms`）、翻译记忆（`tm_list`）、领域提示，`source_lang` 可设为 `"auto"` | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |

> **注意**：文档 6 中重复列出了北京、新加坡、美国地域的配置说明（如“**新加坡地域**”标题出现两次，“**美国（弗吉尼亚）地域**”也重复），属冗余内容，实际使用时仅需按目标地域选择对应 `base_url` 即可。

## 关键参数

所有模型均需以下通用参数：
- `model`: 必选字符串，如 `"farui-plus"`、`"qwen-mt-plus"`；
- `messages`: 必选数组，按对话顺序组织 `role`（`system`/`user`/`assistant`）与 `content`；
- `result_format`（DashScope）或 `response_format`（OpenAI）：建议设为 `"message"` 以获取结构化输出。

模型特有参数：
- OCR 模型（`qwen3.5-ocr`）：`content` 中需包含 `image_url` 对象，并可指定 `min_pixels`/`max_pixels` 控制图像缩放；
- 意图识别模型（`tongyi-intent-detect-v3`）：`system` 消息必须显式声明 `Response in INTENT_MODE.`（工具调用）或 `just reply with the chosen tag.`（纯意图分类）；
- 翻译模型（`qwen-mt-plus`）：通过 `extra_body.translation_options` 传递 `source_lang`、`target_lang`、`terms`、`tm_list`；
- 深度研究模型（`qwen-deep-research`）：仅支持 Python DashScope SDK，且需两阶段调用（先反问、再深入），`output_format` 可选 `"model_detailed_report"` 或 `"model_summary_report"`；
- GUI 模型（`gui-plus-2026-02-26`）：需在 `system` 消息中完整定义 `<tools>` 和 `<tool_call>` 响应格式，并通过 `extra_body={"vl_high_resolution_images": True}` 启用高清图像处理。

## 使用方式

### 接口协议
- **推荐**：使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性更优；
- **兼容**：[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)路径为 `/compatible-mode/v1/chat/completions`；DashScope 原生接口路径为 `/api/v1/services/aigc/text-generation/generation`；
- 所有请求均需 `Authorization: Bearer <API_KEY>`，API Key 需按地域单独申请并配置到环境变量 `DASHSCOPE_API_KEY`。

### SDK 调用示例（Python）
```python
import os
from openai import OpenAI  # OpenAI 兼容
# 或 from dashscope import Generation  # DashScope 原生

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

# OCR 示例
completion = client.chat.completions.create(
    model="qwen3.5-ocr",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": "https://..."}},
            {"type": "text", "text": "提取发票号码和金额"}
        ]
    }]
)

# 翻译示例（带术语干预）
completion = client.chat.completions.create(
    model="qwen-mt-plus",
    messages=[{"role": "user", "content": "生物传感器"}],
    extra_body={
        "translation_options": {
            "source_lang": "Chinese",
            "target_lang": "English",
            "terms": [{"source": "生物传感器", "target": "biological sensor"}]
        }
    }
)
```

### [流式输出](../concepts/streaming-output.md)
- DashScope：设置 `stream=True`，遍历响应流；
- OpenAI：设置 `stream=True`，配合 `stream_options={"include_usage": True}` 获取 [Token](../concepts/token.md) 统计；
- 注意：`qwen-deep-research` 的流式响应包含多阶段 `phase` 字段（`ResearchPlanning`/`WebResearch`/`answer`），需解析 `output.message.phase` 判断当前状态。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他模型在多地域可用（详见各文档的 `base_url` 配置）；
- **SDK 限制**：`qwen-deep-research` 暂不支持 Java SDK 和 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，仅限 Python DashScope SDK [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)；
- **成本与限流**：`farui-plus` 输入成本为 20 元/百万 [Token](../concepts/token.md)，具体限流策略参见 [限流](https://help.aliyun.com/zh/model-studio/rate-limit)；`tongyi-intent-detect-v3` 提供 100 万 [Token](../concepts/token.md) 免费额度（开通后 90 天内）；
- **安全实践**：强烈建议将 API Key 配置至环境变量，避免硬编码；Java SDK 中 `Generation` 对象非线程安全，需复用并自行管理同步 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)；
- **图像处理**：OCR 和 GUI 模型对输入图像分辨率敏感，务必按文档要求设置 `min_pixels`/`max_pixels`，否则可能触发降级或失败；
- **响应解析**：意图识别模型返回特殊标记（如 `<tags>`/<tool_call>/`<content>`），需用正则或专用 `parse_text` 函数提取结构化结果 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)


