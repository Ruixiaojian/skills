# preparations

在调用阿里云百炼平台的模型服务前，开发者需完成 SDK 安装、API Key 获取与配置、CLI 工具部署等基础准备。这些步骤共同构成安全、合规、可复用的接入前提，直接影响后续模型调用的稳定性与权限控制粒度。本文档整合关键操作路径与约束条件，面向工程实践提供结构化指引。

## 支持的模型/功能

百炼平台支持多模态模型调用，包括文本生成（如 `qwen3.7-max`）、图像生成（如 `qwen-image-2.0`）、视频生成（如 `happyhorse-1.1-t2v`）、语音合成（如 `cosyvoice`）、语音识别（如 `paraformer`）、向量嵌入（如 `text-embedding-v2`）及排序模型（如 `text-rerank`）。所有模型均通过统一 API 接口暴露，部分模型具备专属能力（如思考模式 `enable_thinking`、结构化输出 `response_format`），具体能力以[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)中开通状态为准。注意：**模型名称必须使用百炼官方 ID（如 `qwen3-235b-a22b-instruct-2507`），不可混用 Hugging Face 格式（如 `Qwen/Qwen3-235B-A22B-Instruct-2507`）**，否则将触发 `Model not exist` 错误 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `DASHSCOPE_API_KEY` | 鉴权凭证，用于 SDK 或 CLI 调用 | 必须配置为环境变量或显式传入；按量付费 Key 以 `sk-ws` 开头，[Token](../concepts/token.md) Plan Key 以 `sk-sp-` 开头 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md) |
| `base_url` / `--base-url` | 服务端点地址，随地域变化 | [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 Anthropic 兼容接口的 `base_url` 不同，需严格匹配文档要求 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md) |
| `--region` | 地域标识 | CLI 默认 `cn`（华北2），支持 `us`（美国弗吉尼亚）、`intl`（新加坡/东京/法兰克福） [原文标题](../../raw/model-api-reference/preparations/use-model-studio-cli.md) |
| `enable_thinking` | 启用思考模式 | 仅部分模型支持（如 `qwen3-235b-a22b-thinking-2507`），且必须配合 `stream=true` 和 `incremental_output=true` 使用；开启后禁用 `response_format=json_object` [原文标题](../../raw/model-api-reference/preparations/error-code.md) |
| `messages` / `prompt` | 输入内容 | 二者必须且仅存在其一；纯文本模型要求 `content` 为字符串，多模态模型允许 `content` 为含 `text`/`image_url` 的数组 [原文标题](../../raw/model-api-reference/preparations/error-code.md) |

> **注意**：文档 3 中 CLI 的 `--region` 参数默认值为 `cn`，但文档 2 明确列出支持地域包含“日本（东京）”和“德国（法兰克福）”，而 CLI 文档未说明 `intl` 是否覆盖这两个地域。实际使用时请以控制台地域列表和对应 `base_url` 为准，避免因地域不匹配导致 404 或鉴权失败。

## 使用方式

### SDK 安装与初始化
- **Python**：支持 `openai>=1.0` 或 `dashscope>=1.29.0`，要求 Python ≥ 3.8  
- **Java**：DashScope SDK 推荐最新版（Maven 坐标 `com.alibaba:dashscope-sdk-java`），OpenAI Java SDK 推荐 `3.5.0`  
- **Node.js/Go**：分别使用 `openai` npm 包或 `github.com/openai/openai-go/v3`，Go 要求 ≥ 1.22  
详细命令见 [原文标题](../../raw/model-api-reference/preparations/install-sdk.md)。

### API Key 管理
- 通过[百炼控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)创建，主账号或具备 `API-Key` 权限的子账号方可操作  
- **强烈建议配置为环境变量**（如 `DASHSCOPE_API_KEY`），避免硬编码泄露风险  
- 权限配置支持“全部”（调用所有模型）或“自定义”（IP 白名单 + 模型范围），美国（弗吉尼亚）地域暂不支持自定义 IP 白名单 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。

### CLI 快速接入
- 安装：`npm install -g bailian-cli`（Node ≥ 22.12.0）  
- 认证：推荐 `bl auth login --console`（浏览器 OAuth），备选 `bl auth login --api-key <key>`  
- 配置：`bl config set --key default-text-model --value qwen3.7-max` 设置默认模型  
- 验证：`bl text chat --message "ping" --non-interactive`  
完整命令参考见 [原文标题](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。

## 限制和注意事项

- **API Key 安全**：新创建 Key 仅在弹窗中显示一次明文，关闭后不可恢复；旧 Key（`sk-` 开头）仍可用，但建议迁移到 `sk-ws` 格式以获得更强保护 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。  
- **模型调用限制**：  
  - `n` 参数范围为 `[1, 4]`（文本生成）或 `[1, 6]`（图像生成），超限将返回 `400-InvalidParameter`  
  - `temperature` 必须 ∈ `[0.0, 2.0)`，`top_p` 必须 ∈ `(0.0, 1.0]`，`seed` 必须 ∈ `[0, 9223372036854775807]`  
  - Qwen-Long 等长文本模型要求输入文件为 TXT/DOCX/PDF/EPUB/MOBI/MD，不支持图片或扫描件 [原文标题](../../raw/model-api-reference/preparations/error-code.md)  
- **协议兼容性**：OpenAI SDK 调用需指定 `base_url` 并启用 `X-DashScope-OssResourceResolve: enable` 头才能解析临时 URL；而 `data:` 或 `file://` URL 仅 DashScope SDK 支持 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。  
- **错误排查**：所有 API 调用失败时，务必记录 `Request ID`（UUID 格式），并结合[错误码文档](../../raw/model-api-reference/preparations/error-code.md)定位原因；推荐使用阿里云 AI 助理输入错误信息自动诊断。

## 来源文档

- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


