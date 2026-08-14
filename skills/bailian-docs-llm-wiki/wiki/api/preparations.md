# preparations

在调用阿里云百炼平台模型服务前，开发者需完成 SDK 安装、API Key 获取与配置、CLI 工具部署等基础准备。这些步骤共同构成安全、稳定、可复现的调用环境，适用于 Python/Java/Node.js/Go 等主流语言及 CLI 场景。所有准备工作均围绕模型调用链路展开，不涉及业务逻辑实现。

## 支持的模型与功能

百炼平台支持多模态模型调用，包括文本生成（如 `qwen3-8b`、`qwen3.7-max`）、图像生成（`qwen-image-2.0`）、视频生成（`happyhorse-1.1-t2v`）、语音合成（`cosyvoice`）、语音识别（`paraformer`）、[向量嵌入](../concepts/embedding.md)（`text-embedding`）和排序（`text-rerank`）等 [原文标题](../../raw/model-api-reference/preparations/install-sdk.md)。[OpenAI 兼容接口](../concepts/openai-compatible-api.md)覆盖全部能力，DashScope SDK 提供原生封装。部分模型具备特殊能力约束：例如 `qwen3-vl-plus` 支持视觉理解，而纯文本模型（如 `qwen3-max`）**不支持** `image_url` 等多模态 `content` 元素；思考模式模型（如 `qwen3-235b-a22b-thinking-2507`）要求 `enable_thinking=true` 且仅支持[流式输出](../concepts/streaming-output.md) [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

> **注意**：文档中 `qwen-image-2.0` 被列为图像生成默认模型，但 [原文标题](../../raw/model-api-reference/preparations/use-model-studio-cli.md) 的 CLI 命令示例使用 `qwen-image-2.0`，而部分旧文档可能引用已下线的 `qwen-vl`。请以控制台[模型列表](https://help.aliyun.com/zh/model-studio/models)为准，避免使用非标准命名（如 `Qwen/Qwen3-235B-A22B-Instruct-2507`）。

## 关键参数

核心参数分为认证类、模型控制类和请求格式类：
- **认证参数**：`DASHSCOPE_API_KEY` 环境变量或 CLI `--api-key` 参数，必须为有效密钥；临时 API Key 有效期最长 1800 秒 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。
- **模型控制参数**：`model`（必需，如 `qwen3.7-max`）、`max_tokens`（范围 `[1, 模型最大输出 Token]`）、`temperature`（`[0.0, 2.0)`）、`top_p`（`(0.0, 1.0]`）、`seed`（`[0, 9223372036854775807]`）。
- **请求格式参数**：`messages` 或 `prompt` 二选一（不可同时为空）；结构化输出需 `response_format={"type": "json_object"}` 且提示词含 `json`；思考模式需 `enable_thinking=true` 且 `incremental_output=true`、`stream=true`、`result_format="message"` [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

## 使用方式

### SDK 调用
- **Python**：安装 `openai>=1.0.0` 或 `dashscope>=1.20.0`，设置 `DASHSCOPE_API_KEY` 环境变量后直接调用。
- **Java**：Maven 引入 `com.alibaba:dashscope-sdk-java` 或 `com.openai:openai-java:3.5.0+`，要求 Java 8+。
- **Node.js/Go**：分别通过 `npm install openai` 或 `go get github.com/openai/openai-go/v3@v3.8.1` 安装，Go 需 `1.22+`。

### CLI 调用
安装 `bailian-cli`（Node.js ≥ 22.12.0）后，通过 `bl auth login --console`（推荐）或 `bl auth login --api-key <key>` 完成鉴权 [原文标题](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。支持全局参数如 `--region cn/us/intl`、`--output json`、`--non-interactive`，命令如 `bl text chat --message "ping"` 可快速验证。

### 环境变量配置
Linux/macOS：追加 `export DASHSCOPE_API_KEY='<YOUR_API_KEY>'` 到 `~/.bashrc` 或 `~/.zshrc`；Windows：通过系统属性或 PowerShell 设置用户级环境变量。**重要**：`sudo` 执行时需加 `-E` 参数传递环境变量 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。

## 限制和注意事项

- **API Key 限制**：单个业务空间最多 20 个 API Key；IP 白名单最多 20 个地址或网段；RAM 用户 Key 在账号移出业务空间时失效（重新加入即恢复）。
- **模型调用限制**：`n` 参数范围 `[1, 4]`（文本生成）或 `[1, 6]`（图像生成）；`qwen3-vl-plus` 等多模态模型要求 `content` 数组元素类型严格为 `{"type": "text", "text": "..."}`
或 `{"type": "image_url", "image_url": {"url": "..."}}`，混入数字或布尔值将触发 `Unexpected item type in content` 错误 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。
- **安全约束**：禁止在客户端代码、聊天记录或公开日志中硬编码 API Key；CI/CD 环境应使用密钥管理服务注入，而非明文写入脚本。
- **兼容性注意**：OpenAI SDK 调用需 Base URL 设为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（中国大陆）或 `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`（国际版），模型名须使用百炼标准 ID（如 `qwen-plus`），非 HuggingFace 格式。

## 来源文档

- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


