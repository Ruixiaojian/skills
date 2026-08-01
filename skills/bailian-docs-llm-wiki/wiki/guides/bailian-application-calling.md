# bailian [application call](../api/application-call.md)ing

百炼平台支持通过统一的 Application API 调用智能体应用（Single Agent Application）和工作流应用（Workflow Application），开发者可使用 DashScope SDK 或原生 HTTP 接口完成集成。所有调用均基于 `POST /api/v1/apps/{app_id}/completion` 端点，核心差异在于应用类型、参数结构及能力边界。本文档聚焦于通用调用规范与关键实践要点。

## 支持的模型/功能

- **应用类型**：当前仅支持两类应用调用：
  - **智能体应用**：面向单任务、轻量级交互场景，适用于问答、摘要、简单工具调用等 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - **工作流应用**：面向复杂编排场景，支持多节点（大模型、插件、条件分支、循环等）协同执行，已替代旧版“智能体编排应用” [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **核心能力**：
  - 单轮/多轮对话（通过 `session_id` 或显式 `messages` 实现）；
  - 自定义插件参数透传（仅限工作流应用中的插件节点，或智能体应用关联的插件）；
  - 调试信息返回（启用 `debug` 字段）；
  - 模型用量统计（`usage.models` 中包含 `input_tokens`/`output_tokens` 及 `model_id`）。

> **注意**：文档 3 明确指出“本文档仅适用于华北2（北京）地域”，而文档 1 和 2 均未声明地域限制；实际生产环境应以控制台所选地域为准，跨地域调用将失败。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在控制台「应用管理」中获取。 |
| `prompt` | string | 否（若提供 `messages` 则不可填） | 当前轮次用户输入文本；若使用 `messages` 数组则必须省略。 |
| `input.prompt` | string | 同上 | HTTP 请求体中 `input` 对象下的 `prompt` 字段，语义同 SDK 的 `prompt` 参数。 |
| `input.biz_params` | object | 否 | 业务自定义参数容器，用于传递插件参数、上下文变量等。其中 `user_defined_params` 是插件参数透传的必用子字段 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。 |
| `session_id` | string | 否 | 启用云端会话管理时提供，有效期 1 小时，最多 50 轮。 |
| `messages` | array | 否（若提供则 `prompt` 必须省略） | 客户端维护的完整对话历史，格式为 `[{ "role": "user/system/assistant", "content": "..." }]`，优先级高于 `session_id`。 |
| `parameters` | object | 否 | 模型级参数（如 `temperature`, `top_p`），对工作流/智能体应用生效，但部分节点可能忽略。 |
| `debug` | object | 否 | 启用后返回详细执行链路（如节点耗时、中间结果），用于调试。 |

## 使用方式

### 1. 前置准备
- 获取并配置 API Key：推荐通过环境变量 `DASHSCOPE_API_KEY` 设置，避免硬编码；
- 安装 SDK（可选）：Python、Java、Node.js 等主流语言均有官方 SDK，HTTP 方式无需安装；
- 确认应用状态：应用需已「发布」，且与 API Key 所属账号位于同一业务空间。

### 2. 调用示例（SDK 与 HTTP 统一）
- **基础调用（无插件）**：  
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？"
  )
  ```
- **插件参数透传（工作流/智能体应用）**：  
  在 `biz_params.user_defined_params` 中按 `{plugin_code}: {param_key: value}` 结构传入，`plugin_code` 为插件 ID，`param_key` 为插件配置的输入参数名（如 `article_index`）[应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

- **多轮对话（推荐 `messages` 方式）**：  
  ```python
  messages = [
      {"role": "user", "content": "你好"},
      {"role": "assistant", "content": "我是通义千问。"},
      {"role": "user", "content": "今天天气如何？"}
  ]
  response = Application.call(
      api_key=..., app_id=..., messages=messages
  )
  ```

### 3. 错误处理
- 检查 `response.status_code`（SDK）或 HTTP 状态码（HTTP）；
- 解析 `response.message` 或响应体中的 `message` 字段；
- 记录 `request_id` 用于服务端问题排查；
- 参考统一错误码文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code。

## 限制和注意事项

- **地域限制**：工作流应用调用仅支持华北2（北京）地域，智能体应用无明确地域限制，但建议与应用创建地域一致；
- **插件参数约束**：  
  - 插件工具的输入参数**传参方式必须设为“业务透传”**，否则 `biz_params.user_defined_params` 无法生效；  
  - 插件与应用必须处于**同一业务空间**，否则关联失败；
- **安全要求**：API Key **严禁硬编码**，生产环境必须通过环境变量或密钥管理服务注入；
- **SDK 版本兼容性**：  
  - Python SDK 建议 ≥ 1.14.0（插件参数支持）；  
  - Java SDK 建议 ≥ 2.12.0（稳定性增强）；  
  > **注意**：文档 1 的 Python 示例注明 “建议 dashscope SDK 的版本 >= 1.14.0”，而文档 2 和 3 的 Java 示例均要求 “>= 2.12.0”，两者版本号不一致属正常（因语言 SDK 独立演进），但需按语言分别满足最低版本。
- **会话管理**：`session_id` 由服务端生成并返回，客户端需自行保存并在后续请求中复用；若同时传 `session_id` 和 `messages`，系统**优先使用 `messages`**。

## 来源文档

- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)


