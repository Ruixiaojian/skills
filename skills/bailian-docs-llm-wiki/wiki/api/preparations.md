# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成基础环境准备：获取并安全配置 API Key、安装适用的 SDK 或 CLI 工具、理解关键参数约束及常见错误应对方式。这些步骤是所有模型调用（文本、图像、语音、视频、向量等）的统一前置条件，直接影响服务可用性与安全性。

## 支持的模型/功能

百炼平台支持全模态模型调用，包括但不限于：
- **文本生成**（如 `qwen3.7-max`, `qwen3-235b-a22b-instruct-2507`）
- **多模态理解与生成**（如 `qwen3.5-omni-plus`, `qwen-image-2.0`, `happyhorse-1.1-t2v`）
- **语音合成与识别**（如 `cosyvoice`, `paraformer-real-time`）
- **向量嵌入与排序**（如 `text-embedding-v3`, `text-rerank-v3`）

所有模型均通过统一 API Key 鉴权，**无需为不同模型创建独立密钥**；权限由 API Key 所属业务空间决定，同一空间内密钥对所有已授权模型有效 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。调用时需显式指定 `model` 参数，名称必须严格匹配[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)中公布的 ID（区分大小写，不可混用开源社区命名），否则将返回 `Model not exist` 错误 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

> **注意**：文档 3 中提到的 `qwen3.7-max` 为 CLI 默认模型，但实际可用模型列表以控制台为准；部分新模型（如 `qwen3-vl-plus`）仅支持特定输入格式（如 `content` 数组含 `image_url`），纯文本模型传入多模态内容将触发 `Unexpected item type in content` 错误 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 关键参数

调用时需关注以下核心参数及其约束：

| 参数 | 说明 | 允许值/范围 | 注意事项 |
|------|------|-------------|----------|
| `model` | 模型唯一标识 | 必须为控制台模型市场中精确的 ID | 不可使用 `Qwen/Qwen3-235B...` 等 Hugging Face 格式 [错误码](../../raw/model-api-reference/preparations/error-code.md) |
| `temperature` | 采样温度 | `[0.0, 2.0)` | 超出范围将报错 `Temperature should be in [0.0, 2.0)` |
| `top_p` | 核采样阈值 | `(0.0, 1.0]` | 同上，需严格满足开闭区间 |
| `max_tokens` | 最大输出 token 数 | `[1, 模型最大输出值]` | 超限将返回 `Range of max_tokens should be [1, xxx]` |
| `enable_thinking` | 是否启用思考模式 | `true`/`false` | 部分模型（如 `qwen3-235b-a22b-thinking-2507`）强制要求 `true`；开启时必须配合 `stream=true` 和 `incremental_output=true`，且禁用 `response_format="json_object"` |
| `messages` / `prompt` | 输入内容 | 二者必选其一，不可同时为空 | `messages` 为数组，每项 `content` 必须为字符串（纯文本模型）或合法对象数组（多模态模型）；`prompt` 已逐步废弃 |

其他高频参数（如 `seed`, `n`, `stop`, `audio` 输出等）详见 [错误码](../../raw/model-api-reference/preparations/error-code.md) 文档中的具体校验规则。

## 使用方式

### 1. 获取与配置 API Key
- **获取**：需主账号或具备 `管理员`/`API-Key` 权限的子账号，在对应地域（如华北2、新加坡、美国弗吉尼亚）的 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建。新创建密钥以 `sk-ws` 开头，明文仅显示一次，务必立即保存 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **配置**：**强烈建议**通过环境变量 `DASHSCOPE_API_KEY` 设置，避免硬编码。Linux/macOS/Windows 的永久与临时配置方法详见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

### 2. 安装调用工具
- **SDK**：支持 DashScope 官方 SDK（Python/Java）或 OpenAI 兼容 SDK（Python/Node.js/Java/Go）。Python 用户可任选：
  ```bash
  pip install -U dashscope    # DashScope SDK
  pip install -U openai       # OpenAI SDK（需配置 base_url）
  ```
  Java/Node.js/Go 安装方式见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。
- **CLI**：适用于快速验证与 Agent 集成，需 Node.js ≥ 22.12.0：
  ```bash
  npm install -g bailian-cli
  bl auth login --console  # 推荐浏览器登录
  # 或
  bl auth login --api-key sk-xxx  # 手动输入密钥
  ```

### 3. 发起调用
- **HTTP 请求**：需在 Header 中携带 `Authorization: Bearer <API_KEY>`，并设置 `base_url`（[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 Anthropic 兼容接口的端点不同，且随地域变化）。
- **SDK 调用**：DashScope SDK 自动读取 `DASHSCOPE_API_KEY` 环境变量；OpenAI SDK 需显式设置 `base_url` 和 `api_key`。
- **CLI 调用**：认证后直接执行命令，如 `bl text chat --message "hello"`。

## 限制和注意事项

- **API Key 安全**：密钥明文仅在创建时可见，关闭弹窗后无法恢复。丢失需重置或新建。禁止在代码、日志、公开渠道硬编码或泄露密钥 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **地域与协议**：API Host（`base_url`）因地域和协议（OpenAI/Anthropic）而异，必须从创建 API Key 的弹窗中获取，不可自行拼接。
- **IP 白名单**：仅华北2（北京）、新加坡、日本（东京）、德国（法兰克福）地域支持自定义 IP 白名单，最多配置 20 个 IPv4/IPv6 地址或网段；美国（弗吉尼亚）地域不支持该功能 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **错误排查**：所有失败请求应记录 `Request ID`（UUID 格式），用于自助排查或提交工单。常见错误原因与解决方案详见 [错误码](../../raw/model-api-reference/preparations/error-code.md)。
- **[Token](../concepts/token.md) Plan/Coding Plan**：若使用 [Token](../concepts/token.md) Plan（`sk-sp-` 开头）或 Coding Plan 密钥，需单独配置，不可与按量付费密钥混用 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


