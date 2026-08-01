# [more](more.md) models

百炼平台提供一系列面向特定场景的专用大模型，覆盖法律、意图理解、深度研究、机器翻译、OCR识别和GUI自动化等方向。这些模型在基础语言能力之上，通过领域精调、多模态融合或工具增强等方式，显著提升垂直任务效果。开发者可根据业务需求选择对应模型，并遵循统一的API调用规范。

## 支持的模型与功能

| 模型名称 | 用途 | 关键特性 | 文档引用 |
|----------|------|----------|----------|
| `farui-plus` | 法律行业问答与文书生成 | RAG检索增强、法律Agent、司法专属小模型支持 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 用户意图识别与工具路由 | 百毫秒级响应，支持`INTENT_MODE`输出结构化工具调用指令或纯标签分类 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-deep-research` | 多阶段深度研究分析 | 自动反问澄清、网络搜索、引用溯源，支持`model_detailed_report`/`model_summary_report`输出格式 | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `qwen-mt-plus` | 高质量机器翻译 | 支持术语干预、翻译记忆（TM）、领域提示，覆盖中英等多语种 | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `qwen3.5-ocr` | 多场景文字识别与结构化提取 | 支持图像输入（含`min_pixels`/`max_pixels`缩放控制）、Prompt引导的JSON结构化输出 | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `gui-plus-2026-02-26` | GUI界面自动化操作 | 基于截图理解执行鼠标键盘动作，支持`computer_use`工具调用及高分辨率图像处理 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |

> **注意**：文档 4 和文档 5 中对“美国（弗吉尼亚）地域”的 base_url 描述存在重复（两次列出），且文档 4 的“新加坡地域”也重复出现两次；实际应以各文档末尾“重要”区块的迁移建议为准，即仅华北2（北京）和新加坡地域支持业务空间专属域名，弗吉尼亚地域仍使用 `https://dashscope-us.aliyuncs.com`。

## 关键参数

- **`model`**（必选）：字符串，指定模型名称（如 `"farui-plus"`、`"qwen3.5-ocr"`），不同模型不兼容。
- **`messages`**（必选）：消息数组，按对话顺序排列。`role` 必须为 `"user"` 或 `"system"`（部分模型如 `qwen-deep-research` 不支持 `"assistant"` 角色输入，仅在第二步调用时作为历史上下文传入）。
- **`result_format` / `output_format`**（可选）：控制响应结构。`farui-plus` 使用 `result_format='message'`；`qwen-deep-research` 使用 `output_format` 指定报告详略程度（默认 `model_detailed_report`）。
- **`stream`**（可选）：布尔值，启用[流式输出](../concepts/streaming-output.md)（如 `qwen-deep-research`、`qwen3.5-ocr`）。需配合 `stream_options={"include_usage": true}` 获取 Token 统计。
- **模型特有参数**：
  - `qwen-mt-plus`：通过 `extra_body={"translation_options": {...}}` 传递 `source_lang`、`target_lang`、`terms`（术语表）、`tm_list`（翻译记忆）。
  - `qwen3.5-ocr`：`content` 中图像项支持 `min_pixels` 和 `max_pixels` 控制分辨率。
  - `gui-plus-*`：需通过 `extra_body={"vl_high_resolution_images": true}` 启用高分辨率图像处理。

## 使用方式

1. **环境准备**：获取 API Key 并配置至环境变量 `DASHSCOPE_API_KEY`；安装对应 SDK（[DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk) 或 [OpenAI SDK](https://help.aliyun.com/zh/model-studio/install-sdk)）。
2. **域名配置**：强烈建议使用业务空间专属域名提升稳定性与性能：
   - 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
   - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
   （`{WorkspaceId}` 在百炼控制台业务空间详情页获取）
3. **调用示例**：
   - **通用 SDK 调用**（如 `farui-plus`, `tongyi-intent-detect-v3`）：
     ```python
     from dashscope import Generation
     response = Generation.call(
         model="farui-plus",
         messages=[{"role": "user", "content": "生成起诉书"}],
         result_format="message"
     )
     ```
   - **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**（如 `qwen-mt-plus`, `qwen3.5-ocr`）：
     ```python
     from openai import OpenAI
     client = OpenAI(
         api_key=os.getenv("DASHSCOPE_API_KEY"),
         base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
     )
     completion = client.chat.completions.create(
         model="qwen-mt-plus",
         messages=[{"role": "user", "content": "我看到这个视频后没有笑"}],
         extra_body={"translation_options": {"source_lang": "Chinese", "target_lang": "English"}}
     )
     ```
   - **多阶段流程**（如 `qwen-deep-research`）：必须分两步调用——先发起研究请求获取反问，再将反问+用户回答组合为新 `messages` 发起第二步调用。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；其他模型（如 `qwen-mt-plus`, `qwen3.5-ocr`, `gui-plus-*`）在多个地域可用，但需匹配对应地域的 API Key 和 base_url。
- **SDK 支持差异**：`qwen-deep-research` 当前**仅支持 Python DashScope SDK**，不支持 Java SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **限流策略**：所有模型均受百炼平台统一限流控制，具体配额请参见 [限流文档](https://help.aliyun.com/zh/model-studio/rate-limit)。
- **安全实践**：务必通过环境变量配置 API Key，避免硬编码；Java SDK 中 `Generation` 对象非线程安全，需自行管理同步机制 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。
- **响应解析**：`tongyi-intent-detect-v3` 的 `INTENT_MODE` 输出需用正则解析 `<tags>`、<tool_call>、`<content>` 三段式结构；`qwen-deep-research` 流式响应中 `phase` 字段标识当前处理阶段（如 `"ResearchPlanning"`、`"answer"`），需据此判断是否完成 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


