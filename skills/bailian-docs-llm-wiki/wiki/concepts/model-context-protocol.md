# 模型上下文协议（MCP）

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化、生产就绪的工具集成协议，用于在大语言模型与外部服务之间建立安全、可靠、可扩展的信息通道。它将工具调用抽象为统一的声明式接口，屏蔽底层通信细节（如传输协议、鉴权方式、错误重试），使开发者无需重复开发适配逻辑，即可在智能体、工作流或高代码应用中快速接入各类能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体应用（Agent 2.0）**：MCP 服务作为“可规划工具”直接参与 ReAct 循环。模型基于用户输入自主判断是否调用、调用哪个 MCP 工具（如 `websearch` 或 `amap_maps`），无需显式指令；支持完整思考-执行-反思链路回溯，工具调用结果自动注入上下文参与后续推理。
  
- **工作流应用（Workflow）**：MCP 以独立节点形式存在，每个节点绑定**唯一** MCP 工具（如 `weather_forecast`）。需手动配置输入参数（常由前置大模型节点提取并映射）、输出参数解析规则及失败重试策略，执行路径确定、可控性强。

- **高代码应用（Rich Code）**：通过 SDK（如 `streamablehttp_client`）或原生 HTTP 客户端直连 MCP 服务端点（`POST /mcp`），结合 [OpenAI 兼容接口](openai-compatible-interface.md)（如 `qwen-max`）实现自定义工具调用循环；支持与业务逻辑深度耦合（如条件分支调用不同 MCP 服务、聚合多服务结果）。

- **Managed Agents（托管智能体）**：MCP 服务可作为扩展工具与内置沙箱工具（`bash`/`read`/`download_file` 等）共存。在沙箱环境中，MCP 调用结果可被后续 `edit` 或 `bash` 操作直接消费，实现“联网搜索 → 解析网页 → 生成报告”的端到端自动化。

> ✅ 提示：MCP 不是插件（Plug-in）的替代品，而是其**协议层升级**——官方 MCP 服务本质是符合 MCP 协议的插件，但具备更严格的 Schema 校验、统一的流式响应规范（Streamable HTTP）和平台级托管保障。

## 关键参数和配置

| 参数 | 必填 | 说明 | 示例值 | 注意事项 |
|------|------|------|--------|----------|
| `type` | 是 | 通信协议类型，决定传输机制与端点路径 | `"streamableHttp"`（推荐）、`"sse"`、`"stdio"` | `streamableHttp` → POST `/mcp`；`sse` → GET `/sse`；混用将触发 `11200058/59` 错误 |
| `url` | 是（远程服务） | MCP 服务根地址（含协议、域名、端口） | `"https://your-service.example.com"` | 不含路径后缀（如 `/mcp`），平台自动拼接 |
| `command` | 是（本地脚本） | 启动命令（仅 `stdio` 类型） | `"npx @mcp/server-websearch"` 或 `"uvx mcp-server-firecrawl"` | 需确保依赖包已发布至公共仓库（npm/PyPI） |
| `env` | 否（但强烈建议） | 敏感环境变量（API Key、密钥等） | `{"AMAP_MAPS_API_KEY": "{{KMS:xxx}}"}` | **必须使用 KMS 凭据加密引用**，明文配置将导致部署失败 |
| `deployment_mode` | 否（默认基础模式） | 计费与性能模式 | `"basic"`（按次计费）、`"ultra"`（常驻+调用双计费） | `ultra` 模式降低首字延迟，适合高频低延迟场景 |

> ⚠️ 重要限制：  
> - 自定义 MCP 服务运行于函数计算（FC），**无法访问本地网络、数据库或硬件设备**；访问云资源需配置 FC 白名单或 VPC 打通。  
> - 返回结果直接注入模型输入上下文，**显著增加 [Token](token.md) 消耗**；建议在提示词中明确要求模型“精简摘要”，避免冗余返回。

## 面向开发者，简洁实用

- **快速上手**：优先选用官方 MCP 服务（如 `websearch`, `amap_maps`），控制台一键启用，免配置、免部署、享免费额度。  
- **自定义部署**：  
  - 脚本部署：`npx @mcp/server-websearch --port 3000` → 配置 `type: "streamableHttp"` + `url: "http://localhost:3000"`；  
  - API 封装：在 AI 网关中导入 RESTful 接口，平台自动生成 MCP Schema 并托管。  
- **调试技巧**：  
  - 使用控制台「测试工具」功能验证连通性与参数映射；  
  - 查看 `tool_output` 事件日志确认 MCP 响应结构是否匹配预期 Schema；  
  - 若遇 `11200058` 错误，立即检查 `type` 与端点路径是否严格匹配（`streamableHttp` ↔ `/mcp`）。  
- **最佳实践**：  
  - 输入参数务必精简（避免嵌套过深），输出参数用 `description` 明确指导模型提取关键字段；  
  - 敏感操作（如支付、删库）务必在 MCP 服务端做二次鉴权，不可仅依赖模型判断。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [plug in](../guides/plug-in.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)


