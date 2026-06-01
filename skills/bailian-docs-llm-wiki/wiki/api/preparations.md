# preparations

在使用阿里云百炼平台的大模型服务之前，需要完成一系列准备工作，包括获取 API Key、配置环境变量、安装 SDK 等。本文汇总了这些准备步骤的核心内容，帮助开发者快速完成接入前的配置工作。

## 准备流程概览

整体准备流程分为三步：

1. **获取 API Key** — 创建鉴权凭证
2. **配置环境变量** — 安全存储 API Key
3. **安装 SDK** — 选择合适的 SDK 进行开发

## 获取 API Key

API Key 是调用百炼大模型和应用的鉴权凭证。详细操作步骤参见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

### 权限要求

需使用主账号，或具备 `管理员` 或 `API-Key` 页面权限的子账号操作。

### 各地域 Base URL

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

### API Key 权限配置

- **全部**：授予调用所有模型与应用的权限。
- **自定义**：可配置 IP 访问白名单（最多 20 个 IPv4/IPv6 地址或网段）。

> **注意**：目前仅华北2（北京）地域支持为 API Key 配置 IP 白名单等精细权限控制，其他地域暂不支持。

### API Key 关键特性

- **无过期时间**：创建后永久有效，手动删除后即失效。
- **权限由归属业务空间决定**：同一空间内的 API Key 权限相同，无需为不同模型类型创建不同的 API Key。
- **数量限制**：华北2（北京）、新加坡和德国（法兰克福）地域每个主账号每个地域最多 50 个；美国（弗吉尼亚）地域每个归属账号最多 20 个。
- **临时 API Key**：如需为第三方提供临时访问权限，可生成有效期 60 秒的临时 API Key。

> **注意**：Coding Plan 使用专属 API Key（格式：`sk-sp-xxxxx`），与本文介绍的百炼通用 API Key（格式：`sk-xxxxx`）不同。

## 将 API Key 配置到环境变量

为避免在代码中硬编码 API Key 导致泄漏风险，建议将其配置为环境变量。环境变量名称统一为 `DASHSCOPE_API_KEY`。详细操作参见 [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)。

### 各平台配置方式速查

| 操作系统 | 永久性环境变量 | 临时性环境变量 |
|---------|-------------|-------------|
| Linux | 追加到 `~/.bashrc`，然后 `source ~/.bashrc` | `export DASHSCOPE_API_KEY="your-key"` |
| macOS (Zsh) | 追加到 `~/.zshrc`，然后 `source ~/.zshrc` | `export DASHSCOPE_API_KEY="your-key"` |
| macOS (Bash) | 追加到 `~/.bash_profile`，然后 `source ~/.bash_profile` | `export DASHSCOPE_API_KEY="your-key"` |
| Windows CMD | `setx DASHSCOPE_API_KEY "your-key"`（新窗口生效） | `set DASHSCOPE_API_KEY=your-key` |
| Windows PowerShell | `[Environment]::SetEnvironmentVariable(...)` | `$env:DASHSCOPE_API_KEY = "your-key"` |
| Windows 系统属性 | 通过"编辑系统环境变量"图形界面配置 | — |

### 环境变量不生效的常见原因

- 仅设置了临时环境变量，对已启动的 IDE 或应用不生效
- 设置永久环境变量后未重启 IDE、命令行工具或应用服务
- 使用 `sudo` 执行脚本时未继承环境变量（可用 `sudo -E` 解决）
- 应用通过 systemd 等服务管理器启动，需在其配置文件中添加环境变量

## 安装 SDK

百炼支持通过官方 DashScope SDK 或 OpenAI 兼容 SDK 进行调用。详细安装步骤参见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

### SDK 支持矩阵

| 语言 | OpenAI SDK | DashScope SDK | 最低版本要求 |
|------|-----------|--------------|------------|
| Python | ✅ `pip install -U openai` | ✅ `pip install -U dashscope` | Python >= 3.8 |
| Java | ✅ `com.openai:openai-java`（推荐 3.5.0） | ✅ `com.alibaba:dashscope-sdk-java` | Java 8+（OpenAI SDK） |
| Node.js | ✅ `npm install --save openai` | — | — |
| Go | ✅ `go get github.com/openai/openai-go/v3` | — | Go 1.22+ |

### 安装提示

- **Node.js**：安装失败时可配置镜像源 `npm config set registry https://registry.npmmirror.com/`
- **Go**：访问超时时可设置代理 `go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct`
- **Java**：Maven/Gradle 依赖中需将 `the-latest-version` 替换为实际的最新版本号

## 常见错误码

调用模型失败时，可根据返回的错误码排查问题。完整错误码列表参见 [错误码](../../raw/model-api-reference/preparations/error-code.md)。以下列出最常遇到的几类错误：

### 参数相关（400-InvalidParameter）

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `Model not exist.` | 模型名称错误或格式不正确 | 检查大小写、空格，使用百炼模型ID而非开源社区名称 |
| `Range of input length should be [1, xxx]` | 输入内容超过模型上限 | 控制 Token 数在模型最大输入范围内 |
| `Range of max_tokens should be [1, xxx]` | `max_tokens` 超出模型允许范围 | 参考模型列表文档中的最大输出 Token 数 |
| `Temperature should be in [0.0, 2.0)` | temperature 参数越界 | 设置为 [0.0, 2.0) 范围内的数字 |
| `enable_thinking only support stream call` | 非流式调用思考模式 | 设置 `enable_thinking=false` 或改用流式输出 |
| `Required body invalid` | 请求体 JSON 格式错误 | 检查 JSON 格式，如多余逗号、括号未闭合等 |

### 文件相关

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `Invalid file` | file-id 无效 | 确认 file-id 是否正确且属于当前账号 |
| `File format is not supported` | 文件格式不支持 | 检查文件格式是否在支持列表中 |
| `File exceeds size limit` | 文件大小超限 | 确保文件小于 150 MB |

### 调试建议

- 推荐使用[阿里云 AI 助理](https://www.aliyun.com/ai-assistant/)，输入完整错误信息即可获取解决方案
- 请勿以任何方式公开 API Key，避免安全风险或资金损失

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)

