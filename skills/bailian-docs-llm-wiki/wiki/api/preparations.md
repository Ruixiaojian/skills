# preparations

在调用阿里云百炼平台的模型服务前，开发者需完成基础环境准备，包括获取并安全配置 API Key、选择合适的 SDK 或 CLI 工具、理解关键参数约束及常见错误应对策略。这些步骤直接影响调用的可用性、安全性与稳定性，是所有模型集成的前置必要条件。

## 支持的模型/功能

百炼平台支持全模态能力，包括文本生成（如 `qwen3.7-max`）、图像生成（`qwen-image-2.0`）、视频生成（`happyhorse-1.1-t2v`）、语音合成（`cosyvoice`）、语音识别（`paraformer`）、向量嵌入（`text-embedding-v3`）和排序（`text-rerank`）等。模型能力取决于其类型：纯文本模型（如 `qwen3-max`）**不支持** `image_url` 等多模态 `content` 元素；而多模态模型（如 `qwen3-vl-plus`）则要求 `content` 数组中每个元素为合法对象（`type` 仅限 `text`、`image_url`、`video_url` 等），且禁止混入数字或布尔值 [错误码](../../raw/model-api-reference/preparations/error-code.md)。此外，部分模型（如 `qwen3-235b-a22b-thinking-2507`）强制启用思考模式（`enable_thinking=true`），而另一些模型（如 Qwen-MT）仅支持特定语种编码 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 关键参数

调用时需严格校验参数范围与格式：
- `temperature` 必须在 `[0.0, 2.0)` 区间，`top_p` 在 `(0.0, 1.0]`；
- `max_tokens` 不得超过模型文档标注的最大输出 [Token](../concepts/token.md) 数；
- `n`（生成数量）上限为 `4`（图像生成除外，`bl image generate --n` 支持最多 `6`）；
- `seed` 在 DashScope 协议下必须为 `[0, 9223372036854775807]` 内整数；
- 结构化输出（`response_format={"type": "json_object"}`）要求提示词含 `json` 关键词，且 **不可与 `enable_thinking=true` 同时使用**；
- `messages` 中 `content` 字段对纯文本模型必须为字符串，多模态模型则需为合规对象数组 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

> **注意**：文档 2 中 `bl image generate --n` 支持 `6` 张图，但文档 4 的错误码明确指出通用 `n` 参数范围为 `[1, 4]`。该矛盾源于 `n` 在不同接口中的语义差异——图像生成接口独立放宽了限制，而文本/Embedding 等接口仍遵循 `[1, 4]`。开发者应以具体接口文档为准，不可跨模态套用参数规则。

## 使用方式

### API Key 获取与配置
必须通过[主账号或具备 `管理员`/`API-Key` 权限的子账号](../../raw/model-api-reference/preparations/get-api-key.md)在控制台创建 API Key。密钥格式已升级：新创建 Key 以 `sk-ws` 开头（旧 `sk-` Key 仍可用）。强烈建议将 Key 配置为环境变量 `DASHSCOPE_API_KEY`，避免硬编码——Linux/macOS 可写入 `~/.bashrc` 或 `~/.zshrc`，Windows 可通过系统属性或 PowerShell 设置 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

### SDK 与 CLI 选择
- **SDK**：推荐使用官方 DashScope SDK（Python/Java）或 OpenAI 兼容 SDK（Python/Node.js/Java/Go）。Python 用户可 `pip install -U dashscope` 或 `pip install -U openai`；Node.js 用户执行 `npm install --save openai` [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。
- **CLI**：百炼 CLI（`bailian-cli`）需 Node.js ≥ 22.12.0，通过 `npm install -g bailian-cli` 安装，并用 `bl auth login --api-key <key>` 或 `bl auth login --console` 完成鉴权 [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。

### 协议与端点
调用时需指定 `base_url`（即创建 Key 时显示的 API Host），其值因地域（北京/新加坡/弗吉尼亚等）和协议（OpenAI 兼容或 Anthropic 兼容）而异，不可复用 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

## 限制和注意事项

- **安全限制**：API Key 创建后仅一次明文展示机会，关闭弹窗即不可恢复；美国（弗吉尼亚）地域不支持禁用/重置操作；IP 白名单最多配置 20 个 IPv4/IPv6 地址或网段 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **模型开通**：未在[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)开通的目标模型会返回 `Model not exist` 或 `The product is not activated` 错误，需手动开通 [错误码](../../raw/model-api-reference/preparations/error-code.md)。
- **文件限制**：Qwen-Long 模型仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD 纯文本文件，单文件 ≤150 MB，且 page 数 ≤1500；图片类文件需改用 Qwen-VL 模型处理 [错误码](../../raw/model-api-reference/preparations/error-code.md)。
- **流式约束**：思考模式模型（`enable_thinking=true`）强制要求 `stream=true` 和 `incremental_output=true`；Qwen-Omni 的音频输出也仅支持流式 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


