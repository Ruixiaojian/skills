# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成基础环境准备，包括获取并安全配置 API Key、安装必要的 SDK 或 CLI 工具、理解关键参数约束及常见错误应对策略。这些步骤直接影响服务调用的可用性、安全性与稳定性，是所有集成工作的前提。

## 支持的模型/功能

百炼平台支持[多模态](../concepts/multi-modal.md)模型调用，涵盖文本生成（如 `qwen3.7-max`）、图像生成（`qwen-image-2.0`）、视频生成（`happyhorse-1.0-t2v`）、语音合成（`cosyvoice-v3-flash`）、视觉理解（`qwen3-vl-plus`）及向量/排序等能力。模型能力与协议兼容性密切相关：  
- **OpenAI 兼容协议**：适用于 `openai` SDK（Python/Node.js/Java/Go），需指定对应地域的 `base_url`（见 [使用API Key](../../raw/model-api-reference/preparations/get-api-key.md) 中“服务端点”说明）；  
- **Anthropic 兼容协议**：仅限特定模型（如 `qwen3.5-omni-plus`），通过 `bl omni` 等 CLI 命令调用；  
- **DashScope 原生协议**：推荐使用 `dashscope` SDK（Python/Java），对参数校验更严格，且部分功能（如文件上传解析）仅原生支持。  
> **注意**：文档 4 中明确指出，`Qwen-Max` 等纯文本模型**不支持图片等[多模态](../concepts/multi-modal.md)输入**，若 `messages` 中混入 `image_url` 会触发 `Unexpected item type in content` 错误；必须改用 `qwen3-vl-plus` 等[多模态](../concepts/multi-modal.md)模型，详见 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 关键参数

调用时需关注以下核心参数及其约束（违反将导致 400 错误）：  
- **`model`**：必须为百炼控制台公布的模型 ID（如 `qwen3.7-max`），**不可混用开源社区命名**（如 `Qwen/Qwen3-235B...`）；  
- **`temperature`**：范围 `[0.0, 2.0)`，`top_p` 范围 `(0.0, 1.0]`，`repetition_penalty > 0.0`；  
- **流式与思考模式**：开启 `enable_thinking` 时，**必须同时设置 `stream=true` 且 `incremental_output=true`**，否则报错；部分模型（如 `qwen3-235b-a22b-thinking-2507`）甚至强制 `enable_thinking=true`；  
- **结构化输出**：启用 `response_format={"type": "json_object"}` 时，提示词中**必须包含 `json` 关键词**，且 `enable_thinking` 必须为 `false`；  
- **`seed`**：DashScope 协议下范围 `[0, 9223372036854775807]`，CLI 默认启用但非必需；  
- **`messages` 格式**：纯文本模型要求 `content` 为字符串；多模态模型要求 `content` 数组中每个元素为合法对象（`type` 仅限 `text`/`image_url`/`video_url` 等），禁止嵌套数组或布尔值。

## 使用方式

### 获取与配置 API Key  
必须通过[阿里云百炼控制台](https://bailian.console.aliyun.com/)创建 API Key（主账号或具备 `API-Key` 权限的子账号），并按地域选择对应入口（如华北2、新加坡、美国弗吉尼亚）。创建时建议权限选“全部”，或自定义 IP 白名单与模型范围。**强烈推荐将 Key 配置为环境变量 `DASHSCOPE_API_KEY`**，避免硬编码（Linux/macOS/Windows 配置方法详见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)）。新创建 Key 以 `sk-ws` 开头，明文仅显示一次，丢失需重置。

### 安装客户端工具  
- **SDK**：Python 用户可选 `openai`（`pip install -U openai`）或 `dashscope`（`pip install -U dashscope`）；Java/Node.js/Go 用户参考对应语言的 SDK 文档；  
- **CLI**：仅支持 `npm install -g bailian-cli`（Node ≥ 22.12.0），认证方式包括浏览器登录（推荐）、`bl auth login --api-key` 或环境变量；CLI 提供 `bl text chat`/`bl image generate` 等命令，支持地域切换（`--region cn|us|intl`）与异步任务管理（`--no-wait`）；  
- **第三方工具**：Chatbox、Postman、Dify 等需手动填入 API Key 与 `base_url`，详见 [使用API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

## 限制和注意事项

- **地域隔离**：API Key 与服务端点（`base_url`）强绑定地域，跨地域调用失败；美国（弗吉尼亚）地域不支持 API Key 禁用/重置操作；  
- **安全约束**：API Key 不可公开（代码/日志/聊天记录），CLI 在交互式安装中禁止回显完整 Key，CI 环境应通过密钥管理注入；  
- **文件限制**：Qwen-Long 模型仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD，单文件 ≤ 150 MB 且 ≤ 15000 页；视觉/音频模型要求 URL 以 `http://`/`https://`/`data:`/`file://` 开头；  
- **错误处理**：常见错误如 `Model not exist`（模型名错误）、`Arrearage`（账号欠费）、`Range of input length should be [1, xxx]`（[Token](../concepts/token.md) 超限）等，均需按 [错误码](../../raw/model-api-reference/preparations/error-code.md) 文档定位；  
- **兼容性差异**：OpenAI SDK 调用时，`messages` 需直接置于请求体顶层；DashScope SDK 则需包裹在 `input.messages` 中，格式错误将触发 `Required body invalid`。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


