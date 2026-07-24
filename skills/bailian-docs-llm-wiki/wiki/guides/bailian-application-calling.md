# bailian [application call](../api/application-call.md)ing

百炼应用调用（bailian [application call](../api/application-call.md)ing）是指通过 DashScope SDK 或标准 HTTP API，将阿里云百炼平台创建的智能体应用或工作流应用集成至外部业务系统的能力。该机制统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义插件参数透传及调试能力，是生产环境集成的核心方式。所有调用均需有效 API Key 与合法 APP_ID。

## 支持的模型/功能

- **应用类型**：同时支持[智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)与[工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)，二者调用接口、参数结构和 SDK 方法完全一致。
- **核心能力**：
  - 单轮文本生成（`prompt` 输入）
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理上下文）
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 传递插件入参）
  - 调试信息返回（启用 `debug` 字段可获取中间节点执行详情）
- **模型绑定**：底层所用大模型由应用在控制台配置决定，调用方无需指定模型 ID；响应中 `usage.models[].model_id` 字段可回溯实际调用的模型（如 `qwen-max`、`qwen-plus`）。

> **注意**：文档 2 明确声明“本文档仅适用于华北2（北京）地域”，而文档 1 和文档 3 均未提及地域限制。实际调用时若在非北京地域遇到 `404 Not Found` 或 `403 Forbidden`，请确认应用部署地域并选用对应 endpoint —— 此为关键兼容性风险点。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | ✅ | 百炼控制台应用卡片上复制的唯一 ID，区分智能体与工作流应用 |
| `prompt` | string | ⚠️（见下文） | 单轮请求必填；若使用 `messages` 进行多轮对话，则此项**不可出现** |
| `messages` | array | ⚠️（见下文） | 多轮对话推荐方式，格式同 OpenAI：`[{ "role": "user/system/assistant", "content": "..." }]`；与 `prompt` 互斥 |
| `session_id` | string | ❌ | 云端托管对话历史的会话标识，有效期 1 小时，最多 50 轮；若同时传 `messages`，则 `messages` 优先 |
| `biz_params` | object | ❌ | 用于透传自定义插件参数，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": <value> } } }`，详见[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |
| `debug` | object | ❌ | 空对象 `{}` 即可启用，返回 `debug_info` 字段含节点执行路径、插件调用日志等 |

## 使用方式

### 1. 准备工作
- 获取 API Key：前往 [密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建并记录；
- 获取 APP_ID：在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面复制目标应用 ID；
- （推荐）配置环境变量：`export DASHSCOPE_API_KEY=sk-xxx`，避免代码硬编码。

### 2. SDK 调用（Python 示例）
```python
from dashscope import Application
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 自动读取环境变量亦可省略
    app_id="YOUR_APP_ID",
    prompt="你好，请介绍自己",
    biz_params={"user_defined_params": {"plugin_abc123": {"query": "天气"}}}
)
if response.status_code == 200:
    print(response.output.text)
```

### 3. HTTP 调用（curl 示例）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "input": {
          "prompt": "你好，请介绍自己",
          "biz_params": {
            "user_defined_params": {
              "plugin_abc123": {"query": "天气"}
            }
          }
        },
        "debug": {}
      }'
```

> 所有语言 SDK（Java/Node.js/PHP/C#/Go）及 HTTP 示例均已在[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)和[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)中完整提供，结构一致，仅需替换 `app_id` 和业务参数。

## 限制和注意事项

- **地域限制**：工作流应用调用明确限定于华北2（北京）地域（见[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)），智能体应用虽未声明，但建议统一部署在北京以确保兼容性。
- **会话管理**：`session_id` 有效期为 1 小时且最多承载 50 轮对话；生产环境强烈推荐自行维护 `messages` 数组，避免会话过期或超限导致上下文丢失。
- **插件参数安全**：`biz_params.user_defined_params` 中的插件 ID（`plugin_code`）必须与控制台中插件卡片显示的 ID 完全一致，大小写敏感；参数键名须与插件工具配置的输入参数名称严格匹配。
- **错误处理**：所有调用均返回 `request_id`，务必在日志中记录，便于问题排查；常见错误码参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。
- **SDK 版本要求**：Java SDK 需 ≥ 2.12.0（见两篇调用文档），Python SDK 需 ≥ 1.14.0（见[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）；低版本可能缺失 `biz_params` 或 `debug` 支持。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


