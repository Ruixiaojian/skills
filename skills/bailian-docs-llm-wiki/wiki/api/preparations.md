# preparations

调用阿里云百炼模型前，需要完成三项准备工作：获取并妥善保管 API Key、将 Key 配置到环境变量以避免硬编码泄漏、安装官方 SDK（DashScope 或 OpenAI 兼容）。本页汇总了准备阶段的关键信息以及常见错误码的速查索引，面向首次接入与排查问题的开发者。

## 1. 获取 API Key

[获取API Key](../../raw/model-api-reference/preparations/get-api-key.md) 必须由主账号或具备 `管理员` / `API-Key` 页面权限的子账号操作。各地域的入口不同：

- **华北2（北京）**：百炼控制台 → API Key → **创建 API Key**，可选择**全部**权限或**自定义**（限制 IP 白名单，最多 20 个 IPv4/IPv6 地址或网段）。
- **新加坡 / 美国（弗吉尼亚）/ 德国（法兰克福）**：在右上角切换到目标地域，进入**工作台 → API Key**。创建成功后弹窗仅展示一次完整 Key，**关闭后无法再次查看明文**，必须立即复制保存。

> **注意**：目前仅华北2（北京）地域支持 IP 白名单等精细权限控制；其他地域只能配置归属业务空间和描述。

**API Key 与业务空间的关系**：API Key 的调用权限完全由其**归属业务空间**决定。同一空间内的 API Key 权限相同，无需为不同模型（文生文 / 文生图 / 语音）创建不同 Key。调优后的模型仅能用所在业务空间的 API Key 调用。

**配额**：

| 地域 | 每个主账号最大 API Key 数 |
| --- | --- |
| 华北2（北京）、新加坡、德国（法兰克福） | 50 |
| 美国（弗吉尼亚） | 20 |

