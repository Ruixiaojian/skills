# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖法律、意图理解、机器翻译、OCR、深度研究和GUI自动化等能力。这些模型均基于通义千问系列基座模型优化，支持通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，适用于对领域精度、响应结构或多模态交互有明确要求的生产场景。所有模型均需配置业务空间专属域名以获得最佳性能与稳定性。

## 支持的模型/功能

当前 `more models` 类别下已开放以下专用模型：

- **通义法睿（`farui-plus`）**：法律行业大模型，支持法律咨询、文书生成、案情分析、合同审查等，基于千问基座经法律数据精调与RAG增强 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)  
- **意图理解模型（`tongyi-intent-detect-v3`）**：毫秒级意图识别，支持双模式输出——结构化[函数调用](../concepts/function-calling.md)（`INTENT_MODE`）或单标签分类（如 `alarm_set`），适用于智能助手路由与工具编排 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)  
- **Qwen-MT（`qwen-mt-plus`）**：专业机器翻译模型，支持术语干预、翻译记忆（TM）、领域提示，可指定源/目标语种并保持技术文档一致性 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)  
- **Qwen-OCR（`qwen3.5-ocr`）**：多场景文字提取模型，支持图像输入（含 URL 或 base64）、自定义 Prompt 提取结构化字段（如车票信息），兼容 OpenAI 多模态消息格式 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)  
- **Qwen-Deep-Research（`qwen-deep-research`）**：支持两阶段深度研究流程（反问确认 → 网络搜索 → 报告生成），输出含引用来源的详尽报告，**仅支持华北2（北京）地域及 Python DashScope SDK** [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)  
- **GUI-Plus（`gui-plus-2026-02-26`）**：界面自动化模型，接收桌面截图与指令，输出鼠标/键盘操作指令（如 `left_click`, `type`），用于 RPA 场景 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)  

> **注意**：文档 3 和文档 4 均重复强调“北京/新加坡地域建议迁移至业务空间专属域名”，但文档 5 明确指出 `qwen-deep-research` **仅支持华北2（北京）地域**，且不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)；而文档 6 的 GUI-Plus 示例中未声明地域限制，但其 base_url 仅给出北京地域配置，实际使用需以控制台支持列表为准。

## 关键参数

| 参数 | 说明 | 示例值 | 是否必选 |
|------|------|--------|----------|
| `model` | 模型唯一标识符 | `"farui-plus"`, `"tongyi-intent-detect-v3"` | 是 |
| `messages` | 对话历史数组，每项含 `role`（`user`/`system`/`assistant`）和 `content` | `[{"role":"user","content":"生成起诉书"}]` | 是 |
| `result_format` / `response_format` | 输出格式，`"message"` 为标准结构化输出 | `"message"`（DashScope）、`"json_object"`（部分模型） | 否（默认 `"message"`） |
| `stream` | 启用流式响应（逐 token 返回） | `True` | 否 |
| `translation_options` | Qwen-MT 特有：`source_lang`, `target_lang`, `terms`, `tm_list` | `{"source_lang":"Chinese","target_lang":"English"}` | Qwen-MT 必选 |
| `extra_body` | [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)扩展字段，承载模型特有参数 | `{"vl_high_resolution_images": true}`（GUI-Plus）、`{"translation_options": {...}}`（Qwen-MT） | 按模型需求 |
| `output_format` | Qwen-Deep-Research 特有：`"model_detailed_report"` 或 `"model_summary_report"` | `"model_summary_report"` | 否 |

## 使用方式

### 1. 域名与认证
- **必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)  
- API Key 需通过环境变量 `DASHSCOPE_API_KEY` 配置，避免硬编码泄露 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)  

### 2. SDK 调用示例（通用流程）
```python
from dashscope import Generation
import os

# 设置专属域名（北京地域）
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

response = Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="farui-plus",  # 替换为目标模型
    messages=[{"role": "user", "content": "我哥欠我10000块钱，给我生成起诉书。"}],
    result_format="message"
)
print(response.output.choices[0].message.content)
```

### 3. OpenAI 兼容接口（推荐用于多模态/扩展参数）
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 注意路径为 /compatible-mode/v1
)

# Qwen-OCR：传入图像 + text prompt
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
```

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，且**不支持 Java SDK 与 OpenAI 兼容接口**，仅限 Python DashScope SDK [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)  
- **流式响应差异**：DashScope SDK 中 `Generation.call(..., stream=True)` 返回迭代器；OpenAI SDK 中需设置 `stream=True` 并遍历 `response`，且 `stream_options={"include_usage": True}` 才返回 token 统计  
- **输入格式约束**：Qwen-OCR 和 GUI-Plus 要求 `messages[0].content` 为 list（含 `image_url` + `text`），不可为纯字符串；意图模型需严格按 `Response in INTENT_MODE.` 格式设置 system [prompt](../guides/prompt.md)  
- **成本与限流**：各模型按输入/输出 token 单独计费（如 `farui-plus` 输入 20元/百万 Token），具体见各模型文档；全局限流策略参见 [限流](https://help.aliyun.com/zh/model-studio/rate-limit)  
- **安全实践**：API Key 务必配置至环境变量，禁止写入代码或日志；Java SDK 中 `Generation` 对象非线程安全，需复用并管理同步 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


