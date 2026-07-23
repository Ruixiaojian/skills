# 模型上下文协议

模型上下文协议（Model Context Protocol，简称 MCP）是百炼平台提供的标准化、生产就绪的[工具集成](tool-integration.md)协议，用于在大语言模型与外部能力（如地图、搜索、数据库、爬虫等）之间建立安全、可扩展、可编排的信息通道。它抽象了通信细节与调用范式，使模型能以统一方式发现、规划并执行工具调用，无需为每个服务定制适配逻辑。

## 在百炼平台的不同场景中，这个概念如何使用

MCP 不是独立运行的服务，而是深度集成于百炼应用架构中的**协议层能力**，其使用严格绑定以下两类核心场景：

- **智能体应用（Agent 2.0）**：  
  在提示词驱动下，模型自动判断是否需要调用工具、选择哪个 MCP 工具（如 `maps_weather`）、提取参数并生成结构化调用请求。开发者只需在智能体编辑页的「工具」区域添加已开通的 MCP 服务（最多 5 个），无需编写调度逻辑。整个“思考-调用-反思”链路全程可观测，支持调试回溯。

- **工作流应用（Workflow）**：  
  开发者通过可视化画布显式拖入「MCP 节点」，手动绑定具体工具（如 `web_search`）、配置输入变量（如从上一节点 `intent_extractor/query` 取值）和输出变量（如将 `result` 写入 `search_result`）。适用于流程确定、需强控制的自动化任务，如“用户提问 → 提取地点 → 查询天气 → 生成摘要”。

> ⚠️ 注意：MCP **不支持直连 DashScope Qwen API**（如 `qwen-turbo` 的 `/v1/chat/completions` 接口）。它仅在百炼平台内托管的应用（智能体/工作流/高代码应用）中生效，不可作为通用插件 SDK 直接注入第三方 LLM 调用。

## 关键参数和配置

MCP 服务的接入与调用依赖以下关键配置项，均需在百炼控制台或 SDK 中明确设置：

| 参数类别 | 参数名 | 说明 | 必填 | 示例值 |
|----------|--------|------|------|--------|
| **协议类型** | `type` | 决定通信协议与端点路径，**必须严格匹配**：<br>• `"streamableHttp"` → 对应 `/mcp` 端点（当前唯一支持的生产协议）<br>• `"sse"` → 已淘汰，配置将触发错误码 `11200058` 或 `11200059` | ✅ | `"streamableHttp"` |
| **部署方式** | `安装方式` | 指定运行环境：<br>• `"npx"`（Node.js）或 `"uvx"`（Python）→ 托管至函数计算（FC），免运维<br>• `"http"` → 连接自建远程服务（需公网可达） | ✅ | `"npx"` |
| **计费模式** | `部署方式` | 影响成本与延迟：<br>• `"基础模式"`：按调用时长计费（0.000156 元/秒），有冷启动延迟<br>• `"极速模式"`：额外收取常驻内存费（0.000036 元/秒），毫秒级响应 | ✅ | `"基础模式"` |
| **安全凭证** | `KMS 凭据` | 所有敏感配置（如 API Key、Secret）**必须通过 KMS 加密 URI 引用**，禁止明文填写 | ✅ | `kms://acs:kms:cn-beijing:1234567890:alias/mcp-amap-key` |
| **服务元信息** | `服务名称` / `描述` | 仅用于控制台识别与管理，不影响模型调度逻辑 | ❌ | `"高德天气"` / `"查询实时城市天气"` |

## 面向开发者，简洁实用

- **快速接入**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，点击「立即开通」任一官方服务（如 WebSearch、Amap Maps），然后在智能体或工作流中直接添加即可使用。
- **自定义服务**：确保服务实现符合 [MCP 官方规范](https://modelcontextprotocol.io/)，部署时选择 `npx` 或 `uvx` 方式，**发布后不会自动更新**——上游包升级需手动重新部署。
- **外部调用（IDE/第三方项目）**：使用 `pip install mcp`，通过 `streamablehttp_client` 连接百炼 MCP endpoint（如 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`），调用 `list_tools()` 获取工具列表，并转换为 OpenAI 兼容格式传入 `tools` 参数。
- **排障要点**：  
  • 报错 `11200058` 或 `11200059`？→ 检查 `type` 是否为 `"streamableHttp"` 且端点路径为 `/mcp`；  
  • 工具无响应？→ 确认服务状态为「已发布」且 KMS 凭据有效；  
  • 自建服务访问云资源失败？→ 函数计算无固定出口 IP，需配置 VPC 打通或白名单。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [plug in](../guides/plug-in.md)
- [managed agents api](../api/managed-agents-api.md)
- [llm application](../guides/llm-application.md)
- [application component api reference](../api/application-component-api-reference.md)


