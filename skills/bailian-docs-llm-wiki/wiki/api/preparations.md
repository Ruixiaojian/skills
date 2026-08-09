# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成基础环境准备，包括获取并安全配置 API Key、安装必要的 SDK 或 CLI 工具、理解关键参数约束及常见错误处理机制。这些步骤是所有模型调用的前置依赖，直接影响服务可用性与安全性。

## 支持的模型/功能

百炼平台支持[多模态](../concepts/multimodal.md)模型（如 `qwen3-vl-plus`、`qwen-image-2.0`）、文本生成模型（如 `qwen3.7-max`）、语音合成（`cosyvoice`）、语音识别（`paraformer`）、向量嵌入（`text-embedding-v2`）及排序模型（`text-rerank`）等。模型能力由其所属业务空间决定：默认业务空间下的 API Key 可调用所有标准模型；子业务空间下的 API Key 仅可调用该空间已授权的模型 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。部分模型（如 `qwen3-235b-a22b-thinking-2507`）强制要求 `enable_thinking=true`，而思考模式模型不支持结构化输出（`response_format=json_object`），需关闭思考模式方可启用 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

## 关键参数

调用时需注意以下核心参数的合法范围与互斥约束：
- `temperature`: 必须在 `[0.0, 2.0)` 区间；
- `top_p`: 必须在 `(0.0, 1.0]` 区间；
- `max_tokens`: 不得超过模型文档中声明的最大输出 [Token](../concepts/token.md) 数；
- `n`: 图像/文本批量生成数，范围为 `[1, 4]`（图像生成 CLI 中上限为 6，见 [原文标题](../../raw/model-api-reference/preparations/use-model-studio-cli.md)）；
- `seed`: DashScope 协议下需为 `[0, 9223372036854775807]` 内整数；
- `enable_thinking`: 开启时必须同时设置 `stream=true` 且 `incremental_output=true`，且 `result_format="message"`；
- `messages` 格式：纯文本模型不接受 `content` 为数组（如含 `image_url`），否则报错；[多模态](../concepts/multimodal.md)模型则要求 `content` 数组元素类型严格为 `text`/`image_url`/`video_url` 等合法模态对象 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

> **注意**：文档 3 中 CLI 的 `bl image generate --n` 参数允许值为 `1-6`，而文档 4 的通用错误码明确 `n` 范围为 `[1, 4]`。实际使用中，图像生成接口（如 `qwen-image-2.0`）支持 `n=6`，该限制属于模型特定行为，非全局协议限制。

## 使用方式

### API Key 获取与配置
需通过[主账号或具备权限的子账号](https://help.aliyun.com/zh/model-studio/permission-management-overview#24ca2dad7djzs)在控制台创建 API Key。华北2（北京）、新加坡等地域支持 IP 白名单与模型范围自定义权限；美国（弗吉尼亚）地域暂不支持此配置 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。强烈建议将 `DASHSCOPE_API_KEY` 配置为环境变量（Linux/macOS/Windows 均有详细指南），避免硬编码泄露风险。

### SDK 与 CLI 安装
- **SDK**：推荐使用官方 `dashscope` SDK（Python/Java）或 OpenAI 兼容 SDK（Python/Node.js/Java/Go）。Python 需 `>=3.8`，Java 需 `>=8`，Node.js 需 `>=22.12.0`（CLI 要求，SDK 无此限制）。
- **CLI**：通过 `npm install -g bailian-cli` 安装，认证支持控制台 OAuth 登录（推荐）、API Key 直接输入、环境变量或配置文件等多种方式，适用于 Agent 集成与 CI/CD 场景 [原文标题](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。

### 协议与端点
调用需指定 `base_url`（即创建 API Key 时显示的 API Host），OpenAI 兼容与 Anthropic 兼容协议的端点不同，且随地域变化，务必以对应接口文档为准。

## 限制和注意事项

- **API Key 安全**：新创建的 API Key 以 `sk-ws` 开头，明文仅在创建弹窗中可见一次，丢失后需重置；旧 `sk-` 密钥仍可用，但建议迁移至新格式 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。
- **地域差异**：美国（弗吉尼亚）地域不支持 API Key 禁用/重置操作，且无 IP 白名单与模型范围配置能力。
- **错误排查**：所有失败请求应记录 `Request ID`（UUID 格式），用于自助排查或提交工单；模型未开通、欠费、参数越界等均会返回明确错误码（如 `Arrearage`、`Model not exist`、`InvalidParameter`），详见错误码文档 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。
- **工具调用**：`tool_choice` 仅支持 `"auto"` 或 `"none"`；`tools` 参数仅 Qwen/DeepSeek 等特定模型支持，纯文本模型传入将报错。
- **文件与 URL**：视觉/语音模型输入 URL 必须以 `http://`、`https://` 或 `data:` 开头（Base64 前需含 `"base64"`），本地路径需以 `file://` 开头；临时 OSS URL 需在 Header 中添加 `X-DashScope-OssResourceResolve: enable`。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


