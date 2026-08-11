# bailian [application call](../api/application-call.md)ing

百炼应用调用是指通过 DashScope SDK 或标准 HTTP API，将阿里云百炼平台创建的智能体应用（Agent 1.0）或工作流应用集成至第三方业务系统的能力。该机制统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮问答、多轮对话及[插件](../concepts/plugin.md)参数透传等核心场景，适用于快速构建 AI 增强型业务逻辑。

## 支持的模型/功能

- **应用类型**：同时支持 [调用智能体应用 (raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 和 [调用工作流应用 (raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)，二者调用方式完全一致。
- **核心能力**：
  - 单轮 [prompt](prompt.md) 响应（基础文本生成）
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）
  - 自定义[插件](../concepts/plugin.md)参数透传（仅限已关联[插件](../concepts/plugin.md)的智能体应用或工作流应用中的插件节点），详见 [应用的自定义参数传递 (raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- **不支持能力**：工作流应用明确不支持文生图类大模型（如 wanx 系列），此限制在文档中强调；智能体应用无此限制，但实际可用模型取决于应用内配置。

> **注意**：文档 3 明确声明“百炼工作流不支持使用文生图大模型”，而文档 1 和文档 2 均未提及该限制。开发者在调用工作流应用时必须遵守此约束，否则将返回模型不可用错误。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | ✓ | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取 |
| `prompt` | string | ✓（若未提供 `messages`） | 当前轮次用户输入文本；若启用 `messages` 模式则可省略 |
| `biz_params` | object | ✗ | 用于插件参数透传，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": <value> } } }`；仅对已关联插件的应用生效 |
| `input.messages` | array | ✓（若启用 `messages` 模式） | 替代 `prompt` 的完整对话历史数组，格式同 OpenAI `messages`，需在应用内配置 `historyList` 变量并发布 |
| `session_id` | string | ✗ | 启用云端会话管理时提供，有效期 1 小时，最多 50 轮；若与 `messages` 同时存在，以 `messages` 为准 |

## 使用方式

### 1. 前置准备
- 获取 API Key（[密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key)）并**推荐配置为环境变量 `DASHSCOPE_API_KEY`**（避免硬编码）；
- 获取目标应用的 `APP_ID`（[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)）；
- 若使用 SDK，按语言安装对应版本（Python ≥ 1.14.0，Java ≥ 2.12.0）。

### 2. 调用示例（统一接口）
所有语言均调用同一 HTTP 端点：`POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`

- **SDK 方式（推荐）**：  
  Python 示例（[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)）：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？"
  )
  ```

- **HTTP 方式（通用）**：  
  curl 示例（[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{"input": {"prompt": "你是谁？"}}'
  ```

### 3. 插件参数透传（进阶）
仅当应用已关联自定义插件时有效，需通过 `biz_params.user_defined_params` 传递：
```json
{
  "input": {
    "prompt": "查询寝室公约",
    "biz_params": {
      "user_defined_params": {
        "plugin_abc123": { "article_index": 2 }
      }
    }
  }
}
```
插件 ID（`plugin_abc123`）需从控制台插件卡片获取。

## 限制和注意事项

- **地域限制**：工作流应用调用**仅支持华北2（北京）地域**（见文档 3 “重要”提示），智能体应用无此限制。
- **会话管理**：
  - `session_id` 有效期为 1 小时，最大轮次 50；
  - 若同时传入 `session_id` 和 `messages`，系统**优先使用 `messages`**（文档 3 明确说明）。
- **安全实践**：
  - **禁止硬编码 API Key**：所有示例均强调“不建议在生产环境中直接将 API Key 硬编码到代码中”，必须通过环境变量或密钥管理服务注入；
  - 插件鉴权需在插件配置中开启（如 Header Basic Auth），SDK/HTTP 调用层无需额外处理。
- **错误处理**：响应含 `request_id`、`code`、`message` 字段，需结合 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code) 定位问题。
- **SDK 版本兼容性**：插件参数透传要求 Python SDK ≥ 1.14.0（文档 2），而多轮对话推荐 Java SDK ≥ 2.12.0（文档 1 & 3），开发者需按功能需求选择最低版本。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)


