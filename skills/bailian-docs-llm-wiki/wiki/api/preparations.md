# preparations

在调用百炼平台模型服务前，开发者需完成 API Key 获取与配置、SDK 或 CLI 工具安装、环境准备等基础步骤。这些操作是所有模型调用（文本、图像、视频、语音、向量等）的共同前置条件，直接影响服务可用性与安全性。本文档汇总关键准备事项，聚焦可执行的技术要点，避免冗余说明。

## 支持的模型/功能

百炼平台支持全模态模型调用，包括：
- **文本生成**：如 `qwen3.7-max`、`qwen3-235b-a22b-instruct-2507` 等；
- **多模态理解与生成**：如 `qwen3.5-omni-plus`（支持图文音视频输入）、`qwen3-vl-plus`（视觉理解）、`qwen-image-2.0`（文生图）；
- **语音与视频**：如 `cosyvoice`（TTS）、`paraformer`（ASR）、`happyhorse-1.1-t2v`（文生视频）；
- **结构化能力**：如 JSON 输出、思考模式（`enable_thinking`）、联网搜索（`enable_search`）等高级功能。

> **注意**：并非所有模型均支持全部功能。例如，`qwen3-235b-a22b-thinking-2507` 模型强制要求 `enable_thinking=true`，而纯文本模型（如 `qwen3-max`）不支持 `image_url` 类型的 `content` 元素 [错误码](../../raw/model-api-reference/preparations/error-code.md)。具体支持情况请以[模型列表](https://help.aliyun.com/zh/model-studio/models)为准。

## 关键参数

调用时需关注以下核心参数及其约束：

| 参数 | 说明 | 合法范围 | 注意事项 |
|--------|------|-----------|----------|
| `model` | 模型 ID | 必须与[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)中开通的模型名称完全一致（大小写敏感、无空格） | 不可混用开源社区命名（如 `Qwen/Qwen3-235B...`），应使用百炼标准 ID（如 `qwen3-235b-a22b-instruct-2507`）[错误码](../../raw/model-api-reference/preparations/error-code.md) |
| `temperature` | 采样温度 | `[0.0, 2.0)` | 超出范围将返回 `400-InvalidParameter` 错误 |
| `top_p` | 核采样阈值 | `(0.0, 1.0]` | 同上 |
| `max_tokens` | 最大输出 token 数 | `[1, 模型最大输出 Token]` | 超限需参考模型文档调整 |
| `seed` | 随机种子 | `[0, 9223372036854775807]` | DashScope 协议下严格校验 |
| `enable_thinking` | 是否启用思考模式 | `true` / `false` | 部分模型强制为 `true`；开启时必须配合 `stream=true` 和 `incremental_output=true`，且禁用 `response_format="json_object"` [错误码](../../raw/model-api-reference/preparations/error-code.md) |
| `messages` / `prompt` | 输入内容 | 二者必选其一，不可同时为空或同时非空 | `messages` 格式需符合 OpenAI 或 DashScope 协议规范，`content` 字段类型需与模型能力匹配（纯文本模型仅接受字符串） |

## 使用方式

### 1. 获取与配置 API Key  
通过[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)完成：
- 在控制台密钥管理页创建或复制 API Key；
- 推荐配置为环境变量 `DASHSCOPE_API_KEY`（Linux/macOS/Windows 均有详细步骤）；
- 若需权限隔离或成本核算，应选择非默认业务空间创建 Key；
- **严禁**在客户端代码或不可信环境中硬编码长期有效 Key；高安全场景请使用[临时 API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)（最长 1800 秒）。

### 2. 安装 SDK 或 CLI  
- **SDK**：支持 Python（`openai` 或 `dashscope`）、Java（`dashscope-sdk-java` 或 `openai-java`）、Node.js（`openai`）、Go（`openai-go`）；详见[安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)；
- **CLI**：推荐使用 `bailian-cli`（`npm install -g bailian-cli`），支持浏览器登录（`bl auth login --console`）或 API Key 登录（`bl auth login --api-key <key>`），并提供 `bl text chat`、`bl image generate` 等开箱即用命令。

### 3. 设置 Base URL 与地域  
- [OpenAI 兼容接口](../concepts/openai-compatible-api.md) Base URL：
  - 中国大陆版：`https://dashscope.aliyuncs.com/compatible-mode/v1`
  - 国际版：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
- CLI 默认地域为 `cn`，可通过 `--region us` 或 `--region intl` 切换；
- SDK 中需显式配置 `base_url`（OpenAI SDK）或 `api_base`（DashScope SDK）。

## 限制和注意事项

- **API Key 限制**：单个业务空间最多创建 20 个 API Key；主账号下最多 20 个业务空间；IP 白名单最多支持 20 个地址或网段。
- **模型调用限制**：不同模型对 `n`（生成数量）、`seed`、`max_tokens` 等参数有独立上限（如 `n` 通常为 `[1, 4]` 或 `[1, 6]`），超限将触发 `400-InvalidParameter` 错误。
- **安全约束**：
  - 环境变量配置后需重启 IDE/终端/服务进程才能生效；
  - 使用 `sudo` 运行脚本时，需加 `-E` 参数传递环境变量（`sudo -E python xx.py`）；
  - CLI 的 `--api-key` 参数仅当次生效，不落盘；持久化推荐 `bl auth login` 而非 `bl config set`（后者不校验 Key 有效性）。
- **调试必备**：调用失败时务必记录 `Request ID`（UUID 格式），用于自助排查或提交工单；可结合[阿里云 AI 助理](https://www.aliyun.com/ai-assistant/)输入错误信息快速定位原因 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


