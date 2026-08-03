# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖法律、意图理解、机器翻译、深度研究、OCR识别和GUI自动化等能力。这些模型均基于通义千问基座，通过领域数据精调与特定架构优化，支持高精度、低延迟的行业级推理任务。开发者可通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)快速集成。

## 支持的模型/功能

当前 `more models` 类别下已开放以下专用模型：

- **通义法睿（`farui-plus`）**：面向法律行业的多能力大模型，支持法律咨询、文书生成、案情分析、合同审查等 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。
- **意图理解模型（`tongyi-intent-detect-v3`）**：毫秒级意图识别与[工具调用](../concepts/tool-use.md)决策，支持 `INTENT_MODE` 输出结构化[函数调用](../concepts/function-calling.md)或纯标签分类 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **Qwen-MT（`qwen-mt-plus`）**：高质量机器翻译模型，支持术语干预、翻译记忆（TM）、领域提示等专业翻译能力 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)。
- **Qwen-Deep-Research（`qwen-deep-research`）**：支持两阶段交互式深度研究（反问确认 + 网络检索+报告生成），仅限华北2（北京）地域且**仅支持 Python DashScope SDK** [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **Qwen-OCR（`qwen3.5-ocr`）**：多模态OCR模型，支持图像输入与结构化文本提取（如车票、发票信息），兼容 OpenAI 多模态消息格式 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **GUI-Plus（`gui-plus-2026-02-26`）**：桌面GUI自动化模型，通过截图理解与动作指令（如点击、输入、等待）执行界面操作 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

> **注意**：文档 4 明确指出 Qwen-Deep-Research “**暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**”，而文档 1 中法睿模型的 Java SDK 示例仍有效；二者能力边界需严格区分，不可混用调用方式。

## 关键参数

所有模型共性参数如下（具体取值见各模型文档）：

| 参数 | 说明 | 示例/范围 |
|------|------|-----------|
| `model` | 模型唯一标识符 | `farui-plus`, `tongyi-intent-detect-v3`, `qwen-mt-plus` 等 |
| `messages` | 对话历史数组，含 `role`（`user`/`system`/`assistant`）与 `content` | 法睿要求 `system` 角色引导，意图模型需 `INTENT_MODE` 提示词 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `result_format` / `response_format` | 输出格式控制 | `message`（推荐）、`text`；OCR 和 GUI-Plus 依赖 OpenAI 多模态 `content` 数组结构 |
| `stream` | 是否启用[流式输出](../concepts/streaming-output.md) | `True`/`false`；法睿、Deep-Research、OCR 均支持 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `extra_body`（OpenAI） / 自定义参数（DashScope） | 模型特有扩展参数 | `translation_options`（Qwen-MT）、`vl_high_resolution_images`（GUI-Plus）、`output_format`（Deep-Research） |

> **注意**：Qwen-MT 的 `translation_options` 必须通过 `extra_body` 传入（OpenAI）或 `GenerationParam.builder().translationOptions(...)`（DashScope），直接置于 `messages` 中无效。

## 使用方式

### 1. 基础准备
- 获取并配置 API Key 到环境变量 `DASHSCOPE_API_KEY`（[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）；
- **强制使用业务空间专属域名**：华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`；旧域名 `dashscope.aliyuncs.com` 已不推荐 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。

### 2. SDK 调用示例（通用流程）
```python
import dashscope
# 设置地域专属 endpoint（必须！）
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

response = dashscope.Generation.call(
    model="farui-plus",  # 替换为目标模型
    messages=[{"role": "user", "content": "你的问题"}],
    result_format="message",
    stream=False
)
```

### 3. OpenAI 兼容调用（通用流程）
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 必须指定
)
response = client.chat.completions.create(
    model="qwen-mt-plus",
    messages=[{"role": "user", "content": "待翻译文本"}],
    extra_body={"translation_options": {"source_lang": "Chinese", "target_lang": "English"}}
)
```

### 4. 特殊能力调用要点
- **意图识别**：`system` 消息中必须包含 `Response in INTENT_MODE.` 或明确的标签列表指令；
- **Qwen-MT 术语干预**：在 `translation_options.terms` 中传入源-目标术语对；
- **Qwen-Deep-Research**：必须分两步调用（先反问、再深入），且 `output_format` 可选 `model_detailed_report` 或 `model_summary_report`；
- **OCR/GUI-Plus**：`messages[0].content` 必须为包含 `image_url` 和 `text` 的数组，不可单字符串。

## 限制和注意事项

- **地域限制**：Qwen-Deep-Research 仅支持华北2（北京）地域；Qwen-MT、OCR、GUI-Plus 在北京/新加坡/美国三地可用，但 API Key 需按地域分别申请。
- **SDK 限制**：Qwen-Deep-Research 不支持 Java SDK 和 OpenAI 接口，仅 Python DashScope SDK 可用；法睿模型 Java SDK 示例完整可用 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。
- **流式响应解析**：法睿、Deep-Research、OCR 的流式响应需按 `response.output.choices[0].message.content` 或 `chunk.choices[0].delta.content` 逐段拼接，不可直接 `json.loads()` 整体响应。
- **成本与限流**：`farui-plus` 输入/输出成本分别为 20元/百万 [Token](../concepts/token.md)；`tongyi-intent-detect-v3` 提供 100万 [Token](../concepts/token.md) 免费额度（90天有效期）；所有模型均受 [限流策略](https://help.aliyun.com/zh/model-studio/rate-limit) 约束。
- **图像处理参数**：OCR 和 GUI-Plus 支持 `min_pixels`/`max_pixels` 控制图像缩放，避免超分辨率导致失败。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


