# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖法律、意图理解、机器翻译、深度研究、OCR 和 GUI 自动化等能力。这些模型均基于通义千问基座，通过领域精调、RAG 增强或工具链集成实现专业化输出，开发者可通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用。所有模型均需配置业务空间专属域名以获得最佳性能与稳定性。

## 支持的模型与功能

| 模型名称 | 用途 | 关键特性 | 文档引用 |
|----------|------|-----------|-----------|
| `farui-plus` | 法律行业大模型 | 支持法律文书生成、案情分析、合同审查、司法推理；支持单轮/多轮对话及[流式输出](../concepts/streaming-output.md) | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 意图识别与工具调用 | 支持 `INTENT_MODE`（输出结构化工具调用）和纯标签分类两种模式；可配置简短字母标签提升响应速度 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-mt-plus` | 专业机器翻译 | 支持术语干预、翻译记忆（TM）、领域提示；支持中英等多语种互译 | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `qwen-deep-research` | 深度研究分析 | 两阶段流程：先反问确认研究焦点，再执行网络搜索与报告生成；支持 `model_detailed_report` / `model_summary_report` 输出格式 | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `qwen3.5-ocr` | 多模态文字提取 | 支持图像输入（含 `min_pixels`/`max_pixels` 调整）、Prompt 引导结构化输出（如 JSON）；支持流式与非流式调用 | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `gui-plus-2026-02-26` | GUI 自动化交互 | 基于截图理解桌面环境，调用 `computer_use` 工具执行鼠标/键盘操作；需传入高分辨率图像并启用 `vl_high_resolution_images` | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |

> **注意**：文档 4 明确指出 `qwen-deep-research` “仅支持华北2（北京）地域”且“暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)”，但文档 3、5、6 中的 OpenAI 兼容示例均未声明该限制。实际调用时请严格遵循 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) 的约束。

## 关键参数

- **`model`**（必选）：模型标识符，如 `"farui-plus"`、`"qwen3.5-ocr"`。
- **`messages`**（必选）：对话消息数组，每条消息含 `role`（`user`/`system`/`assistant`）和 `content`；OCR 与 GUI-Plus 模型支持 `image_url` 类型内容。
- **`result_format` / `output_format`**：指定返回格式。`farui-plus` 等通用模型使用 `result_format='message'`；`qwen-deep-research` 使用 `output_format` 控制报告粒度（`model_detailed_report` 或 `model_summary_report`）。
- **`stream`**：布尔值，启用[流式输出](../concepts/streaming-output.md)（如 `qwen-deep-research`、`qwen3.5-ocr`）。
- **领域专用参数**：
  - `qwen-mt-plus`：通过 `extra_body.translation_options` 传入 `source_lang`、`target_lang`、`terms`（术语表）、`tm_list`（翻译记忆）。
  - `tongyi-intent-detect-v3`：依赖 `system` 消息中的 `Response in INTENT_MODE.` 或意图字典指令。
  - `gui-plus-2026-02-26`：需在 `extra_body` 中设置 `{"vl_high_resolution_images": true}`。

## 使用方式

1. **环境准备**  
   - 获取 API Key 并[配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)（推荐）。
   - 安装 SDK：Python 使用 `pip install dashscope openai`，Java 使用 Maven 依赖（见 [安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)）。

2. **域名配置（强制）**  
   所有模型均**必须**使用业务空间专属域名，否则可能失败或性能下降：
   - 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
   - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
   - 美国（弗吉尼亚）：`https://dashscope-us.aliyuncs.com`（仅 `qwen-mt-plus` 和 `qwen3.5-ocr` 支持）
   > 业务空间 ID 在百炼控制台 **业务空间详情** 页面获取。

3. **调用示例（统一模式）**  
   ```python
   from openai import OpenAI  # 或 import dashscope
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 注意路径后缀
   )
   response = client.chat.completions.create(
       model="farui-plus",  # 替换为目标模型
       messages=[{"role": "user", "content": "生成一份离婚协议书"}],
       result_format="message"  # DashScope SDK 参数名，OpenAI 兼容接口通常省略
   )
   ```

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他模型在多地可用（详见各文档的 endpoint 说明）。
- **[Token](../concepts/token.md) 成本与限流**：`farui-plus` 输入成本为 20 元/百万 [Token](../concepts/token.md)；`tongyi-intent-detect-v3` 提供 100 万 [Token](../concepts/token.md) 免费额度（90 天有效期）。所有模型均受[全局限流策略](https://help.aliyun.com/zh/model-studio/rate-limit)约束。
- **SDK 线程安全**：DashScope Java SDK 的 `Generation` 对象**非线程安全**，需复用实例并自行管理同步（见 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) 说明）。
- **图像处理参数**：`qwen3.5-ocr` 和 `gui-plus-2026-02-26` 要求显式设置 `min_pixels`/`max_pixels` 或 `vl_high_resolution_images`，否则可能因分辨率不足导致识别失败。
- **响应解析差异**：`tongyi-intent-detect-v3` 的 `INTENT_MODE` 输出需用正则解析 `<tags>`/<tool_call>/`<content>` 结构；`qwen-deep-research` 的流式响应含 `phase` 字段（如 `"ResearchPlanning"`），需按阶段处理。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


