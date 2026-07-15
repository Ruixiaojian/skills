# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成 API Key 获取、SDK/CLI 安装与配置、环境变量设置等基础准备。这些步骤是所有后续调用（文本生成、多模态理解、语音合成等）的前提，直接影响鉴权有效性、调用协议兼容性及安全性。本文档结构化梳理关键环节，聚焦可操作项，避免冗余说明。

## 支持的模型/功能

百炼平台支持全模态能力调用，包括：
- **文本生成**：如 `qwen3.7-max`、`qwen3-235b-a22b-instruct-2507` 等大语言模型；
- **多模态理解与生成**：`qwen3-vl-plus`（视觉理解）、`qwen-image-2.0`（文生图）、`happyhorse-1.0-t2v`（文生视频）；
- **语音处理**：`cosyvoice-v3-flash`（TTS）、`paraformer-real-time`（ASR）；
- **向量与排序**：`text-embedding-v3`、`text-rerank-v3`。

所有模型均通过统一 API Key 鉴权，**无需为不同模型创建独立密钥**；权限由 API Key 所属业务空间决定，详见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md) 中“API Key权限说明”章节。

> **注意**：文档 3 中 CLI 命令示例默认使用 `qwen3.7-max` 作为文本模型，但文档 4 的错误码明确指出部分思考模式模型（如 `qwen3-235b-a22b-thinking-2507`）**强制要求 `enable_thinking=true`**，且不支持非流式调用。实际选型需以[模型列表文档](https://help.aliyun.com/zh/model-studio/model-list)为准，不可仅依赖 CLI 默认值。

## 关键参数

| 参数 | 说明 | 取值范围/格式 | 来源依据 |
|------|------|----------------|----------|
| `DASHSCOPE_API_KEY` | 鉴权凭证，必须配置为环境变量或显式传入 | `sk-ws-` 开头（新密钥）或 `sk-` 开头（旧密钥），长度固定 | [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md) |
| `base_url` / `--base-url` | 服务端点地址，随地域和协议变化 | 如 `https://dashscope.aliyuncs.com/api/v1`（OpenAI 兼容）或 `https://dashscope.aliyuncs.com/anthropic/v1`（Anthropic 兼容） | [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md) |
| `--region` | 地域标识 | `cn`（华北2）、`us`（弗吉尼亚）、`intl`（新加坡/东京等） | [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md) |
| `enable_thinking` | 启用思考模式 | `true` 或 `false`，部分模型强制为 `true` | [错误码](../../raw/model-api-reference/preparations/error-code.md) |
| `stream` | 启用[流式输出](../concepts/streaming-output.md) | `true`（必需用于思考模式、Qwen-Omni 音频输出等） | [错误码](../../raw/model-api-reference/preparations/error-code.md) |

## 使用方式

### 1. 获取并配置 API Key
- 通过[控制台](https://bailian.console.aliyun.com/)创建 API Key，**主账号或具备 `API-Key` 权限的子账号**方可操作；
- 创建时选择 **全部权限**（快速上手）或 **自定义权限**（IP 白名单 + 模型范围）；
- **强烈建议配置为环境变量**：Linux/macOS 使用 `export DASHSCOPE_API_KEY="sk-ws-xxx"`，Windows 使用系统属性或 PowerShell 的 `[Environment]::SetEnvironmentVariable`；
- 美国（弗吉尼亚）地域不支持禁用/重置操作，且不显示完整明文密钥，需立即保存。

### 2. 安装调用工具
- **SDK 方式**：  
  - Python：`pip install -U dashscope`（原生）或 `pip install -U openai`（OpenAI 兼容）；  
  - Java/Node.js/Go：参考对应语言的 SDK 依赖声明（如 Maven/Gradle/GitHub）；  
- **CLI 方式**：  
  - 要求 Node.js ≥ 22.12.0，仅支持 `npm install -g bailian-cli`；  
  - 认证推荐 `bl auth login --console`（浏览器 OAuth），备选 `bl auth login --api-key <key>`；  
  - 支持 `--api-key` 临时传入、环境变量、配置文件三种鉴权方式，互不冲突。

### 3. 发起调用
- 代码中：SDK 初始化时传入 `api_key` 和 `base_url`（如 `dashscope.ApiKeyAuth(api_key=..., base_url=...)`）；
- CLI 中：全局参数 `--api-key`、`--region`、`--base-url` 可覆盖配置；
- HTTP 请求：Header 中添加 `Authorization: Bearer sk-ws-xxx`，Body 指定 `model` 和 `messages`（或 `prompt`）。

## 限制和注意事项

- **密钥安全**：API Key 创建后**仅一次明文展示机会**（除美国地域外），关闭弹窗即不可恢复；禁止硬编码、日志打印、Git 提交；建议定期轮换。
- **地域隔离**：API Key 与地域强绑定，华北2 创建的 Key 无法直接调用美国地域服务，需切换 `--region` 或创建对应地域 Key。
- **参数强约束**：  
  - `temperature` 必须 ∈ [0.0, 2.0)，`top_p` ∈ (0.0, 1.0]，`n` ∈ [1, 4]（图像生成最多 6 张，但 `n` 参数上限为 4）；  
  - 思考模式（`enable_thinking=true`）**必须启用 `stream=true`**，且 `result_format` 固定为 `"message"`；  
  - 结构化输出（`response_format={"type": "json_object"}`）**与思考模式互斥**，需关闭 `enable_thinking`。
- **输入限制**：  
  - `messages` 数组不能为空；纯文本模型禁止 `content` 为数组（含 `image_url` 等多模态元素），否则报错 `Unexpected item type in content`；  
  - 文件类调用（Qwen-Long）要求文件 ≤ 150 MB、≤ 15000 页、内容非空，且仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD 格式。
- **模型兼容性**：  
  - OpenAI SDK 调用需严格匹配百炼的[OpenAI 兼容接口规范](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope)，如 `messages` 必须嵌套在 `input` 对象内（DashScope 协议）或平级（OpenAI 协议）；  
  - 不同 SDK 对 `seed` 等参数的校验逻辑可能差异（如 DashScope 协议要求 `seed ∈ [0, 9223372036854775807]`），应以[错误码文档](../../raw/model-api-reference/preparations/error-code.md)为准排障。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


