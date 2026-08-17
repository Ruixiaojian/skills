# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖法律、意图理解、机器翻译、深度研究、OCR图文识别及GUI自动化等能力。这些模型均基于通义千问系列基座模型优化，支持通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，适用于需要高精度、低延迟或领域强约束的生产级任务。

## 支持的模型/功能

| 模型名称 | 主要能力 | 适用场景 | 文档引用 |
|----------|----------|----------|----------|
| `farui-plus` | 法律问答、文书生成、案情分析、合同审查、RAG检索增强 | 法律咨询、司法辅助、律所SaaS | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 百毫秒级意图识别与工具调用决策（支持 `INTENT_MODE`） | 智能客服、语音助手、多跳任务编排 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-mt-plus` | 高保真机器翻译，支持术语干预、翻译记忆、领域提示 | 技术文档本地化、多语种内容运营 | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `qwen-deep-research` | 多阶段深度研究（反问确认 → 网络搜索 → 报告生成），含引用溯源 | 行业分析、竞品调研、学术预研 | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `qwen3.5-ocr` | 图文混合输入下的结构化文本提取（支持自定义Prompt与图像缩放控制） | 车票/发票/证件识别、表单自动化 | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `gui-plus-2026-02-26` | 基于截图的GUI操作自动化（鼠标/键盘/等待/终止等15类动作） | 桌面应用RPA、无障碍交互、UI测试 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |

> **注意**：`qwen-deep-research` 明确声明**仅支持华北2（北京）地域且仅限 Python DashScope SDK**，不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)；而其他多数模型（如 `qwen-mt-plus`、`qwen3.5-ocr`、`gui-plus-2026-02-26`）均明确支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)。开发者在选型时需严格遵循该限制。

## 关键参数

所有模型共性关键参数如下（具体取值见各模型文档）：

- **`model`**：必填字符串，模型标识符（如 `"farui-plus"`、`"qwen-deep-research"`）。
- **`messages`**：必填数组，按对话顺序组织的 message 列表，每个 message 含 `role`（`user`/`system`/`assistant`）与 `content`（纯文本或含 `image_url` 的多模态内容）。
- **`result_format` / `response_format`**：指定输出格式，常见值为 `"message"`（返回结构化 message 对象）。
- **`stream`**：布尔值，启用流式响应（默认 `False`），配合 `incremental_output=True`（Python）或 `streamCall()`（Java）使用。
- **模型特有参数**：
  - `tongyi-intent-detect-v3`：依赖 `system` message 中显式声明 `Response in INTENT_MODE.` 或意图列表格式；
  - `qwen-mt-plus`：通过 `extra_body.translation_options` 传入 `source_lang`、`target_lang`、`terms`、`tm_list`；
  - `qwen3.5-ocr`：`content` 中 `image_url` 对象支持 `min_pixels`/`max_pixels` 控制图像分辨率；
  - `gui-plus-2026-02-26`：需在 `extra_body` 中设置 `vl_high_resolution_images: true` 以启用高分辨率截图处理。

## 使用方式

### 通用前提
- 已开通百炼服务并获取对应地域的 [API Key](https://help.aliyun.com/zh/model-studio/get-api-key)；
- 强烈建议将 API Key 配置至环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄露；
- **必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低 —— 此要求在 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)、[Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)、[Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 和 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) 中均被强调。

### SDK 调用示例（Python）
```python
import os
import dashscope
# 设置专属域名（以北京地域为例）
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

# 法律文书生成（farui-plus）
response = dashscope.Generation.call(
    model="farui-plus",
    messages=[{"role": "user", "content": "我哥欠我10000块钱，给我生成起诉书。"}],
    result_format="message"
)

# 意图识别（tongyi-intent-detect-v3）
system_prompt = "You are Qwen... Response in INTENT_MODE."
response = dashscope.Generation.call(
    model="tongyi-intent-detect-v3",
    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": "杭州天气"}],
    result_format="message"
)
```

### OpenAI 兼容接口（Python）
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 注意路径后缀
)

# OCR 提取（qwen3.5-ocr）
completion = client.chat.completions.create(
    model="qwen3.5-ocr",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": "https://..."}},
            {"type": "text", "text": "请提取车票中的发票号码、起始站..."}
        ]
    }]
)
```

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，调用时必须使用该地域的 API Key 与专属域名；其他模型（如 `qwen-mt-plus`、`qwen3.5-ocr`）支持北京、新加坡、美国（弗吉尼亚）三地，但需匹配对应地域的 API Key 与 `base_url`。
- **SDK 支持差异**：`qwen-deep-research` 明确不支持 Java SDK 与 OpenAI 兼容接口；`farui-plus`、`tongyi-intent-detect-v3`、`qwen-mt-plus`、`qwen3.5-ocr`、`gui-plus-2026-02-26` 均同时支持 DashScope SDK 与 OpenAI 兼容接口。
- **流式响应兼容性**：`qwen-deep-research` 必须启用 `stream=True` 以完成两阶段交互（反问 → 研究）；`farui-plus` 支持 `stream=True` + `incremental_output=True`；`qwen3.5-ocr` 与 `gui-plus-2026-02-26` 的 OpenAI 兼容接口需设置 `stream=True` 与 `stream_options={"include_usage": True}`。
- **成本与限流**：各模型计费标准（输入/输出 [Token](../concepts/token.md) 单价）及限流策略详见对应文档，例如 `farui-plus` 输入成本为 20 元/百万 [Token](../concepts/token.md)，限流规则参见 [限流](https://help.aliyun.com/zh/model-studio/rate-limit) —— 此信息在 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) 中明确列出。
- **安全实践**：所有文档均强调将 API Key 配置至环境变量而非代码内硬编码，此为强制安全要求，不可忽略。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


