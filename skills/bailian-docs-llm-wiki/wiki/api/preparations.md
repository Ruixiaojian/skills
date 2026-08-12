# preparations

在调用百炼平台模型服务前，开发者需完成 API Key 获取与配置、SDK 或 CLI 工具安装、环境适配等基础准备。这些步骤直接影响调用的安全性、兼容性与稳定性，是所有模型调用的前置依赖。本文档整合关键操作路径与约束条件，帮助开发者快速建立可运行的开发环境。

## 支持的模型/功能

百炼平台支持多模态模型调用，包括文本生成（如 `qwen3-8b`、`qwen3.7-max`）、图像生成（`qwen-image-2.0`）、视频生成（`happyhorse-1.1-t2v`）、语音合成（`cosyvoice`）、语音识别（`paraformer`）、[向量嵌入](../concepts/vector-embedding.md)（`text-embedding-v3`）及排序（`text-rerank`）等。所有模型均通过统一 API 接口或 OpenAI 兼容协议访问。模型能力与参数支持详见 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 中关于“归属业务空间”与“访问模型范围”的权限说明。

> **注意**：文档 3 中 `bl text chat` 默认模型为 `qwen3.7-max`，而文档 4 的错误码示例中多次出现 `qwen3-235b-a22b-thinking-2507` 等长名称模型 ID；实际调用时必须使用控制台[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)中显示的**精确模型 ID**（区分大小写、无空格），不可混用开源社区命名（如 `Qwen/Qwen3-235B-A22B-Instruct-2507`）。该矛盾已在文档 4 的 `Model not exist.` 错误说明中明确警示。

## 关键参数

| 参数 | 说明 | 取值范围/格式 | 来源 |
|------|------|----------------|------|
| `DASHSCOPE_API_KEY` | 认证凭据，用于所有 HTTP/SDK/CLI 调用 | 长字符串，无固定长度限制，需保密 | [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) |
| `--api-key` | CLI 命令行临时传入凭据 | 同上，仅当次生效 | [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md) |
| `temperature` | 采样温度 | `[0.0, 2.0)` 浮点数 | [错误码](../../raw/model-api-reference/preparations/error-code.md) |
| `top_p` | 核采样阈值 | `(0.0, 1.0]` 浮点数 | [错误码](../../raw/model-api-reference/preparations/error-code.md) |
| `max_tokens` | 最大输出 token 数 | `[1, 模型最大输出 Token 数]` 整数 | [错误码](../../raw/model-api-reference/preparations/error-code.md) |
| `seed` | 随机种子 | `[0, 9223372036854775807]` 整数 | [错误码](../../raw/model-api-reference/preparations/error-code.md) |
| `enable_thinking` | 是否启用思考模式 | `true` / `false`，部分模型强制为 `true` | [错误码](../../raw/model-api-reference/preparations/error-code.md) |

## 使用方式

### 1. 获取并配置 API Key  
前往百炼控制台密钥管理页创建 API Key，选择归属账号（主账号或 RAM 用户）与业务空间（默认空间可调用全部标准模型），并配置 IP 白名单（最多 20 个 IPv4 地址或网段）与模型访问范围。API Key 无失效时间，但建议敏感场景使用[临时 API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)（最长 1800 秒）。配置方式包括：  
- **环境变量**：Linux/macOS 设置 `DASHSCOPE_API_KEY`；Windows 通过系统属性或 `setx` 命令；systemd 服务需通过 `EnvironmentFile` 加载（参见 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）；  
- **CLI 工具**：执行 `bl auth login --api-key <key>` 或 `bl config set --key api_key --value <key>`；  
- **第三方工具**：在 Chatbox、Dify 等工具中填入 API Key、Base URL（中国大陆版 `https://dashscope.aliyuncs.com/compatible-mode/v1`）及模型名。

### 2. 安装 SDK 或 CLI  
- **SDK**：Python 开发者可选 `openai`（`pip install -U openai`）或 `dashscope`（`pip install -U dashscope`）；Java/Node.js/Go 开发者按文档 2 的 Gradle/Maven/npm/go get 指令安装对应 SDK；  
- **CLI**：需 Node.js ≥ 22.12.0，全局安装 `npm install -g bailian-cli`，再执行 `npx skills add modelstudioai/cli --all -g` 注册能力；认证推荐 `bl auth login --console`（浏览器 OAuth），备选 `bl auth login --api-key`；  
- **验证**：SDK 调用前检查环境变量是否生效；CLI 执行 `bl auth status --output json` 和 `bl text chat --message "ping" --non-interactive` 确认连通性。

## 限制和注意事项

- **安全限制**：API Key **严禁**硬编码于客户端代码（浏览器、移动 App）、公开日志或聊天记录中；生产环境应使用临时 Key 或服务端代理；CLI 在 CI/CD 中需通过密钥管理注入，禁止明文写入脚本（参见 [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md) 的 Agent 安全约束）。
- **地域与网络**：Base URL 分中国大陆版与国际版；IPv6 白名单仅华北2（北京）支持，美国（弗吉尼亚）仅支持 IPv4；CLI 安装需访问 `registry.npmjs.org`，企业网络需配置镜像或代理。
- **参数校验**：常见错误如 `temperature` 超出 `[0.0, 2.0)`、`messages` 为空数组、`content` 类型不匹配（纯文本模型不支持 `image_url`）等，均会在 400 错误中返回明确提示（参见 [错误码](../../raw/model-api-reference/preparations/error-code.md)）。
- **模型兼容性**：思考模式（`enable_thinking=true`）要求 `stream=true` 且 `incremental_output=true`，禁用结构化输出（`response_format=json_object`）；部分模型（如 `qwen3-235b-a22b-thinking-2507`）强制 `enable_thinking=true`，不可设为 `false`。
- **额度与开通**：调用前需确认模型已在[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)开通，否则返回 `The product is not activated`；欠费账户会触发 `Arrearage` 错误，需充值后等待系统同步。

## 来源文档

- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


