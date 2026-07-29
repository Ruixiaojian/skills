# preparations

在调用阿里云百炼平台的模型与服务前，开发者需完成 SDK 安装、API Key 获取与配置、CLI 工具部署等基础准备。这些步骤共同构成安全、稳定、可维护的调用链路，直接影响后续模型调用的可用性与合规性。本文档整合关键操作路径与约束条件，面向工程实践提供结构化指引。

## 支持的模型/功能

百炼平台支持全模态模型调用，包括文本生成（如 `qwen3.7-max`）、图像生成（`qwen-image-2.0`）、视频生成（`happyhorse-1.0-t2v`）、语音合成（`cosyvoice-v3-flash`）、语音识别（Paraformer）、向量嵌入（`text-embedding-v3`）、排序（`text-rerank-v3`）及多模态理解（`qwen3-vl-plus`、`qwen3.5-omni-plus`）。所有模型均通过统一 API 接口暴露，但协议兼容性存在差异：[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)适用于多数第三方 SDK，而 Anthropic 兼容接口仅限 Messages 协议（如 `anthropic.messages`），具体请以各模型文档为准。[安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 文档列出了各语言 SDK 对应的模型支持范围与调用示例。

## 关键参数

调用时需关注以下核心参数及其取值约束：

- **`model`**：必须为百炼控制台模型市场中已开通的**标准模型 ID**（如 `qwen3.7-max`），不可混用 Hugging Face 格式（如 `Qwen/Qwen3-7B-Instruct`）；未开通模型将返回 `Model not exist` 或 `The product is not activated` 错误。
- **`temperature`**：取值范围 `[0.0, 2.0)`，超出将触发 `400-InvalidParameter`。
- **`top_p`**：取值范围 `(0.0, 1.0]`。
- **`max_tokens`**：必须为 `[1, 模型最大输出 Token 数]` 内的整数，上限见各模型文档。
- **`n`**（生成数量）：图像/视频类接口默认为 `1`，上限为 `6`；文本类接口上限为 `4`。
- **`seed`**：DashScope 协议下有效范围为 `[0, 9223372036854775807]`。
- **`enable_thinking`**：思考模式仅支持[流式输出](../concepts/streaming-output.md)（`stream=true`），且与 `response_format="json_object"` 互斥；部分模型（如 `qwen3-235b-a22b-thinking-2507`）强制要求设为 `true`。
- **`messages` / `prompt`**：二者必须且仅存在其一；纯文本模型不接受 `content` 为数组或含 `image_url` 的多模态消息，否则报错 `Unexpected item type in content`。

> **注意**：文档 3 中 CLI 的 `bl text chat` 默认模型为 `qwen3.7-max`，而文档 4 的错误码示例中多次出现 `qwen3-235b-a22b-thinking-2507` 等长 ID 模型。实际使用时须以 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md) 后在控制台模型市场确认的**已开通模型列表**为准，避免因模型名过时或未开通导致 `Model not exist`。

## 使用方式

### 1. SDK 集成
推荐使用 DashScope SDK（官方维护）或 OpenAI 兼容 SDK（跨平台适配）。Python 开发者可任选：
```bash
pip install -U dashscope      # DashScope 原生 SDK
pip install -U openai         # OpenAI 兼容 SDK（需配置 base_url）
```
Java、Node.js、Go 等语言同理，详见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。调用时需显式指定 `base_url`（即 API Host），不同地域与协议的端点不同，不可复用。

### 2. CLI 快速验证
百炼 CLI（`bailian-cli`）适用于本地调试与自动化脚本：
```bash
npm install -g bailian-cli
bl auth login --console  # 浏览器 OAuth 登录（推荐）
# 或
bl auth login --api-key sk-xxx  # 手动输入 API Key
bl text chat --message "ping" --non-interactive
```
CLI 要求 Node.js ≥ 22.12.0，且**仅支持 npm 全局安装**（禁用 pnpm/yarn）。认证后可通过 `bl config set` 持久化模型、输出目录等参数。

### 3. 环境变量安全配置
**强烈建议**将 API Key 存入环境变量而非硬编码：
- Linux/macOS：写入 `~/.bashrc` 或 `~/.zshrc`，执行 `source` 生效  
- Windows：通过系统属性或 PowerShell 设置用户级变量 `DASHSCOPE_API_KEY`  
详情见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md) 中的环境变量配置章节。

## 限制和注意事项

- **API Key 安全**：新创建的按量付费 API Key 以 `sk-ws` 开头，创建后**仅展示一次明文**，关闭弹窗即不可恢复；旧 `sk-` 密钥仍可用，但建议升级。切勿在代码、日志、Git 仓库中明文存储。
- **地域隔离**：API Key 与服务端点（`base_url`）严格绑定地域（如华北2、新加坡、美国弗吉尼亚）。跨地域调用需单独创建对应地域的 Key 并配置 `--region` 参数。
- **权限模型**：API Key 权限由其**归属业务空间**决定，同一空间内所有 Key 权限一致。子业务空间下的 Key 仅能调用该空间已授权的模型，需提前在控制台完成模型授权。
- **文件限制**：Qwen-Long 等长文本模型仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD 格式，单文件 ≤ 150 MB、≤ 1500 页；图片类文件需先用 Qwen-VL 提取文本。
- **错误处理**：常见错误如 `Arrearage`（欠费）、`InvalidParameter`（参数越界）、`Model not exist`（未开通）均有明确修复路径，建议集成 [阿里云 AI 助理](https://www.aliyun.com/ai-assistant/) 实时解析错误响应。[错误码](../../raw/model-api-reference/preparations/error-code.md) 文档覆盖全部 HTTP 4xx/5xx 场景及解决方案。

> **注意**：文档 3 中 CLI 的 `bl image generate --n 6` 允许单次生成 6 张图，但文档 4 的错误码说明中 `n` 参数上限为 `4` —— 此矛盾源于**接口协议差异**：CLI 封装层对图像类接口做了特殊处理（非标准 OpenAI 协议），而错误码文档描述的是通用文本生成接口约束。开发者应以具体接口文档（如 [图像生成 API](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)）为准。

## 来源文档

- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


