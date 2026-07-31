# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成基础环境准备：获取并安全配置 API Key、安装适用的 SDK 或 CLI 工具、理解关键参数约束及常见错误应对策略。这些步骤直接影响调用的合法性、安全性与稳定性，是所有后续开发工作的前提。

## 支持的模型/功能

百炼平台支持多模态模型（如 `qwen3-vl-plus`、`qwen-image-2.0`）、文本生成模型（如 `qwen3.7-max`、`qwen3-235b-a22b-instruct-2507`）、语音合成/识别（`cosyvoice`、`paraformer`）、向量嵌入（`text-embedding-v3`）及排序模型（`text-rerank-v3`）等。部分模型具备特定能力限制，例如：
- `qwen3-235b-a22b-thinking-2507` 等思考模式模型**强制要求** `enable_thinking=true`，且仅支持[流式输出](../concepts/streaming-output.md)（`stream=true`）和 `result_format="message"` [原文标题](../../raw/model-api-reference/preparations/error-code.md)；
- 纯文本模型（如 `qwen3-max`）**不支持** `image_url` 等多模态 `content` 元素，混用将触发 `Unexpected item type in content` 错误 [原文标题](../../raw/model-api-reference/preparations/error-code.md)；
- Qwen-Long 模型仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD 等纯文本格式文件，不支持图片或扫描件 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

> **注意**：文档 3 中列出的默认模型 `qwen3.7-max` 与文档 4 中示例模型 `qwen3-235b-a22b-instruct-2507` 均属有效模型 ID，但实际可用性取决于控制台模型市场开通状态——未开通的模型会返回 `Model not exist` 或 `The product is not activated` 错误，需先在[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)中手动开通 [原文标题](../../raw/model-api-reference/preparations/error-code.md)。

## 关键参数

调用时需关注以下核心参数及其约束：

| 参数 | 合法范围 | 说明 |
|------|----------|------|
| `temperature` | `[0.0, 2.0)` | 温度值必须为浮点数，超出范围将报错 |
| `top_p` | `(0.0, 1.0]` | 核采样阈值，需严格满足开闭区间 |
| `max_tokens` | `[1, 模型最大输出 Token 数]` | 上限见各模型文档，超限将被拒绝 |
| `seed` | `[0, 9223372036854775807]` | DashScope 协议下整型种子必须在此范围内 |
| `n`（图像生成数量） | `[1, 6]` | `bl image generate` 最多生成 6 张图 |
| `enable_thinking` | `true`（部分模型强制）或 `false`（非思考模式） | 与 `stream`、`incremental_output`、`response_format` 存在强耦合约束 |

结构化输出（`response_format={"type": "json_object"}`）要求提示词中必须包含 `"json"` 关键词，且**不可与 `enable_thinking=true` 同时启用**；工具调用（`tool_choice`）仅支持 `"auto"` 或 `"none"` 字符串值。

## 使用方式

### API Key 获取与配置
- 必须通过[主账号或具备 `管理员`/`API-Key` 权限的子账号](https://help.aliyun.com/zh/model-studio/permission-management-overview#24ca2dad7djzs)在控制台创建 API Key [原文标题](../../raw/model-api-reference/preparations/get-api-key.md)；
- 推荐将 Key 配置为环境变量 `DASHSCOPE_API_KEY`，避免硬编码（Linux/macOS/Windows 配置方法详见文档）；
- 美国（弗吉尼亚）地域 API Key 不支持禁用/重置操作，且创建后无法再次查看明文。

### SDK 与 CLI 安装
- **SDK**：支持 DashScope（Python/Java）和 OpenAI 兼容 SDK（Python/Node.js/Java/Go），需按语言版本要求安装（如 Python ≥3.8，Node.js ≥22.12.0）；
- **CLI**：仅支持 `npm install -g bailian-cli` 安装，认证方式包括控制台 OAuth 登录（推荐）、API Key 直接登录、环境变量或命令行临时传入 [原文标题](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。

### 调用协议选择
- [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)需指定对应地域的 `base_url`（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`），并确保模型 ID 符合百炼命名规范（如 `qwen3.7-max`，而非开源社区名 `Qwen/Qwen3-235B...`）；
- Anthropic 兼容接口使用独立 `base_url`，详见[Anthropic兼容-Messages](https://help.aliyun.com/zh/model-studio/anthropic-api-messages)。

## 限制和注意事项

- **安全限制**：API Key 创建后仅一次明文展示机会（升级后以 `sk-ws` 开头），丢失需重置；禁止在代码、日志、公开渠道泄露 Key；
- **地域隔离**：华北2（北京）、新加坡、东京、法兰克福、美国（弗吉尼亚）等地域的 API Key 和 `base_url` 互不通用，需按实际部署地域分别配置；
- **权限隔离**：API Key 权限由其**归属业务空间**决定，同一空间内 Key 权限一致；子业务空间 Key 仅能调用该空间已授权的模型；
- **IP 白名单**：仅华北2（北京）等部分地域支持 IPv4/IPv6 白名单（最多 20 条），美国（弗吉尼亚）地域不支持；
- **错误处理**：常见错误如 `Arrearage`（欠费）、`Model not exist`（未开通模型）、`InvalidParameter`（参数越界）均需结合具体错误码定位，建议优先使用[阿里云 AI 助理](https://www.aliyun.com/ai-assistant/)解析报错信息 [原文标题](../../raw/model-api-reference/preparations/error-code.md)；
- **文件限制**：Qwen-Long 模型单文件 ≤150 MB、≤1500 页，且仅支持纯文本格式；上传文件 ID（`file-fe-*`）需通过百炼文件接口获取，跨账号无效。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


