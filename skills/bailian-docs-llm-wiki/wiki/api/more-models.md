# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖法律、意图理解、机器翻译、OCR、深度研究和GUI自动化等能力。这些模型在通用大模型基础上进行了领域精调或架构增强，具备更强的专业性与任务适配性。开发者可通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，需注意地域、域名、API Key 和参数格式等关键配置。

## 支持的模型/功能

当前支持以下专用模型：

- **通义法睿（`farui-plus`）**：法律行业大模型，支持法律咨询、文书生成、案情分析、合同审查等，基于千问基座并融合RAG、法律Agent等技术 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)  
- **意图理解（`tongyi-intent-detect-v3`）**：毫秒级意图识别模型，支持工具调用（INTENT_MODE）或纯标签分类两种模式，适用于对话路由与智能助手 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)  
- **Qwen-MT（`qwen-mt-plus`）**：专业机器翻译模型，支持术语干预、翻译记忆（TM）、领域提示等高级功能，适用于技术文档、本地化等高精度场景 [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)  
- **Qwen-OCR（`qwen3.5-ocr`）**：多模态OCR模型，支持图像+文本Prompt联合输入，可精准提取票据、证件等结构化信息 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)  
- **Qwen-Deep-Research（`qwen-deep-research`）**：支持两阶段交互式深度研究的模型，自动规划、网络检索、引用溯源，仅限华北2（北京）地域调用 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)  
- **GUI-Plus（`gui-plus-2026-02-26`）**：界面交互专用模型，通过截图理解GUI状态并执行鼠标/键盘操作，适用于自动化测试与RPA场景 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)  

> **注意**：文档 3 和文档 5 均重复列出新加坡/美国地域的 endpoint 配置，且文档 3 中“新加坡地域”条目出现两次，属冗余表述；实际使用时请以控制台中业务空间详情页显示的 `{WorkspaceId}` 和对应地域为准。

## 关键参数

| 模型 | 必选参数 | 关键可选参数 | 说明 |
|--------|-----------|----------------|------|
| `farui-plus` | `model`, `messages` | `result_format='message'`, `stream=True` | `result_format` 推荐设为 `'message'`；流式需显式启用 `stream` 并处理增量响应 |
| `tongyi-intent-detect-v3` | `model`, `messages`（含特定 system [prompt](../guides/prompt.md)） | `result_format='message'` | System [prompt](../guides/prompt.md) 必须包含 `Response in INTENT_MODE.` 或明确 tag 列表，否则无法正确解析意图 |
| `qwen-mt-plus` | `model`, `messages`, `translation_options` | `extra_body={'translation_options': {...}}`（OpenAI）或直接传参（DashScope） | `translation_options` 必须包含 `source_lang` 和 `target_lang`；`terms` 和 `tm_list` 为可选增强字段 |
| `qwen3.5-ocr` | `model`, `messages`（含 `image_url` + `text`） | `min_pixels`, `max_pixels`, `stream=True` | 图像尺寸需满足像素阈值约束；`min_pixels=3072`, `max_pixels=8388608` 是典型值 |
| `qwen-deep-research` | `model`, `messages`（两阶段构造） | `output_format='model_summary_report'` | 仅支持 Python DashScope SDK；第二步必须包含第一步的 assistant 回复作为历史上下文 |
| `gui-plus-2026-02-26` | `model`, `messages`（含 system [prompt](../guides/prompt.md) + image） | `extra_body={'vl_high_resolution_images': True}` | system prompt 必须严格遵循工具定义与响应格式规范；`vl_high_resolution_images` 启用高分辨率图像处理 |

## 使用方式

1. **环境准备**  
   - 获取并配置 API Key 到环境变量 `DASHSCOPE_API_KEY`（[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)）  
   - 安装 SDK：`pip install dashscope`（Python）或 `npm install openai`（Node.js）  
   - **强烈建议迁移至业务空间专属域名**：华北2（北京）使用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡使用 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` —— 此举可提升性能与稳定性 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)

2. **调用示例（统一模式）**  
   ```python
   from openai import OpenAI  # 或 import dashscope
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # OpenAI 兼容
   )
   # 或
   import dashscope
   dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"  # DashScope 原生
   ```

3. **[流式输出](../concepts/streaming-output.md)**  
   - OpenAI 接口：设置 `stream=True`，遍历 `completion` 迭代器  
   - DashScope 接口：`Generation.call(..., stream=True)`，循环读取 `response` 对象  
   - 注意：`qwen-deep-research` 仅支持流式调用，且需按 `phase` 字段区分研究阶段；`gui-plus` 和 `qwen3.5-ocr` 的流式响应需解析 `delta.content`  

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他模型虽支持多地域，但 API Key 与 WorkspaceId 需匹配 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)  
- **SDK 限制**：`qwen-deep-research` 当前**不支持 Java SDK 和 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)**，仅限 Python DashScope SDK 调用  
- **输入格式**：`qwen3.5-ocr` 和 `gui-plus` 的 `messages` 中 `content` 必须为 list，包含 `{"type": "image_url", ...}` 和 `{"type": "text", ...}` 两项，顺序无关但缺一不可  
- **成本与限流**：各模型按输入/输出 [Token](../concepts/token.md) 计费（如 `farui-plus` 输入 20元/百万[Token](../concepts/token.md)），具体见各模型文档；全局限流策略参见 [限流](https://help.aliyun.com/zh/model-studio/rate-limit)  
- **安全实践**：API Key **严禁硬编码**，务必通过环境变量注入；Java SDK 中 `Generation` 对象非线程安全，需自行管理生命周期 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)  
- **响应解析**：`tongyi-intent-detect-v3` 的 INTENT_MODE 响应需用正则解析 `<tags>`/<tool_call>/`<content>` 三段式结构；`qwen-deep-research` 响应中 `phase` 字段是判断当前处理阶段的关键依据

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


