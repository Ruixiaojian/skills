# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成基础环境准备：获取并安全配置 API Key、选择合适的 SDK 或 CLI 工具、理解关键参数约束及常见错误边界。这些步骤直接影响服务可用性、安全性与调试效率，是所有集成工作的前提。

## 支持的模型/功能

百炼平台提供全模态模型能力，包括文本生成（如 `qwen3.7-max`）、图像生成（`qwen-image-2.0`）、视频生成（`happyhorse-1.0-t2v`）、语音合成（`cosyvoice-v3-flash`）、视觉理解（`qwen3-vl-plus`）及向量/排序等专用模型。不同模型对输入格式、协议兼容性（OpenAI 或 Anthropic）和调用方式有明确要求。例如，Qwen-Omni 模型仅支持[流式输出](../concepts/streaming-output.md)，而 Qwen-Long 仅接受纯文本类文件（TXT/DOCX/PDF 等），不支持图片或扫描件 [错误码](../../raw/model-api-reference/preparations/error-code.md)。多模态模型（如 `qwen3.5-omni-plus`）支持 `image`、`audio`、`video` 参数混合输入，纯文本模型则严格拒绝非字符串 `content` [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 关键参数

核心参数需严格遵循取值范围与类型约束：
- `temperature`: 必须在 `[0.0, 2.0)` 区间；
- `top_p`: 必须在 `(0.0, 1.0]` 区间；
- `max_tokens`: 上限由具体模型文档定义，不可超过其最大输出 Token 数；
- `n`: 图像/文本批量生成数，范围为 `[1, 4]`（部分 CLI 命令如 `bl image generate` 支持最多 6 张，属工具层扩展，非 API 层通用限制）；
- `seed`: DashScope 协议下必须为 `[0, 9223372036854775807]` 内整数；
- `enable_thinking`: 仅特定模型（如 `qwen3-235b-a22b-thinking-2507`）强制设为 `true`，且开启时必须同时设置 `stream=true` 和 `incremental_output=true`，禁用结构化输出（`response_format="json_object"`）[错误码](../../raw/model-api-reference/preparations/error-code.md)。

> **注意**：文档 2 中 `bl image generate --n` 支持 `6`，但文档 4 明确 `Range of n should be [1, 4]`。该差异源于 CLI 工具对批量请求的封装逻辑（内部拆分为多次 API 调用），而非 API 协议本身允许单次请求 `n=6`。实际 HTTP 调用仍需遵守 `n ≤ 4` 的服务端限制。

## 使用方式

### API Key 获取与配置
必须通过[阿里云百炼控制台](https://bailian.console.aliyun.com/)创建 API Key，并按地域（华北2、新加坡、美国弗吉尼亚等）进入对应 `API Key` 页面操作 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。强烈建议将 Key 配置为环境变量 `DASHSCOPE_API_KEY`，避免硬编码；Linux/macOS/Windows 各系统配置方法详见原文档。

### SDK 与 CLI 集成
- **SDK**：推荐使用官方 DashScope SDK（Python/Java）或 OpenAI 兼容 SDK（Python/Node.js/Java/Go）。安装命令统一为 `pip install -U dashscope` 或 `npm install openai` [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。
- **CLI**：`bailian-cli`（命令 `bl`）需 Node.js ≥ 22.12.0，通过 `npm install -g bailian-cli` 安装，并支持 `bl auth login --api-key` 或浏览器 OAuth 登录 [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。CLI 提供 `bl text chat`、`bl image generate` 等高阶命令，自动处理模型路由、异步轮询与文件下载。

### 协议与端点
调用时必须指定 `base_url`（即创建 API Key 时弹窗显示的 **API Host**），其值因地域和协议（OpenAI 兼容 vs Anthropic 兼容）而异，不可复用 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

## 限制和注意事项

- **API Key 安全**：新创建 Key 以 `sk-ws` 开头，明文仅创建时可见一次，丢失后需重置；旧 `sk-` Key 可继续使用，但建议迁移 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **地域隔离**：华北2（北京）、新加坡等地域支持 IP 白名单与模型范围自定义权限；美国（弗吉尼亚）地域不支持禁用/重置操作及权限精细化配置。
- **文件限制**：Qwen-Long 模型处理文件大小 ≤ 150 MB、页数 ≤ 15000、内容非空，且仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD 格式 [错误码](../../raw/model-api-reference/preparations/error-code.md)。
- **错误处理**：`Model not exist` 错误常因模型 ID 大小写错误或混用开源名称（如 `Qwen/Qwen3-235B...`）导致，务必使用控制台模型列表中的标准 ID（如 `qwen3-235b-a22b-instruct-2507`）。
- **调试建议**：遇到参数错误（如 `400-InvalidParameter`），优先使用阿里云 AI 助理输入报错信息获取精准方案，而非手动排查 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


