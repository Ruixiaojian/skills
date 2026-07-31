# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成基础环境准备：获取并安全配置 API Key、安装适用的 SDK 或 CLI 工具、理解关键参数约束及常见错误应对策略。这些步骤是所有 API 调用和本地开发的前提，直接影响服务可用性、安全性与调试效率。

## 支持的模型/功能

百炼平台支持全模态能力调用，包括文本生成（如 `qwen3.7-max`）、图像生成（`qwen-image-2.0`）、视频生成（`happyhorse-1.1-t2v`）、语音合成（`cosyvoice`）、语音识别（`paraformer`）、向量嵌入（`text-embedding-v3`）和排序（`text-rerank`）等。  
- **模型兼容性**：既可通过官方 DashScope SDK 调用原生协议，也支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（需注意 `base_url` 因地域和协议而异）[获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)；  
- **CLI 工具能力**：百炼 CLI（`bl`）提供开箱即用的文本、图像、视频、语音、视觉理解等命令行操作，并原生支持[多模态](../concepts/multi-modal.md)输入（图片/音频/视频 URL 或本地文件）和结构化输出 [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)；  
- **特殊模型限制**：部分模型（如 `qwen3-235b-a22b-thinking-2507`）强制要求 `enable_thinking=true`，而思考模式模型不支持非流式调用或 JSON 结构化输出 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 关键参数

调用时需严格校验以下核心参数范围，否则将触发 400 错误：

| 参数 | 合法范围 | 说明 |
|--------|-----------|------|
| `temperature` | `[0.0, 2.0)` | 必须为浮点数，不可为整数或超出区间 |
| `top_p` | `(0.0, 1.0]` | 必须为浮点数，不可 ≤ 0 或 > 1 |
| `max_tokens` | `[1, 模型最大输出 Token]` | 查阅对应模型文档确认上限 |
| `n`（生成数量） | `[1, 4]`（文本）、`[1, 6]`（图像） | 图像生成上限为 6，文本为 4 |
| `seed` | `[0, 9223372036854775807]` | DashScope 协议下必须为有符号 64 位整数 |
| `repetition_penalty` | `> 0.0` | 必须为正浮点数 |
| `presence_penalty` | `[-2.0, 2.0]` | 必须在此闭区间内 |

> **注意**：`messages` 字段中 `content` 类型必须与模型能力严格匹配——纯文本模型（如 `qwen3-max`）仅接受字符串，若传入含 `image_url` 的数组会报错；[多模态](../concepts/multi-modal.md)模型（如 `qwen3-vl-plus`）则需确保 `content` 数组中每个元素为合法对象（`type` 仅限 `text`/`image_url`/`video_url` 等），禁止混入数字、布尔值或非法 `type` 值 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 使用方式

### 1. 获取并配置 API Key
- 通过[控制台](https://bailian.console.aliyun.com/)创建 API Key（主账号或具备 `API-Key` 权限的子账号），注意区分地域（北京/新加坡/东京/法兰克福 vs 弗吉尼亚）和 Key 类型（`sk-` 或 `sk-ws-` 开头）[获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)；  
- **强烈建议**将 `DASHSCOPE_API_KEY` 配置为环境变量（Linux/macOS/Windows 均支持永久或临时方式），避免硬编码泄露；  
- 美国（弗吉尼亚）地域不支持 IP 白名单和权限自定义，且无法禁用/重置密钥。

### 2. 安装客户端工具
- **SDK**：Python 推荐 `pip install -U dashscope` 或 `pip install -U openai`；Java/Node.js/Go 同样支持 DashScope 或 OpenAI 官方 SDK [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)；  
- **CLI**：仅支持 `npm install -g bailian-cli`（Node ≥ 22.12.0），认证方式包括浏览器 OAuth 登录（推荐）、`--api-key` 参数、环境变量或配置文件 [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)；  
- 所有工具均需指定 `--region`（`cn`/`us`/`intl`）和可选 `--base-url`，默认地域为 `cn`。

### 3. 首次调用验证
- 使用 `bl auth status --output json` 确认鉴权状态；  
- 运行最小验证命令：`bl text chat --message "ping" --non-interactive --output json`；  
- 若失败，依据返回的 `hint` 或 `message` 字段排查（网络、Key 无效、region 不匹配等）。

## 限制和注意事项

- **API Key 安全**：创建后仅一次明文展示机会，关闭弹窗即不可恢复；旧版 `sk-` Key 可继续使用，但新创建 Key 统一以 `sk-ws-` 开头，安全性更高 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)；  
- **地域隔离**：API Key、模型开通状态、服务端点（`base_url`）均按地域独立，跨地域调用需分别配置；  
- **模型开通**：即使拥有有效 API Key，调用前仍需在[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)手动开通目标模型，否则返回 `The product is not activated`；  
- **文件限制**：Qwen-Long 模型仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD 纯文本文件，大小 ≤ 150 MB，页数 ≤ 1500；图片类文件需改用 Qwen-VL 模型处理；  
- **错误诊断**：遇到错误优先使用[阿里云 AI 助理](https://www.aliyun.com/ai-assistant/)输入完整报错信息自动分析，或查阅 [错误码](../../raw/model-api-reference/preparations/error-code.md) 文档定位原因。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


