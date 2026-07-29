# application call

`application call` 是指通过 API 调用阿里云百炼平台已发布的应用（包括新版智能体、旧版智能体、工作流等）的核心能力。开发者无需自行部署模型或编排逻辑，只需提供应用 ID、API Key 及输入内容，即可获得结构化响应。调用支持同步与异步两种模式，适配实时交互与长耗时任务场景，并兼容 DashScope 原生接口和 OpenAI 兼容的 Responses API。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体、工作流三类应用；其中[文件输入](../concepts/file-input.md)仅限智能体应用，图像输入需选用通义千问 VL 系列模型 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
- **交互模式**：
  - 单轮对话：直接传入 [prompt](../guides/prompt.md) 或 input 字符串；
  - 多轮对话：通过 `session_id`（DashScope API）或完整 `messages` 数组（Responses API）维护上下文；
  - [流式输出](../concepts/streaming-output.md)：仅同步调用支持 `stream=true`，且工作流应用需在结束节点启用流式开关 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)；
  - 异步执行：通过 `background=true` 提交任务，后续轮询获取结果，适用于生成报告、多步骤工具调用等长耗时场景 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **多模态输入**：支持文本、图像（`input_image`）、音频/文档等文件（`input_file`），但[文件输入](../concepts/file-input.md)仅限智能体应用，且需在应用配置中选择“全文引用”或“切片检索”。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面复制。若应用位于子业务空间，还需配合 `workspace_id` 使用 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` | string / array | 是 | 核心输入内容：<br>• 字符串：用于单轮纯文本对话；<br>• 消息数组：支持 `system`/`user`/`assistant` 角色，含 `input_text`/`input_image`/`input_file` 子类型；<br>• 注意：基于 `pre_response_id` 或 `conversation_id` 的上下文暂不支持，需显式传递完整历史。 |
| `stream` | boolean | 否（默认 false） | 是否启用[流式输出](../concepts/streaming-output.md)。**异步调用不支持该参数**（设置将被忽略）。 |
| `background` | boolean | 否（默认 false） | 是否启用异步模式。设为 `true` 时立即返回任务 ID，需额外调用 `retrieve` 接口查询结果。 |
| `biz_params` | object | 否 | 仅 Responses API 支持，用于向工作流或插件节点传递自定义参数（如 `{"city": "北京"}`），参数名须与应用内定义严格一致。 |

> **注意**：文档 2 和文档 4 均描述了 DashScope SDK 的 `Application.call()` 方法，但文档 2 明确限定“仅适用于华北2（北京）地域”，而文档 4 未注明地域限制，存在潜在矛盾。实际使用请以控制台显示的可用地域为准，并优先参考 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 中关于 Workspace ID 地域要求的说明。

## 使用方式

### 1. 准备凭证
- 获取 `APP ID` 和（如需）`Workspace ID`：通过控制台手动复制，**不支持 API 查询** [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)；
- 获取并配置 `DASHSCOPE_API_KEY`：通过[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)获取，推荐配置为环境变量。

### 2. 选择调用入口
- **DashScope 原生 API**（推荐用于高性能/全功能场景）：
  - Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
  - SDK 示例（Python）：
    ```python
    from dashscope import Application
    response = Application.call(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        app_id="YOUR_APP_ID",
        prompt="你是谁？"
    )
    ```
- **OpenAI 兼容 Responses API**（推荐用于快速迁移/复用现有 OpenAI 代码）：
  - 同步 Endpoint：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
  - 异步 Endpoint：同上，请求体中添加 `"background": true`
  - SDK 示例（Python）：
    ```python
    from openai import OpenAI
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/YOUR_APP_ID/compatible-mode/v1/"
    )
    response = client.responses.create(input="你是谁？")
    ```

### 3. 处理响应
- 同步调用：直接解析 `response.output.text`（DashScope）或 `response.output[0].content[0].text`（Responses）；
- 异步调用：先 `create` 获取 `task_id`，再循环 `retrieve(task_id)` 直至 `status` 为 `completed`/`failed`/`cancelled`；
- 流式调用：遍历 `response` 的 `delta` 字段逐块消费。

## 限制和注意事项

- **地域限制**：所有文档均明确标注“本文档仅适用于华北2（北京）地域”。若应用部署在德国（法兰克福）、新加坡等其他地域，必须提供 `Workspace ID`，且 Base URL 会不同 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **会话有效期**：DashScope API 的 `session_id` 在最后一次请求后 1 小时内有效；Responses API 无原生会话机制，需显式传入完整 `messages` 数组。
- **权限要求**：RAM 子账号访问“业务空间管理”页面需被授予超级管理员权限，否则无法查询全部 Workspace ID [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **安全实践**：严禁在生产代码中硬编码 `API Key`，务必通过环境变量或密钥管理服务注入。
- **调试支持**：所有应用均提供控制台在线调试功能（路径：应用卡片 → 发布 → API 调试），可快速验证参数与响应。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


