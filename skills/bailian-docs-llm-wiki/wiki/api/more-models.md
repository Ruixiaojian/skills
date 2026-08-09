# [more](more.md) models

百炼平台提供一系列面向特定任务的专用模型，覆盖法律、意图理解、机器翻译、深度研究、OCR 和 GUI 自动化等场景。这些模型在通用大模型基础上进行了领域精调或架构优化，具备更强的专业能力与推理效率。开发者可通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，支持流式/非[流式输出](../concepts/streaming-output.md)、多轮对话及结构化参数控制。

## 支持的模型与功能

| 模型名称 | 用途 | 关键能力 | 文档引用 |
|----------|------|----------|----------|
| `farui-plus` | 法律行业大模型 | 回答法律问题、生成文书、审查合同、案情分析、RAG检索增强、法律Agent [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 意图理解 | 百毫秒级意图识别、[函数调用](../concepts/function-calling.md)解析（INTENT_MODE）、单标签分类（含简写优化） | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-mt-plus` | 机器翻译 | 多语言互译、术语干预、翻译记忆（TM）、领域提示 | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `qwen-deep-research` | 深度研究 | 两阶段工作流（反问确认 → 网络搜索 → 报告生成）、自动引用来源、支持 `model_detailed_report` / `model_summary_report` 输出格式 | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `qwen3.5-ocr` | 图像文字提取 | 多格式图像 OCR、结构化 Prompt 提取（如车票字段）、支持 `min_pixels`/`max_pixels` 图像预处理 | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `gui-plus-2026-02-26` | GUI 自动化 | 基于截图的桌面操作（点击、输入、滚动、等待），需配合 `<tools>` 系统提示与 `<tool_call>` 格式化响应 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |

> **注意**：文档 4 明确指出 `qwen-deep-research` “仅支持华北2（北京）地域”且“暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)”，而文档 2 和文档 3 均推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），但未声明地域限制。实际调用时请以文档 4 的约束为准，避免在非北京地域或通过 OpenAI 接口调用该模型。

## 关键参数

所有模型均支持以下通用参数（部分模型有扩展）：

- **`model`**（必填）：模型标识符，如 `"farui-plus"`、`"qwen-mt-plus"`。
- **`messages`**（必填）：对话消息数组，每项含 `role`（`user`/`system`/`assistant`）和 `content`；OCR 与 GUI 模型支持 `content` 为图像 URL 数组（含 `image_url` + `text`）。
- **`result_format` / `response_format`**：指定返回格式，常用 `"message"`（结构化输出）。
- **`stream`**（可选，布尔值）：启用[流式输出](../concepts/streaming-output.md)，需配合 `incremental_output=True`（Python）或 `streamCall()`（Java）。
- **`extra_body`**（[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)）：传递模型特有参数，例如：
  - `qwen-mt-plus`：`{"translation_options": {"source_lang": "...", "target_lang": "...", "terms": [...], "tm_list": [...]}}`
  - `gui-plus-*`：`{"vl_high_resolution_images": true}`
- **`output_format`**（仅 `qwen-deep-research`）：取值 `"model_detailed_report"`（默认，~6000 [Token](../concepts/token.md)）或 `"model_summary_report"`（~1500–2000 [Token](../concepts/token.md)）。

## 使用方式

### 1. 环境准备
- 获取并配置 API Key 到环境变量 `DASHSCOPE_API_KEY`（[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）。
- 安装 SDK：Python（`pip install dashscope`）或 Java（[SDK 版本 ≥ 2.12.0](https://help.aliyun.com/zh/model-studio/install-sdk)）。
- **强制要求**：华北2（北京）或新加坡地域用户必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 和 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) 中的迁移说明。

### 2. 调用示例（核心模式）
- **单轮对话**（如法睿生成起诉书）：
  ```python
  from dashscope import Generation
  response = Generation.call(
      model="farui-plus",
      messages=[{"role": "user", "content": "我哥欠我10000块钱，给我生成起诉书。"}],
      result_format="message"
  )
  ```
- **多轮对话**（需维护 `messages` 列表并追加历史）：
  ```python
  messages.append({"role": "assistant", "content": response.output.choices[0].message.content})
  messages.append({"role": "user", "content": "如果借款利率是4%，再重新生成一份起诉书"})
  # 再次调用 Generation.call(...)
  ```
- **[流式输出](../concepts/streaming-output.md)**（适用于长文本生成或实时 UI 反馈）：
  ```python
  responses = Generation.call(model="qwen-deep-research", messages=..., stream=True)
  for r in responses:
      if r.output and r.output.choices:
          print(r.output.choices[0].message.content, end="", flush=True)
  ```

### 3. 领域专用调用
- **意图识别**：System Message 必须包含 `Response in INTENT_MODE.`（[函数调用](../concepts/function-calling.md)）或 `just reply with the chosen tag.`（单标签分类）。
- **OCR 提取**：`messages` 中 `content` 为图像 URL + 提取指令，支持 `min_pixels`/`max_pixels` 控制图像分辨率。
- **GUI 自动化**：System Message 需完整定义 `<tools>` 和 `<tool_call>` 响应格式，`extra_body={"vl_high_resolution_images": true}` 启用高分辨率截图解析。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他模型虽未明文限制，但推荐优先使用业务空间专属域名以保障性能与稳定性。
- **SDK 兼容性**：`qwen-deep-research` 不支持 Java SDK 和 OpenAI 兼容接口，仅限 Python DashScope SDK；其余模型均支持 Python/Java SDK 及 OpenAI 兼容调用。
- **[Token](../concepts/token.md) 成本与限流**：各模型成本差异显著（如 `farui-plus` 输入 20元/百万 Token，`tongyi-intent-detect-v3` 输入仅 0.4元/百万 Token），具体见 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) 与 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。全局限流策略参见 [限流文档](https://help.aliyun.com/zh/model-studio/rate-limit)。
- **图像处理参数**：OCR 模型对输入图像有像素阈值要求（`min_pixels`/`max_pixels`），超出范围将自动缩放，影响识别精度。
- **安全实践**：API Key 务必配置到环境变量，禁止硬编码；DashScope Java SDK 中 `Generation` 对象非线程安全，需复用或加锁管理。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


