# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成基础环境准备：获取并安全配置 API Key、安装适用的 SDK 或 CLI 工具、理解关键参数约束及常见限制。这些步骤是所有模型调用（文本、图像、语音、视频、向量等）的前置依赖，直接影响服务可用性与安全性。

## 支持的模型/功能

百炼平台支持全模态模型调用，包括：
- **文本生成**：如 `qwen3.7-max`、`qwen3-235b-a22b-instruct-2507` 等；
- **[多模态](../concepts/multimodal.md)理解与生成**：如 `qwen3.5-omni-plus`（全模态）、`qwen-image-2.0`（文生图）、`happyhorse-1.1-t2v`（文生视频）；
- **语音与视觉专用模型**：如 `cosyvoice`（TTS）、`paraformer`（ASR）、`qwen3-vl-plus`（视觉描述）；
- **结构化能力**：支持 `response_format={"type": "json_object"}` 的结构化输出（需提示词含 `json` 关键词）；
- **高级功能**：思考模式（`enable_thinking=true`）、联网搜索（`enable_search=true`）、工具调用（`tools` 参数）等，但需模型显式支持（参见[错误码文档](../../raw/model-api-reference/preparations/error-code.md)中“Model does not support enable_search”等条目）。

> **注意**：文档 3 中列出的 `qwen3.5-omni-plus` 为当前推荐全模态模型，但文档 4 的错误码说明指出 `qwen3-vl-plus` 才是视觉理解（`bl vision describe`）的默认模型——二者用途不同，不可混用。实际选型应以 [模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market) 中的最新支持列表为准。

## 关键参数

调用时需关注以下核心参数及其约束（违反将触发 400 错误）：
- `model`：必须为百炼控制台模型市场中已开通的**精确模型 ID**（如 `qwen3.7-max`），大小写敏感，不可使用开源社区命名（如 `Qwen/Qwen3-235B...`）；
- `temperature`：取值范围 `[0.0, 2.0)`，非浮点数将报错；
- `top_p`：取值范围 `(0.0, 1.0]`；
- `max_tokens`：必须在 `[1, 模型最大输出 Token 数]` 内，上限见各模型文档；
- `n`（生成数量）：图像类接口最多支持 `6`，文本类接口通常为 `1`（部分模型支持 `4`）；
- `seed`：DashScope 协议下需为 `[0, 9223372036854775807]` 内整数；
- `enable_thinking`：仅特定模型（如 `qwen3-235b-a22b-thinking-2507`）支持，且开启时强制要求 `stream=true`、`incremental_output=true`、`result_format="message"`，且**不支持结构化输出**（`response_format=json_object`）；
- `messages`：纯文本模型禁止 `content` 为数组（如 `[{type: "text", text: "..."}]`），必须为字符串；[多模态](../concepts/multimodal.md)模型则需严格按 `{"type": "text"/"image_url"/"video_url", ...}` 格式构造。

## 使用方式

### 1. 获取与配置 API Key  
必须通过 [阿里云百炼控制台](https://bailian.console.aliyun.com/) 创建 API Key，并**立即保存明文**（关闭弹窗后不可再查看）。密钥格式已升级：新创建的 Key 以 `sk-ws` 开头（旧 `sk-` Key 仍可用）。推荐配置为环境变量 `DASHSCOPE_API_KEY`，避免硬编码（详见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md) 文档）。

### 2. 安装客户端工具  
- **SDK**：支持 DashScope（Python/Java）和 OpenAI 兼容 SDK（Python/Node.js/Java/Go）。Python 用户可任选 `pip install -U dashscope` 或 `pip install -U openai`；Java 用户需按文档添加对应 Maven/Gradle 依赖（参见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）。  
- **CLI**：通过 `npm install -g bailian-cli` 安装，支持 `bl text chat`、`bl image generate` 等命令。认证推荐 `bl auth login --console`（浏览器 OAuth），或 `bl auth login --api-key <key>`（适用于无界面环境）（参见 [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)）。

### 3. 指定服务端点（base_url）  
除 API Key 外，**必须指定 `base_url`**（即创建 API Key 时弹窗显示的 API Host）。[OpenAI 兼容接口](../concepts/openai-compatible-api.md)与 Anthropic 兼容接口的 `base_url` 不同，且随地域变化（如北京、新加坡、弗吉尼亚），请以具体接口文档为准。

## 限制和注意事项

- **地域与权限隔离**：API Key 的可用模型取决于其**归属业务空间**。默认空间 Key 可调用所有标准模型；子业务空间 Key 仅能调用该空间已授权的模型。美国（弗吉尼亚）地域不支持 IP 白名单与模型范围自定义权限（参见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)）。
- **安全约束**：  
  - API Key 明文仅创建时可见一次，丢失需重置；  
  - 禁止在代码、日志、聊天记录中硬编码或明文传输 Key；  
  - CLI 工具要求 Node.js ≥ 22.12.0，且**仅允许 `npm` 全局安装**（禁用 `pnpm`/`yarn`）；  
  - 环境变量配置需在新终端会话中 `source` 生效（Linux/macOS）或重启 CMD/PowerShell（Windows）。
- **模型能力限制**：  
  - 部分模型（如 `qwen3-235b-a22b-thinking-2507`）强制要求 `enable_thinking=true`，不可设为 `false`；  
  - Qwen-Long 模型仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD 纯文本文件，不支持图片或扫描件；  
  - 视觉模型（如 `qwen3-vl-plus`）传入 URL 必须以 `http://`、`https://`、`data:` 或 `file://` 开头，且 `data:` 前需含 `base64` 标识。
- **错误排查**：调用失败时务必记录 `Request ID`（响应 Header 或 Body 中），并结合 [错误码文档](../../raw/model-api-reference/preparations/error-code.md) 定位原因（如 `Arrearage` 表示账号欠费，`Model not exist` 表示模型未开通）。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


