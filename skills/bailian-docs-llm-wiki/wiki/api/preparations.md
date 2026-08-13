# preparations

在调用阿里云百炼平台的模型服务前，开发者需完成 SDK 安装、API Key 获取与配置、CLI 工具部署等基础准备。这些步骤共同构成安全、稳定、可复现的调用链路，适用于 Python/Java/Node.js/Go 等主流语言及 CLI 场景。本文档整合关键实践路径，明确支持能力、参数约束与常见陷阱。

## 支持的模型/功能

百炼平台通过统一 API 接口支持多类模型能力，包括文本生成（如 `qwen3-8b`、`qwen3.7-max`）、图像生成（`qwen-image-2.0`）、视频生成（`happyhorse-1.1-t2v`）、语音合成（`cosyvoice`）、语音识别（`paraformer`）、向量嵌入（`text-embedding-v3`）和排序（`text-rerank-v3`）等。所有模型均需通过已授权的 API Key 调用，且模型可用性受其归属**业务空间**严格控制：默认业务空间下的 Key 可调用全部标准模型；子业务空间下的 Key 仅能调用该空间已显式授权的模型 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。[OpenAI 兼容接口](../concepts/openai-compatibility.md)支持部分模型（如 `qwen-plus`），但需注意模型 ID 必须使用百炼官方命名（如 `qwen3-235b-a22b-instruct-2507`），不可混用 Hugging Face 格式（如 `Qwen/Qwen3-235B...`）[错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 关键参数

调用时需关注以下核心参数及其约束：

- **`model`**：必需，值必须为控制台模型市场中已开通的合法 ID，大小写敏感，无空格；未开通将返回 `Model not exist.` 或 `The product is not activated...` 错误。
- **`temperature`**：范围 `[0.0, 2.0)`，非浮点数或越界将报错。
- **`top_p`**：范围 `(0.0, 1.0]`。
- **`max_tokens`**：必须在 `[1, 模型最大输出 Token 数]` 区间内，超限触发 `Range of max_tokens should be [1, xxx]`。
- **`n`**（生成数量）：图像生成最多 `6` 张，文本/Embedding 等场景通常限 `1–4`。
- **`seed`**：DashScope 协议下需为 `[0, 9223372036854775807]` 内整数。
- **`enable_thinking`**：思考模式有强耦合约束——仅支持流式（`stream=true`）、需 `incremental_output=true`、禁用 `response_format=json_object`，且部分模型（如 `qwen3-235b-a22b-thinking-2507`）强制要求设为 `true` [错误码](../../raw/model-api-reference/preparations/error-code.md)。
- **`messages` vs `prompt`**：二者必选其一且不可共存；`messages` 必须为非空数组，纯文本模型不接受 `content` 为数组（如 `[{type:"text",text:"..."}]`），而应为字符串。

> **注意**：文档 3 中 `bl text chat` 的默认模型 `qwen3.7-max` 与文档 1 中示例 `qwen-plus`、`deepseek-r1` 存在版本命名不一致问题。实际调用应以[模型列表](https://help.aliyun.com/zh/model-studio/models)为准，避免使用过时别名。

## 使用方式

### SDK 集成
- **Python**：推荐安装 `openai>=1.0.0` 或 `dashscope>=1.20.0`，二者均可调用百炼 [OpenAI 兼容接口](../concepts/openai-compatibility.md) [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。
- **Java/Node.js/Go**：分别通过 Maven/Gradle、npm/yarn、go get 引入 `dashscope-sdk-java` 或 `openai-java`（推荐 `3.5.0+`）、`openai`、`openai-go/v3`。
- **环境变量**：统一使用 `DASHSCOPE_API_KEY`，支持 Linux/macOS/Windows 全平台永久或临时配置；注意 `sudo` 默认不继承环境变量，需加 `-E` 参数。

### CLI 工具
- **安装**：仅支持 `npm install -g bailian-cli`（Node ≥ 22.12.0），禁用 pnpm/yarn [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。
- **鉴权**：优先使用 `bl auth login --console`（浏览器 OAuth），备选 `bl auth login --api-key <key>`；环境变量、配置文件、命令行 `--api-key` 均可生效，互不覆盖。
- **调用**：通过 `bl text chat`、`bl image generate` 等子命令操作，支持 `--region cn/us/intl` 切换地域，默认 `cn`。

### 直接 HTTP/cURL
- Base URL：中国大陆版 `https://dashscope.aliyuncs.com/compatible-mode/v1`，国际版 `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`。
- 请求头：`Authorization: Bearer <YOUR_API_KEY>`，`Content-Type: application/json`。

## 限制和注意事项

- **API Key 管理**：单个业务空间最多创建 20 个 Key；主账号下最多 20 个业务空间。Key 无自动过期，但可通过 RAM 控制台删除或移出业务空间使其失效 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **IP 白名单**：自定义权限时最多配置 20 个 IPv4 地址或网段（`0.0.0.0/0` 表示全放通），IPv6 仅华北2（北京）支持。
- **安全红线**：**严禁**在客户端代码（浏览器/移动端）、公开日志、Git 仓库中硬编码或明文传输长期 Key；生产环境应使用临时 Key（最长 1800 秒）或服务端代理。
- **错误排查**：所有失败请求应记录 `Request ID`（UUID 格式），用于自助查日志或提工单；常见错误如 `400-InvalidParameter` 多由参数越界、类型错误或模型未开通导致，详见 [错误码](../../raw/model-api-reference/preparations/error-code.md)。
- **CLI 特殊约束**：`bailian-cli` 要求 Node ≥ 22.12.0，且必须用 npm 全局安装；若 `bl: command not found`，需检查 `npm prefix -g` 输出的 `bin` 目录是否在 `PATH` 中。

## 来源文档

- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


