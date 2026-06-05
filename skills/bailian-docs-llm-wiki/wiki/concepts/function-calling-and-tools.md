# 函数调用与工具集成

函数调用（Function Calling）与工具集成是让大模型突破自身知识与能力边界、连接外部系统的核心机制。在百炼平台上，开发者可通过插件、MCP（模型上下文协议）、OpenAI 兼容 `tools` 参数、意图理解模型等多种方式，将搜索、计算、API、数据库、第三方服务等外部能力暴露给大模型，由模型根据上下文自主或按编排顺序调用，并把工具返回结果回填到对话中生成最终回复。

## 在百炼平台的不同场景中如何使用

### 智能体应用（Agent）

智能体是函数调用最典型的载体。在新版 Agent 2.0 中，知识库、MCP 服务、插件被统一抽象为"工具"，由大模型根据提示词与对话上下文自主规划"规划-执行-反思"链路：

- 添加方式：在控制台应用编辑页选择 MCP 服务或插件，配置完毕即可对话调试。
- 工具上限：单个智能体最多挂载 **10 个插件工具**，最多同时启用 **5 个 MCP 服务**。
- 调用控制：可配置 `ReAct 最大轮次`（1–50）限制单次会话中的工具调用次数，防止失控。
- 模型选择：推荐使用工具调用能力强的 `qwen-max` 系列、`qwen-plus` 或开启 `enable_thinking` 的推理模型，效果显著优于小模型。

旧版 Agent 1.0 通过插件机制调用工具，自定义插件存在 **5 秒超时限制**。

### 工作流应用（Workflow）

工作流以可视化节点方式串联工具调用，与智能体的"自主规划"形成对比：

- 每个 MCP 节点手动指定一个工具，由编排顺序决定调用时机。
- 通常需要在 MCP/插件节点前后增加大模型节点，完成自然语言到结构化参数、工具输出到自然语言回复的转换。
- 适合诈骗识别、订单处理、报告生成等流程固定、需要精确控制的场景。

### Assistant API / 应用 API

通过 API 直接调用工具时：

- **Assistant API**：在请求体的 `tools` 数组中传入工具 ID，可在百炼控制台插件详情页查询。
- **应用 API**：通过 `biz_params` 透传业务参数或用户级鉴权信息，避免把敏感配置写入提示词。

### [OpenAI 兼容接口](openai-compatible-api.md)

百炼的 `/v1/chat/completions` 与 `/v1/responses` 接口完全兼容 OpenAI Function Calling 协议：

- `tools` 参数声明函数 schema（`name` / `description` / `parameters`），由模型返回 `tool_calls` 数组。
- `/v1/responses` 进一步内置了联网搜索、网页抓取、代码解释器、文搜图/图搜图等"开箱即用"工具，通过 `previous_response_id` 自动维护多轮上下文，免去手动拼装消息历史。
- 只需替换 `api_key`、`base_url`、`model` 三个参数即可让原有 OpenAI 代码迁移到百炼，工具调用语义保持不变。

### MCP（Model Context Protocol）

MCP 是百炼推荐的"工具协议层"，把工具注册与调用从应用代码中解耦：

- **官方 MCP 服务**：Amap Maps、Sequential Thinking、QuickChart、联网搜索等，开通即可使用。
- **自定义 MCP 服务**：支持三种部署方式——`npx`（公共 npm 包）、`uvx`（公共 PyPI 包）、`http`（已部署的远程 SSE / Streamable HTTP 服务），也可从 AI 网关或阿里云 OpenAPI 导入。
- **外部调用**：第三方客户端（Cherry Studio、Cursor）或 Qwen Agent 等 SDK 可直接接入百炼 MCP，端点格式为 `https://dashscope.aliyuncs.com/api/v1/mcps/<service-name>/mcp`，请求头携带 `Authorization: Bearer <API Key>`。
- **协议升级**：旧版 SSE 协议已废弃，统一升级为 Streamable HTTP，已开通用户需重新开通完成迁移。

### 插件（Plugin）

插件是百炼早期的工具集成机制，至今仍可在智能体应用中使用，并可一键转换为 MCP 服务：

