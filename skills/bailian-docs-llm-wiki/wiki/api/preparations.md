# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成 API Key 获取、SDK/CLI 安装、环境配置等基础准备。这些步骤是所有模型调用的前提，直接影响鉴权、协议兼容性与功能可用性。本文档整合关键操作路径与约束条件，面向开发者提供可直接执行的结构化指引。

## 支持的模型/功能

百炼平台支持全模态模型调用，包括文本生成（如 `qwen3.7-max`）、图像生成（如 `qwen-image-2.0`）、视频生成（如 `happyhorse-1.0-t2v`）、语音合成（如 `cosyvoice-v3-flash`）、视觉理解（如 `qwen3-vl-plus`）及[向量嵌入](../concepts/vector-embedding.md)等。模型能力与调用方式强绑定：例如 `qwen3-vl-plus` 支持[多模态输入](../concepts/multimodal-input.md)（`image_url`, `video_url`），而纯文本模型（如 `qwen3-max`）仅接受字符串型 `content`；部分模型（如 `qwen3-235b-a22b-thinking-2507`）强制要求 `enable_thinking=true`，且仅支持[流式输出](../concepts/streaming-output.md) [错误码](../../raw/model-api-reference/preparations/error-code.md)。所有模型均需通过已开通的服务调用——未在[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)中手动开通的模型将返回 `The product is not activated` 错误 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 关键参数

| 参数 | 说明 | 取值范围/格式 | 注意事项 |
|------|------|----------------|----------|
| `DASHSCOPE_API_KEY` | 鉴权凭证，必须配置 | `sk-ws` 开头（新创建）或 `sk-` 开头（旧密钥） | 升级后新密钥仅创建时可见明文，丢失需重置；美国（弗吉尼亚）地域不支持重置 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md) |
| `base_url` / `--base-url` | 服务端点地址 | 地域相关，如 `https://dashscope.aliyuncs.com/api/v1`（北京） | OpenAI 兼容与 Anthropic 兼容协议的端点不同，需严格匹配 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md) |
| `enable_thinking` | 启用思考模式 | `true` 或 `false` | 非流式调用时必须为 `false`；思考模式下 `response_format="json_object"` 不被支持 [错误码](../../raw/model-api-reference/preparations/error-code.md) |
| `stream` | 启用[流式输出](../concepts/streaming-output.md) | `true` 或 `false` | `qwen3-vl-plus` 等模型强制要求 `stream=true`；`audio` 输出必须启用流式 [错误码](../../raw/model-api-reference/preparations/error-code.md) |
| `messages` | 对话消息数组 | JSON 数组，每项含 `role` 和 `content` | 纯文本模型禁止 `content` 为数组（如含 `image_url`）；多模态模型需确保 `type` 为 `text`/`image_url` 等合法值 [错误码](../../raw/model-api-reference/preparations/error-code.md) |

> **注意**：文档 2 中 `bl text chat` 默认模型为 `qwen3.7-max`，但文档 4 的错误码示例中明确使用 `qwen3-235b-a22b-instruct-2507` 等长模型 ID。实际开发中应以[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)当前展示的精确 ID 为准，避免混用社区命名（如 `Qwen/Qwen3-235B...`）。

## 使用方式

### 1. 获取并配置 API Key  
- **创建**：登录百炼控制台，在对应地域（北京/新加坡/东京/法兰克福/弗吉尼亚）的 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建，权限建议选“全部”或按需配置 IP 白名单与模型范围 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。  
- **配置**：强烈建议设为环境变量 `DASHSCOPE_API_KEY`（Linux/macOS/Windows 均有详细配置步骤），避免硬编码 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。  

### 2. 安装客户端工具  
- **SDK**：Python/Java/Node.js/Go 开发者可选 DashScope SDK（原生支持）或 OpenAI SDK（需指定 `base_url`）。安装命令见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。  
- **CLI**：运行 `npm install -g bailian-cli` 安装 CLI，通过 `bl auth login --console`（推荐）或 `bl auth login --api-key <key>` 完成鉴权 [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。  

### 3. 发起调用  
- **代码调用**：初始化 SDK 时传入 `api_key` 和 `base_url`，构造符合模型要求的 `messages` 或 `prompt`。  
- **CLI 调用**：使用 `bl text chat --message "hello"` 等子命令，支持 `--model`、`--region`、`--output json` 等全局参数 [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。  

## 限制和注意事项

- **地域隔离**：API Key 在不同地域（如北京 vs 弗吉尼亚）独立创建，且弗吉尼亚地域不支持禁用/重置操作，权限配置也更简化 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。  
- **安全约束**：API Key 明文仅创建时可见，关闭弹窗后不可恢复；CLI 工具禁止在日志/聊天记录中回显完整 Key，CI 环境应通过密钥管理注入 [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。  
- **模型限制**：  
  - 输入长度、`max_tokens`、`temperature` 等参数均有严格范围（如 `temperature ∈ [0.0, 2.0)`），超限将返回 400 错误 [错误码](../../raw/model-api-reference/preparations/error-code.md)。  
  - 文件处理（Qwen-Long）限制单文件 ≤150 MB、≤1500 页，且仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD 格式 [错误码](../../raw/model-api-reference/preparations/error-code.md)。  
- **协议差异**：[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)要求 `messages` 直接置于请求体顶层，而 DashScope HTTP 接口需将 `messages` 放入 `input` 对象内，位置错误将触发 `Required body invalid` [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


