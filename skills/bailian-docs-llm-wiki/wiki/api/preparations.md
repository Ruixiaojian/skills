# preparations

在调用阿里云百炼平台的模型或应用前，开发者需完成基础环境准备：获取并安全配置 API Key、安装兼容 SDK、理解关键参数约束，并选择合适的调用方式（HTTP、SDK 或 CLI）。这些步骤直接影响服务可用性、安全性与调试效率，是所有集成工作的前提。

## 支持的模型/功能

百炼平台支持[多模态](../concepts/multi-modal.md)模型（如 `qwen3-vl-plus`、`qwen-image-2.0`）、文本生成模型（如 `qwen3.7-max`、`qwen3-235b-a22b-instruct-2507`）、语音合成（`cosyvoice`）、语音识别（`paraformer`）、向量嵌入（`text-embedding-v2`）及排序模型（`text-rerank`）等。部分模型具备特定能力约束：  
- 思考模式（`enable_thinking=true`）仅支持[流式输出](../concepts/streaming-output.md)（`stream=true`），且要求 `incremental_output=true`；[错误码文档](../../raw/model-api-reference/preparations/error-code.md) 明确指出 `parameter.enable_thinking must be set to false for non-streaming calls`；  
- 联网搜索（`enable_search=true`）仅限指定模型支持，非支持模型会返回 `This model does not support enable_search` 错误；  
- 结构化输出（`response_format={"type": "json_object"}`）要求提示词中包含 `json` 关键词，且不可与思考模式共用；  
- 百炼 CLI 提供全模态交互能力（`bl omni`），支持图片、音频、视频混合输入，底层调用 `qwen3.5-omni-plus` 等模型 [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。

> **注意**：文档 1 中提到“API Key 的调用权限完全由其归属业务空间决定”，而文档 4 的 CLI 配置说明中明确支持 `--config token-plan` 切换 [Token](../concepts/token.md) Plan 订阅配置。但文档 1 未说明 [Token](../concepts/token.md) Plan API Key（`sk-sp-` 开头）是否受业务空间权限控制——实际中 [Token](../concepts/token.md) Plan Key 权限独立于业务空间，此为隐含差异，开发者应以控制台实际权限策略为准。

## 关键参数

调用时需严格校验以下参数范围，否则将触发 400 错误：  
- `temperature`: `[0.0, 2.0)`；`top_p`: `(0.0, 1.0]`；`top_k`: `≥ 0`；`repetition_penalty`: `> 0.0`；`presence_penalty`: `[-2.0, 2.0]`；  
- `max_tokens`: 必须在模型文档标注的“最大输出 Token 数”范围内；  
- `n`: 文本生成最多 4 个候选结果；`seed`: DashScope 协议下需为 `[0, 9223372036854775807]` 内整数；  
- `thinking_budget`: 必须为正整数且 ≤ 模型支持的最大思维链长度；  
- `stop`: 类型必须为 `str`、`list[str]`、`list[int]` 或 `list[list[int]]`，且列表内元素类型一致；  
- `messages` 输入不能为空数组，且纯文本模型不接受 `content` 为数组（如 `{"role":"user","content":[{"type":"text","text":"..."}]}`），必须为字符串 [错误码文档](../../raw/model-api-reference/preparations/error-code.md)。

## 使用方式

### API Key 获取与配置  
- 通过[阿里云百炼控制台](https://bailian.console.aliyun.com/)创建 API Key，主账号或具备 `管理员`/`API-Key` 权限的子账号可操作；  
- 推荐将 Key 配置为环境变量 `DASHSCOPE_API_KEY`（Linux/macOS/Windows 均支持），避免硬编码泄露风险 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)；  
- 美国（弗吉尼亚）地域不支持禁用/重置 Key，且创建后仅显示一次明文，需立即保存。

### SDK 安装  
- **Python**: 可选 `openai`（`pip install -U openai`）或 `dashscope`（`pip install -U dashscope`）；  
- **Java**: DashScope SDK（Maven/Gradle 引入 `com.alibaba:dashscope-sdk-java`）或 OpenAI Java SDK（推荐 `3.5.0+`）；  
- **Node.js/Go**: 分别使用 `npm install openai` 或 `go get github.com/openai/openai-go/v3`；  
- 所有 SDK 均需配合 `base_url`（即 API Host）使用，该地址因地域和协议（OpenAI 兼容/Anthropic 兼容）而异 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

### CLI 快速验证  
- 安装：`npm install -g bailian-cli`（要求 Node.js ≥ 22.12.0）；  
- 认证：`bl auth login --console`（推荐）或 `bl auth login --api-key sk-xxx`；  
- 首次调用：`bl text chat --message "ping" --non-interactive`；  
- CLI 支持 `--region cn|us|intl` 切换地域，默认 `cn`，且全局参数如 `--timeout`、`--output json` 可统一控制行为 [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。

## 限制和注意事项

- **API Key 安全**：新创建 Key 以 `sk-ws` 开头，创建后仅一次明文展示，关闭弹窗即不可恢复；旧 `sk-` Key 仍可用，但建议迁移至新格式；  
- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域的 API Key 和服务端点相互独立，跨地域调用需对应 Key；  
- **模型开通**：调用前需在[模型市场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)开通目标模型，否则返回 `The product is not activated`；  
- **错误排查**：失败请求务必记录 `Request ID`（UUID 格式），用于自助排查或提交工单；模型监控日志仅支持部分地域和模型，且存在分钟级延迟；  
- **CLI 约束**：百炼 CLI 仅支持 npm 安装，禁止使用 pnpm/yarn；认证时若控制台登录后仍提示缺 Key，需先 `bl update` 升级 CLI 版本。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)


