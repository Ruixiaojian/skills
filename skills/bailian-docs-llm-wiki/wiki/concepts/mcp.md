# 模型上下文协议

模型上下文协议（Model Context Protocol，简称 MCP）是阿里云百炼平台提供的标准化工具接入协议，用于在大模型应用（如智能体、工作流）与外部服务之间建立安全、可扩展的上下文交互通道。它通过统一声明、自动发现与按需调用机制，屏蔽第三方服务接口差异，使模型能基于自然语言理解动态调用工具，无需为每个服务单独开发适配逻辑。

## 在百炼平台的不同场景中如何使用

MCP 仅适用于**智能体应用**和**工作流应用**，不支持直接集成到千问 API 调用中。其使用方式因应用类型而异，核心目标一致：将外部能力作为“上下文”注入模型推理过程。

- **智能体（Agent）中使用**  
  在智能体配置页的「规划」模块中，添加已开通的 MCP 服务（最多 5 个）。模型根据用户输入自主判断是否调用、调用哪个服务及传入哪些参数。例如提示词：“查一下北京今天天气”，模型可自动触发 `maps_weather` 工具并解析返回结果。无需显式编写工具调用逻辑，完全由模型自主规划（ReAct 链路）。

- **工作流（Workflow）中使用**  
  在工作流画布中拖入「MCP 节点」，手动指定服务名称（如 `web_search`）和输入参数（支持变量引用，如 `${sys.query}`）。典型模式为：前置大模型节点提取结构化参数 → MCP 节点执行调用 → 后置大模型节点解析返回内容并生成最终响应。适合需要确定性编排、多步参数传递或结果后处理的场景。

- **高代码应用中使用**  
  在高代码应用的「工具」Tab 中关联已开通的 MCP 服务。开发者可通过 SDK（如 `@modelcontextprotocol/client`）在 Python 函数中直接调用，也可将 MCP 服务封装为自定义组件供前端调用，实现深度定制与可观测集成。

> ⚠️ 注意：MCP 不支持在知识库检索、文件解析等非 Agent/Workflow 场景中直接调用；也不可用于替代 Prompt 工程或数据连接器功能。

## 关键参数和配置

MCP 服务配置需严格匹配协议类型与端点，否则将触发错误码 `11200058`（协议不匹配）或 `11200059`（端点不可达）。关键字段如下：

| 参数 | 必填 | 说明 | 示例/约束 |
|------|------|------|-----------|
| `type` | ✅ | 协议传输类型，**必须与后端端点路径严格对应** | `"streamableHttp"`（对应 `/mcp`）、`"sse"`（对应 `/sse`）、`"stdio"`（本地脚本） |
| `service_name` | ❌ | 仅用于控制台显示标识，不影响调用逻辑 | `"天气查询"`、`"长期记忆"` |
| `command` 或 `url` | ✅ | 启动命令（脚本部署）或远程服务地址（HTTP） | `npx -y @modelcontextprotocol/server-memory` 或 `https://my-mcp-service.aliyuncs.com/mcp` |
| `env` | ❌（敏感时必填） | 敏感环境变量（如 API Key），**必须使用 KMS 加密 URI 格式** | `{ "AMAP_MAPS_API_KEY": "kms://akxxx/xxx" }` |
| `deployment_mode` | ❌（仅脚本部署） | 决定计费与性能特性 | `"基础模式"`（按调用计费，有冷启动延迟）或 `"极速模式"`（常驻实例+调用双计费） |

> 🔑 安全提示：所有含凭证的 `env` 字段禁止明文填写；自定义 MCP 服务运行于函数计算（FC），**无法访问本地文件、数据库或硬件设备**，访问云资源需配置 VPC 或 IP 白名单。

## 面向开发者的实用建议

- **快速起步**：优先使用 MCP 广场中的官方服务（如 `WebSearch`、`QuickChart`），开通即用，无需部署。
- **协议升级**：旧版 SSE 协议已停用，新部署务必使用 `type: "streamableHttp"` + `/mcp` 端点；存量服务需重新开通以完成协议升级。
- **调试技巧**：在智能体「文本对话体验」面板中开启「工具调用日志」，可查看模型决策链路、参数传递与原始返回内容。
- **[Token](token.md) 优化**：MCP 返回内容直接注入模型上下文，显著增加输入 [Token](token.md)。对返回结果较长的服务（如全文搜索），建议在工作流中先做摘要再送入模型。
- **外部调用**：可通过百炼 MCP SDK 或兼容 OpenAI 的 `chat.completions.create` 接口调用（需设置 `tool_choice="auto"` 并传入 `tools` 列表），支持 Cherry Studio/Cursor 等 IDE 一键集成。

如遇 `11200058` 错误，请立即检查 `type` 与实际服务端点路径是否匹配（如 `streamableHttp` → `POST /mcp`）；如需访问内网服务，请选择 AI 网关导入方式并配置 VPC 连接。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [llm application](../guides/llm-application.md)
- [application component api reference](../api/application-component-api-reference.md)


