# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成基础环境准备，包括获取并安全配置 API Key、安装适配的 SDK 或 CLI 工具、理解关键参数约束及常见错误处理机制。这些步骤是所有模型调用的前置依赖，直接影响服务可用性与安全性。

## 支持的模型/功能

百炼平台支持[多模态](../concepts/multi-modal.md)模型（如 `qwen3-vl-plus`、`qwen-image-2.0`）、文本生成模型（如 `qwen3.7-max`）、语音合成/识别（如 `cosyvoice`、`paraformer`）、向量嵌入（`text-embedding-v2`）及排序模型（`text-rerank`）等。模型能力取决于其类型：纯文本模型不支持 `image_url` 等[多模态](../concepts/multi-modal.md) `content` 元素；而全模态模型（如 `qwen3.5-omni-plus`）则支持图像、音频、视频输入 [原文标题](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。调用前须确认模型是否已开通——未在[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)激活的模型将返回 `Model not exist` 或 `The product is not activated` 错误 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

> **注意**：文档 3 中列出的 `qwen3.5-omni-plus` 默认模型与文档 2 中 `qwen3.7-max` 的默认值存在不一致。实际调用时应以控制台模型市场当前可用版本为准，并显式指定 `--model` 参数，避免依赖 CLI 或 SDK 的隐式默认值。

## 关键参数

核心参数需严格遵循取值范围与格式要求：
- `temperature` 必须在 `[0.0, 2.0)` 区间，`top_p` 在 `(0.0, 1.0]`；
- `max_tokens` 不得超出模型最大输出 [Token](../concepts/token.md) 数，`n`（生成数量）限于 `[1, 4]`（图像生成支持最多 6 张，见 CLI 文档）；
- `seed` 范围为 `[0, 9223372036854775807]`；
- 启用 `enable_thinking` 时，必须同时设置 `stream=true` 且 `incremental_output=true`，且不可与 `response_format={"type": "json_object"}` 共用；
- `messages` 中 `content` 字段对纯文本模型必须为字符串，[多模态](../concepts/multi-modal.md)模型则需为合法对象数组（`type` 仅支持 `text`/`image_url`/`video_url` 等） [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

## 使用方式

### API Key 获取与配置
需通过[主账号或具备权限的子账号](https://bailian.console.aliyun.com/?tab=model#/api-key)创建 API Key。按量付费 Key 以 `sk-ws` 开头（安全升级后），[Token](../concepts/token.md) Plan Key 以 `sk-sp-` 开头，二者不可混用。强烈建议将 Key 配置为环境变量 `DASHSCOPE_API_KEY`，而非硬编码 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。Windows/macOS/Linux 的配置方法详见该文档。

### SDK 与 CLI 选择
- **SDK**：Python 开发者可选 `openai`（OpenAI 兼容协议）或 `dashscope`（原生协议）；Java/Node.js/Go 项目推荐使用对应语言的 OpenAI SDK（需注意兼容性说明）；
- **CLI**：`bailian-cli`（命令 `bl`）专为 AI Agent 场景设计，支持文本、图像、视频、语音等全模态命令，要求 Node.js ≥ 22.12.0 且仅通过 `npm install -g bailian-cli` 安装 [原文标题](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。

### 协议与端点
调用时必须指定 `base_url`（即创建 API Key 时显示的 API Host）。[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 Anthropic 兼容接口的端点不同，且随地域变化（如华北2、新加坡、美国弗吉尼亚），务必以对应接口文档为准。

## 限制和注意事项

- **API Key 权限**：Key 的调用范围由其归属业务空间决定。默认空间 Key 可调用所有标准模型；子空间 Key 仅限该空间授权的模型。IP 白名单与模型范围自定义权限仅在华北2、新加坡、东京、法兰克福地域支持，美国（弗吉尼亚）地域不支持 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。
- **安全约束**：API Key 明文仅在创建弹窗中显示一次，关闭后不可恢复；`sk-` 开头的旧 Key 可继续使用，但建议迁移到 `sk-ws` 新格式。CLI 工具严禁在日志、聊天记录或代码中明文暴露 Key，CI/CD 环境应通过密钥管理服务注入 [原文标题](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。
- **错误排查**：所有失败请求应记录 `Request ID`（UUID 格式），用于自助排查或提交工单。常见错误如 `Arrearage`（欠费）、`InvalidParameter`（参数越界或格式错误）、`Model not exist`（未开通模型）均有明确解决方案，详见错误码文档 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


