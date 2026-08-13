# bailian [application call](../api/application-call.md)ing

百炼应用调用是指通过 DashScope SDK 或 HTTP API，将百炼平台创建的智能体应用（Agent 1.0）或工作流应用集成至业务系统的过程。所有调用均统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮与多轮对话，并可透传自定义参数以驱动插件或工作流节点。该机制是构建 AI 原生应用的核心交互方式。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - **智能体应用（Agent 1.0）**：基于大模型自主规划与工具调用的轻量级智能体，适用于简单任务编排 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - **工作流应用**：可视化编排的多节点流程（含大模型节点、插件节点、条件分支等），替代已下线的“智能体编排应用” [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **核心能力**：
  - 单轮 [prompt](prompt.md) 响应；
  - 多轮对话（支持 `session_id` 自动管理或显式传入 `messages` 数组）；
  - 插件参数透传（仅限关联了自定义插件的智能体应用，或工作流中配置了插件节点的应用）；
  - 不支持文生图类大模型节点（工作流应用明确限制）[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。

> **注意**：文档 1 中提及“智能体编排应用已被工作流应用替代”，而文档 2 和 3 均未再提及其存在；当前控制台已无该类型应用入口，此说明准确，无需修正。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在百炼控制台「应用管理」页面获取。 |
| `prompt` | string | 是（若未传 `messages`） | 当前轮次用户输入文本；若启用 `messages` 模式则非必填。 |
| `biz_params` | object | 否 | 业务扩展参数对象，用于传递插件参数等。其中 `user_defined_params` 字段为插件透传必需结构（格式见下文）。 |
| `parameters` | object | 否 | 模型推理参数（如 `temperature`, `max_tokens`），按应用内节点配置生效。 |
| `debug` | object | 否 | 调试开关，设为空对象 `{}` 可启用调试日志。 |

- **插件参数透传格式（`biz_params.user_defined_params`）**：
  ```json
  {
    "user_defined_params": {
      "<plugin_code>": {
        "<param_name>": <value>
      }
    }
  }
  ```
  其中 `<plugin_code>` 为插件 ID（非名称），`<param_name>` 必须与插件工具配置中“输入参数”的 `name` 完全一致，且该参数的“传参方式”必须设为 **业务透传** [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

## 使用方式

### 1. 前置准备
- 获取并配置 API Key（推荐设为环境变量 `DASHSCOPE_API_KEY`）；
- 确保应用已发布（未发布的应用无法被 API 调用）；
- 若使用 SDK，安装对应语言版本（Python ≥ 1.14.0，Java ≥ 2.12.0）。

### 2. 调用示例（通用结构）
所有语言 SDK 和 HTTP 请求均遵循相同数据结构：

- **SDK（Python）**
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你好",
      biz_params={"user_defined_params": {"plugin_abc123": {"query": "天气"}}}
  )
  ```

- **HTTP（curl）**
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
      "input": {
        "prompt": "你好",
        "biz_params": {
          "user_defined_params": {
            "plugin_abc123": {"query": "天气"}
          }
        }
      },
      "parameters": {},
      "debug": {}
    }'
  ```

> **注意**：文档 2 和文档 3 的 Python/Java/HTTP 示例代码完全一致，但文档 1 的 SDK 示例中 `Application.call()` 的 `biz_params` 位置在顶层（与文档 2/3 一致），而其 HTTP 示例中 `biz_params` 被嵌套在 `input` 内——这符合实际接口规范（`biz_params` 属于 `input` 对象），文档 2/3 的 HTTP 示例遗漏了该嵌套，属**过时信息**。正确结构请以 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) 中的 HTTP 示例为准。

### 3. 多轮对话
- **推荐方式：显式维护 `messages`**
  ```python
  messages = [
      {"role": "user", "content": "你好"},
      {"role": "assistant", "content": "我是千问。"},
      {"role": "user", "content": "今天天气如何？"}
  ]
  response = Application.call(
      ...,
      input={"messages": messages}  # 注意：SDK 中需传入 input 字典，非顶层 messages
  )
  ```
- **简化方式：使用 `session_id`**（有效期 1 小时，最多 50 轮）

## 限制和注意事项

- **地域限制**：工作流应用调用**仅支持华北2（北京）地域**，智能体应用无此限制 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **插件依赖约束**：
  - 自定义插件必须与调用的应用处于**同一业务空间**；
  - 插件工具的输入参数“传参方式”**必须选择“业务透传”**，否则 `user_defined_params` 无效 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。
- **安全实践**：
  - **禁止硬编码 API Key**：所有示例均强调“不建议在生产环境中直接将 API Key 硬编码到代码中”，应始终通过环境变量或密钥管理服务注入。
- **错误处理**：
  - 所有调用均需检查 `status_code`（HTTP）或 `response.status_code`（SDK），非 `200`/`HTTPStatus.OK` 时解析 `message` 和 `request_id` 进行排查；
  - 错误码参考统一文档：[开发者参考-错误码](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)。

## 来源文档

- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)


