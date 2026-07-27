# 模型上下文协议

模型上下文协议（Model Context Protocol，简称 MCP）是阿里云百炼平台提供的标准化、可扩展的工具调用协议，用于在大语言模型与外部能力（如搜索、地图、数据库、代码执行等）之间建立安全、统一、语义清晰的信息交互通道。它将各类工具抽象为符合规范的“MCP 服务”，使模型能基于自然语言意图自主发现、选择并调用合适能力，无需开发者为每个工具重复编写适配逻辑。

## 在百炼平台的不同场景中如何使用

MCP 是百炼平台统一的外部能力接入标准，已全面替代旧版“插件”概念（见 LLM Application 文档说明），在以下核心场景中作为唯一推荐机制使用：

- **智能体应用（Agent 2.0）**：模型根据用户输入和 System Prompt 自主规划是否调用 MCP 工具、调用哪个工具及传入参数。最多可同时配置 5 个 MCP 服务；调用过程（思考→工具调用→结果解析→反思）全程可观测，支持开启 `enable_thinking` 和设置 `ReAct 最大轮次` 控制调用深度。
- **工作流应用（Workflow）**：通过可视化拖拽添加“MCP 节点”，显式指定工具 ID（如 `maps_weather`），输入参数需由前置节点（如大模型或变量处理器）生成并传递，输出可被后续节点直接引用（如 `${mcp_weather/result}`），适用于确定性、强编排需求的业务流程。
- **高代码应用**：在 Python 项目中通过百炼 SDK（如 `streamablehttp_client`）直接调用 `/mcp` 端点，结合 [OpenAI 兼容接口](openai-compatible-api.md)实现多轮工具调用循环，支持细粒度错误处理与自定义重试策略。
- **文件问答中的“自定义处理”模式**：当用户上传图片、PDF 或视频时，模型可自主决策是否调用 MCP 工具（如 OCR 解析、网页爬取、图表生成）进行预处理，再基于结果生成回答——此能力依赖 MCP 协议而非内置解析器。

> ✅ 注意：所有新开发应基于 MCP 协议。旧版“插件”功能已收敛至 MCP 架构下；控制台中仍显示“插件市场”的入口，实际底层均按 MCP 标准注册与调用。

## 关键参数和配置

MCP 服务配置的核心参数如下（适用于平台内集成与自定义部署）：

| 参数 | 说明 | 必填 | 常见值/约束 |
|------|------|------|-------------|
| `type` | 通信协议类型 | ✅ | 必须与端点路径严格匹配：<br>• `"streamableHttp"` → 对应 `/mcp` 端点（**推荐，新版默认**）<br>• `"sse"` → 对应 `/sse` 端点（仅兼容旧服务，不建议新集成） |
| `url` 或 `command` | 服务地址或启动命令 | ✅ | • HTTP 地址（如 `https://your-mcp-service.com/mcp`）<br>• 本地托管命令（如 `npx mcp-server-http` 或 `uvx mcp-server-http`） |
| `env` | 环境变量 | ⚠️（敏感信息必填） | 用于注入 API Key、[Token](token.md)、密钥等；建议配合 KMS 加密凭据使用 |
| `deploymentMode` | 部署模式 | ✅ | • `基础模式`：按调用秒计费（0.000156 元/秒），无部署费<br>• `极速模式`：额外收取部署费（0.000036 元/秒），适合高频稳定调用 |
| `tool_id` | 工具唯一标识符 | ✅（API 调用时） | 由 MCP 服务定义，在 Assistant API 的 `tools` 字段中声明；可通过控制台复制 |

> 💡 提示：MCP 服务必须部署在百炼函数计算（FC）环境中，**无法访问本地文件、硬件或用户私有网络内的数据库**；如需对接本地系统，请先通过 AI 网关或 OpenAPI 门户将其封装为公网可达的 RESTful 接口。

## 面向开发者的实用建议

- **优先使用官方 MCP 服务**：Amap Maps、WebSearch、Firecrawl 等开箱即用，部分限时免费，开通后可在 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 一键添加。
- **自定义 MCP 服务三步走**：① 用 `npx`/`uvx` 启动开源 MCP Server；② 或用 AI 网关将现有 API 封装为 `/mcp` 接口；③ 或通过 OpenAPI 开发者门户发布阿里云产品能力（如 OSS、ECS）。
- **Prompt 是调用成败的关键**：在 System Prompt 中清晰描述工具名称、功能、输入格式（如“天气查询需提供城市名”）和预期输出结构，避免模糊指令。
- **调试从控制台开始**：启用智能体“调试面板”，实时查看模型是否识别到工具、参数是否正确生成、MCP 返回结果是否被合理解析。
- **外部调用请认准 `/mcp` 端点**：第三方客户端（如 Cherry Studio）或 SDK 集成时，务必使用 `streamableHttp` 类型 + `/mcp` 路径；SSE 配置仅作历史兼容，新项目禁用。

> 🚫 不要尝试：在 MCP 服务中直接读写本地磁盘、连接 localhost 数据库、或调用未开放公网的内部服务——所有网络出向均受限于百炼 FC 安全沙箱。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [llm application](../guides/llm-application.md)
- [start using](../guides/start-using.md)
- [plug in](../guides/plug-in.md)
- [application component api reference](../api/application-component-api-reference.md)


