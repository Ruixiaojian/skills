# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成基础环境准备：获取并安全配置 API Key、安装适用的 SDK 或 CLI 工具、理解关键参数约束及常见错误应对策略。这些步骤是所有模型调用的前置依赖，直接影响服务可用性与安全性。

## 支持的模型/功能

百炼平台支持多模态模型（如 `qwen3-vl-plus`、`qwen-image-2.0`）、文本生成模型（如 `qwen3.7-max`）、语音合成（`cosyvoice-v3-flash`）、语音识别（`paraformer-real-time`）、向量嵌入（`text-embedding-v3`）及排序模型（`text-rerank-v3`）等。模型能力与调用方式严格绑定其类型：纯文本模型不接受 `image_url` 等多模态 `content` 元素；Qwen-Omni 等全模态模型则需配合 `--image`、`--audio` 等 CLI 参数或 `messages` 中合法 `type` 字段（如 `"image_url"`）使用。具体支持列表请以[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)为准，调用前务必确认模型已开通且名称拼写准确（例如 `qwen3-235b-a22b-instruct-2507`，非开源社区命名格式）[原文标题](../../raw/model-api-reference/preparations/error-code.md)。

## 关键参数

核心参数需严格遵循取值范围与组合规则：
- `temperature`: 必须在 `[0.0, 2.0)` 区间；
- `top_p`: 必须在 `(0.0, 1.0]` 区间；
- `max_tokens`: 上限由模型文档明确标注，不可超过该值；
- `n`: 图像生成等场景中最大为 `6`（CLI）或 `4`（HTTP 接口），详见 [原文标题](../../raw/model-api-reference/preparations/error-code.md)；
- `seed`: DashScope 协议下有效范围为 `[0, 9223372036854775807]`；
- `enable_thinking`: 思考模式仅支持[流式输出](../concepts/streaming-output.md)（`stream=true`），且与 `response_format="json_object"` 冲突，启用时必须设置 `incremental_output=true` 和 `result_format="message"`；
- `messages` 构造：纯文本模型要求 `content` 为字符串；多模态模型允许数组，但元素 `type` 仅限 `text`、`image_url`、`video_url` 等受支持类型，禁止混入数字或布尔值 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

> **注意**：文档 3 中 CLI 的 `bl image generate --n` 默认值为 `1`，最大支持 `6`；而文档 4 的错误码说明中 `Range of n should be [1, 4]` 针对的是 HTTP 接口（如 OpenAI 兼容协议）的通用限制。实际使用时，请依据所选调用方式（CLI vs SDK/HTTP）参考对应文档。

## 使用方式

### API Key 获取与配置
- **获取**：需主账号或具备 `管理员`/`API-Key` 权限的子账号，在[百炼控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)创建。华北2（北京）、新加坡等地域支持权限精细化配置（IP 白名单、模型范围）；美国（弗吉尼亚）地域暂不支持自定义权限 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。
- **安全配置**：强烈建议将 `DASHSCOPE_API_KEY` 设为环境变量（Linux/macOS/Windows 均有详细步骤），避免硬编码。新创建的 Key 以 `sk-ws` 开头，明文仅显示一次，丢失后需重置 [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)。

### SDK 与 CLI 安装
- **SDK**：Python 开发者可选 `openai`（`pip install -U openai`）或 `dashscope`（`pip install -U dashscope`）；Java/Node.js/Go 用户按文档 2 的 Gradle/Maven/npm/go get 指令安装对应 SDK。
- **CLI**：仅支持 `npm install -g bailian-cli`（Node ≥ 22.12.0），认证方式包括浏览器登录（`bl auth login --console`）、API Key 直接输入（`bl auth login --api-key sk-xxx`）或环境变量配置。CLI 提供 `bl text chat`、`bl image generate` 等命令，支持地域切换（`--region cn|us|intl`）和[异步任务](../concepts/asynchronous-task.md)轮询 [原文标题](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。

## 限制和注意事项

- **地域与端点**：API Host（`base_url`）随地域变化，OpenAI 兼容与 Anthropic 兼容协议的端点不同，必须从创建 API Key 弹窗中复制，不可自行构造。
- **权限隔离**：API Key 权限由其归属业务空间决定。默认空间 Key 可调用所有标准模型；子业务空间 Key 仅能调用已授权模型及该空间内应用；调优模型仅允许所在空间的 Key 调用。
- **安全红线**：严禁公开 API Key；CLI 在 CI/Agent 场景中禁止将 Key 写入日志或脚本；环境变量配置后需重启终端/IDE 才生效。
- **错误处理**：常见错误如 `Model not exist`（模型未开通或名称错误）、`Arrearage`（账号欠费）、`InvalidParameter`（参数越界或格式错误）均需结合 [原文标题](../../raw/model-api-reference/preparations/error-code.md) 定位。推荐使用阿里云 AI 助理输入错误信息获取实时解决方案。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


