# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化工具接入机制，用于在大模型推理过程中安全、高效地调用外部能力（如地图、天气、网页爬取、知识图谱等）。它屏蔽了底层接口差异，使开发者无需为每个工具单独编写适配代码，即可在智能体、工作流或第三方应用中统一集成和管理工具服务。协议基于开源 MCP 标准实现，支持 Streamable HTTP 和 SSE 两种传输方式。

## 支持的模型/功能

MCP 服务本身不绑定特定大模型，但其调用效果高度依赖所配置的推理模型能力。官方推荐使用通义千问系列模型（如 `qwen-max`、`qwen-3`）以获得更准确的工具识别与参数生成能力。当前支持以下三类服务接入方式：

- **官方 MCP 服务**：由阿里云百炼预部署并托管的即开即用服务，例如 [Amap Maps](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)、联网搜索（WebSearch）、Sequential Thinking 等，部分限时免费。
- **自定义 MCP 服务**：支持三种部署路径：
  - *使用脚本部署*（npx/uvx）：适用于已发布至 npm 或 PyPI 的开源或自研 MCP 服务；
  - *从 AI 网关导入*：将现有 RESTful API 封装为 MCP 工具；
  - *从阿里云 OpenAPI 导入*：将 OSS、ECS 等云产品能力暴露为可调用工具。
- **外部客户端集成**：支持通过标准协议接入 Cherry Studio、Cursor 等主流 MCP 客户端，详见 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) 文档。

> **注意**：文档 2 中提到“智能体和工作流应用已支持接入两种 MCP 服务”，该表述已过时；实际支持官方、自定义（含全部三种方式）及外部客户端多源接入，以 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) 文档为准。

## 关键参数

MCP 服务配置与调用涉及以下核心参数：

- `type`：指定通信协议类型，必须与后端端点严格匹配。`"sse"` 对应 `/sse` 路径（GET），`"streamableHttp"` 对应 `/mcp` 路径（POST）；配置错误将导致 `11200058` 或 `11200059` 错误码。
- `command` / `args`：脚本部署模式下指定启动命令（如 `npx`）及参数，需确保包名正确且可公开访问（私有 npm 仓库暂不支持）。
- `url`：远程服务地址，必须可公网访问；若服务位于 VPC 内，需通过函数计算 FC 的 VPC 打通或 IP 白名单配置。
- 敏感凭证（如 `AMAP_MAPS_API_KEY`）：禁止明文填写，必须通过 KMS 凭据加密管理，参见 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md) 中的安全说明。
- `env`：环境变量注入，用于传递非敏感配置（如 `YOUR_ENV_KEY`）。

## 使用方式

### 平台内集成（智能体/工作流）
- **智能体应用**：最多可同时添加 5 个 MCP 服务；大模型根据对话自动判断是否调用及选择工具，无需显式指定。示例场景包括路径规划、逻辑推理、多工具协同绘图等。
- **工作流应用**：每个 MCP 节点仅能绑定一个工具，需手动配置输入参数（如通过前置大模型节点提取城市名）和输出参数映射（如将 `maps_weather` 结果传给总结节点）。

### 外部调用
- **第三方应用集成**：支持一键配置至 Cherry Studio、Cursor，或通过 DASHSCOPE_API_KEY 手动配置。
- **SDK 编程集成**：推荐使用 `mcp` SDK（如 `streamablehttp_client`）配合 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用。示例代码见 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) 文档，需注意 `base_url` 和认证头格式。

## 限制和注意事项

- **网络与资源限制**：MCP 服务托管于函数计算 FC，无固定出口 IP，访问云数据库等资源需配置 IP 白名单或 VPC 打通；**不支持访问用户本地资源（如本地文件、数据库）**。
- **计费模式**：
  - 官方服务：部署免费，调用费用由第三方 API 提供方收取（如高德地图）；联网搜索服务有 2000 次/月免费额度，超量后 29 元/千次。
  - 自定义服务：分“基础模式”（按调用时长计费，0.000156 元/秒）和“极速模式”（额外收取部署时长费 0.000036 元/秒），冷启动延迟仅存在于基础模式。
- **协议兼容性**：所有 MCP 服务必须遵循 [MCP 官方协议规范](https://modelcontextprotocol.io/)；非标准实现可能导致 `11200054`（协议解析错误）等异常。
- **版本与维护**：自定义服务（npx/uvx 部署）版本更新后需手动重新部署；第三方 MCP 服务可用性由服务商保障，百炼仅提供接入渠道，不承诺 SLA。
- **[Token](../concepts/token.md) 开销**：MCP 返回结果作为上下文注入模型，**必然增加输入 [Token](../concepts/token.md) 数量**；输出 [Token](../concepts/token.md) 也可能因响应更详尽而间接增加。

## 来源文档

- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


