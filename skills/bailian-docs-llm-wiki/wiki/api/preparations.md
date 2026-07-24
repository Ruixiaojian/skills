# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成基础环境准备：获取并安全配置 API Key、安装适用的 SDK 或 CLI 工具、理解关键参数约束及常见错误应对方式。这些步骤是所有模型调用（文本、图像、视频、语音、向量等）的通用前置条件，直接影响服务可用性与安全性。

## 支持的模型/功能

百炼平台支持全模态模型调用，包括但不限于：
- **文本生成**：`qwen3.7-max`、`qwen3-235b-a22b-instruct-2507` 等推理与思考模式模型；
- **多模态理解与生成**：`qwen3.5-omni-plus`（全模态对话）、`qwen-image-2.0`（文生图）、`happyhorse-1.0-t2v`（文生视频）；
- **语音与视觉**：`cosyvoice-v3-flash`（TTS）、`qwen3-vl-plus`（视觉描述）；
- **结构化能力**：支持 `response_format={"type": "json_object"}` 的结构化输出（需提示词含 `json` 关键词）；
- **工具调用（Function Calling）**：仅限 Qwen 系列及 DeepSeek 模型，不支持 `search` 作为工具名 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

> **注意**：文档 3 中列出的 `qwen3.5-omni-plus` 默认模型与文档 4 中 `qwen3-vl-plus` 的视觉模型命名不一致，实际应以控制台模型列表或 [模型 API 参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/) 中的最新 ID 为准；`qwen3-vl-plus` 是当前视觉理解推荐模型，而非 `qwen3.5-omni-plus` 的子集。

## 关键参数

调用时需关注以下核心参数及其取值范围（违反将触发 400 错误）：

| 参数 | 合法范围 | 说明 |
|------|----------|------|
| `temperature` | `[0.0, 2.0)` | 必须为浮点数，不可为整数或超出区间 [原文标题](../../raw/model-api-reference/preparations/error-code.md) |
| `top_p` | `(0.0, 1.0]` | 必须为浮点数，不可 ≤ 0 或 > 1 |
| `max_tokens` | `[1, 模型最大输出 Token]` | 超出将被拒绝，具体上限见各模型文档 |
| `n`（生成数量） | `[1, 4]`（文本）、`[1, 6]`（图像） | 图像生成 `bl image generate --n` 支持最多 6 张，但文本 `n` 严格限 4 |
| `seed` | `[0, 9223372036854775807]` | DashScope 协议下必须为非负整数，超长整型需确保语言层无截断 |
| `enable_thinking` | `true` / `false`（依模型而定） | 部分模型（如 `qwen3-235b-a22b-thinking-2507`）强制要求 `true`；开启时必须同时设 `stream=true` 且 `incremental_output=true` [原文标题](../../raw/model-api-reference/preparations/error-code.md) |
| `response_format` | `{"type": "json_object"}` | 结构化输出必需，且提示词中必须出现 `json` 字样 |

## 使用方式

### 1. 获取并配置 API Key  
- 通过 [百炼控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建（主账号或具备 `API-Key` 权限的子账号）；
- **地域差异**：华北2（北京）、新加坡等地域支持 IP 白名单与模型范围自定义权限；美国（弗吉尼亚）地域**不支持**自定义权限配置，仅提供基础创建与重置 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)；
- **安全实践**：务必配置为环境变量 `DASHSCOPE_API_KEY`（Linux/macOS/Windows 均有详细配置指南），避免硬编码；
- **密钥格式**：新创建 Key 以 `sk-ws` 开头（安全升级后），旧 `sk-` Key 仍可用但建议迁移。

### 2. 安装客户端工具  
- **SDK**：支持 DashScope SDK（Python/Java）与 OpenAI 兼容 SDK（Python/Node.js/Java/Go）；Python 要求 ≥ 3.8，Java ≥ 8，Node.js ≥ 22.12（CLI 专用） [原文标题](../../raw/model-api-reference/preparations/install-sdk.md)；
- **CLI**：`bailian-cli`（命令 `bl`）专为 AI Agent 设计，支持 `bl text chat`、`bl image generate` 等全模态命令，认证方式包括控制台 OAuth 登录、API Key 直接注入、环境变量或临时传参；
- **协议选择**：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)需指定 `base_url`（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`），Anthropic 兼容接口地址不同，务必按文档匹配。

### 3. 鉴权与端点  
- 除 API Key 外，**必须显式指定 `base_url`（即 API Host）**，其值随地域和协议变化，不可复用其他地域密钥的默认地址；
- 控制台创建时弹窗显示的 `API Host` 即为该地域对应协议的 `base_url`，SDK 初始化或 HTTP 请求中需准确传入。

## 限制和注意事项

- **地域隔离**：API Key 与地域强绑定。在北京地域创建的 Key **无法**直接用于美国（弗吉尼亚）服务，反之亦然；跨地域调用需分别创建 Key 并配置对应 `base_url`。
- **权限继承**：API Key 权限由其**归属业务空间**决定，同一空间内所有 Key 权限一致；子业务空间 Key 仅能访问已授权模型，未授权模型调用将返回 `Model not exist` 错误 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。
- **文件限制（Qwen-Long 等）**：上传文件需为纯文本格式（TXT/DOCX/PDF/EPUB/MOBI/MD），大小 < 150 MB，页数 < 15000，内容非空；图片类文件需先用 VL 模型提取文本 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。
- **流式强制要求**：思考模式模型（`enable_thinking=true`）、Qwen-Omni 音频输出、部分视觉模型**仅支持流式调用**，禁用 `stream` 将直接报错。
- **安全红线**：API Key 明文仅在创建弹窗中可见一次，关闭后不可恢复；切勿提交至代码仓库、日志或公开聊天记录；生产环境推荐使用 RAM 子账号 + 最小权限策略 + 环境变量注入。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


