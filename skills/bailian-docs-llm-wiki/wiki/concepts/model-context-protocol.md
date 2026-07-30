# 模型上下文协议（MCP）

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化工具集成协议，用于在大语言模型与外部服务之间建立安全、可扩展、语义一致的交互通道。它将各类工具（如地图、搜索、图表生成、数据库查询等）抽象为统一的“能力单元”，使模型能基于自然语言意图自主规划、调用并消费结果，无需硬编码适配逻辑。

## 在百炼平台的不同场景中，这个概念如何使用

MCP 是百炼平台统一的工具接入范式，**已全面替代旧版“插件”概念**，适用于以下核心场景：

- **智能体应用（Agent 2.0）**：  
  MCP 服务作为可调度工具直接纳入模型的自主决策链。模型根据用户输入自动判断是否调用、调用哪个工具、传入哪些参数（如发送“查北京明天天气”触发 `maps_weather`）。最多可同时配置 5 个 MCP 服务，支持动态、非固定顺序调用，并完整展示思考链与执行过程。

- **工作流应用（Workflow）**：  
  MCP 以独立节点形式存在，每个节点绑定一个具体工具（如 `websearch_query`），需显式配置输入参数来源（如引用上游节点输出的关键词）。适用于确定性、强编排的任务流，不依赖模型自主决策。

- **自定义 Skill 与高代码应用**：  
  自定义 Skill 可通过 MCP 封装后复用；高代码应用（Python Serverless/K8s）可通过 MCP SDK（如 `streamablehttp_client`）编程调用已开通的 MCP 服务，实现细粒度控制。

> ⚠️ 注意：MCP **不支持直接在千问基础 API（如 `qwen-max` 同步调用接口）中使用**，也不支持 Assistant API（已下线）。必须通过智能体或工作流应用容器承载。

## 关键参数和配置

| 参数 | 说明 | 开发提示 |
|------|------|----------|
| `tool_name` | 模型在 function calling 中实际引用的工具名（非服务名），必须与 MCP 服务端注册的名称严格一致 | 示例：`"maps_weather"`；命名需小写+下划线，避免空格或特殊字符 |
| `inputSchema` | JSON Schema 格式定义输入参数结构，直接影响模型参数生成准确性 | 必须严格匹配下游服务要求；缺失必填字段或类型错误将返回 `11200060` 错误；建议用 [JSON Schema Validator](https://jsonschema.dev/) 验证 |
| `type` | 协议传输类型，决定端点路径与请求方式 | 当前仅支持 `"streamableHttp"`（推荐，POST `/mcp`），已弃用 `"sse"`；部署自定义服务时务必指定此值 |
| `env` | 环境变量配置，用于传递 API Key、[Token](token.md) 等敏感凭据 | **必须通过 KMS 凭据加密注入**，禁止明文写入配置；控制台开通时自动引导完成加密流程 |
| `service_name` | 服务管理标识，纯 UI 层命名，不影响调用逻辑 | 用于控制台区分多个同类服务（如 `"杭州地图服务"`、`"北京地图服务"`），可自由填写 |

## 面向开发者，简洁实用

- ✅ **快速上手三步走**：  
  1. 前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 开通官方服务（如 WebSearch）或导入自定义服务；  
  2. 在智能体/工作流编辑页 → 「MCP 区块」→ 添加服务 → 配置 `tool_name` 和 `inputSchema`；  
  3. 发送测试消息（如“上海外滩现在几点？”），观察模型是否自动调用并返回结构化结果。

- ✅ **调试要点**：  
  - 若模型未调用工具：检查 `inputSchema` 是否缺失 `required` 字段，或 `description` 是否未覆盖用户常用表达；  
  - 若调用失败：查看日志中的 `11200060` 错误码，验证 `inputSchema` 与下游服务实际接收格式是否一致；  
  - 若响应延迟：确认自定义 MCP 服务部署在函数计算 FC，且未因冷启动或超时（默认 30s）中断。

- ✅ **开发建议**：  
  - 官方服务开箱即用，优先选用；  
  - 自定义服务推荐使用 `npx mcp-server-node` 脚本快速启动（Node.js）或 `uvx mcp-server-python`（Python）；  
  - 外部 IDE 集成（如 Cherry Studio）支持一键同步 MCP 配置，适合本地开发联调。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [plug in](../guides/plug-in.md)
- [llm application](../guides/llm-application.md)
- [start using](../guides/start-using.md)
- [skill](../guides/skill.md)


