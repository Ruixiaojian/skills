# 模型上下文协议（MCP）

模型上下文协议（Model Context Protocol，简称 MCP）是阿里云百炼平台提供的标准化、生产就绪的工具接入协议，用于在大语言模型与外部能力（如地图、搜索、图表生成、代码执行等服务）之间建立安全、可扩展、声明式的信息交换通道。它基于开源 MCP 规范实现，并深度集成百炼智能体与工作流引擎，使开发者无需编写适配胶水代码，即可统一纳管官方服务、三方插件及自定义工具。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体应用（Agent 2.0）**：MCP 是智能体调用外部能力的**唯一标准协议**。开通 MCP 服务后，在应用配置中一键添加，模型将基于自然语言指令自动完成工具识别、参数抽取、多步规划与结果整合（ReAct 范式）。例如，用户问“北京今天天气如何？”，模型可自主调度 `Amap Maps` 的 `maps_weather` 工具并结构化呈现结果。旧版“插件”机制已全面迁移至 MCP，新建智能体不再支持原生插件配置。

- **工作流应用（Workflow）**：MCP 以显式节点形式嵌入流程编排。开发者拖入“MCP 节点”，手动选择已开通的服务及其具体工具（如 `web_search`），并绑定上游节点输出作为输入参数（如 `{"query": "{{input.query}}"}`）。适用于需强控制、确定性执行路径的业务场景。

- **外部系统集成**：通过百炼托管的 MCP Server（`https://dashscope.aliyuncs.com/api/v1/mcps/{service}/mcp`），支持第三方 MCP 客户端（如 Cherry Studio、Cursor）直接连接；也可在自有项目中使用 `mcp` SDK（如 `streamablehttp_client`）发起调用，兼容 OpenAI 工具调用接口风格，实现跨平台能力复用。

> ⚠️ 注意：MCP 服务**不可**通过直接调用千问 RESTful API（如 `qwen-max` 的 `/v1/chat/completions`）启用——必须部署于百炼智能体或工作流应用内，或通过上述外部 MCP 接口调用。

## 关键参数和配置

| 参数 | 说明 | 示例值 | 场景 |
|------|------|--------|------|
| `type` | 协议类型，决定通信方式与端点路径 | `"streamableHttp"`（推荐，对应 `/mcp`）<br>（SSE 已弃用） | 所有 MCP 配置 |
| `deploymentMode` | 计费与性能模式 | `"basic"`（按次计费）<br>`"ultra"`（极速响应，需额外开通） | 服务开通时选择 |
| `env` | 启动环境变量（仅自定义 MCP） | `{"AMAP_MAPS_API_KEY": "sk-xxx"}` | 自定义服务部署时配置密钥等凭证 |
| `command` / `args` | 本地启动命令（仅自定义 MCP） | `"npx"`, `["@modelcontextprotocol/server-memory"]` | 用于 `npx`/`uvx` 方式部署的轻量服务 |
| `tool_id`（外部调用） | 工具唯一标识符（非服务名） | `"maps_weather"` | API 调用时在 `tools` 列表中声明 |

> ✅ 提示：智能体中无需手动传参 `tool_id` 或 `args`——由模型自动推理；工作流和外部调用则需显式指定。

## 面向开发者，简洁实用

- **快速上手三步**：  
  1️⃣ 前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 开通服务（如 `WebSearch`）；  
  2️⃣ 智能体中进入「应用配置 → MCP 服务」添加；工作流中拖入「MCP 节点」并选工具；  
  3️⃣ 发布应用后，对话中自然触发（智能体）或按流程执行（工作流）。

- **调试建议**：  
  - 查看智能体调试面板的「思考链」卡片，确认工具是否被正确识别与调用；  
  - 工作流节点失败时，检查输入参数格式（如 JSON 字段名是否匹配工具文档）；  
  - 外部调用超时？确认 `streamableHttp` 端点 URL 正确，且请求头含有效鉴权 `Authorization`。

- **避坑指南**：  
  - 自定义 MCP 服务超时上限为 **5 秒**，耗时操作请异步化或拆分；  
  - MCP 托管于函数计算（FC），**无法访问本地文件或数据库**——需通过 VPC 或公网 API 对接云资源；  
  - `description` 字段质量直接影响智能体调用准确率：务必明确支持/不支持的输入类型、操作与关键词（参考 Skill 规范）。  

MCP 不是模型特性，而是百炼平台的能力中枢——统一协议，一次接入，处处可用。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [llm application](../guides/llm-application.md)
- [plug in](../guides/plug-in.md)
- [skill](../guides/skill.md)


