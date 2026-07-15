# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，覆盖意图理解、法律咨询、机器翻译、深度研究、OCR文字识别及GUI自动化等能力。这些模型均基于通义千问系列基座模型精调或增强，具备领域适配性与高精度输出特性，适用于构建专业级AI应用。

## 支持的模型/功能

当前支持的专用模型包括：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持毫秒级意图识别与工具调用决策，适用于对话路由、智能助手等场景 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)；
- **法律大模型**：`farui-plus`，专为法律行业优化，支持法律问答、文书生成、案情分析与合同审查等功能；
- **机器翻译模型**：`qwen-mt-plus`，支持多语言互译、术语干预与翻译记忆，适用于本地化与技术文档翻译；
- **深度研究模型**：`qwen-deep-research`，仅限华北2（北京）地域，支持两阶段交互式研究（反问确认 + 深度分析），并集成网络搜索与引用溯源能力 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)；
- **OCR模型**：`qwen3.5-ocr`，支持图像中结构化文本提取，兼容 OpenAI 多模态消息格式（含 `image_url` 与 `text` 组合输入）；
- **GUI自动化模型**：`gui-plus-2026-02-26`，面向桌面界面操作，支持截图理解、鼠标键盘控制与任务终止，需配合 `<tools>` 系统提示与 `<tool_call>` 格式化响应 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

> **注意**：文档4明确指出 `qwen-deep-research` “仅支持通过 Python DashScope SDK 调用，暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)”，但文档5和文档6均提供了完整的 OpenAI 兼容调用示例（含 `qwen3.5-ocr` 和 `gui-plus-2026-02-26`）。该矛盾表明 `qwen-deep-research` 的 OpenAI 兼容支持状态与其他模型不一致，开发者应以文档4的声明为准，避免在生产环境中尝试非支持接口。

## 关键参数

各模型通用关键参数如下：

- **`model`**（必选）：字符串，指定模型名称，如 `"tongyi-intent-detect-v3"`、`"qwen-mt-plus"` 等；
- **`messages`**（必选）：消息数组，按对话顺序排列；对多模态模型（如 `qwen3.5-ocr`、`gui-plus-2026-02-26`），`content` 支持混合类型（`text` + `image_url`）；
- **`extra_body`**（可选，OpenAI 兼容）：用于传递模型特有参数：
  - `qwen-mt-plus`：传入 `translation_options`（含 `source_lang`、`target_lang`、`terms`、`tm_list`）；
  - `gui-plus-2026-02-26`：建议设置 `"vl_high_resolution_images": true` 以提升图像理解精度；
- **`output_format`**（可选，`qwen-deep-research`）：取值 `model_detailed_report`（默认，约6000 [Token](../concepts/token.md)）或 `model_summary_report`（约1500–2000 [Token](../concepts/token.md)）；
- **图像处理参数**（`qwen3.5-ocr` / `gui-plus-2026-02-26`）：`image_url` 对象内可指定 `min_pixels` 与 `max_pixels` 控制缩放行为。

## 使用方式

### 基础调用前提
- 已获取并配置 API Key（推荐设为环境变量 `DASHSCOPE_API_KEY`）；
- 安装对应 SDK（[DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk) 或 [OpenAI SDK](https://help.aliyun.com/zh/model-studio/install-sdk)）；
- **强烈建议迁移至业务空间专属域名**：华北2（北京）使用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡使用 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，以获得更高性能与稳定性 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。

### 接口选择
- **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**：适用于 `tongyi-intent-detect-v3`、`qwen-mt-plus`、`qwen3.5-ocr`、`gui-plus-2026-02-26`，`base_url` 统一为 `.../compatible-mode/v1`；
- **DashScope 原生接口**：适用于 `farui-plus`、`qwen-deep-research`（仅 Python SDK），`base_http_api_url` 设为 `.../api/v1`；
- **[流式输出](../concepts/streaming-output.md)**：所有模型均支持，OpenAI 接口设 `stream=True`，DashScope 接口使用 `stream=True`（Python）或 `streamCall`（Java）。

### 特殊调用模式
- **意图识别双模式**：
  - `INTENT_MODE`：System Message 中声明 `Response in INTENT_MODE.` 并注入工具定义，返回 `<tags>`/`<tool_call>`/`<content>` 结构化结果；
  - **纯标签模式**：System Message 指定意图字典并要求“仅回复所选标签”，可进一步压缩为单 [Token](../concepts/token.md) 输出以优化延迟。
- **深度研究两阶段流程**：先调用获取模型反问（`ResearchPlanning` 阶段），再将用户澄清与历史消息组合发起第二轮调用，触发 `WebResearch` 与 `answer` 阶段。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他地域调用将失败；
- **SDK 限制**：`qwen-deep-research` 当前**不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**，仅 Python DashScope SDK 可用；
- **域名迁移强制建议**：旧域名（如 `dashscope.aliyuncs.com`）虽仍可用，但新业务空间专属域名提供“卓越的性能和更高的稳定性”，生产环境务必迁移；
- **成本与配额**：`tongyi-intent-detect-v3` 提供开通后90天内100万 Token 免费额度；`farui-plus` 输入/输出成本为20元/百万 Token（文档2未列明输出成本，存在信息缺失）；
- **OCR 图像约束**：`qwen3.5-ocr` 对输入图像像素有硬性要求（`min_pixels`/`max_pixels`），超限将自动缩放，需在请求中显式配置；
- **GUI 模型行为约束**：`gui-plus-2026-02-26` 无终端或应用菜单访问权限，所有操作必须通过点击桌面图标启动应用，并需合理插入 `wait` 动作应对加载延迟。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


