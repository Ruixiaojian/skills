# bailian [application call](../api/application-call.md)ing

百炼应用调用是指通过 DashScope SDK 或 HTTP API，将百炼平台创建的智能体应用（Agent 1.0）或工作流应用集成至业务系统的过程。调用方式统一、接口一致，支持单轮/多轮对话及插件参数透传，适用于各类 AI 应用场景。所有调用均需有效 API Key 和应用 ID，并遵循地域与模型限制。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - 智能体应用（Agent 1.0），详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - 工作流应用（Workflow Application），替代了已下线的“智能体编排应用”，详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **核心能力**：
  - 单轮文本生成（`prompt` 输入 → `output.text` 输出）；
  - 多轮对话支持两种模式：
    - 云端会话管理（通过 `session_id` 自动加载历史，有效期 1 小时，最多 50 轮）；
    - 客户端自主管理（通过 `messages` 数组显式传递完整对话历史，**优先级高于 `session_id`**）；
  - 自定义插件参数透传（仅限已关联插件的应用），通过 `biz_params.user_defined_params.{plugin_code}` 传递业务参数，详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

> **注意**：工作流应用明确不支持文生图类大模型；而文档 1 和文档 2 中均未声明此限制，但文档 2 的“重要”说明中已明确限定适用地域为华北2（北京），该限制在文档 1 中缺失，属信息不一致。实际调用前请确认应用所在地域与 API Endpoint 匹配。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼控制台应用卡片上获取的 APP_ID，区分智能体应用与工作流应用 |
| `prompt` | string | 否（若提供 `messages` 则可省略） | 当前轮次用户输入文本；若使用 `messages` 模式则不应同时提供 |
| `messages` | array | 否（若提供则 `prompt` 不生效） | 完整对话历史数组，格式同 OpenAI：`[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]` |
| `session_id` | string | 否 | 用于启用云端会话管理；若同时传 `messages`，系统将忽略 `session_id` |
| `biz_params` | object | 否 | 仅用于插件参数透传，结构为 `{"user_defined_params": {"{plugin_code}": {...}}}` |
| `parameters` | object | 否 | 预留扩展字段，当前暂无公开可用参数 |
| `debug` | object | 否 | 预留调试字段，当前暂无公开用途 |

## 使用方式

### 前置准备
1. 获取并配置凭证：
   - API Key：通过 [密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建；
   - APP_ID：在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面复制对应应用 ID；
   - **强烈建议**将 `DASHSCOPE_API_KEY` 配置为环境变量，避免硬编码。
2. 安装 SDK（如使用 SDK 方式）：
   - Python：`pip install -U dashscope`；
   - Java：添加 `com.alibaba:dashscope-sdk-java` 依赖（推荐 ≥2.12.0）；
   - 其他语言参考各文档示例中的依赖安装说明。

### 调用示例（统一接口）
- **SDK 调用（Python）**：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？"
  )
  print(response.output.text)
  ```
- **HTTP 调用（curl）**：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "input": {"prompt": "你是谁？"},
          "parameters": {},
          "debug": {}
        }'
  ```

### 插件参数透传（补充）
需在 `input.biz_params.user_defined_params` 中按插件 ID 嵌套传参，例如：
```json
{
  "input": {
    "prompt": "查询寝室公约",
    "biz_params": {
      "user_defined_params": {
        "plugin_abc123": {"article_index": 2}
      }
    }
  }
}
```
该能力同时适用于智能体应用和工作流应用，具体配置流程见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

## 限制和注意事项

- **地域限制**：工作流应用**仅支持华北2（北京）地域**，调用时必须使用对应地域的 Endpoint（`https://dashscope.aliyuncs.com`），其他地域调用将失败；智能体应用虽未明文限制，但应确保应用部署地域与 API 请求地域一致。
- **会话限制**：`session_id` 有效期为 1 小时，单个会话最多支持 50 轮对话；超出后需新建 `session_id` 或切换为 `messages` 模式。
- **安全要求**：
  - 禁止在代码中硬编码 API Key，务必通过环境变量或密钥管理服务注入；
  - 插件鉴权配置（如 Basic Auth）需在插件创建时正确设置，否则透传参数将无法触发插件调用。
- **版本兼容性**：
  - Java SDK 推荐 ≥2.12.0（文档 1 和 2 均明确要求）；
  - Python SDK 推荐 ≥1.14.0（文档 3 明确要求，用于 `biz_params` 支持）。
- **错误处理**：所有调用均返回标准 HTTP 状态码与 `request_id`，错误详情请查阅 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


