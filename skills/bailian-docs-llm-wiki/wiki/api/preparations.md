# preparations

在调用阿里云百炼平台的模型服务前，开发者需完成 SDK 安装、API Key 获取与配置、CLI 工具准备等基础环境搭建。这些步骤共同构成服务调用的前提条件，直接影响后续模型调用的可用性、安全性与兼容性。本文档系统梳理了核心准备事项，涵盖支持的接入方式、关键参数约束、典型使用路径及常见限制。

## 支持的模型/功能

百炼平台通过统一 API 接口支持多类模型能力，包括文本生成（如 `qwen3.7-max`）、图像生成（如 `qwen-image-2.0`）、视频生成（如 `happyhorse-1.0-t2v`）、语音合成（如 `cosyvoice-v3-flash`）、语音识别（Paraformer）、向量嵌入（Embedding）和排序（Rerank）等。所有模型均需通过已开通的服务调用——未在[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)中开通的模型将返回 `The product is not activated` 错误 [错误码](../../raw/model-api-reference/preparations/error-code.md)。部分模型（如 `qwen3-235b-a22b-thinking-2507`）对参数有强约束，例如 `enable_thinking` 必须为 `true`；而思考模式模型（如 Qwen3/QwQ 系列）仅支持[流式输出](../concepts/streaming-output.md)，非流式调用会触发 `400-InvalidParameter` 错误 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

> **注意**：文档 3 中列出的 CLI 默认模型 `qwen3.7-max` 与文档 4 示例错误码中出现的 `qwen3-235b-a22b-instruct-2507` 均属有效模型 ID，但二者能力与参数要求不同。开发者应以[模型列表文档](https://help.aliyun.com/zh/model-studio/model-list)为准，不可混用开源社区命名（如 `Qwen/Qwen3-235B-A22B-Instruct-2507`），否则将报 `Model not exist` 错误 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 关键参数

调用时需关注以下核心参数及其取值范围：
- `temperature`：必须在 `[0.0, 2.0)` 区间；
- `top_p`：必须在 `(0.0, 1.0]` 区间；
- `max_tokens`：必须在 `[1, 模型最大输出 Token 数]` 范围内；
- `n`（生成数量）：图像生成最多支持 `6`，文本生成默认为 `1`，部分接口上限为 `4`；
- `seed`：DashScope 协议下需为 `[0, 9223372036854775807]` 内整数；
- `response_format`：结构化输出需设为 `{"type": "json_object"}`，且提示词中必须包含 `json` 关键词；
- `enable_thinking`：开启时必须同时设置 `stream=true` 和 `incremental_output=true`，且禁用 `response_format` 的 JSON 模式；
- `messages`：纯文本模型仅接受字符串型 `content`，[多模态](../concepts/multi-modal.md)模型（如 `qwen3-vl-plus`）才支持 `content` 数组含 `image_url` 等对象。

## 使用方式

### SDK 接入
支持两种 SDK 路径：
- **DashScope SDK**：官方维护，提供 Python、Java、Node.js、Go 等语言支持，推荐用于需要深度集成或使用百炼特有功能（如文件上传、异步任务轮询）的场景 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。
- **OpenAI 兼容 SDK**：支持 Python、Node.js、Java、Go，适用于已适配 OpenAI 接口的项目快速迁移，但需注意：视觉/音频理解等[多模态](../concepts/multi-modal.md)能力仅 DashScope SDK 支持 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

### CLI 工具
百炼 CLI（`bailian-cli`）面向 AI Agent 场景设计，需 Node.js ≥ 22.12.0，仅支持 `npm install -g bailian-cli` 安装。认证方式包括浏览器 OAuth 登录（推荐）、API Key 直接登录、环境变量或命令行临时传入。CLI 提供 `bl text chat`、`bl image generate` 等子命令，支持地域切换（`--region cn|us|intl`）、输出格式控制（`--output json`）及并发请求（`--concurrent`）等能力 [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。

### API Key 配置
API Key 是核心鉴权凭证，必须通过[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)创建。建议配置为环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄露风险。不同地域（如华北2、美国弗吉尼亚）的 API Host（`base_url`）不同，且 OpenAI 兼容与 Anthropic 兼容协议的端点地址亦不相同，需按实际接口文档指定 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

## 限制和注意事项

- **API Key 安全**：新创建的 API Key 以 `sk-ws` 开头，创建后仅展示一次明文，关闭弹窗即不可恢复；旧 `sk-` 密钥仍可用，但建议升级。美国（弗吉尼亚）地域不支持禁用/重置操作 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **地域与权限隔离**：API Key 权限由其归属业务空间决定，同一空间内所有 Key 权限一致；子业务空间下的 Key 仅可调用该空间已授权的模型 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **文件限制**：Qwen-Long 模型仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD 纯文本文件，单文件 ≤150 MB，且页数 ≤1500；图片类文件需先用 Qwen-VL 提取文本 [错误码](../../raw/model-api-reference/preparations/error-code.md)。
- **网络与依赖**：百炼 CLI 强制要求 Node.js ≥22.12.0 及 npm（禁用 pnpm/yarn）；Python SDK 要求 `python >= 3.8`；Go SDK 要求 `Go 1.22+` [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。
- **错误处理**：常见错误如 `Arrearage`（账号欠费）、`InvalidParameter`（参数越界）、`Model not exist`（模型未开通）等，均可通过[阿里云 AI 助理](https://www.aliyun.com/ai-assistant/)输入错误信息快速定位 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)




