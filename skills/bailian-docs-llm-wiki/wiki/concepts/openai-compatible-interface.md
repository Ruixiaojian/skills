# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 REST API，严格遵循 OpenAI 的请求/响应协议（如 `chat/completions`、`embeddings`、`files` 等路径与结构），使开发者无需修改业务代码即可将现有基于 OpenAI SDK 或工具链（如 LangChain、Dify、Cursor、Cherry Studio）的应用快速迁移到百炼平台。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用**：支持 `qwen-plus`、`qwen-turbo`、`qwen3-*`、`Qwen-VL`、`Qwen-Coder`、`DeepSeek`、`Kimi`、`GLM` 等数十个模型，通过统一的 `/compatible-mode/v1` 协议层接入。注意：`Qwen-Audio` 和部分多模态 Embedding 模型不支持该协议。
- **智能体（Agent）调用**：通过 `application call` 的 OpenAI 兼容模式（endpoint: `https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`），以 `client.responses.create()` 方式触发已发布的智能体应用，支持同步[流式输出](streaming-output.md)（异步模式不支持流式）。
- **工具增强场景**：`Responses API` 是 OpenAI 兼容的增强子集，内置联网搜索、网页抓取、代码解释器等工具能力，适用于需轻量级智能体功能的场景；而标准 `Chat Completions` 接口默认禁用[工具调用](tool-use.md)。
- **多模态与批量处理**：  
  - `Vision` 接口支持图像理解（`Qwen-VL`、`QVQ`）；  
  - `Batch` 接口支持异步批量文件处理（如文档解析）；  
  - `Batch Chat` 支持单请求多对话并发；  
  - `Conversations` 接口提供会话生命周期管理，配合 Responses 实现跨设备上下文延续。
- **开发工具集成**：所有主流客户端（Hermes Agent、Qwen Code、Cherry Studio）、IDE 插件（Cline、Qoder）及低代码平台（Dify *仅限按量计费 Key*）均可通过配置 `base_url` + `api_key` + `model` 三要素直接接入，零代码适配。

## 关键参数和配置

- **`base_url`（必需）**：必须为兼容模式专属地址，格式为  
  `https://{WorkspaceId}.<region>.maas.aliyuncs.com/compatible-mode/v1`（北京/新加坡/东京/法兰克福）  
  或 `https://dashscope-us.aliyuncs.com/compatible-mode/v1`（弗吉尼亚）。  
  ⚠️ 旧域名 `dashscope.aliyuncs.com` 已过时，使用将导致 404。
- **`api_key`（必需）**：须与 `base_url` 所属方案及地域严格匹配（如 [Token](token.md) Plan 个人版 Key 仅可用于对应地域的 [Token](token.md) Plan Base URL）。
- **`model`（必需）**：模型 ID 必须在所选方案支持列表内（如 `qwen3.8-max-preview` 仅限 [Token](token.md) Plan，`qwen3.7-plus` 可用于 Coding Plan），大小写敏感，部分工具需转义（如 `glm-5.2` → `glm-5-2`）。
- **`stream`（可选）**：设为 `true` 启用流式响应，适用于实时对话场景；注意异步调用（`background: true`）不支持流式。
- **`thinking` / `enable_thinking`（Qwen3 系列专用）**：控制思考模式开关，部分模型（如 `qwen3.8-max-preview`）强制启用，需显式传入 `"enable_thinking": true`。
- **`workspace_id`（条件必需）**：当应用或模型部署在子业务空间，或位于德国（法兰克福）、新加坡、日本（东京）等地域时，必须作为 Base URL 的子域或请求参数显式指定。

## 面向开发者，简洁实用

✅ **快速上手三步走**：  
1. 在百炼控制台获取对应方案的 `API Key`；  
2. 构造 `base_url`（务必含 `/compatible-mode/v1` 后缀）；  
3. 使用任一 OpenAI SDK 初始化客户端（Python 示例）：  
```python
from openai import OpenAI
client = OpenAI(
    api_key="sk-xxx",
    base_url="https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
response = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你好"}]
)
```

⚠️ **避坑提醒**：  
- 不要混用方案凭证（Token Plan Key ≠ Coding Plan Key ≠ 按量计费 Key）；  
- `system` 消息计入输入 token，长上下文需预留足够 `max_tokens`；  
- [工具调用](tool-use.md)请优先选用 `Responses API`，而非标准 `chat/completions`；  
- 文件类输入（图像、PDF）需先上传获取 `oss://` URL，并在请求 Header 中添加 `X-DashScope-OssResourceResolve: enable`。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more about models](../api/more-about-models.md)


