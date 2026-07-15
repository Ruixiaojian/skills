# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成基础环境准备，包括获取并安全配置 API Key、安装必要的 SDK 或 CLI 工具、理解关键参数约束及常见错误处理机制。这些步骤是所有模型调用的前置依赖，直接影响服务可用性与安全性。

## 支持的模型/功能

百炼平台支持多模态模型（如 `qwen3-vl-plus`、`qwen-image-2.0`）、文本生成模型（如 `qwen3.7-max`）、语音合成（`cosyvoice-v3-flash`）、语音识别（`paraformer-real-time`）、向量嵌入（`text-embedding-v3`）及排序模型（`text-rerank-v3`）等。不同模型对输入格式、协议兼容性（OpenAI 兼容 / Anthropic 兼容）、输出模式（流式/非流式）有明确要求。例如，`qwen3-235b-a22b-thinking-2507` 等思考模式模型**仅支持流式调用**，且 `enable_thinking` 参数不可设为 `false`；而纯文本模型（如 `qwen3-max`）**不支持 `image_url` 等多模态 `content` 元素**，混用将触发 400 错误 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。多模态能力需通过 `bl omni` 或 `bl vision describe` 等 CLI 命令或对应 SDK 接口调用。

## 关键参数

核心参数需严格遵循取值范围与类型约束：
- `temperature`: 必须在 `[0.0, 2.0)` 区间；
- `top_p`: 必须在 `(0.0, 1.0]` 区间；
- `max_tokens`: 上限由模型文档明确指定，超出将报错 `Range of max_tokens should be [1, xxx]`；
- `n`: 图像生成等场景中最大值为 `6`（CLI）或 `4`（HTTP API），超限触发 `Range of n should be [1, 4]`；
- `seed`: DashScope 协议下必须为 `[0, 9223372036854775807]` 内整数；
- `messages` 格式：纯文本模型要求 `content` 为字符串，多模态模型要求 `content` 数组元素为合法对象（`type` 仅限 `text`/`image_url`/`video_url` 等）[原文标题](../../raw/model-api-reference/preparations/error-code.md)；
- 结构化输出（`response_format={"type": "json_object"}`）时，提示词中**必须包含 `json` 关键词**，且 `enable_thinking` 必须为 `false`。

> **注意**：文档 3 中 `bl image generate` 的 `--n` 参数默认值为 `1`，最大支持 `6`；而文档 4 的错误码说明中 `Range of n should be [1, 4]` 针对的是 HTTP API 的通用限制。实际使用时，请以目标接口（CLI vs HTTP）的文档为准——CLI 扩展了图像生成的并发上限，但标准 HTTP 接口仍遵循 `n ≤ 4` 规则 [原文标题](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。

## 使用方式

### API Key 获取与配置
- **获取**：需主账号或具备 `管理员`/`API-Key` 权限的子账号，在[百炼控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)创建。新创建的 Key 统一以 `sk-ws` 开头，仅创建时可见明文，丢失需重置 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。
- **配置**：强烈建议通过环境变量 `DASHSCOPE_API_KEY` 设置（Linux/macOS/Windows 均支持永久或临时配置），避免代码硬编码。CLI 工具还支持 `bl auth login --api-key`、`bl config set` 或命令行 `--api-key` 临时传入等多种方式。

### SDK 与 CLI 安装
- **SDK**：支持 DashScope 官方 SDK（Python/Java）及 OpenAI 兼容 SDK（Python/Node.js/Java/Go）。Python 环境需 `≥ 3.8`，Java 需 `≥ 8`，Go 需 `≥ 1.22` [原文标题](../../raw/model-api-reference/preparations/install-sdk.md)。
- **CLI**：`bailian-cli` 仅支持 `npm install -g bailian-cli`（Node ≥ 22.12.0），不支持 `pnpm`/`yarn`。认证推荐 `bl auth login --console`（浏览器 OAuth），也可 `--api-key` 或环境变量方式。

## 限制和注意事项

- **地域与端点**：API Key 创建地域（如华北2、新加坡、美国弗吉尼亚）决定了默认 `base_url`，OpenAI 兼容与 Anthropic 兼容协议的端点不同，必须匹配所选协议。
- **权限隔离**：API Key 权限由其**归属业务空间**决定，同一空间内 Key 权限一致；子业务空间 Key 仅可访问该空间已授权的模型与应用。
- **安全红线**：API Key 明文禁止日志打印、代码提交、聊天记录留存；CLI 在 `auth status` 输出中仅显示脱敏字段（如 `masked: "sk-...xxx"`）。
- **错误处理**：常见 400 错误（如 `Model not exist`、`InvalidParameter`）需核对模型 ID 大小写、参数范围及 `messages` 结构；`Arrearage` 类错误表明账户欠费，需充值后等待系统同步。
- **文件限制**：Qwen-Long 模型支持 TXT/DOCX/PDF/EPUB/MOBI/MD，单文件 ≤ 150 MB 且 ≤ 15000 页；无效 URL 需以 `http://`/`https://`/`data:`/`file://` 开头，并注意 `X-DashScope-OssResourceResolve` Header 配置。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


