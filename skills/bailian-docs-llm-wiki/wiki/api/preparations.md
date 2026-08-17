# preparations

在调用百炼平台模型服务前，开发者需完成 API Key 获取与配置、SDK 或 CLI 工具安装、环境适配等基础准备。这些步骤直接影响调用的安全性、兼容性与稳定性，是所有模型调用（文本、图像、语音、视频、向量等）的共同前置条件。本文档整合关键实践路径，聚焦可执行的技术要点。

## 支持的模型/功能

百炼平台支持全模态模型调用，包括：
- **文本生成**：如 `qwen3-235b-a22b-instruct-2507`、`qwen3.7-max`、`deepseek-r1` 等；
- **[多模态](../concepts/multi-modal.md)理解与生成**：如 `qwen3-vl-plus`（视觉理解）、`qwen3.5-omni-plus`（全模态对话）、`qwen-image-2.0`（文生图）、`happyhorse-1.1-t2v`（文生视频）；
- **语音与音频**：如 `cosyvoice`（TTS）、`paraformer`（ASR）；
- **结构化能力**：如 `response_format: {"type": "json_object"}`（需提示词含 `json` 关键词）；
- **高级功能**：思考模式（`enable_thinking=true`，仅限流式）、联网搜索（`enable_search=true`，需模型支持）、工具调用（`tool_calls`）等。

> **注意**：文档 4 明确指出 `Model not exist.` 错误的常见原因是混用开源社区模型名（如 `Qwen/Qwen3-235B...`）与百炼官方模型 ID（如 `qwen3-235b-a22b-instruct-2507`），请严格以 [模型列表](https://help.aliyun.com/zh/model-studio/models) 中的 ID 为准。该约束在 [原文标题](../../raw/model-api-reference/preparations/error-code.md) 中有详细说明。

## 关键参数

调用时需关注以下核心参数及其取值范围（违反将触发 400 错误）：

| 参数 | 合法范围 | 说明 |
|------|----------|------|
| `temperature` | `[0.0, 2.0)` | 文档 4 要求必须为浮点数，且严格小于 2.0 |
| `top_p` | `(0.0, 1.0]` | 必须大于 0 且小于等于 1 |
| `max_tokens` | `[1, 模型最大输出 Token 数]` | 具体上限见各模型文档 |
| `n`（生成数量） | `[1, 4]`（文本）或 `[1, 6]`（图像） | 图像生成上限为 6，见 [原文标题](../../raw/model-api-reference/preparations/use-model-studio-cli.md) |
| `seed` | `[0, 9223372036854775807]` | DashScope 协议下整数范围严格限定 |
| `thinking_budget` | 正整数，≤ 模型最大思维链长度 | 详见模型列表中“思维链长度”字段 |
| `enable_thinking` | `true` 或 `false`，部分模型强制为 `true` | 如 `qwen3-235b-a22b-thinking-2507` 不允许设为 `false` |

此外，结构化输出（`response_format={"type":"json_object"}`）要求提示词中必须包含 `json` 字样；思考模式与结构化输出互斥，启用前者时需关闭后者。

## 使用方式

### 1. 获取与配置 API Key  
通过 [百炼控制台密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建 API Key，并按归属账号（主账号或 RAM 用户）、业务空间（默认空间支持全部标准模型）、权限（IP 白名单/模型范围）进行精细化配置。推荐将 Key 配置为环境变量 `DASHSCOPE_API_KEY`，支持 Linux/macOS/Windows 全平台永久或临时设置，具体方法详见 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。

### 2. 安装 SDK 或 CLI  
- **SDK**：支持 OpenAI 兼容 SDK（Python/Node.js/Java/Go）或 DashScope 官方 SDK（Python/Java）。Python 环境需 `>=3.8`，Java 需 `>=8`，Go 需 `>=1.22`。安装命令统一为 `pip install -U openai` 或 `pip install -U dashscope`。  
- **CLI**：`bailian-cli`（命令 `bl`）专为 AI Agent 设计，需 Node.js `>=22.12.0`，仅支持 `npm install -g bailian-cli` 安装。认证支持控制台 OAuth 登录（推荐）、API Key 直接登录、环境变量、配置文件等多种方式，详见 [原文标题](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。

### 3. 调用入口  
- **HTTP 接口**：Base URL 分中国大陆版 `https://dashscope.aliyuncs.com/compatible-mode/v1` 与国际版 `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`；  
- **SDK/CLI**：自动适配，无需手动拼接 URL。

## 限制和注意事项

- **API Key 安全**：严禁在客户端代码（浏览器、移动 App）或不可信环境中硬编码长期有效 Key；高风险场景应使用 [临时 API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)（最长 1800 秒）。  
- **地域与网络**：IPv6 白名单仅华北2（北京）支持；美国（弗吉尼亚）仅支持 IPv4；CLI 安装需确保能访问 `registry.npmjs.org`，否则需配置镜像代理。  
- **模型能力边界**：纯文本模型（如 `qwen3-max`）不支持 `image_url` 等[多模态](../concepts/multi-modal.md) `content`，否则报错 `Unexpected item type in content`；思考模式模型（如 `qwen3.5-omni-plus`）强制要求 `stream=true` 和 `incremental_output=true`，详见 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。  
- **调试与排障**：所有失败请求务必记录 `Request ID`（UUID 格式），用于自助排查或提交工单；JSON 请求体需通过 `jsonlint.com` 等工具校验语法，避免因引号缺失、逗号冗余等低级错误导致 `Required body invalid`。

## 来源文档

- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


