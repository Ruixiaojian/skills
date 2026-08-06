# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，覆盖意图理解、法律咨询、深度研究、机器翻译、OCR图文识别和GUI自动化等能力。这些模型均基于通义千问基座，通过领域精调与增强技术实现专业性能优化，支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与 DashScope SDK 调用。

## 支持的模型/功能

| 模型名称 | 主要能力 | 适用场景 | 地域支持 | 文档引用 |
|----------|----------|----------|----------|----------|
| `tongyi-intent-detect-v3` | 用户意图识别与[函数调用](../concepts/function-calling.md)生成 | 智能助手、多工具调度 | 华北2（北京）、新加坡 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `farui-plus` | 法律问答、文书生成、案情分析、合同审查 | 法律服务、司法辅助 | 全地域（文档未限定） | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `qwen-deep-research` | 多阶段网络检索+结构化报告生成 | 学术研究、竞品分析、政策解读 | **仅华北2（北京）** | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `qwen-mt-plus` | 领域自适应机器翻译（支持术语干预、翻译记忆） | 技术文档本地化、多语种内容生产 | 华北2（北京）、新加坡、美国（弗吉尼亚） | [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) |
| `qwen3.5-ocr` | 图文识别与结构化信息抽取（支持自定义Prompt） | 票据识别、证件提取、表单解析 | 华北2（北京）、新加坡、美国（弗吉尼亚） | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `gui-plus-2026-02-26` | 基于屏幕图像的GUI自动化操作（鼠标/键盘/截图） | RPA流程自动化、UI测试、桌面任务代理 | 华北2（北京） | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |

> **注意**：`qwen-deep-research` 明确声明“仅支持华北2（北京）地域”，而 `farui-plus` 文档未注明地域限制，但其示例代码中均使用北京专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），实际部署可能受限于业务空间所在地域。建议以控制台开通情况为准。

## 关键参数

- **模型标识符（model）**：所有调用必须显式指定模型名（如 `"qwen-mt-plus"`），不支持别名或通配符。
- **输入格式（messages）**：
  - 意图识别模型需在 `system` message 中声明 `Response in INTENT_MODE.` 或意图字典；
  - OCR 和 GUI-Plus 模型要求 `content` 为数组，包含 `image_url` + `text` 元素；
  - Deep-Research 使用两阶段消息流（初始请求 → 模型反问 → 用户澄清 → 深度分析）；
- **扩展参数（extra_body / 参数对象）**：
  - `qwen-mt-plus`：通过 `translation_options` 传入 `source_lang`, `target_lang`, `terms`, `tm_list`；
  - `qwen3.5-ocr`：支持 `min_pixels` / `max_pixels` 控制图像缩放；
  - `gui-plus-*`：需设置 `vl_high_resolution_images: true` 以启用高分辨率图像处理；
  - `qwen-deep-research`：支持 `output_format`（`model_detailed_report` 或 `model_summary_report`）控制输出长度。
- **流式响应（stream）**：除 `qwen-deep-research`（强制流式）外，其余模型均支持 `stream=True`；OCR 和 GUI-Plus 推荐启用 `stream_options={"include_usage": True}` 获取实时 token 统计。

## 使用方式

1. **环境准备**：
   - 获取并配置 `DASHSCOPE_API_KEY` 到环境变量（[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）；
   - 安装对应 SDK（[DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk) 或 [OpenAI SDK](https://help.aliyun.com/zh/model-studio/install-sdk)）；
   - **强烈建议迁移至业务空间专属域名**：华北2（北京）使用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡使用 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` —— 此变更已在 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)、[Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) 和 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 中多次强调。

2. **SDK 调用示例（通用模式）**：
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 北京地域
   )
   response = client.chat.completions.create(
       model="qwen-mt-plus",
       messages=[{"role": "user", "content": "Hello"}],
       extra_body={"translation_options": {"source_lang": "English", "target_lang": "Chinese"}}
   )
   ```

3. **特殊流程说明**：
   - `tongyi-intent-detect-v3` 的响应需用正则解析 `<tags>` / `<tool_call>` / `<content>` 三段式结构（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）；
   - `qwen-deep-research` 必须分两步调用：先获取模型反问，再将反问+用户回答拼入第二轮 `messages`；
   - `gui-plus-*` 的 system [prompt](../guides/prompt.md) 必须严格包含 `<tools>` XML 块及 `<tool_call>` 分隔符规则，否则无法触发工具调用。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他模型虽文档标注多地域，但实际可用性取决于业务空间开通状态与 API Key 所属地域。
- **SDK 兼容性**：`qwen-deep-research` **仅支持 Python DashScope SDK**，明确不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)）。
- **成本与额度**：`tongyi-intent-detect-v3` 提供 90 天内 100 万 [Token](../concepts/token.md) 免费额度；`farui-plus` 输入成本为 20 元/百万 [Token](../concepts/token.md)，未列明输出成本（见 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)）；具体计费请以控制台最新公示为准。
- **稳定性提示**：所有模型均推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性不及新域名（该建议在 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)、[Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md) 和 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 中一致强调）。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


