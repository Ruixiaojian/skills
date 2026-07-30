# bailian [application call](../api/application-call.md)ing

百炼应用调用是指通过 DashScope SDK 或 HTTP API，将百炼平台创建的智能体应用（Single Agent Application）或工作流应用（Workflow Application）集成到自有业务系统中。调用过程统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话及插件参数透传，适用于各类 AI 增强型业务场景。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)（即 Single Agent Application），适用于简单意图识别+大模型响应场景；
  - [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)，适用于含插件、条件分支、多节点编排的复杂逻辑场景。
- **核心能力**：
  - 单轮文本生成（`prompt` 输入 → `output.text` 输出）；
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组维护上下文）；
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 传递插件所需业务参数）；
  - 调试信息返回（`debug` 字段可启用）；
  - [Token](../concepts/token.md) 统计与模型用量（`usage.models` 中包含 `model_id`、`input_tokens`、`output_tokens`）。

> **注意**：文档 2 明确声明“本文档仅适用于华北2（北京）地域”，而文档 1 和文档 3 均未限定地域。实际调用时若在非北京地域遇到 404 或地域不可用错误，请确认应用部署地域并参考 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 的地域约束说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | ✅ | 百炼控制台应用卡片上复制的 APP_ID，区分智能体应用与工作流应用 |
| `prompt` | string | ⚠️ | 单轮调用必需；若使用 `messages` 进行多轮对话，则此项可省略 |
| `biz_params` | object | ❌ | 用于插件参数透传，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": <value> } } }`，详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |
| `session_id` | string | ❌ | 启用云端会话管理时传入，有效期 1 小时，最多 50 轮；与 `messages` 同时存在时优先使用 `messages` |
| `messages` | array | ❌ | 显式维护的对话历史数组，格式同 OpenAI `messages`（`role`, `content`），推荐用于精确上下文控制 |
| `parameters` | object | ❌ | 预留扩展字段，当前暂无公开可用参数 |
| `debug` | object | ❌ | 设为空对象 `{}` 可启用调试模式，返回更详细的内部执行链路信息 |

## 使用方式

### 1. 准备工作
- 获取 API Key：前往 [密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建并配置为环境变量 `DASHSCOPE_API_KEY`（[推荐做法](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)）；
- 获取 `app_id`：在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面复制目标应用 ID；
- （SDK 方式）安装对应语言 SDK：Python 使用 `pip install -U dashscope`；Java 需引入 `dashscope-sdk-java`（建议 ≥2.12.0）；其他语言参考各文档示例。

### 2. 调用示例（统一接口）
所有方式均请求 `POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`：

- **SDK（Python）**
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？",
      biz_params={"user_defined_params": {"plugin_abc123": {"query_id": 42}}}
  )
  print(response.output.text)
  ```

- **HTTP（curl）**
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "input": {
            "prompt": "你是谁？",
            "biz_params": {
                "user_defined_params": {
                    "plugin_abc123": {"query_id": 42}
                }
            }
        }
      }'
  ```

### 3. 多轮对话处理
- **推荐方式（显式 `messages`）**：客户端自行维护 `messages` 列表，每次请求携带完整历史（含最新用户输入），避免依赖服务端状态；
- **便捷方式（`session_id`）**：首次调用后从响应中提取 `session_id`，后续请求复用该值即可自动加载历史（需注意 1 小时过期限制）。

## 限制和注意事项

- **地域限制**：工作流应用调用仅支持华北2（北京）地域，智能体应用无明确地域限制，但建议与应用部署地域保持一致以降低延迟；
- **API Key 安全**：严禁硬编码 API Key，必须通过环境变量或密钥管理服务注入；
- **插件参数透传**：仅当应用已关联对应插件且插件参数配置为“业务透传”时生效；插件 ID（`plugin_code`）需从插件卡片获取，不可猜测；
- **错误处理**：所有调用均需检查 `status_code`（HTTP）或 `response.status_code`（SDK），失败时解析 `request_id` 和 `message` 并查阅 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)；
- **SDK 版本兼容性**：Java SDK 要求 ≥2.12.0（见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 和 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)），Python SDK 无显式版本要求，但插件参数功能需 ≥1.14.0（见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）；
- **响应结构一致性**：无论应用类型，成功响应均含 `output.text` 字段；`usage.models` 中 `model_id` 表明实际执行模型（如 `qwen-max`、`qwen-plus`），可用于计费与性能分析。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)



