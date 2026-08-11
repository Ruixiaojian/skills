# preparations

在调用百炼平台模型服务前，开发者需完成 API Key 获取与配置、SDK 或 CLI 工具安装、环境适配及参数合规性校验。这些步骤是所有模型调用（文本、图像、视频、语音、向量等）的通用前置条件，直接影响调用成功率与安全性。本文档整合关键准备动作，聚焦可执行的技术要点，避免冗余说明。

## 支持的模型/功能

百炼平台支持全模态模型调用，包括：
- **文本生成**：如 `qwen3-8b`、`qwen3.7-max`、`deepseek-r1` 等；
- **[多模态](../concepts/multi-modal.md)理解与生成**：如 `qwen3-vl-plus`（视觉理解）、`qwen3.5-omni-plus`（全模态对话）、`qwen-image-2.0`（文生图）、`happyhorse-1.1-t2v`（文生视频）；
- **语音与向量模型**：如 `cosyvoice`（TTS）、`paraformer`（ASR）、`text-embedding-v3`（Embedding）；
- **结构化输出与思考模式**：需配合 `response_format={"type": "json_object"}` 或 `enable_thinking=true` 使用（详见 [错误码](../../raw/model-api-reference/preparations/error-code.md) 中的约束说明）。

> **注意**：文档 3 中 `bl text chat` 默认模型为 `qwen3.7-max`，而文档 2 中 OpenAI SDK 示例未指定默认模型；实际调用时必须显式传入 `model` 参数，否则可能因网关路由失败返回 `Model not exist.` 错误（见 [错误码](../../raw/model-api-reference/preparations/error-code.md)）。

## 关键参数

以下参数在各类调用方式中通用，且受严格校验：

| 参数 | 合法范围 | 说明 | 来源依据 |
|------|----------|------|----------|
| `temperature` | `[0.0, 2.0)` | 必须为浮点数，超出将报错 `Temperature should be in [0.0, 2.0)` | [错误码](../../raw/model-api-reference/preparations/error-code.md) |
| `top_p` | `(0.0, 1.0]` | 必须为浮点数，超出将报错 `Range of top_p should be (0.0, 1.0]` | [错误码](../../raw/model-api-reference/preparations/error-code.md) |
| `max_tokens` | `[1, 模型最大输出 Token]` | 需查模型文档确认上限，超限将触发 `Range of max_tokens should be [1, xxx]` | [错误码](../../raw/model-api-reference/preparations/error-code.md) |
| `seed` | `[0, 9223372036854775807]` | DashScope 协议下整型，超限将报错 | [错误码](../../raw/model-api-reference/preparations/error-code.md) |
| `n`（生成数量） | `[1, 4]`（文本）或 `[1, 6]`（图像） | 图像生成 `bl image generate --n` 支持最多 6 张，但文本 `n` 仍限 4 | [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md) |
| `enable_thinking` | `true` / `false` | 部分模型（如 `qwen3-235b-a22b-thinking-2507`）强制要求 `true`；开启时必须同时设 `stream=true` 和 `incremental_output=true` | [错误码](../../raw/model-api-reference/preparations/error-code.md) |

## 使用方式

### 1. 获取并配置 API Key  
前往[密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key)创建或复制 API Key，归属账号建议选主账号（数字ID），归属业务空间选“默认业务空间”以获得全部标准模型访问权限。配置方式二选一：  
- **环境变量**：Linux/macOS 执行 `export DASHSCOPE_API_KEY='sk-xxx'`；Windows 在系统属性中新建变量 `DASHSCOPE_API_KEY`（见 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）；  
- **CLI 工具鉴权**：运行 `bl auth login --api-key sk-xxx`（推荐控制台登录 `bl auth login --console`，自动打通应用管理能力）。

### 2. 安装调用工具  
- **SDK**：Python 用户可选 `pip install -U openai`（OpenAI 兼容）或 `pip install -U dashscope`（原生 SDK）；Java/Node.js/Go 用户按 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 文档添加对应依赖；  
- **CLI**：仅支持 `npm install -g bailian-cli`（Node ≥ 22.12.0），安装后通过 `bl text chat --message "ping"` 验证（见 [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)）。

### 3. 发起调用  
- OpenAI SDK 示例（Python）：
  ```python
  from openai import OpenAI
  client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
  response = client.chat.completions.create(model="qwen3-8b", messages=[{"role": "user", "content": "你好"}])
  ```
- CLI 示例（图像生成）：
  ```bash
  bl image generate --prompt "科技感办公室" --model qwen-image-2.0 --n 2 --out-dir ./output/
  ```

## 限制和注意事项

- **API Key 安全**：严禁在客户端代码（浏览器、移动 App）或公开日志中硬编码长期 API Key；高风险场景应使用[临时 API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)（最长 1800 秒）；  
- **地域与 Endpoint**：中国大陆版 Base URL 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`，国际版为 `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`；CLI 可通过 `--region cn/us/intl` 切换；  
- **模型开通状态**：调用前必须在[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)开通目标模型，否则返回 `The product is not activated`；  
- **环境变量生效问题**：IDE 或服务进程需重启才能加载新环境变量；使用 `sudo` 时需加 `-E` 参数（`sudo -E python script.py`）传递变量；  
- **参数冲突**：`enable_thinking=true` 时禁止设置 `response_format={"type": "json_object"}`，否则报错 `Json mode response is not supported when enable_thinking is true`（见 [错误码](../../raw/model-api-reference/preparations/error-code.md)）。

## 来源文档

- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


