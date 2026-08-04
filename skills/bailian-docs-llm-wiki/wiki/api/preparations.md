# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成基础环境准备：获取并安全配置 API Key、安装适配的 SDK 或 CLI 工具、理解关键参数约束及常见错误应对策略。这些步骤是所有模型调用（文本、图像、语音、视频、向量等）的统一前置条件，直接影响服务可用性与安全性。

## 支持的模型/功能

百炼平台支持全模态模型调用，包括但不限于：
- **文本生成**：如 `qwen3.7-max`、`qwen3-vl-plus`（多模态理解）、`qwen3-235b-a22b-thinking-2507`（思考模式专用）；
- **图像生成与编辑**：如 `qwen-image-2.0`；
- **视频生成**：如 `happyhorse-1.1-t2v`（文生视频）、`happyhorse-1.1-r2v`（多图参考视频）；
- **语音合成与识别**：如 `cosyvoice`、`paraformer`；
- **向量与排序模型**：如 `text-embedding-v3`、`text-rerank-v3`。

> **注意**：并非所有模型均支持全部功能（如联网搜索、结构化输出、思考模式）。例如，文档 4 明确指出 [`This model does not support enable_search`](../../raw/model-api-reference/preparations/error-code.md) 和 [`Json mode response is not supported when enable_thinking is true`](../../raw/model-api-reference/preparations/error-code.md)，开发者需根据具体模型能力选择参数组合。

## 关键参数

调用时需关注以下核心参数及其约束（详见 [错误码文档](../../raw/model-api-reference/preparations/error-code.md)）：

| 参数 | 合法范围 | 说明 |
|------|----------|------|
| `temperature` | `[0.0, 2.0)` | 温度值必须为浮点数，超出范围将报错 `Temperature should be in [0.0, 2.0)` |
| `top_p` | `(0.0, 1.0]` | 核采样阈值，必须严格大于 0 且小于等于 1 |
| `max_tokens` | `[1, 模型最大输出 Token 数]` | 超出上限将触发 `Range of max_tokens should be [1, xxx]` 错误 |
| `n`（生成数量） | `[1, 4]`（图像生成为 `[1, 6]`） | 文本模型默认为 1，图像生成 `bl image generate` 支持最多 6 张 |
| `seed` | `[0, 9223372036854775807]` | 仅 DashScope 协议支持，OpenAI 兼容协议不支持该参数 |
| `enable_thinking` | 布尔值，部分模型强制为 `true` | 如 `qwen3-235b-a22b-thinking-2507` 要求 `enable_thinking=true`，否则报错 [`The value of the enable_thinking parameter is restricted to True`](../../raw/model-api-reference/preparations/error-code.md) |
| `response_format` | `{"type": "json_object"}` | 结构化输出需显式指定，且提示词中必须包含 `json` 关键词 |

## 使用方式

### 1. 获取并配置 API Key  
必须通过[阿里云百炼控制台](https://bailian.console.aliyun.com/)创建 API Key，并按地域（如华北2、新加坡、美国弗吉尼亚）进入对应 API Key 页面操作。创建后务必立即复制保存，关闭弹窗后无法再次查看明文密钥（美国弗吉尼亚地域除外）。推荐将密钥配置为环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄露风险 —— 具体配置方法详见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md) 文档中的 Linux/macOS/Windows 操作指南。

### 2. 安装调用工具  
- **SDK 方式**：支持 DashScope SDK（Python/Java）和 OpenAI 兼容 SDK（Python/Node.js/Java/Go）。Python 用户可任选 `pip install -U dashscope` 或 `pip install -U openai`；Java 用户需按 Gradle/Maven 依赖声明引入对应 SDK（见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）。  
- **CLI 方式**：使用 `npm install -g bailian-cli` 安装百炼 CLI（要求 Node.js ≥ 22.12.0），并通过 `bl auth login --api-key <key>` 或 `bl auth login --console` 完成鉴权（见 [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)）。

### 3. 指定服务端点（base_url）  
除 API Key 外，**必须指定正确的 API Host（即 base_url）**。该地址因地域和协议（OpenAI 兼容 / Anthropic 兼容）而异，需以创建 API Key 时弹窗显示的 `API Host` 为准，不可自行拼接。例如 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)的 `base_url` 与 Anthropic 兼容接口不同，且随地域变化。

## 限制和注意事项

- **API Key 权限隔离**：API Key 的调用权限由其**归属业务空间**决定。同一空间内的 API Key 权限一致，无需为不同模型单独创建密钥；子业务空间下的 API Key 仅能调用该空间已授权的模型（见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md) 中“API Key权限说明”章节）。
- **密钥安全升级**：新创建的按量付费 API Key 统一以 `sk-ws` 开头（旧密钥 `sk-` 仍可用），且仅在创建时展示一次明文，丢失后需重置（见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md) 中“API Key 安全升级说明”）。
- **地域与模型开通**：调用前需确认目标模型已在对应地域的[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)中开通，否则返回 `The product is not activated` 错误（见 [错误码](../../raw/model-api-reference/preparations/error-code.md)）。
- **输入格式强校验**：纯文本模型（如 `qwen3-max`）不接受 `content` 为数组或含 `image_url` 的消息；若混入多模态内容，将报错 [`The provided messages input is invalid. The error info is [Unexpected item type in content]`](../../raw/model-api-reference/preparations/error-code.md)。务必根据模型类型清理 `messages` 输入结构。
- **CLI 特殊约束**：百炼 CLI 仅支持 `npm` 全局安装，且要求 Node.js ≥ 22.12.0；认证时优先使用 `bl auth login --console`（OAuth），备选 `--api-key` 方式需确保 Key 有效（见 [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md) 中“认证与配置”章节）。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


