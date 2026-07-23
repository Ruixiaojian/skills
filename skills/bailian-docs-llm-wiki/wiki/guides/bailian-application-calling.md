# bailian [application call](../api/application-call.md)ing

百炼应用调用（bailian [application call](../api/application-call.md)ing）是指通过 DashScope SDK 或标准 HTTP API，将阿里云百炼平台创建的智能体应用或工作流应用集成至第三方业务系统的能力。该机制统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义插件参数透传等核心能力，适用于从简单问答到复杂编排的各类 AI 应用场景。所有调用均需有效的 API Key 和已发布的应用 ID。

## 支持的模型/功能

- **应用类型**：同时支持**智能体应用**（单 Agent 应用）和**工作流应用**（原“智能体编排应用”，已在[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)中明确说明“智能体编排应用已被工作流应用替代”）。  
- **核心功能**：
  - 单轮文本生成（`prompt` 输入）
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 字段，详见[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）
  - 调试信息返回（`debug` 字段可选启用）

> **注意**：文档 2（调用工作流应用）声明“本文档仅适用于华北2（北京）地域”，而文档 1（调用智能体应用）及文档 3 均未限定地域。实际生产环境应以控制台所选应用部署地域为准，建议在调用前确认应用所在 Region 并匹配对应 endpoint —— 当前所有示例均使用 `https://dashscope.aliyuncs.com`，该域名默认路由至用户应用所在地域，无需手动切换。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼控制台应用卡片上复制的唯一 ID，见[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)前提条件 |
| `prompt` | string | 否（若提供 `messages` 则不可用） | 单轮指令文本；若启用多轮且使用 `messages`，则此字段必须省略 |
| `messages` | array | 否（若提供则替代 `prompt`） | 显式对话历史数组，格式为 `[{"role": "user/system/assistant", "content": "..."}]`；优先级高于 `session_id` |
| `session_id` | string | 否（用于云端会话） | 由服务端生成并返回的会话标识符，有效期 1 小时，最多支持 50 轮；与 `messages` 同时存在时，以 `messages` 为准 |
| `biz_params` | object | 否 | 用于透传自定义插件参数，结构为 `{"user_defined_params": {"{plugin_code}": {...}}}`，详见[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |
| `parameters` | object | 否 | 模型级超参（如 `temperature`, `top_p`），当前对应用调用影响有限，建议保持空对象 `{}` |
| `debug` | object | 否 | 开启调试模式（如 `{"enable": true}`），返回详细执行链路信息 |

## 使用方式

### 1. 准备工作
- 获取 [API Key](https://bailian.console.aliyun.com/?tab=model#/api-key) 并配置为环境变量 `DASHSCOPE_API_KEY`（推荐，避免硬编码）；
- 在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取目标应用的 `APP_ID`；
- 若使用 SDK，按语言安装对应版本（Python ≥1.14.0，Java ≥2.12.0，见[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)）。

### 2. 调用示例（SDK 与 HTTP 统一接口）
- **SDK 调用（Python）**：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？",
      biz_params={"user_defined_params": {"plugin_abc": {"param1": "value1"}}}
  )
  print(response.output.text)
  ```

- **HTTP 调用（curl）**：
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "input": {
            "prompt": "你是谁？",
            "biz_params": {"user_defined_params": {"plugin_abc": {"param1": "value1"}}}
          }
        }'
  ```

> 所有语言（Java/PHP/Node.js/C#/Go）的完整示例请参考[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)和[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)中的代码片段。

## 限制和注意事项

- **地域限制**：工作流应用调用受地域约束，当前仅支持华北2（北京），智能体应用无明确限制，但建议与应用部署地域一致；
- **会话管理**：`session_id` 有效期为 1 小时，最大轮次 50；生产环境推荐自行维护 `messages` 数组以获得确定性行为；
- **插件参数安全**：`biz_params.user_defined_params` 中的插件 ID 必须与应用内已关联的插件完全匹配，否则参数被忽略；
- **错误处理**：所有调用均返回 `request_id`，务必记录该字段用于问题排查；错误码含义请查阅[开发者参考错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)；
- **SDK 版本兼容性**：Python SDK 要求 ≥1.14.0（插件参数支持）、Java SDK 要求 ≥2.12.0（多轮对话稳定性），旧版本可能缺失关键功能。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


