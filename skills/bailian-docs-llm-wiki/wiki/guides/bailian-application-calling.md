# bailian [application call](../api/application-call.md)ing

百炼平台支持通过统一 API（DashScope SDK 或 HTTP 接口）调用两类核心应用：**智能体应用（Agent 1.0）** 和 **工作流应用**（原“智能体编排应用”已由其替代）。调用方式简洁一致，适用于快速集成至业务系统，开发者只需提供 `app_id`、`prompt` 及可选的业务参数即可发起推理请求。所有调用均需有效 API Key，并推荐通过环境变量安全配置。

## 支持的模型/功能

- **应用类型**：仅支持调用已发布的**智能体应用**和**工作流应用**，二者 API 调用接口完全兼容（同一 `/completion` 端点），但底层执行逻辑与能力边界不同：
  - 智能体应用面向单任务对话场景，依赖大模型自主规划与工具调用；
  - 工作流应用支持可视化节点编排（如大模型节点、插件节点、条件分支等），适合复杂逻辑控制。
- **插件能力**：仅工作流应用及智能体应用（通过关联插件）支持自定义插件调用；插件参数需通过 `biz_params.user_defined_params` 透传，且插件必须与应用处于同一业务空间 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。
- **多轮对话**：两类应用均支持，可通过 `session_id`（云端自动维护历史）或显式传入 `messages` 数组（推荐）实现上下文管理。`session_id` 有效期 1 小时，最多 50 轮；若同时传入 `session_id` 和 `messages`，系统优先使用 `messages` [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | ✓ | 应用唯一标识，在百炼控制台「应用管理」页面获取。 |
| `prompt` | string | ✓（若未传 `messages`） | 当前轮次的用户输入指令。若启用 `messages` 模式，则此字段忽略。 |
| `messages` | array | ✗（推荐用于多轮） | 按时间序排列的对话历史数组，格式为 `[{"role": "user/system/assistant", "content": "..."}, ...]`。启用后 `prompt` 不生效。 |
| `biz_params` | object | ✗ | 业务扩展参数对象，核心子字段：<br>• `user_defined_params`: 用于向关联插件透传参数，结构为 `{"plugin_code": {"param_key": value}}`；<br>• 其他字段暂无公开语义，不建议自行添加。 |
| `debug` | object | ✗ | 调试开关，设为 `{}` 可返回更详细的 trace 信息（如节点执行路径），仅限调试环境使用。 |

> **注意**：文档 2 和文档 3 均给出 `prompt` 为必填项的示例，但实际在 `messages` 模式下 `prompt` 是被忽略的；文档 3 的「多轮对话」章节已明确该行为，而文档 2 未提及 `messages`，存在表述不完整风险。请以 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 中的 `messages` 说明为准。

## 使用方式

### 前置准备
1. 获取并配置 API Key：[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 并[配置到环境变量 `DASHSCOPE_API_KEY`](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)（强烈推荐，避免硬编码）；
2. 安装 SDK（可选）：若使用 SDK，需安装对应语言版本（Python ≥1.14.0，Java ≥2.12.0）[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
3. 确认地域：工作流应用调用**仅支持华北2（北京）地域**，智能体应用无此限制 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。

### 调用示例（通用）
- **SDK（Python）**
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你好，请总结这篇文档",
      biz_params={"user_defined_params": {"plugin_abc": {"file_id": "123"}}}
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
            "biz_params": {"user_defined_params": {"plugin_abc": {"file_id": "123"}}}
        },
        "parameters": {},
        "debug": {}
    }'
  ```

## 限制和注意事项

- **插件参数约束**：自定义插件的输入参数**必须配置为“业务透传”** 方式，否则无法通过 `user_defined_params` 传递 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)；
- **插件鉴权**：若插件开启鉴权，需确保插件配置的鉴权方式（如 Basic Auth Header）与后端服务实际要求一致，SDK 和 HTTP 调用本身不处理鉴权逻辑；
- **地域隔离**：工作流应用调用强制限定于华北2（北京）地域，跨地域调用将失败，智能体应用无此限制；
- **错误处理**：所有调用均返回标准 HTTP 状态码与 `request_id`，错误详情请查阅 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)；
- **安全实践**：严禁在代码中硬编码 `DASHSCOPE_API_KEY`，生产环境务必使用环境变量或密钥管理服务。

## 来源文档

- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)


