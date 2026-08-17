# bailian [application call](../api/application-call.md)ing

百炼应用调用是将阿里云百炼平台构建的智能体应用（Agent 1.0）或工作流应用集成至业务系统的标准方式，支持通过 DashScope SDK 或原生 HTTP API 发起请求。调用过程统一使用 `/api/v1/apps/{app_id}/completion` 接口，核心逻辑围绕 `prompt` 输入、可选的业务参数透传及会话管理展开，适用于单轮问答与多轮对话场景。

## 支持的模型/功能

- **应用类型**：当前支持两类应用调用：
  - **智能体应用（Agent 1.0）**：面向单任务、轻量级交互场景，基于大模型直接响应用户 [prompt](prompt.md)；详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)。
  - **工作流应用**：面向复杂编排场景，支持多节点（如大模型、插件、条件分支等）协同执行；详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **功能能力**：
  - 基础文本生成（`prompt` → `output.text`）
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 传递插件 ID 及其输入参数），仅限已关联插件的智能体应用或工作流应用中的插件节点；详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。
  - 多轮对话支持（通过 `session_id` 或显式 `messages` 数组管理上下文）

> **注意**：文档 3 明确指出“百炼工作流不支持使用文生图大模型”，而文档 1 和文档 3 均未提及图像生成能力；因此，**所有百炼应用调用均仅支持文本类模型（如 qwen-max、qwen-plus）**，不支持 multimodal 模型（如 qwen-vl）或文生图模型。该限制在三份文档中一致，无矛盾。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，从[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取。 |
| `prompt` | string | 是（若未提供 `messages`） | 用户输入的自然语言指令，作为本轮对话主输入。 |
| `biz_params` | object | 否 | 业务扩展参数对象，用于透传自定义插件参数：<br>• `user_defined_params`: `{ "plugin_code": { "param_key": "param_value" } }`<br>• 插件 code 需与控制台插件卡片上显示的 ID 完全一致。 |
| `input`（HTTP） | object | 是（HTTP 请求体顶层字段） | 包含 `prompt` 和可选 `biz_params` 的容器对象。SDK 中自动封装。 |
| `session_id` | string | 否 | 启用云端会话历史加载（有效期 1 小时，最多 50 轮）。若同时传 `messages`，则 `session_id` 被忽略。 |
| `messages` | array | 否（替代 `prompt`） | 显式维护的对话历史数组，格式为 `[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]`，推荐用于精确上下文控制。 |

## 使用方式

### 前置准备
1. 获取并配置 API Key：前往[密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key)创建 API Key，并**强烈建议通过环境变量 `DASHSCOPE_API_KEY` 设置**，避免硬编码；
2. 获取目标应用的 `app_id`：在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面复制对应应用卡片上的 APP_ID；
3. （可选）安装 SDK：Python 使用 `pip install -U dashscope`；Java 需在 `pom.xml` 或 `build.gradle` 中引入 `com.alibaba:dashscope-sdk-java`（推荐 ≥2.12.0）。

### 调用示例（统一接口）
- **SDK（Python）**
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你好，请介绍自己",
      biz_params={"user_defined_params": {"plugin_abc123": {"query_id": 42}}}
  )
  print(response.output.text)
  ```

- **HTTP（curl）**
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "input": {
            "prompt": "你好，请介绍自己",
            "biz_params": {
              "user_defined_params": {
                "plugin_abc123": {"query_id": 42}
              }
            }
          }
        }'
  ```

> 所有语言 SDK 和 HTTP 示例均保持接口一致性，详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 与 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 中的完整代码片段。

## 限制和注意事项

- **地域限制**：工作流应用调用**仅支持华北2（北京）地域**，智能体应用无此限制；该约束明确记载于 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 文档头部。
- **插件参数透传前提**：`biz_params.user_defined_params` 仅在应用已关联对应插件时生效；未关联插件时传入该参数将被忽略，不会报错但无实际作用。
- **安全实践**：
  - 禁止在代码中硬编码 `DASHSCOPE_API_KEY`，必须使用环境变量或密钥管理服务；
  - 插件鉴权配置（如 Basic Auth Header）需在插件创建时正确设置，SDK/HTTP 调用层不参与鉴权流程。
- **错误处理**：所有调用均返回标准 HTTP 状态码（如 400、401、429、500）及 `request_id`，需结合 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code) 进行诊断。
- **多轮对话容量**：`session_id` 方式下，单个会话最多保留 50 轮历史，超限时需新建会话；`messages` 方式由开发者自行控制长度，但总 token 数受所用模型上下文窗口限制。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)


