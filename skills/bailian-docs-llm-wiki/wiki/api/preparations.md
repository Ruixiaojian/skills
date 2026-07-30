# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成基础环境准备：获取并安全配置 API Key、安装适用的 SDK 或 CLI 工具、理解关键参数约束及常见错误应对策略。这些步骤是所有模型调用的前置依赖，直接影响服务可用性与安全性。

## 支持的模型/功能

百炼平台支持[多模态](../concepts/multi-modal.md)模型调用，包括文本生成（如 `qwen3.7-max`）、图像生成（`qwen-image-2.0`）、视频生成（`happyhorse-1.0-t2v`）、语音合成（`cosyvoice-v3-flash`）、视觉理解（`qwen3-vl-plus`）及向量嵌入等。模型能力由其所属业务空间决定：**默认业务空间下的 API Key 可调用所有标准模型**；子业务空间下的 API Key 仅能调用该空间已授权的模型 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。部分模型（如 `qwen3-235b-a22b-thinking-2507`）强制启用思考模式，而 `qwen3-vl-plus` 等[多模态](../concepts/multi-modal.md)模型支持 `image_url` 等结构化 `content` 输入，纯文本模型（如 `qwen3-max`）则仅接受字符串类型 `content` [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

## 关键参数

调用时需注意以下核心参数范围与约束：
- `temperature`：必须在 `[0.0, 2.0)` 区间；
- `top_p`：必须在 `(0.0, 1.0]` 区间；
- `max_tokens`：上限取决于具体模型，不可超过文档标注的最大输出 [Token](../concepts/token.md) 数；
- `n`（生成数量）：图像类接口最多支持 `6`，文本类接口通常为 `[1, 4]`；
- `seed`：DashScope 协议下需为 `[0, 9223372036854775807]` 内整数；
- `enable_thinking`：开启时必须配合 `stream=true` 和 `incremental_output=true`，且禁用 `response_format={"type": "json_object"}` [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

> **注意**：文档 3 中 `bl text chat` 命令默认 `--model qwen3.7-max`，但文档 4 明确指出 `qwen3-235b-a22b-thinking-2507` 模型要求 `enable_thinking=true` 且不可设为 `false`。实际使用中应以模型文档为准，避免硬编码默认值导致 400 错误。

## 使用方式

### API Key 获取与配置
必须通过[主账号或具备管理员/API-Key 权限的子账号](../../raw/model-api-reference/preparations/get-api-key.md)在对应地域控制台创建 API Key。新创建的 Key 统一以 `sk-ws` 开头（美国弗吉尼亚地域除外），且**仅在创建弹窗中显示一次明文**，关闭后不可恢复。强烈建议将 `DASHSCOPE_API_KEY` 配置为环境变量（Linux/macOS 的 `~/.bashrc`/`~/.zshrc`，Windows 系统属性），避免代码硬编码 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。

### SDK 与 CLI 安装
- **SDK**：推荐使用 DashScope 官方 SDK（Python/Java）或 OpenAI 兼容 SDK（Python/Node.js/Java/Go）。Python 要求 `>=3.8`，Java 要求 `>=8`，Go 要求 `>=1.22` [原文标题](../../raw/model-api-reference/preparations/install-sdk.md)。
- **CLI**：百炼 CLI（`bailian-cli`）需 `Node.js >=22.12.0`，仅支持 `npm install -g bailian-cli` 安装。认证方式包括浏览器 OAuth 登录（推荐）、API Key 直接登录、环境变量或命令行临时传入 `--api-key` [原文标题](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。

## 限制和注意事项

- **地域与端点**：API Host（`base_url`）随地域变化，OpenAI 兼容与 Anthropic 兼容协议的端点不同，必须按接口文档指定。
- **权限隔离**：API Key 权限由归属业务空间决定，**同一空间内所有 Key 权限相同**，无需为不同模型单独创建 Key [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。
- **安全红线**：禁止在代码、日志、聊天记录中明文存储或传输 API Key；CI/CD 环境应通过密钥管理服务注入，而非硬编码。
- **错误处理**：`Model not exist` 错误通常因模型未在控制台[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)开通所致；`Arrearage` 表示账号欠费，需充值后等待系统同步 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。
- **文件限制**：Qwen-Long 模型仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD 格式，单文件 ≤150 MB，且 page limit ≤1500 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


