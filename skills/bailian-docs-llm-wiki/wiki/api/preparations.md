# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成基础环境准备，包括获取并安全配置 API Key、安装合适的 SDK 或 CLI 工具、理解关键参数约束及常见限制。这些步骤是所有 API 调用和本地开发的前提，直接影响服务可用性、安全性与调试效率。

## 支持的模型/功能

百炼平台支持多类模型与能力，涵盖文本生成（如 `qwen3-max`、`qwen3-235b-a22b-instruct-2507`）、图像生成（`qwen-image-2.0`）、视频生成（`happyhorse-1.0-t2v`）、语音合成（`cosyvoice-v3-flash`）、语音识别（`paraformer-real-time`）、向量嵌入（`text-embedding-v3`）、排序（`text-rerank-v3`）及全模态理解（`qwen3.5-omni-plus`）。部分模型具备特定能力约束，例如：
- 思考模式（`enable_thinking=true`）仅适用于指定模型（如 `qwen3-235b-a22b-thinking-2507`），且强制要求 `stream=true` 与 `incremental_output=true`；
- 结构化输出（`response_format={"type": "json_object"}`）不支持与思考模式共用；
- 联网搜索（`enable_search=true`）仅限明确标注支持该能力的模型；
- 工具调用（`tools` 参数）仅被 Qwen 和 DeepSeek 系列模型支持，纯文本模型（如 `qwen3-max`）若传入含 `image_url` 的 `messages` 将报错 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

## 关键参数

调用时需注意以下核心参数的合法范围与互斥关系（详见 [原文标题](../../raw/model-api-reference/preparations/error-code.md)）：
- `temperature`：必须在 `[0.0, 2.0)` 区间；
- `top_p`：必须在 `(0.0, 1.0]` 区间；
- `max_tokens`：不得超过模型文档中声明的最大输出 [Token](../concepts/token.md) 数；
- `n`：取值范围为 `[1, 4]`；
- `seed`：DashScope 协议下需为 `[0, 9223372036854775807]` 内整数；
- `thinking_budget`：须为正整数且不超过模型最大思维链长度；
- `stop`：仅接受 `str`、`list[str]`、`list[int]` 或 `list[list[int]]` 类型，且列表内元素类型必须一致；
- `messages`：纯文本模型要求 `content` 为字符串；[多模态](../concepts/multi-modal.md)模型要求 `content` 数组中每个元素为合法对象（`type` 仅限 `text`/`image_url`/`video_url` 等）；
- `response_format`：结构化输出必须设为 `{"type": "json_object"}`，且提示词中需包含 `json` 关键词。

> **注意**：文档 3 中“`The value of the enable_thinking parameter is restricted to True`”与文档 1 中“API Key 权限说明”存在隐含矛盾——前者指出部分模型强制开启思考模式，后者未提及该限制对权限配置的影响。实际调用时应以模型文档为准，而非仅依赖 API Key 权限设置。

## 使用方式

### API Key 获取与配置
需使用主账号或具备 `管理员`/`API-Key` 页面权限的子账号，在对应地域（如华北2、新加坡、美国弗吉尼亚）的 [API Key 管理页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建密钥。新创建的密钥以 `sk-ws` 开头，明文仅显示一次，务必立即保存 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。推荐将 `DASHSCOPE_API_KEY` 配置为环境变量（Linux/macOS/Windows 均有详细步骤），避免硬编码。

### SDK 安装
- **Python**：可选 `openai`（OpenAI 兼容协议）或 `dashscope`（原生协议）SDK，均需 `pip install -U <package>`；
- **Java/Node.js/Go**：DashScope 提供官方 Java SDK；OpenAI SDK 支持多语言（Java/Node.js/Go），其中 Go 需 `Go 1.22+` 并建议配置阿里云镜像代理；
- **CLI 工具**：通过 `npm install -g bailian-cli` 安装百炼 CLI（要求 Node.js ≥ 22.12.0），支持 `bl text chat`、`bl image generate` 等命令行调用 [原文标题](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。

### 协议与端点
调用时除 API Key 外，**必须指定服务端点（API Host）**，其值取决于所选协议与地域：
- OpenAI 兼容协议：`base_url` 为 `https://dashscope.aliyuncs.com/v1`（中国站）或对应国际站地址；
- Anthropic 兼容协议：`base_url` 为 `https://dashscope.aliyuncs.com/anthropic/v1`；
- 不同地域的端点不同，务必以控制台创建 API Key 时弹窗显示的 `API Host` 为准。

## 限制和注意事项

- **API Key 安全**：`sk-` 开头旧密钥仍可用，但新密钥统一为 `sk-ws` 格式，且不可再次查看明文。美国（弗吉尼亚）地域不支持禁用/重置操作。
- **地域隔离**：API Key 与模型服务绑定地域，跨地域调用需对应地域的 API Key 和端点。
- **IP 白名单**：仅北京、新加坡等部分地域支持自定义 IP 白名单（最多 20 个 IPv4/IPv6 地址或网段），美国（弗吉尼亚）地域不支持。
- **文件限制**：Qwen-Long 模型仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD 纯文本文件，单文件大小 ≤ 150 MB、页数 ≤ 15000、内容非空；图片/扫描件需先用 Qwen-VL 提取文本。
- **[Token](../concepts/token.md) 限制**：输入总长度（含 messages、[prompt](../guides/prompt.md)、file content）不得超过模型最大上下文窗口；纯文本模型不支持[多模态](../concepts/multi-modal.md) `content`，否则触发 `Unexpected item type in content` 错误。
- **CLI 环境约束**：百炼 CLI 严格依赖 npm（非 pnpm/yarn）且要求 Node.js ≥ 22.12.0；认证方式中，`bl auth login --console` 推荐用于交互式场景，`--api-key` 适用于 CI/CD 或无浏览器环境。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)


