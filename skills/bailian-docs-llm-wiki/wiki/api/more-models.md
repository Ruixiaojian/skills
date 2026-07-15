# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，覆盖法律、翻译、意图理解、深度研究、OCR和GUI自动化等能力。这些模型基于通义千问基座，通过领域精调、RAG增强、多模态融合或工具调用机制实现专业任务优化。开发者可通过DashScope SDK或OpenAI兼容接口调用，需注意地域、域名及参数配置差异。

## 支持的模型/功能

| 模型名称 | 用途 | 输入类型 | 关键特性 | 文档引用 |
|----------|------|----------|----------|----------|
| `farui-plus` | 法律行业问答、文书生成、合同审查 | 文本 | RAG检索增强、法律Agent、司法专属小模型 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `qwen-mt-plus` | 高质量机器翻译 | 文本 | 支持术语干预、翻译记忆（TM）、领域提示 | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `tongyi-intent-detect-v3` | 意图识别与[函数调用](../concepts/function-calling.md)决策 | 文本 | 双模式输出：`INTENT_MODE`（含工具调用）或纯标签分类；支持简写单Token响应 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-deep-research` | 多阶段深度研究（规划→搜索→报告生成） | 文本 | 仅支持华北2（北京）地域；必须分两步调用（反问确认 + 深入研究）；支持`model_detailed_report`/`model_summary_report`输出格式 | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `qwen3.5-ocr` | 图像文字提取与结构化解析 | 图文混合（image_url + text） | 支持自定义Prompt、min/max_pixels图像缩放控制、[流式输出](../concepts/streaming-output.md) | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `gui-plus-2026-02-26` | GUI界面自动化操作 | 图文混合（image_url + text） | 基于工具调用（`computer_use`），需严格遵循Action + `<tool>`响应格式；支持高分辨率图像处理 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |

> **注意**：文档4明确指出`qwen-deep-research`“仅支持华北2（北京）地域”，而文档2、3、5中均提及新加坡/美国地域的兼容接口配置。若在非北京地域调用该模型将失败，此为硬性限制而非配置问题。

## 关键参数

- **`model`**（必选）：模型标识符，如`farui-plus`、`qwen-mt-plus`等，大小写敏感。
- **`messages`**（必选）：对话消息数组，每项含`role`（`user`/`system`/`assistant`）和`content`。OCR与GUI模型支持图文混合`content`（含`image_url`和`text`子项）。
- **`result_format` / `output_format`**：
  - DashScope SDK通用参数：`result_format='message'`（推荐）或`'text'`；
  - `qwen-deep-research`特有：`output_format`可选`model_detailed_report`（默认，~6000 Token）或`model_summary_report`（~1500–2000 Token）。
- **`stream`**（可选）：启用[流式输出](../concepts/streaming-output.md)（`True`/`true`），适用于长文本生成或实时反馈场景。
- **领域扩展参数**：
  - `qwen-mt-plus`：`translation_options`对象，含`source_lang`、`target_lang`、`terms`（术语表）、`tm_list`（翻译记忆）；
  - `qwen3.5-ocr`：`image_url`子项支持`min_pixels`/`max_pixels`控制图像预处理；
  - `gui-plus-2026-02-26`：`extra_body={"vl_high_resolution_images": True}`启用高分辨率图像支持。

## 使用方式

### 基础调用流程
1. **环境准备**：安装SDK（[DashScope](https://help.aliyun.com/zh/model-studio/install-sdk) 或 [OpenAI](https://help.aliyun.com/zh/model-studio/install-sdk)），获取并配置API Key至环境变量`DASHSCOPE_API_KEY`；
2. **域名配置**：强烈建议使用业务空间专属域名（如`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），详见各文档中的迁移提示；
3. **构造请求**：按模型要求组织`messages`，设置必要参数；
4. **发起调用**：使用SDK方法（如`dashscope.Generation.call()`或`client.chat.completions.create()`）。

### 典型调用示例
- **法律文书生成（farui-plus）**：  
  ```python
  response = dashscope.Generation.call(
      model="farui-plus",
      messages=[{"role": "user", "content": "我哥欠我10000块钱，给我生成起诉书。"}],
      result_format='message'
  )
  ```
- **翻译+术语干预（qwen-mt-plus）**：  
  ```python
  completion = client.chat.completions.create(
      model="qwen-mt-plus",
      messages=[{"role": "user", "content": "生物传感器"}],
      extra_body={"translation_options": {"source_lang": "Chinese", "target_lang": "English", "terms": [{"source": "生物传感器", "target": "biological sensor"}]}}
  )
  ```
- **OCR结构化提取（qwen3.5-ocr）**：  
  ```python
  completion = client.chat.completions.create(
      model="qwen3.5-ocr",
      messages=[{
          "role": "user",
          "content": [
              {"type": "image_url", "image_url": {"url": "https://..."}},
              {"type": "text", "text": "提取发票号码、金额、日期"}
          ]
      }]
  )
  ```

## 限制和注意事项

- **地域限制**：`qwen-deep-research`仅支持华北2（北京）地域，其他模型虽支持多地域，但需匹配对应API Key和`base_url`（如新加坡地域Key不可用于北京域名）；
- **限流策略**：所有模型受百炼平台统一限流控制，详情见[限流文档](https://help.aliyun.com/zh/model-studio/rate-limit)；
- **成本与免费额度**：`tongyi-intent-detect-v3`提供90天内100万Token免费额度，其余模型按输入/输出Token计费（如`farui-plus`输入20元/百万Token）；
- **SDK兼容性**：`qwen-deep-research`当前**仅支持Python DashScope SDK**，不支持Java SDK或OpenAI兼容接口 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)；
- **安全实践**：API Key务必配置至环境变量，避免硬编码；Java SDK中`Generation`对象非线程安全，需自行管理同步 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)；
- **响应解析**：`tongyi-intent-detect-v3`返回内容含XML标记（如`<tags>`、<tool_call>），需用正则解析提取工具调用JSON [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


