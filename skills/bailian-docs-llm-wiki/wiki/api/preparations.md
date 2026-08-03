# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成三项核心准备：获取并安全配置 API Key、安装合适的 SDK 或 CLI 工具、理解关键参数与调用约束。这些步骤直接影响服务可用性、安全性及功能完整性，是所有后续开发工作的前提。

## 支持的模型/功能

百炼平台支持全模态模型调用，包括文本生成（如 `qwen3.7-max`）、图像生成（如 `qwen-image-2.0`）、视频生成（如 `happyhorse-1.1-t2v`）、语音合成/识别（如 `cosyvoice`）、向量嵌入（如 `text-embedding-v3`）、排序（`text-rerank`）及多模态理解（如 `qwen3-vl-plus`）。  
不同模型能力差异显著：纯文本模型（如 `qwen3-max`）**不支持** `image_url` 等多模态 `content` 元素；而 `qwen3-vl-plus`、`qwen3.5-omni-plus` 等多模态模型则要求 `content` 为合法对象数组（`type` 仅限 `text`/`image_url`/`video_url` 等）[原文标题](../../raw/model-api-reference/preparations/error-code.md)。  
部分模型有强制约束，例如 `qwen3-235b-a22b-thinking-2507` 要求 `enable_thinking` 必须为 `true`，而思考模式模型又**禁止**与 `response_format: {"type": "json_object"}` 同时使用 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

## 关键参数

| 参数 | 说明 | 取值范围/格式 | 注意事项 |
|------|------|----------------|----------|
| `model` | 模型 ID | 字符串，区分大小写（如 `qwen3.7-max`） | **不可混用开源社区命名**（如 `Qwen/Qwen3-235B...`），必须使用百炼控制台模型市场中的标准 ID [原文标题](../../raw/model-api-reference/preparations/error-code.md) |
| `temperature` | 采样温度 | `[0.0, 2.0)` | 超出范围将报错 `400-InvalidParameter` |
| `top_p` | 核采样阈值 | `(0.0, 1.0]` | 同上，需严格校验 |
| `max_tokens` | 最大输出 token 数 | `[1, 模型最大输出值]` | 上限见各模型文档，超限将拒绝请求 |
| `seed` | 随机种子 | `[0, 9223372036854775807]` | DashScope 协议下必须为整数，OpenAI 兼容协议可能放宽 |
| `enable_thinking` | 是否启用思考模式 | `true`/`false` | 非流式调用时必须设为 `false`；部分模型强制为 `true`；开启时 `incremental_output` 必须为 `"true"` [原文标题](../../raw/model-api-reference/preparations/error-code.md) |
| `messages` / `prompt` | 输入内容 | JSON 数组 或 字符串 | 二者**必选其一且不可共存**；`messages` 中 `content` 类型需与模型能力匹配（纯文本模型仅接受字符串） |

> **注意**：文档 3 中 `bl text chat` 命令默认 `--model qwen3.7-max`，但文档 4 明确指出 `qwen3.7-max` 是有效模型 ID；而文档 2 的 SDK 示例未指定具体模型，易导致开发者误用已下线或非标准名称。请始终以 [原文标题](../../raw/model-api-reference/preparations/error-code.md) 中 `Model not exist.` 错误说明为准——通过控制台模型市场确认 ID。

## 使用方式

### 1. 获取与配置 API Key
- **创建**：需主账号或具备 `管理员`/`API-Key` 权限的子账号，在对应地域（如华北2、新加坡、美国弗吉尼亚）的 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建。新密钥以 `sk-ws` 开头，旧密钥（`sk-`）仍可用但建议升级 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。
- **安全配置**：**强烈建议**将 API Key 存入环境变量 `DASHSCOPE_API_KEY`，避免硬编码。Linux/macOS/Windows 的永久/临时配置方法详见 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。
- **地域与端点**：除 API Key 外，**必须指定 `base_url`（即 API Host）**，其值随地域和协议（OpenAI 兼容/Anthropic 兼容）变化，不可复用。

### 2. 安装客户端工具
- **SDK**：Python/Java/Node.js/Go 开发者可选：
  - DashScope SDK（官方，功能完整）：`pip install -U dashscope`
  - OpenAI 兼容 SDK（多语言生态）：`pip install -U openai`（Python）、`npm install openai`（Node.js）等 [原文标题](../../raw/model-api-reference/preparations/install-sdk.md)。
- **CLI**：面向 AI Agent 或命令行场景，安装 `bailian-cli`（`npm install -g bailian-cli`），支持 `bl text chat`、`bl image generate` 等全模态命令，并提供 `--api-key`、`--region`、`--base-url` 等灵活参数 [原文标题](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。

### 3. 鉴权与调用
- CLI 支持多种鉴权：`bl auth login --console`（推荐，OAuth 浏览器登录）、`bl auth login --api-key <key>`（API Key 直接登录）、环境变量或配置文件持久化。
- 所有调用均需明确指定 `--region`（`cn`/`us`/`intl`）和 `--model`，例如：  
  `bl text chat --model qwen3.7-max --message "你好" --region cn`

## 限制和注意事项

- **API Key 权限**：权限由**归属业务空间**决定，同一空间内所有 API Key 权限一致。默认业务空间 Key 可调用所有标准模型；子业务空间 Key 仅能调用该空间已授权的模型 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。
- **地域隔离**：API Key 和服务端点（`base_url`）严格绑定地域。在北京地域创建的 Key **不可**用于调用美国弗吉尼亚的模型，反之亦然。
- **安全红线**：
  - API Key **明文仅显示一次**，关闭弹窗后无法恢复，丢失需重置。
  - **严禁**在代码、日志、聊天记录、公开仓库中硬编码或泄露 Key。
  - CLI 的 `--api-key` 参数仅本次生效，不落盘；持久化应使用 `bl auth login` 或 `bl config set`。
- **常见错误规避**：
  - `400-InvalidParameter` 类错误（如 `temperature` 超限、`messages` 格式错误）占绝大多数，务必按 [原文标题](../../raw/model-api-reference/preparations/error-code.md) 中的解决方案逐项校验。
  - 模型未开通将返回 `The product is not activated`，需前往 [模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market) 手动开通。
  - 文件类操作（Qwen-Long、Paraformer）对格式、大小（≤150 MB）、页数（≤1500）有严格限制，超限即报错。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