- **官方插件**：`code_interpreter`（Python 代码解释器）、`calculator`（计算器）、`text_to_image`（图片生成）、`quark_search`（夸克搜索）、`generate_qrcode`、`github_search` 等，无需配置即可调用。
- **三方插件**：经过效果测试的商业服务、图像视频、学习教育类工具。
- **自定义插件**：通过定义 URL、工具路径、参数 schema、鉴权方式接入自有 API，也支持从云市场一键导入。

### 意图理解模型 `tongyi-intent-detect-v3`

当只需要"判断用户想做什么 / 该调哪个函数"时，使用通用大模型成本过高。意图理解模型在百毫秒级内完成意图识别与函数路由，常作为"工具调用前的路由层"：

- 通过 System Message 切换三种工作模式：同时输出意图与函数调用、仅输出意图、仅输出函数调用。
- 上下文 8,192 Token，最大输出 1,024 Token。

## 关键参数和配置

### 工具/函数 schema 设计

无论是 OpenAI 兼容 `tools`、自定义插件还是 MCP，**工具名称与工具描述都直接影响大模型的调用决策**：

| 字段 | 作用 | 建议 |
| --- | --- | --- |
| 工具名称 / `name` | 语义标识，模型用于选工具 | 使用动词短语，明确动作 |
| 工具描述 / `description` | 告诉模型"什么时候用这个工具" | 写清触发条件、输入输出形态 |
| 参数 schema / `parameters` | 输入字段的类型、必填性、含义 | 提供示例值与字段描述，命中率显著提升 |

### 自定义插件 / 工具配置

| 参数 | 说明 |
| --- | --- |
| 插件 URL | 插件访问域名，与工具路径拼接成完整 URL |
| 工具路径 | 必须以 `/` 开头，相对插件 URL |
| 请求方法 | `GET` 或 `POST`；`GET` 不支持 `Object` 类型入参 |
| 提交方式 | `application/json` 或 `application/x-www-form-urlencoded` |
| 鉴权 | 服务级 / 用户级；可放 Header 或 Query；Token 类型支持 `basic` / `bearer` / `appcode` |
| 输入参数传参方式 | **大模型识别**（从用户输入提取）或 **业务透传**（外部主动传入） |
| 输出参数 | 模型据此对 API 返回结果做筛选与重组 |

### MCP 自定义服务配置示例

```json
{
  "mcpServers": {
    "本地 MCP 服务": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@your_acc_name/your_pkg_name"],
      "env": { "YOUR_ENV_KEY": "YOUR_ENV_VALUE" }
    },
    "远程 MCP 服务": {
      "type": "sse/streamableHttp",
      "url": "https://your-mcp-server/sse"
    }
  }
}
```

### 计费与限制相关参数

- MCP 调用会把工具返回内容回填到上下文，**显著增加输入与输出 Token 消耗**。
- 自定义部署 MCP：基础模式仅按调用秒数计费（约 0.000156 元/秒），极速模式额外收取部署费但消除冷启动延迟。
- 智能体应用 API 默认限流 **100 次/分钟**，主账号与 RAM 子账号共享。
- 联网搜索 MCP：免费额度 2000 次，超出后 29 元/千次，限流 15 QPS。

## 常见注意事项

- **本地资源不可达**：云部署的 MCP / 插件无法访问用户本地数据库与文件，访问私网资源需配置 IP 白名单或 VPC 打通。
- **私有仓库暂不支持**：`npx` / `uvx` 仅支持公共 npm / PyPI。
- **删除即不可撤回**：删除插件或工具会让关联应用失效，无法恢复。
- **Python 代码解释器沙箱受限**：不支持外网访问与本地文件上传，仅可使用预置依赖库。
- **夸克搜索 vs `enable_search`**：前者作为工具显式调用并把搜索结果文本回填；后者由模型内部隐式使用搜索结果，不会原样返回。
- **跨端点不能复用代码**：`qwen3-rerank` 走 OpenAI 兼容扁平参数，`qwen3-vl-rerank` / `gte-rerank-v2` 走 DashScope 嵌套参数，请求与响应结构均不同。
- **效果不佳时优先升级模型**：工具调用质量与模型能力强相关，遇到不调用、调错工具、参数缺失等问题，先换更强的推理模型（如 `qwen-max`、`qwen3` 推理系列），再优化提示词与工具描述。

## 关联主题页

- [plug in](../guides/plug-in.md)
- [model context protocol](../guides/model-context-protocol.md)
- [llm application](../guides/llm-application.md)
- [more models](../api/more-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


