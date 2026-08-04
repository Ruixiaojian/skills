# 模型上下文协议（MCP）

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化、安全、可扩展的工具调用协议，用于在大语言模型与外部能力（如地图、搜索、图表生成等）之间建立结构化上下文传递通道。它基于开源 MCP 标准（[modelcontextprotocol.io](https://modelcontextprotocol.io/)），屏蔽底层接入复杂性，使模型能以声明式方式动态调度工具，无需为每个服务单独开发适配逻辑。

## 在百炼平台的不同场景中如何使用

MCP 仅集成于百炼平台内应用，**不支持直接通过千问原始 API 调用**。其核心使用场景分为两类：

- **智能体应用（Agent）**：  
  开发者在配置页添加已开通的 MCP 服务（如 Amap Maps、WebSearch），无需指定具体工具。模型根据对话上下文自主决策是否调用、调用哪个工具及传入参数，支持单次最多并发调用 5 个 MCP 服务，适用于自然语言驱动的动态能力融合（例如“对比北京和上海今日天气并生成折线图”）。

- **工作流应用（Workflow）**：  
  通过拖拽 MCP 节点，从下拉列表中**显式选择具体工具**（如 `maps_weather`、`web_search`），并手动绑定输入参数（可引用上游节点输出）。适用于确定性流程编排，例如“提取城市名 → 查询实时天气 → 渲染可视化图表”。

> ✅ 提示：官方插件可通过“发布为 MCP 服务”后，在智能体或工作流中统一通过 MCP 区块接入，实现跨空间复用；自定义插件也需先发布为 MCP 服务才能被上述两种应用调用。

## 关键参数和配置

| 参数 | 说明 | 取值示例 | 使用位置 |
|------|------|----------|----------|
| `type` | 协议传输类型 | `"sse"` 或 `"streamableHttp"` | MCP 服务配置、自定义部署时 `mcpServers.<name>.type` |
| `url` | MCP 服务端点地址 | SSE：`https://dashscope.aliyuncs.com/api/v1/mcps/AmapMaps/sse`<br>Streamable HTTP：`https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp` | 应用配置、SDK 初始化 |
| `headers.Authorization` | 外部调用必需认证头 | `Bearer ${DASHSCOPE_API_KEY}` | SDK 请求头、第三方集成（如 Cherry Studio） |
| `mcpServers.<name>.type` | 自定义部署服务类型 | `"stdio"`（本地进程）、`"sse"`、`"streamableHttp"` | `mcp.json` 配置文件 |

⚠️ 注意：  
- 所有 MCP 服务均需通过 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 开通，敏感参数（如 API Key）必须通过 KMS 凭据加密管理；  
- 自定义 MCP 服务托管于函数计算（FC），无固定出口 IP，访问云数据库等资源时需配置白名单或 VPC 打通；  
- MCP 返回内容将作为上下文注入模型，会增加输入 [Token](token.md) 消耗，建议对返回结果做必要裁剪。

## 面向开发者的实用指引

- **快速起步**：进入 MCP 广场 → 选择服务 → “立即开通” → 在智能体/MCP 工作流节点中添加即可使用；  
- **调试建议**：使用 `mcp` 官方 SDK（如 Python 的 `streamablehttp_client`）直连服务端点，验证工具响应格式与字段语义；  
- **版本升级**：旧版 SSE 服务需主动取消再重开，才能升级至新版 Streamable HTTP 协议；  
- **错误排查**：若工具调用失败，请检查：① 服务是否已开通且状态为“可用”；② KMS 凭据是否有效；③ `input_params` 中 `Object` 类型子属性是否全部非空（否则发布失败，错误码 `130022`）；④ 网络策略是否放行 FC 出口流量。  

MCP 是百炼平台统一工具生态的核心协议——它让模型真正“懂工具”，也让开发者专注业务逻辑，而非胶水代码。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [plug in](../guides/plug-in.md)
- [managed agents api](../api/managed-agents-api.md)
- [application call](../api/application-call.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


