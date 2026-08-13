# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖法律、意图理解、深度研究、OCR、机器翻译和GUI自动化等方向。这些模型在基础大语言模型能力之上，通过领域精调、RAG增强、多阶段推理或视觉-语言联合建模等方式，显著提升了特定任务的准确性与实用性。所有模型均通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatibility.md)调用，支持流式/非[流式输出](../concepts/streaming-output.md)。

## 支持的模型/功能

当前可用的专用模型及其核心能力如下：

- **通义法睿（`farui-plus`）**：法律行业大模型，支持法律咨询、案情分析、文书生成、合同审查等，基于千问基座经法律数据精调，并融合RAG与法律Agent技术 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。
- **意图理解模型（`tongyi-intent-detect-v3`）**：毫秒级意图识别，支持两类模式：① 输出结构化工具调用指令（需 `Response in INTENT_MODE.` 系统提示），② 输出预定义标签（支持单[Token](../concepts/token.md)简写优化响应速度） [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **Qwen-Deep-Research（`qwen-deep-research`）**：两阶段深度研究模型，先反问澄清需求，再联网检索并生成详尽报告（支持 `model_detailed_report` / `model_summary_report` 格式），**仅限华北2（北京）地域且仅支持 Python DashScope SDK** [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **Qwen-OCR（`qwen3.5-ocr`）**：[多模态](../concepts/multimodal.md)OCR模型，支持图像中文字提取与结构化信息抽取（如车票字段），兼容 OpenAI 接口，支持 `min_pixels` / `max_pixels` 图像分辨率控制。
- **Qwen-MT（`qwen-mt-plus`）**：专业机器翻译模型，支持术语干预（`terms`）、翻译记忆（`tm_list`）和领域提示，适用于技术文档等高精度场景。
- **GUI-Plus（`gui-plus-2026-02-26`）**：界面交互专用模型，接收截图与指令，输出鼠标/键盘操作指令（如 `left_click`, `type`），用于自动化GUI操作。

> **注意**：文档 5 中对新加坡/美国地域的 `base_url` 和 HTTP endpoint 描述存在重复罗列，实际配置应以地域唯一性为准；文档 6 的 curl 示例末尾被截断，完整请求体需包含闭合的 JSON 和引号。

## 关键参数

| 参数 | 类型 | 说明 | 示例/取值 |
|------|------|------|-----------|
| `model` | string | 必选。模型标识符 | `"farui-plus"`, `"tongyi-intent-detect-v3"`, `"qwen-deep-research"` |
| `messages` | array | 必选。对话消息列表，含 `role`（`user`/`system`/`assistant`）和 `content` | `[{ "role": "user", "content": "起诉书生成" }]` |
| `result_format` / `response_format` | string | 指定输出格式（DashScope 用 `result_format='message'`；[OpenAI 兼容接口](../concepts/openai-compatibility.md)默认为 `message`） | `"message"` |
| `stream` | boolean | 启用[流式输出](../concepts/streaming-output.md) | `True`（Python）或 `stream: true`（OpenAI） |
| `output_format` | string | Qwen-Deep-Research 专用，控制报告粒度 | `"model_detailed_report"`（默认）或 `"model_summary_report"` |
| `translation_options` | object | Qwen-MT 专用，含 `source_lang`, `target_lang`, `terms`, `tm_list` | `{ "source_lang": "Chinese", "target_lang": "English" }` |
| `extra_body` | object | [OpenAI 兼容接口](../concepts/openai-compatibility.md)扩展参数载体 | `{ "vl_high_resolution_images": true }`（GUI-Plus） |
| `image_url` + `min_pixels`/`max_pixels` | object | OCR/GUI-Plus 图像输入控制 | `{"url": "...", "min_pixels": 3072, "max_pixels": 8388608}` |

## 使用方式

1. **环境准备**  
   - 获取并配置 API Key 到环境变量 `DASHSCOPE_API_KEY`（推荐）或代码内显式传入 [获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)；
   - 安装 SDK：`pip install dashscope`（Python）或 `npm install openai`（Node.js）；
   - **强制使用业务空间专属域名**：华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 和 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。

2. **调用示例（通用流程）**  
   ```python
   from dashscope import Generation  # 或 from openai import OpenAI
   import os

   # 配置地域域名（必须）
   dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

   response = Generation.call(
       model="farui-plus",  # 替换为目标模型
       messages=[{"role": "user", "content": "生成离婚协议书"}],
       result_format="message",
       stream=False
   )
   print(response.output.choices[0].message.content)
   ```

3. **特殊模型调用要点**  
   - **意图理解**：System Message 必须包含 `Response in INTENT_MODE.`（工具调用）或明确的 tag 列表（纯分类）；
   - **Qwen-Deep-Research**：需两阶段调用——首调获取反问，次调传入用户回答与历史消息；
   - **GUI-Plus**：`messages` 中 `user` 内容必须包含截图（`image_url`）和文本指令，且需 `extra_body={"vl_high_resolution_images": True}`；
   - **Qwen-MT**：翻译参数必须置于 `extra_body`（DashScope）或顶层（OpenAI）的 `translation_options` 字段。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；其他模型虽多地可用，但**强烈建议迁移至业务空间专属域名**以获得更高稳定性与性能 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **SDK 限制**：`qwen-deep-research` 当前**不支持 Java SDK 和 OpenAI 兼容接口**，仅限 Python DashScope SDK [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **[流式输出](../concepts/streaming-output.md)**：DashScope 需设置 `stream=True` 并遍历响应迭代器；OpenAI 兼容接口需 `stream=True` 且处理 `chunk` 流。
- **成本与配额**：各模型按输入/输出 [Token](../concepts/token.md) 计费（如 `farui-plus` 输入 20元/百万[Token](../concepts/token.md)），`tongyi-intent-detect-v3` 提供开通后90天内100万Token免费额度 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **安全实践**：API Key **严禁硬编码**，务必通过环境变量配置；Java SDK 中 `Generation` 对象非线程安全，需复用并管理同步 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。
- **限流**：所有模型受平台统一限流策略约束，详情参见 [限流文档](https://help.aliyun.com/zh/model-studio/rate-limit)。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


