# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成 API Key 获取、SDK 或 CLI 工具安装、环境配置等基础准备。这些步骤是所有模型调用的前提，直接影响鉴权有效性、协议兼容性与调试效率。本文档汇总关键操作路径、参数约束与常见陷阱，面向实际开发场景提供结构化指引。

## 支持的模型/功能

百炼平台支持多模态模型（如 `qwen3-vl-plus`、`qwen-image-2.0`）、文本生成模型（如 `qwen3.7-max`）、语音合成（`cosyvoice-v3-flash`）、向量嵌入（`text-embedding-v3`）及排序模型（`text-rerank-v3`）等。**模型能力与调用方式强绑定**：纯文本模型不支持 `image_url` 等多模态 `content` 元素；Qwen-Omni 等全模态模型才支持图像/音频/视频输入；思考模式（`enable_thinking=true`）仅对特定模型（如 `qwen3-235b-a22b-thinking-2507`）有效且强制要求[流式输出](../concepts/streaming-output.md) [错误码](../../raw/model-api-reference/preparations/error-code.md)。模型开通状态需在[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)手动确认，未开通将返回 `The product is not activated` 错误 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 关键参数

| 参数 | 说明 | 取值范围/格式 | 注意事项 |
|------|------|----------------|----------|
| `DASHSCOPE_API_KEY` | 鉴权凭证 | `sk-ws-xxx`（新密钥）或 `sk-xxx`（旧密钥） | 新创建密钥以 `sk-ws` 开头，明文仅创建时可见；旧密钥仍可用但建议迁移 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md) |
| `base_url` / `--base-url` | 服务端点 | 地域相关，如 `https://dashscope.aliyuncs.com/api/v1`（北京） | OpenAI 兼容与 Anthropic 兼容协议的端点不同，必须匹配所选 SDK 协议 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md) |
| `enable_thinking` | 思考模式开关 | `true` / `false` | 部分模型（如 `qwen3-235b-a22b-thinking-2507`）仅支持 `true`；开启时必须同时设置 `stream=true` 和 `incremental_output=true` [错误码](../../raw/model-api-reference/preparations/error-code.md) |
| `messages` / `prompt` | 输入内容 | `messages` 为 JSON 数组；`prompt` 已逐步弃用 | 必须二选一；`messages` 中 `content` 类型需严格匹配模型能力（纯文本模型仅接受字符串） [错误码](../../raw/model-api-reference/preparations/error-code.md) |
| `seed` | 随机种子 | `[0, 9223372036854775807]` | 超出范围将触发 `Range of seed should be [...]` 错误 [错误码](../../raw/model-api-reference/preparations/error-code.md) |

> **注意**：文档 3 中 `bl text chat` 命令默认模型为 `qwen3.7-max`，而文档 4 的错误码示例中多次出现 `qwen3-235b-a22b-thinking-2507` 等长模型 ID。实际使用时应以[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)当前可开通列表为准，避免硬编码过时 ID。

## 使用方式

### 1. 获取并配置 API Key
- **创建**：登录百炼控制台 → 切换目标地域（北京/新加坡/东京/法兰克福/弗吉尼亚）→ 进入 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) → 创建。注意：美国（弗吉尼亚）地域不支持 IP 白名单和权限自定义 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **安全配置**：强烈建议通过环境变量注入（如 `export DASHSCOPE_API_KEY="sk-ws-xxx"`），避免代码硬编码。Linux/macOS/Windows 的永久/临时配置方法详见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

### 2. 安装调用工具
- **SDK**：Python 推荐 `pip install -U dashscope` 或 `pip install -U openai`；Java/Node.js/Go 同样支持 DashScope 或 OpenAI 官方 SDK [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。
- **CLI**：仅支持 `npm install -g bailian-cli`（Node ≥ 22.12.0），认证方式包括浏览器登录（推荐）、`bl auth login --api-key` 或环境变量 [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。

### 3. 首次调用验证
- 使用 `bl auth status --output json` 确认 CLI 鉴权成功；
- 执行 `bl text chat --message "ping" --non-interactive` 测试基础文本模型连通性；
- 若失败，依据错误码定位问题（如 `Arrearage` 表示账号欠费，`Model not exist` 表示模型未开通） [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 限制和注意事项

- **地域隔离**：API Key 与地域强绑定，北京地域创建的 Key 无法调用弗吉尼亚地域服务，反之亦然。`--region` 参数仅影响 CLI 默认行为，不改变 Key 本身权限。
- **权限管控**：API Key 权限由其归属业务空间决定，同一空间内所有 Key 权限一致。子业务空间下的 Key 仅能调用该空间已授权的模型 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **文件限制**：Qwen-Long 模型处理文件时，单文件 ≤150 MB、≤1500 页、仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD 格式；图片类文件需改用 Qwen-VL 模型 [错误码](../../raw/model-api-reference/preparations/error-code.md)。
- **安全红线**：API Key 明文不可出现在代码、日志、公开仓库或聊天记录中。CLI 在 `auth status` 输出中自动脱敏，开发者需遵守此规范 [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。
- **协议差异**：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)要求 `messages` 结构符合 OpenAI 规范；DashScope 原生协议则要求 `messages` 包裹在 `input` 对象内。混用会导致 `Required body invalid` 错误 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


