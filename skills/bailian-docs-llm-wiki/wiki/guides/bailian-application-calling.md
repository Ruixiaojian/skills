# bailian [application call](../api/application-call.md)ing

百炼应用调用（bailian [application call](../api/application-call.md)ing）是指通过 DashScope SDK 或标准 HTTP API，将百炼平台创建的**工作流应用**或**智能体应用**集成到自有业务系统中的核心能力。该机制支持单轮/多轮对话、自定义插件参数透传、上下文管理等关键场景，适用于构建 AI 原生应用和服务编排。所有调用均需在华北2（北京）地域执行。

## 支持的模型/功能

- **应用类型**：当前仅支持调用**工作流应用**（Workflow Application）和**智能体应用**（Single Agent Application），其中智能体编排应用已由工作流应用替代 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。
- **模型绑定**：底层模型由应用发布时所选模型决定（如 `qwen-max`、`qwen-plus`），调用方无需显式指定模型 ID；响应中 `usage.models[].model_id` 字段可回溯实际使用的模型。
- **核心能力**：
  - 单轮文本生成（`prompt` 输入）
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组管理历史）
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 传递插件输入参数）[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
  - 调试信息返回（启用 `debug` 字段可获取推理链路详情）

> **注意**：文档 1 明确声明“本文档仅适用于华北2（北京）地域”，而文档 3 未提及地域限制。实际生产环境必须遵循文档 1 的地域约束，否则请求将失败 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | ✅ | 应用唯一标识，从百炼控制台「应用管理」页面获取 |
| `prompt` | string | ⚠️ | 单轮调用必需；若使用 `messages` 进行多轮对话，则此项**不可提供** |
| `messages` | array | ⚠️ | 多轮对话推荐方式，格式为 `[{ "role": "user/system/assistant", "content": "..." }]`；与 `session_id` 同时存在时优先使用 `messages` |
| `session_id` | string | ❌ | 云端托管对话历史的会话标识，有效期 1 小时，最多支持 50 轮 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) |
| `biz_params` | object | ❌ | 用于传递自定义插件参数，结构为 `{ "user_defined_params": { "<plugin_code>": { "<param_key>": <value> } } }` |
| `parameters` | object | ❌ | 预留扩展字段，当前暂无公开可用参数 |
| `debug` | object | ❌ | 设为空对象 `{}` 即可启用调试模式，返回详细推理过程 |

## 使用方式

### SDK 调用（推荐）
- **Python**：使用 `dashscope.Application.call()`，支持 `api_key`（环境变量优先）、`app_id`、`prompt`/`messages` 等参数  
- **Java**：使用 `ApplicationParam.builder()` 构建参数，要求 SDK 版本 ≥ 2.12.0（文档 1 和文档 3 均明确要求）  
- 其他语言 SDK（Node.js/Go/C#）均需配置 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 请求头  

### HTTP 直接调用
- **Endpoint**：`POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`  
- **Headers**：`Authorization: Bearer ${DASHSCOPE_API_KEY}` + `Content-Type: application/json`  
- **Body 结构**：
  ```json
  {
    "input": {
      "prompt": "...",
      "biz_params": { ... }
    },
    "parameters": {},
    "debug": {}
  }
  ```

## 限制和注意事项

- **地域强制约束**：所有调用必须发生在 **华北2（北京）** 地域，其他地域请求将被拒绝 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。  
- **API Key 安全**：严禁硬编码 `sk-xxx` 到源码；务必通过环境变量 `DASHSCOPE_API_KEY` 注入，并确保运行时环境隔离。  
- **多轮对话选择**：  
  - `session_id` 方式简单但灵活性低，依赖服务端存储且有 1 小时/50 轮限制；  
  - `messages` 方式需客户端自行维护完整对话历史，推荐用于对上下文精度要求高的场景。  
- **插件参数透传**：`biz_params.user_defined_params` 中的 `plugin_code` 必须与百炼控制台中插件卡片显示的 ID 完全一致，大小写敏感；参数键名需与插件定义中“传参方式=业务透传”的输入参数名称严格匹配。  
- **错误处理**：所有响应均含 `request_id`，应记录该字段用于问题排查；错误码参考 [开发者错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

## 来源文档

- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)


