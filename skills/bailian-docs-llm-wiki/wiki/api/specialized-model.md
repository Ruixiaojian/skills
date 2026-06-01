# specialized model

百炼平台提供多个专用模型（Specialized Model），分别面向机器翻译、深度研究、文字提取（OCR）和界面交互自动化等垂直场景。这些模型通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope API 调用，各模型的接口协议和参数有所差异。本文汇总各专用模型的核心能力、关键参数与使用注意事项。

## 支持的模型

| 模型 | 用途 | 支持的接口 | 多地域部署 |
|------|------|-----------|-----------|
| `qwen-mt-plus` / `qwen-mt-turbo` | 机器翻译（含术语干预、翻译记忆、领域提示） | OpenAI 兼容、DashScope | 北京、新加坡、弗吉尼亚 |
| `qwen-deep-research` | 深度研究（自动搜索、规划、生成研究报告） | 仅 Python DashScope SDK | 仅北京（中国大陆版） |
| `qwen-vl-ocr-latest` | 图像文字提取 | OpenAI 兼容、DashScope | 北京、新加坡、弗吉尼亚 |
| `gui-plus-2026-02-26` | GUI 界面交互自动化（鼠标/键盘操作） | OpenAI 兼容、DashScope | 北京 |

> **注意**：Qwen-Deep-Research 当前**仅支持 Python DashScope SDK**，不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，这与其他专用模型不同。详见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/specialized-model/qwen-deep-research-api.md)。

## 关键参数与功能

### Qwen-MT（机器翻译）

通过 `translation_options` 参数控制翻译行为，主要字段包括：

- **`source_lang`** / **`target_lang`**：源语言与目标语言，`source_lang` 支持设为 `"auto"` 自动检测。
- **`terms`**：术语干预列表，每项包含 `source`（原文术语）和 `target`（译文术语），用于强制统一专业术语翻译。
- **`tm_list`**：翻译记忆列表，提供类似句对作为参考，帮助模型保持风格一致。
- **`domains`**：领域提示，以自然语言描述翻译领域和风格要求。

使用 OpenAI SDK 时，`translation_options` 通过 `extra_body` 传入。详细用法参见 [Qwen-MT API 参考](../../raw/model-api-reference/specialized-model/qwen-mt-api.md)。

### Qwen-Deep-Research（深度研究）

采用**两阶段调用**流程：

1. **反问确认**：发送初始研究主题，模型返回澄清式问题。
2. **深入研究**：将第一步的 assistant 回复和用户的补充说明一起发送，模型执行搜索并生成报告。

关键参数：
- **`output_format`**：报告格式。`model_detailed_report`（默认，约 6000 Token）或 `model_summary_report`（约 1500-2000 Token）。

响应中的 `phase` 字段标识当前阶段：`ResearchPlanning`、`WebResearch`、`KeepAlive`、`answer`。

### Qwen-OCR（文字提取）

通过多模态消息格式传入图像和提取指令：

- **`image_url`**：图片 URL 或 Base64 编码。
- **`min_pixels`** / **`max_pixels`**：控制图像分辨率缩放阈值（如 `min_pixels: 3072`，`max_pixels: 8388608`）。
- **`text`**（可选）：自定义提取 Prompt。未传入时使用默认 Prompt：`Please output only the text content from the image without any additional descriptions or formatting.`

支持流式与非[流式输出](../concepts/streaming.md)。详细参数参见 [Qwen-OCR API参考](../../raw/model-api-reference/specialized-model/qwen-vl-ocr-api-reference.md)。

### GUI-Plus（界面交互）

通过 `computer_use` 工具函数实现 GUI 自动化，支持的操作包括：

- 鼠标操作：`left_click`、`right_click`、`double_click`、`mouse_move`、`scroll` 等
- 键盘操作：`key`（组合键）、`type`（输入文本）
- 流程控制：`wait`、`terminate`、`answer`

需要在 `system` 消息中配置工具定义（function schema），并通过 `extra_body` 传入 `vl_high_resolution_images: true` 以启用高分辨率图像处理。屏幕分辨率默认为 1000×1000。

## 使用方式

### 接口端点

各模型（Qwen-Deep-Research 除外）均支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，端点按地域区分：

| 地域 | base_url |
|------|----------|
| 北京 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` |
| 弗吉尼亚 | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |

Qwen-Deep-Research 使用 DashScope 原生端点：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`。

### 认证

所有模型均需通过 API Key 认证。不同地域的 API Key 不通用，需在对应地域的控制台获取。

### 快速示例（Python，Qwen-MT）

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen-mt-plus",
    messages=[{"role": "user", "content": "我看到这个视频后没有笑"}],
    extra_body={
        "translation_options": {
            "source_lang": "Chinese",
            "target_lang": "English"
        }
    }
)
print(completion.choices[0].message.content)
```

## 限制和注意事项

- **地域限制**：Qwen-Deep-Research 仅在中国大陆版（北京）可用，必须使用北京地域的 API Key。
- **SDK 限制**：Qwen-Deep-Research 仅支持 Python DashScope SDK，暂不支持 Java SDK 和 OpenAI 兼容接口。
- **API Key 隔离**：北京、新加坡、弗吉尼亚各地域的 API Key 不互通，调用时需确保 `base_url` 与 API Key 匹配。
- **[流式输出](../concepts/streaming.md)**：Qwen-Deep-Research 的响应始终为流式；Qwen-OCR 和 GUI-Plus 支持通过 `stream` 参数切换。
- **图像输入**：Qwen-OCR 和 GUI-Plus 均为多模态模型，需在 `messages` 中以 `image_url` 类型传入图片。
- **Qwen-OCR 默认行为**：如未传入自定义 `text` Prompt，模型会使用英文默认 Prompt 提取图像中的全部文本。

## 来源文档

- [Qwen-MT API 参考](../../raw/model-api-reference/specialized-model/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/specialized-model/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/specialized-model/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/specialized-model/gui-plus-interface-interaction-model.md)

