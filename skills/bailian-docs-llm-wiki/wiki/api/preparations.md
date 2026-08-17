# preparations

在调用阿里云百炼平台模型服务前，开发者需完成 SDK 安装、API Key 获取与配置、CLI 工具部署等基础准备。这些步骤共同构成安全、稳定、可复现的调用环境，适用于 Python/Java/Node.js/Go 等主流语言及 CLI 场景。本文档整合关键操作路径与约束条件，帮助开发者快速建立合规接入链路。

## 支持的模型/功能

百炼平台支持全模态模型调用，包括：
- **文本生成**：如 `qwen3.7-max`、`qwen-plus`、`deepseek-r1`
- **多模态理解与生成**：`qwen3.5-omni-plus`（全模态对话）、`qwen-image-2.0`（文生图）、`happyhorse-1.1-t2v`（文生视频）
- **语音与向量能力**：`cosyvoice`（TTS）、`paraformer`（ASR）、`text-embedding-v3`（向量模型）
- **结构化输出与工具调用**：支持 `response_format={"type": "json_object"}` 及 `tools` 参数（需模型显式支持，见 [错误码文档](../../raw/model-api-reference/preparations/error-code.md) 中 `The tool call is not supported.` 条目）

> **注意**：模型名称区分大小写且不可混用开源社区命名（如 `Qwen/Qwen3-235B...`），必须使用控制台模型市场中显示的精确 ID（如 `qwen3-235b-a22b-instruct-2507`）——详见 [错误码文档](../../raw/model-api-reference/preparations/error-code.md) 的 `Model not exist.` 条目。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `DASHSCOPE_API_KEY` | 认证凭据，用于所有 HTTP/SDK 调用 | 必须配置为环境变量或通过 CLI `bl auth login` 注入；禁止硬编码于客户端代码中 |
| `--region` | 地域标识 | CLI 默认 `cn`；[OpenAI 兼容接口](../concepts/openai-compatible-api.md)需匹配 Base URL（中国大陆版：`https://dashscope.aliyuncs.com/compatible-mode/v1`） |
| `enable_thinking` | 思考模式开关 | 仅部分模型支持（如 `qwen3-235b-a22b-thinking-2507`），且开启时必须同时设置 `stream=true` 和 `incremental_output=true`（见 [错误码文档](../../raw/model-api-reference/preparations/error-code.md)） |
| `max_tokens` / `temperature` / `top_p` | 生成控制参数 | `max_tokens` 范围为 `[1, 模型最大输出 Token]`；`temperature` ∈ `[0.0, 2.0)`；`top_p` ∈ `(0.0, 1.0]` |
| `messages` | 对话消息数组 | 必须非空；纯文本模型不支持 `image_url` 等多模态元素；多模态模型要求 `content` 数组中每个元素为合法对象（`type` 仅限 `text`/`image_url`/`video_url`） |

## 使用方式

### 1. SDK 安装
- **Python**：推荐安装 `openai>=1.0.0` 或 `dashscope>=1.20.0`（需 `python>=3.8`）  
- **Java**：Maven 引入 `com.openai:openai-java:3.5.0`（兼容性推荐）或 `com.alibaba:dashscope-sdk-java` 最新版  
- **Node.js/Go**：分别执行 `npm install openai` 或 `go get github.com/openai/openai-go/v3`  
详情请参考 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 文档。

### 2. API Key 配置
- 从 [密钥管理页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建或复制 Key  
- **推荐方式**：设为环境变量 `DASHSCOPE_API_KEY`（Linux/macOS：追加至 `~/.bashrc` 或 `~/.zshrc`；Windows：系统属性→环境变量）  
- **替代方式**：CLI 中执行 `bl auth login --api-key <key>`，或 OpenAI SDK 中直接传入 `api_key` 参数  

### 3. CLI 快速启动
- 前置：`Node.js >= 22.12.0`，`npm`（禁用 pnpm/yarn）  
- 安装：`npm install -g bailian-cli` → `npx skills add modelstudioai/cli --all -g`  
- 鉴权：`bl auth login --console`（推荐）或 `bl auth login --api-key <key>`  
- 验证：`bl text chat --message "ping" --non-interactive`  

## 限制和注意事项

- **API Key 管理**：单个业务空间最多创建 20 个 Key；默认业务空间 Key 可调用所有标准模型，子空间 Key 仅限已授权模型；RAM 用户 Key 格式为 `username@<AccountAlias>.onaliyun.com`  
- **地域与网络**：IPv6 白名单仅华北2（北京）支持；美国（弗吉尼亚）地域仅支持 IPv4；企业网络需配置 npm 镜像（如 `https://registry.npmmirror.com/`）或 GOPROXY（`https://mirrors.aliyun.com/goproxy/`）  
- **安全约束**：  
  - 禁止在浏览器/移动应用等客户端暴露长期 Key；敏感场景应使用 [临时 API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)（最长 1800 秒）  
  - CLI 在 CI/CD 中必须通过 `--non-interactive` + 环境变量注入 Key，严禁硬编码或明文传递  
- **模型能力边界**：  
  - `qwen3-vl-plus` 等视觉模型支持 `--image`/`--video` 输入，但纯文本模型（如 `qwen3-max`）若收到含 `image_url` 的 `messages` 将报错 `Unexpected item type in content`  
  - 结构化输出（`response_format=json_object`）与思考模式互斥，启用前者时必须 `enable_thinking=false`  
- **错误排查**：所有调用失败均应记录 `Request ID`（UUID 格式），并结合 [错误码文档](../../raw/model-api-reference/preparations/error-code.md) 定位原因；常见问题如 `Arrearage`（欠费）、`Model not exist`（未开通模型服务）需优先检查账户状态与模型市场开通情况

## 来源文档

- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


