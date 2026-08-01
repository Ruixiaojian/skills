# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成基础环境准备，包括获取并安全配置 API Key、安装适用的 SDK 或 CLI 工具、理解关键参数约束及常见错误应对策略。这些步骤直接影响服务调用的可用性、安全性与稳定性，是所有集成工作的前提。

## 支持的模型/功能

百炼平台支持多模态模型（如 `qwen3-vl-plus`、`qwen-image-2.0`）、文本生成模型（如 `qwen3.7-max`）、语音合成/识别（`cosyvoice`、`paraformer`）、向量嵌入（`text-embedding-v2`）及排序模型（`text-rerank`）等。**模型能力与调用方式强绑定**：纯文本模型不接受 `image_url` 等多模态 `content` 元素；Qwen-Omni 等全模态模型才支持图像/音频/视频输入；思考模式（`enable_thinking=true`）仅适用于特定模型（如 `qwen3-235b-a22b-thinking-2507`），且必须配合[流式输出](../concepts/streaming-output.md)（`stream=true`）与 `incremental_output=true` [原文标题](../../raw/model-api-reference/preparations/error-code.md)。模型开通状态需在[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)中手动启用，未开通将返回 `The product is not activated` 错误 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

## 关键参数

核心请求参数需严格遵循取值范围与类型约束：
- `temperature`: 必须在 `[0.0, 2.0)` 区间；
- `top_p`: 必须在 `(0.0, 1.0]` 区间；
- `max_tokens`: 上限由模型文档明确指定，超出将报 `Range of max_tokens should be [1, xxx]`；
- `seed`: DashScope 协议下必须为 `[0, 9223372036854775807]` 内整数；
- `n`: 图像生成等场景最大值为 `6`，文本生成等场景为 `4`；
- `messages` 构造：纯文本模型要求 `content` 为字符串，多模态模型要求 `content` 数组元素为合法对象（`type` 仅限 `text`/`image_url`/`video_url` 等）；
- `response_format`: 结构化输出需设为 `{"type": "json_object"}`，且提示词中必须包含 `json` 关键词；
- `enable_thinking`: 开启时必须同时设置 `stream=true`、`incremental_output=true`、`result_format="message"`，且禁用 `response_format=json_object` [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

> **注意**：文档 3 中 `bl text chat` 命令默认 `--model qwen3.7-max`，但文档 4 明确指出 `qwen3.7-max` 并非官方模型 ID（正确 ID 如 `qwen3-max`），实际使用应以[模型列表](https://help.aliyun.com/zh/model-studio/model-list)为准，避免因模型名错误导致 `Model not exist` 错误。

## 使用方式

### API Key 获取与配置
- **获取**：需主账号或具备 `管理员`/`API-Key` 权限的子账号，在对应地域（如华北2、新加坡、美国弗吉尼亚）的[API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)创建。新创建 Key 统一以 `sk-ws` 开头，旧 `sk-` Key 仍可使用 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。
- **配置**：强烈建议通过环境变量 `DASHSCOPE_API_KEY` 设置，避免硬编码。Linux/macOS/Windows 的永久与临时配置方法详见 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。

### SDK 与 CLI 安装
- **SDK**：支持 DashScope SDK（Python/Java）和 OpenAI 兼容 SDK（Python/Node.js/Java/Go）。Python 需 `>=3.8`，Java 需 `>=8`，Node.js 需 `>=22.12.0`（CLI 要求） [原文标题](../../raw/model-api-reference/preparations/install-sdk.md)。
- **CLI**：通过 `npm install -g bailian-cli` 安装，认证支持控制台 OAuth 登录（推荐）、API Key 直接注入、环境变量或配置文件等多种方式，适用于 Agent 集成与 CI/CD 场景 [原文标题](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。

### 协议与端点
- **协议选择**：[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`base_url` 形如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）或 Anthropic 兼容接口（`base_url` 形如 `https://dashscope.aliyuncs.com/anthropic/v1`），二者 `base_url` 不同且随地域变化，务必以对应接口文档为准 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。

## 限制和注意事项

- **API Key 安全**：创建后仅一次明文展示机会，关闭弹窗即不可恢复；美国（弗吉尼亚）地域不支持禁用/重置操作；IP 白名单最多配置 20 个地址/网段 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。
- **地域与权限隔离**：API Key 的调用权限由其**归属业务空间**决定，同一空间内 Key 权限一致；子业务空间下的 Key 仅能调用该空间已授权的模型 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。
- **错误处理**：常见错误如 `Arrearage`（账号欠费）、`InvalidParameter`（参数越界/格式错误）、`Model not exist`（模型名错误或未开通）、`The audio is empty`（音频过短）等，均需按具体错误码定位原因 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。
- **文件限制**：Qwen-Long 模型仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD 纯文本文件，单文件 ≤150 MB，且需等待文件解析完成后再调用 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


