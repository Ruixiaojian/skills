# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成基础环境准备，包括获取并安全配置 API Key、安装必要的 SDK 或 CLI 工具、理解关键参数约束及常见错误应对策略。这些步骤是所有模型调用的前置依赖，直接影响服务可用性与安全性。本文档整合官方最新实践，聚焦可执行的技术要点。

## 支持的模型/功能

百炼平台支持全模态模型调用，涵盖文本生成（如 `qwen3.7-max`）、图像生成（`qwen-image-2.0`）、视频生成（`happyhorse-1.1-t2v`）、语音合成（`cosyvoice`）、语音识别（`paraformer`）、向量嵌入（`text-embedding-v3`）和排序（`text-rerank-v3`）等。模型能力由其所属业务空间决定：默认业务空间下的 API Key 可调用所有标准模型；子业务空间下的 API Key 仅能调用该空间已授权的模型 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。部分模型（如 `qwen3-235b-a22b-thinking-2507`）强制启用思考模式，而另一些（如纯文本系列 `qwen3-max`）不支持多模态输入（如 `image_url`），误用将触发 `400` 错误 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

> **注意**：文档 3 中列出的 `qwen3.5-omni-plus` 为全模态模型，但文档 2 的 SDK 安装说明未明确区分多模态与纯文本模型的兼容性要求。实际使用中，必须根据模型类型选择对应 SDK 调用方式——DashScope SDK 对多模态输入支持更完整，而 OpenAI SDK 在部分场景（如文件 URL 解析）需额外配置 `X-DashScope-OssResourceResolve: enable` 头 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 关键参数

核心参数需严格遵循取值范围，否则将返回明确错误码：
- `temperature`：必须在 `[0.0, 2.0)` 区间；
- `top_p`：必须在 `(0.0, 1.0]` 区间；
- `max_tokens`：上限由模型文档定义，例如 `qwen3-max` 为 `8192`，超出将报 `Range of max_tokens should be [1, xxx]`；
- `seed`：DashScope 协议下须为 `[0, 9223372036854775807]` 内整数；
- `n`（生成数量）：图像生成最多 `6` 张，文本补全最多 `4` 次；
- `enable_thinking`：与 `stream`、`incremental_output`、`result_format` 强耦合——开启时必须启用[流式输出](../concepts/streaming-output.md)、设置 `incremental_output=true` 且 `result_format="message"`，否则报错 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 使用方式

### API Key 管理
- **获取**：主账号或具备 `管理员`/`API-Key` 权限的子账号，在控制台对应地域（如华北2、新加坡、美国弗吉尼亚）的 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建。新创建密钥以 `sk-ws` 开头，仅创建时可见明文，关闭后不可恢复 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **配置**：强烈建议通过环境变量 `DASHSCOPE_API_KEY` 设置，避免代码硬编码。Linux/macOS/Windows 各系统配置方法详见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **鉴权**：除环境变量外，CLI 支持控制台 OAuth 登录（`bl auth login --console`）、命令行传参（`--api-key`）或配置文件写入（`bl config set --key api_key`）。

### SDK 与 CLI
- **SDK**：Python 开发者可选 `openai`（需适配 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)）或 `dashscope`（原生支持）；Java/Node.js/Go 推荐使用 OpenAI SDK，但需注意文件 URL 等高级特性需 DashScope SDK [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。
- **CLI**：`bailian-cli`（命令 `bl`）要求 Node.js ≥ 22.12.0，仅支持 `npm install -g bailian-cli` 安装。认证后可通过 `bl text chat`、`bl image generate` 等命令直接调用模型，支持异步任务轮询与批量操作 [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。

## 限制和注意事项

- **地域隔离**：API Key 与服务端点（`base_url`）强绑定地域，北京地域的 Key 不可用于美国节点，且不同地域的 `base_url` 格式不同，务必以创建时弹窗显示的 API Host 为准 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **权限粒度**：IP 白名单（最多 20 个 IPv4/IPv6 地址或网段）和模型范围控制仅在华北2、新加坡等非美国地域支持；美国（弗吉尼亚）地域不支持禁用/重置 Key [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **安全红线**：API Key 明文严禁出现在代码、日志、公开仓库或聊天记录中。CLI 在交互式安装中禁止回显完整 Key，仅汇报 masked 字段；CI/CD 环境必须通过密钥管理服务注入 [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。
- **错误处理**：`Model not exist` 错误通常因模型未在控制台[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)开通，而非参数错误；`Arrearage` 表示账号欠费，需充值后等待系统同步 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


