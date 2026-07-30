# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成基础环境准备，包括获取并安全配置 API Key、安装必要的 SDK 或 CLI 工具、理解关键参数约束及常见错误应对策略。这些步骤是所有模型调用的前置依赖，直接影响服务可用性与安全性。

## 支持的模型/功能

百炼平台支持多模态模型（如 `qwen3-vl-plus`、`qwen-image-2.0`）、文本生成模型（如 `qwen3.7-max`、`qwen3-235b-a22b-thinking-2507`）、语音合成（`cosyvoice-v3-flash`）、语音识别（`paraformer-real-time`）、向量嵌入（`text-embedding-v3`）及排序模型（`text-rerank-v3`）等。不同模型对输入格式、协议兼容性（OpenAI / Anthropic）、流式能力及工具调用（Function Calling）支持存在差异。例如，思考模式模型（如 `qwen3-235b-a22b-thinking-2507`）**仅支持[流式输出](../concepts/streaming-output.md)**且 `enable_thinking` 参数不可设为 `false`；纯文本模型不接受 `image_url` 等多模态 `content` 元素，否则将报错 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。具体支持列表请以[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)为准。

## 关键参数

核心调用参数需严格遵循范围与类型约束：
- `temperature`: 必须在 `[0.0, 2.0)` 区间；
- `top_p`: 必须在 `(0.0, 1.0]` 区间；
- `max_tokens`: 上限由模型文档明确指定，超出将触发 `Range of max_tokens should be [1, xxx]` 错误；
- `n`: 图像生成等场景中最大值为 `6`（CLI）或 `4`（HTTP API），详见 [原文标题](../../raw/model-api-reference/preparations/error-code.md)；
- `seed`: DashScope 协议下必须为 `[0, 9223372036854775807]` 内整数；
- `enable_thinking` 与 `stream`、`incremental_output`、`result_format` 存在强耦合：开启思考模式时，`stream` 和 `incremental_output` 必须为 `true`，且 `result_format` 必须为 `"message"`；
- 结构化输出（`response_format={"type": "json_object"}`）要求提示词中包含 `json` 关键词，且**不可与 `enable_thinking=true` 同时使用**。

> **注意**：文档 3 中 CLI 的 `bl text chat` 默认 `--model qwen3.7-max`，但文档 4 明确指出 `qwen3-235b-a22b-thinking-2507` 等模型强制要求 `enable_thinking=true`，而 `qwen3.7-max` 并非其别名——实际模型 ID 应以控制台或 [模型列表文档](https://help.aliyun.com/zh/model-studio/model-list) 为准，避免混淆命名。

## 使用方式

### API Key 获取与配置
需通过[主账号或具备权限的子账号](../../raw/model-api-reference/preparations/get-api-key.md)在对应地域（如华北2、新加坡、美国弗吉尼亚）的控制台创建 API Key。新创建的 Key 统一以 `sk-ws` 开头，且**仅在创建弹窗中可见一次**，关闭后无法恢复明文，务必立即保存。推荐将 Key 配置为环境变量 `DASHSCOPE_API_KEY`，避免硬编码（Linux/macOS/Windows 配置方法详见 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)）。

### SDK 与 CLI 安装
- **SDK**：支持 DashScope 官方 SDK（Python/Java）及 OpenAI 兼容 SDK（Python/Node.js/Java/Go）。Python 环境需 `>=3.8`，Java 需 `>=8`，Go 需 `>=1.22`。安装命令如 `pip install -U dashscope` 或 `npm install --save openai`。
- **CLI**：仅支持 `npm install -g bailian-cli`（Node.js ≥ 22.12.0），不支持 pnpm/yarn。认证方式包括浏览器登录（`bl auth login --console`）、API Key 直接登录（`bl auth login --api-key sk-xxx`）、环境变量或配置文件。CLI 支持全模态命令（`bl text`/`bl image`/`bl video`/`bl speech`），默认地域为 `cn`，可通过 `--region us` 切换。

## 限制和注意事项

- **地域隔离**：API Key、服务端点（API Host）、模型开通状态均按地域独立管理。美国（弗吉尼亚）地域的 API Key **不支持禁用/重置操作**，且无 IP 白名单与模型范围自定义权限配置。
- **安全约束**：API Key 是敏感凭证，禁止明文存储于代码、Git 仓库、日志或聊天记录中。CLI 在非交互模式（`--non-interactive`）下应通过密钥管理器注入 Key，而非硬编码。
- **模型开通**：调用前需在[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)开通目标模型，否则返回 `The product is not activated` 错误。
- **文件限制**：Qwen-Long 模型仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD 格式，单文件 ≤ 150 MB，且 page 数 ≤ 1500；无效 URL 需满足 `http://`/`https://`/`data:`/`file://` 格式规范。
- **错误处理**：常见错误如 `Model not exist`（模型 ID 大小写/空格错误）、`Arrearage`（账号欠费）、`InvalidParameter`（参数越界）等，可借助[阿里云 AI 助理](https://www.aliyun.com/ai-assistant/)快速诊断，详细解决方案见 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


