# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者可使用 DashScope 原生 API 或 OpenAI 兼容的 Responses API 进行集成，支持文本、图像、文件等[多模态](../concepts/multi-modal.md)输入，并提供会话管理、[流式输出](../concepts/streaming-output.md)与异步任务处理等关键功能。所有调用均需有效凭证（API Key + APP ID），部分场景还需 Workspace ID。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流三类应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **[多模态](../concepts/multi-modal.md)能力**：
  - 图像输入：需选用通义千问 VL 系列模型，并在应用中配置为“自定义处理”（智能体）或设置 `imageList` 入参（工作流）[同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
  - 文件输入：仅智能体应用支持，需启用“全文引用”或“切片检索”文件处理方式。
- **交互模式**：
  - 单轮/多轮对话：DashScope API 通过 `session_id` 维护上下文；Responses API 则需显式传递完整 `messages` 数组。
  - [流式输出](../concepts/streaming-output.md)：仅同步调用支持，且工作流应用需在结束节点启用“[流式输出](../concepts/streaming-output.md)”开关并重新发布。
  - 异步执行：通过 `background=true` 触发，适用于耗时较长任务（如报告生成），但不支持流式输出。

> **注意**：文档 2（新版智能体 API）和文档 4（通用 DashScope API）均声明“仅适用于华北2（北京）地域”，而文档 1 明确指出 Workspace ID 在德国（法兰克福）、华北2（北京）、新加坡、日本（东京）等地域为必需参数。二者存在隐含矛盾——文档 4 未说明 Workspace ID 是否需参与请求 URL 或 Header，而文档 1 明确其是 Base URL 的组成部分。实际调用时，若目标地域非北京，必须按 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 所述构造 endpoint 并传入 Workspace ID，不可仅依赖文档 4 的示例 URL。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在控制台 [应用管理](https://bailian.console.aliyun.com/#/app-center) 页面获取。 |
| `input` | string \| array | 是 | 核心输入内容：<br>- 字符串：单轮纯文本（如 `"你好"`）；<br>- 消息数组：支持多轮对话及[多模态](../concepts/multi-modal.md)（`input_text`/`input_image`/`input_file`）。 |
| `stream` | boolean | 否 | 默认 `false`。设为 `true` 启用流式响应（仅同步调用支持）。 |
| `background` | boolean | 否 | 默认 `false`。设为 `true` 触发异步任务，返回 `task_id` 而非结果。 |
| `biz_params` | object | 否 | 用于向工作流或智能体传递自定义参数（如城市名、索引值），需与应用内参数定义严格一致。 |

## 使用方式

### 1. 凭证准备
- 获取 `DASHSCOPE_API_KEY`：通过 [密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key) 创建并配置至环境变量。
- 获取 `APP_ID`：在 [应用管理](https://bailian.console.aliyun.com/#/app-center) 复制应用卡片 ID。
- 获取 `Workspace ID`（按需）：若应用位于子业务空间或目标地域为法兰克福/北京/新加坡/东京，需通过控制台右上角用户菜单或 [业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 获取 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

### 2. API 调用路径
- **DashScope 原生 API**（推荐用于高性能/全功能场景）：
  - Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
  - 请求体示例（HTTP）：
    ```json
    {
      "input": { "prompt": "你是谁？" },
      "parameters": {},
      "debug": {}
    }
    ```
- **OpenAI 兼容 Responses API**（便于迁移现有 OpenAI 代码）：
  - 同步 Endpoint：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
  - 异步 Endpoint：同上，但请求体中添加 `"background": true`。
  - SDK 初始化示例（Python）：
    ```python
    from openai import OpenAI
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/"
    )
    ```

### 3. 多轮对话实现
- **DashScope API**：首请求不带 `session_id`，响应中返回 `session_id`；后续请求携带该值即可延续会话（有效期 1 小时）。
- **Responses API**：无需 `session_id`，直接在 `input` 数组中传入完整历史消息（`role: user/assistant/system`）。

## 限制和注意事项

- **地域限制**：所有文档均明确标注“仅适用于华北2（北京）地域”，但 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 指出 Workspace ID 在法兰克福、新加坡等多地为必需。开发者须根据实际部署地域选择对应 endpoint 并补充 Workspace ID，否则将返回 404 或权限错误。
- **异步限制**：异步调用不支持 `stream=true`，且需自行实现轮询逻辑（如 Python 示例中的 `retrieve` 调用）以获取最终结果。
- **凭证时效性**：API Key 无自动刷新机制，需定期轮换；APP ID 和 Workspace ID 为静态标识，长期有效。
- **调试支持**：所有应用均提供控制台在线调试入口（应用卡片 → 发布 → API 调试），建议首次集成时优先使用。
- **权限要求**：RAM 子账号查询 Workspace ID 需被授予 `AliyunBailianFullAccess` 或 `AliyunBailianControlFullAccess` 权限，否则访问 [业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 将失败。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


