# bailian [application call](../api/application-call.md)ing

百炼平台支持通过统一 API 接口调用智能体应用（Single Agent Application）和工作流应用（Workflow Application），开发者可使用 DashScope SDK 或原生 HTTP 请求完成集成。调用过程需提供 API Key 和应用 ID，并支持基础 [prompt](prompt.md) 输入、自定义参数透传及多轮对话管理。

## 支持的模型/功能

- **应用类型**：当前支持两类应用调用：
  - 智能体应用（[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)）：面向单一角色或任务的轻量级智能体，适用于问答、工具调用等场景；
  - 工作流应用（[调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）：基于节点编排的复杂逻辑应用（原“智能体编排应用”已下线并由工作流应用替代），支持条件分支、循环、多模型协同等能力。
- **核心能力**：
  - 基础文本生成（`prompt` 输入 → `output.text` 输出）；
  - 自定义[插件](../concepts/plugin.md)参数透传（仅限智能体应用与工作流应用中的[插件](../concepts/plugin.md)节点），通过 `biz_params.user_defined_params` 传递业务参数；
  - 多轮对话支持：可通过 `session_id`（云端自动维护，有效期 1 小时，最多 50 轮）或显式 `messages` 数组（推荐）管理上下文；
  - Debug 信息与 token 统计（`usage.models` 中含 `model_id`、`input_tokens`、`output_tokens`）。

> **注意**：文档 1 明确指出“智能体编排应用已被工作流应用替代”，而文档 2 和 3 均未提及该废弃状态，存在表述不一致。请以 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) 中的说明为准，新项目应使用工作流应用而非已下线的编排应用。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | ✓ | 应用唯一标识，在控制台「应用管理」页面获取。 |
| `prompt` | string | ✓（若未提供 `messages`） | 当前轮次的用户指令，用于单轮调用或作为 `messages` 的补充。 |
| `messages` | array | ✗（但推荐用于多轮） | 替代 `prompt` 的结构化对话历史，格式为 `[{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]`；若同时存在 `prompt` 和 `messages`，`prompt` 将被忽略。 |
| `session_id` | string | ✗ | 用于启用云端自动维护的对话历史；与 `messages` 同时存在时，`messages` 优先级更高。 |
| `biz_params` | object | ✗ | 扩展参数对象，**关键字段为 `user_defined_params`**，用于向关联[插件](../concepts/plugin.md)透传参数（详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）。 |
| `parameters` | object | ✗ | 预留扩展字段，当前暂无通用参数，各应用内部可自定义。 |
| `debug` | object | ✗ | 调试开关，设为空对象 `{}` 即可启用调试模式（返回更详细的中间执行日志）。 |

## 使用方式

### 1. 前置准备
- 获取并配置 API Key（推荐设为环境变量 `DASHSCOPE_API_KEY`）；
- 安装对应语言的 DashScope SDK（[调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 和 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 均明确要求 SDK ≥ 2.12.0（Java）或 ≥ 1.14.0（Python））；
- 确保应用已发布且位于同一业务空间（插件关联场景下）。

### 2. SDK 调用（Python 示例）
```python
from dashscope import Application
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？"
)
if response.status_code == 200:
    print(response.output.text)
```

### 3. HTTP 调用（curl 示例）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "input": {
      "prompt": "你是谁？"
    }
  }'
```

### 4. 插件参数透传（关键扩展）
在 `biz_params.user_defined_params` 中按插件 ID 组织参数：
```python
biz_params = {
    "user_defined_params": {
        "your_plugin_code": {
            "article_index": 2  # 对应插件定义的业务透传参数
        }
    }
}
# 传入 call() 方法即可
```
详细配置要求见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

## 限制和注意事项

- **地域限制**：工作流应用调用仅支持华北2（北京）地域（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)）；智能体应用无此限制，但建议确认控制台中应用部署地域。
- **插件参数约束**：
  - 插件输入参数的「传参方式」**必须选择 `业务透传`**（文档 1 强调）；
  - 插件描述与工具描述需使用自然语言，直接影响大模型是否触发该插件（文档 1 强调）；
  - 插件与应用须在同一业务空间内才能关联。
- **安全实践**：
  - **禁止硬编码 API Key**：所有示例均强调“不建议在生产环境中直接将 API Key 硬编码到代码中”，应始终通过环境变量注入；
  - SDK 版本需满足最低要求（Python ≥ 1.14.0，Java ≥ 2.12.0），否则可能缺少 `biz_params` 支持或 `session_id` 兼容性。
- **多轮对话**：
  - `session_id` 由服务端生成并返回（响应中 `output.session_id`），客户端需自行保存并在后续请求中复用；
  - `messages` 方式更可控，但需客户端完整维护历史，且首条消息 `role` 必须为 `"user"`。

## 来源文档

- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)


