# bailian [application call](../api/application-call.md)ing

阿里云百炼平台支持通过统一 API（DashScope SDK 或 HTTP 接口）调用两类核心应用：**智能体应用（Agent 1.0）** 和 **工作流应用**。二者均基于 `POST /api/v1/apps/{app_id}/completion` 统一端点，共享基础调用协议与鉴权机制，适用于快速集成业务系统。开发者需预先获取 API Key 与应用 ID，并推荐通过环境变量安全配置密钥。

## 支持的模型/功能

- **智能体应用**：面向单任务场景的轻量级 Agent，支持[插件](../concepts/plugin.md)调用、自定义工具集成及简单逻辑编排。详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)。
- **工作流应用**：面向复杂多步骤任务的可视化编排应用，支持节点化流程控制（如条件分支、循环、大模型节点、[插件](../concepts/plugin.md)节点等），但**不支持文生图类大模型**（如 qwen-vl、wanx-image）[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **共性能力**：
  - 多轮对话（通过 `session_id` 或显式 `messages` 数组）
  - 自定义参数透传（`biz_params.user_defined_params` 用于[插件](../concepts/plugin.md)参数传递）[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
  - 调试信息输出（`debug` 字段）

> **注意**：文档 3 明确声明“百炼工作流不支持使用文生图大模型”，而文档 1 和文档 2 均未提及此限制；该限制为工作流应用特有，智能体应用是否支持需以控制台实际可用模型为准，此处以文档 3 的明确声明为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | ✓ | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取 |
| `prompt` | string | ✓（若未提供 `messages`） | 当前轮次用户输入文本；若使用 `messages` 模式则可省略 |
| `messages` | array | ✗（推荐用于多轮） | 完整对话历史数组，格式同 OpenAI `messages`，含 `role`（`user`/`assistant`）和 `content`；**优先级高于 `session_id`** |
| `session_id` | string | ✗（可选） | 用于启用云端自动维护的对话上下文；有效期 1 小时，最多 50 轮 |
| `biz_params` | object | ✗ | 扩展参数对象，当前主要用途为插件参数透传：<br>`{"user_defined_params": {"{plugin_code}": {"param_key": "value"}}}` |
| `parameters` | object | ✗ | 预留字段，当前暂无通用参数，部分节点可能支持内部扩展 |
| `debug` | object | ✗ | 启用调试模式（如 `{"enable": true}`），返回更详细的执行链路信息 |

## 使用方式

### 1. 准备工作
- 获取 [API Key](https://bailian.console.aliyun.com/?tab=model#/api-key) 并配置为环境变量 `DASHSCOPE_API_KEY`
- 在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)中获取目标应用的 `APP_ID`

### 2. 调用方式（三选一）
- **DashScope SDK（推荐）**：支持 Python、Java、Node.js 等主流语言，自动处理鉴权与序列化。Python 示例：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？"
  )
  ```
- **HTTP API（通用）**：所有语言均可调用，Endpoint 为 `POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`，需手动设置 `Authorization: Bearer ${API_KEY}` 头。
- **不依赖 SDK 的 HTTP（如 cURL/PHP/Go）**：直接构造 JSON 请求体，结构与 SDK 内部一致（见各文档示例）。

### 3. 插件参数传递（仅限已关联插件的应用）
通过 `biz_params.user_defined_params` 透传插件所需参数，`{plugin_code}` 替换为插件卡片上显示的实际插件 ID：
```python
biz_params = {
    "user_defined_params": {
        "abc123xyz": {"article_index": 2}  # abc123xyz 是插件 ID
    }
}
Application.call(..., biz_params=biz_params)
```

## 限制和注意事项

- **地域限制**：工作流应用调用**仅支持华北2（北京）地域**，智能体应用无此限制（文档 3 明确声明，文档 1/2 未提，应视为工作流专属约束）。
- **多轮对话限制**：
  - `session_id` 模式：单个 `session_id` 最多 50 轮，超时（1 小时）后历史自动清除；
  - `messages` 模式：由客户端完全控制上下文长度，但需注意总 token 数不能超过所用模型的上下文窗口。
- **安全实践**：
  - **禁止硬编码 API Key**：所有示例均强调“不建议在生产环境中直接将 API Key 硬编码到代码中”，必须使用环境变量或密钥管理服务。
  - 插件鉴权：若插件开启鉴权，需在插件配置中正确设置 Header/BASIC 等方式，SDK 与 HTTP 调用均不代为处理插件层鉴权。
- **错误处理**：所有调用均需检查 `status_code`（HTTP）或 `response.status_code`（SDK），失败时解析 `request_id` 与 `message` 并参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)