> **注意**：[Coding Plan](https://help.aliyun.com/zh/model-studio/coding-plan) 必须使用专属 API Key（格式 `sk-sp-xxxxx`），不能与本文获取的通用 API Key（格式 `sk-xxxxx`）混用。

**临时 API Key**：若需为第三方应用提供临时访问权限，可生成有效期 60 秒的临时 Key，避免长期 Key 外泄。RAM 用户在 RAM 控制台被禁用或删除后，其创建的所有 API Key 都会立即失效。

## 2. 配置环境变量（DASHSCOPE_API_KEY）

强烈建议将 API Key 写入环境变量 `DASHSCOPE_API_KEY`，避免硬编码到代码中。[将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md) 给出了三大操作系统的完整命令。

### Linux / macOS

| 类型 | Linux | macOS (Zsh) | macOS (Bash) |
| --- | --- | --- | --- |
| 永久 | 写入 `~/.bashrc` | 写入 `~/.zshrc` | 写入 `~/.bash_profile` |
| 临时 | `export DASHSCOPE_API_KEY="..."` | 同左 | 同左 |
| 生效 | `source ~/.bashrc` | `source ~/.zshrc` | `source ~/.bash_profile` |
| 验证 | `echo $DASHSCOPE_API_KEY` | 同左 | 同左 |

写入永久变量的最简单方式：

```bash
echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.zshrc
source ~/.zshrc
```

### Windows

- **系统属性**：`Win+Q` 搜索“编辑系统环境变量” → **环境变量 → 新建**，变量名 `DASHSCOPE_API_KEY`。
- **CMD 永久**：`setx DASHSCOPE_API_KEY "YOUR_KEY"`（验证 `echo %DASHSCOPE_API_KEY%`）。
- **PowerShell 永久**：`[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "YOUR_KEY", [EnvironmentVariableTarget]::User)`（验证 `echo $env:DASHSCOPE_API_KEY`）。
- **临时**：CMD 用 `set DASHSCOPE_API_KEY=...`，PowerShell 用 `$env:DASHSCOPE_API_KEY = "..."`。

> **注意**：环境变量生效后**不会**自动注入到已经启动的 IDE、命令行工具或服务进程。常见失败原因：
> - 只设置了临时变量，新窗口或新会话失效；
> - 未重启 IDE / 应用 / 命令行；
> - 通过 `systemd` / `supervisord` 等服务管理器启动的进程，需要在服务配置中显式声明；
> - 使用 `sudo python xx.py` 时不继承用户环境，需改用 `sudo -E python xx.py`。

## 3. 安装 SDK

百炼同时支持官方 [DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md)（Python / Java）与 OpenAI 官方 SDK（通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，覆盖 Python / Node.js / Java / Go）。语言与 SDK 对照如下：

| 语言 | DashScope 官方 | OpenAI 兼容 |
| --- | --- | --- |
| Python (`>=3.8`) | `pip install -U dashscope` | `pip install -U openai` |
| Java (`>=8`) | Maven `com.alibaba:dashscope-sdk-java` | Maven `com.openai:openai-java`（推荐 `3.5.0`） |
| Node.js | — | `npm install --save openai` |
| Go (`>=1.22`) | — | `go get github.com/openai/openai-go/v3` |

部分常用配置：

- npm 安装失败时切换镜像：`npm config set registry https://registry.npmmirror.com/`
- Go 走代理：`go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct`
- Java 项目须将 `the-latest-version` 替换为 Maven Central 上的实际版本号。

完成安装后即可调用[文本生成](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)、[图像生成](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)、[视频生成](https://help.aliyun.com/zh/model-studio/legacy-image-to-video-api-reference/)、[语音合成 / 识别](https://help.aliyun.com/zh/model-studio/cosyvoice-python-sdk)、向量、排序等模型。

## 4. 调用方式：Base URL 速查

通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用时，需要根据 API Key 所属地域设置 Base URL：

| 地域 | Base URL |
| --- | --- |
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

> **注意**：新加坡与德国 Base URL 中的 `{WorkspaceId}` 必须替换为真实的[业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)，否则会返回鉴权错误。

## 5. 排错：常见错误码索引

[错误码](../../raw/model-api-reference/preparations/error-code.md) 文档以 HTTP 状态码 + 错误名分组（如 `400-InvalidParameter`）。准备阶段最容易踩到的几类如下：

### 参数类（400-InvalidParameter）

| 报错关键词 | 典型原因 | 修复 |
| --- | --- | --- |
| `Model not exist` | 模型名拼错或混用了开源社区命名 | 严格用百炼模型 ID，如 `qwen3-235b-a22b-instruct-2507`（不是 `Qwen/Qwen3-...`） |
| `Range of max_tokens / input length should be [1, xxx]` | 超出模型最大输入 / 输出 Token | 对照模型列表的上限；连续对话时开启新会话清空历史 |
| `Temperature should be in [0.0, 2.0)` / `top_p (0.0, 1.0]` / `top_k >= 0` | 采样参数越界 | 按区间修正 |
| `parameter.enable_thinking must be set to false for non-streaming calls` | 思考模式只能流式调用 | 改用流式，且 `incremental_output=true`、`result_format="message"` |
| `'audio' output only support with stream=true` | Qwen-Omni 强制流式 | 启用 `stream=true` |
| `messages with role "tool" must be a response to a preceding ... tool_calls` | Function Calling 缺少 Assistant Message | 把模型上一轮的 Assistant Message 追加回 `messages` 再加 Tool Message |
| `'messages' must contain the word 'json' ...` | 用 `response_format=json_object` 但提示词无 `json` 关键字 | 在提示词中加入 `json` 字样 |
| `Json mode response is not supported when enable_thinking is true` | 结构化输出与思考模式互斥 | 把 `enable_thinking` 设为 `false` |
| `Required body invalid, please check the request body format` | JSON 体不合法 | 检查多余逗号、括号闭合 |
| `The provided URL does not appear to be valid` | 多模态输入 URL 格式不符 | URL 需以 `http(s)://` / `data:` / `file://` 开头；OSS 临时 URL 走 HTTP 时要加 Header `X-DashScope-OssResourceResolve: enable`，SDK 仅支持 DashScope SDK |

### 文件 / 多模态类

- 单张图片或 Base64 文件不得超过 10 MB；视频 URL 上限按模型不同分别为 2 GB（Qwen3-VL、qwen-vl-max）/ 1 GB（qwen-vl-plus 系列）/ 150 MB（其他）。
- Qwen-Long 仅支持纯文本格式（TXT / DOCX / PDF / EPUB / MOBI / MD），图片或扫描文档请改用千问 VL。
- 视频以图像序列输入时：Qwen3-VL 与 Qwen2.5-VL 系列需 4–512 张，其他模型 4–80 张。
- File 接口：单文件 ≤ 150 MB、≤ 15000 页，`file-id` 同时引用数量 < 100。

### 账号 / 鉴权类

- `Arrearage`：账号欠费，登录控制台**费用与成本**充值，等待几分钟同步。
- 调试时遇到难以判断的报错，推荐直接复制报错原文到[阿里云 AI 助理](https://www.aliyun.com/ai-assistant/)，其知识库整合了官方文档可直接给出修复方案。

## 6. 安全与运维要点

- API Key 一旦创建无失效日期，**只能手动删除**；丢失需立即删除并重建。
- 任何第三方场景请优先使用临时 API Key（有效期 60 秒）或为 Key 配置 IP 白名单（华北2）。
- 切勿将 API Key 提交到 Git、写入前端代码或公开渠道；强烈建议读取自 `DASHSCOPE_API_KEY` 环境变量。
- 多业务 / 多团队场景使用子业务空间隔离权限与账单；调优后的模型只能在所在业务空间的 API Key 下调用。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


