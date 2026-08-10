# 工具集成

工具集成是百炼平台中将外部能力（如搜索、计算、文件处理、API 服务等）以标准化、可编排、可调度的方式接入大模型应用的核心机制。它不依赖模型自身能力，而是通过统一协议与运行时协调，让智能体或工作流能安全、可靠地调用外部工具，从而扩展时效性、精确性、[多模态](multi-modal.md)和业务专属能力。

## 在百炼平台的不同场景中，这个概念如何使用

工具集成在百炼中并非单一技术，而是覆盖三类互补能力的统一抽象，适用于不同控制粒度与开发需求：

- **MCP（Model Context Protocol）服务**：面向需要**语义驱动、自主决策调用**的场景。适用于智能体（Agent）中模型根据对话上下文自动判断是否调用、何时调用、调用哪个工具（如“查杭州天气”→ 自动触发 `maps_weather`）。也支持在工作流中作为显式节点，但需手动指定工具名与参数映射。MCP 是当前推荐的标准化工具接入协议，基于 Streamable HTTP，兼容性强、扩展性好。

- **插件（Plug-in）**：面向**开箱即用、快速验证**的通用能力。官方插件（如 `code_interpreter`、`quark_search`）无需配置即可添加到智能体或工作流；自定义插件则需定义工具 URL、输入/输出 Schema 和鉴权方式，适合已有 RESTful API 的轻量封装。插件调用由模型自主触发，但必须完成空间级授权且受工具数量上限（10 个/智能体）约束。

- **Skill（技能包）**：面向**无代码、语义触发的文件/结构化数据处理**场景。不涉及网络调用或外部 API，而是将预置或自定义的 ZIP 包（含 `SKILL.md` 描述）挂载为能力模块。智能体通过理解 `description` 中的自然语言语义（如“清洗 Excel 表格”）自动匹配并执行，适用于 PDF 解析、CSV 清洗等确定性任务。

> ✅ 共同原则：  
> - 所有工具集成均需通过**服务关联角色**（如 `AliyunServiceRoleForSFMAccessCloudAPI`）授权，否则调用失败；  
> - 均支持在**智能体应用**（自动推理）与**工作流应用**（显式编排）中复用；  
> - 均可通过 **Managed Agents API** 统一管理（Agent 配置中声明 `tools` 或 `skills` 列表）；  
> - 不绑定具体模型，但实际可用性取决于所选模型对工具协议的支持（如 `qwen-plus` 支持 MCP 与插件，`qwen-vl-max` 支持插件与 Skill）。

## 关键参数和配置

| 类型 | 参数名 | 必填 | 说明 | 示例值 |
|------|--------|------|------|--------|
| **通用** | `tool_id` / `skill_id` / `mcp_service_id` | 是 | 工具唯一标识，在控制台或 API 中获取，用于引用与编排 | `"websearch"`, `"xlsx"`, `"WebSearch"` |
| **MCP** | `type` | 是 | 协议类型，决定通信方式 | `"streamableHttp"`（生产首选），`"sse"`（仅兼容） |
| | `url` | 是（远程） | MCP 服务端点，必须与 `type` 匹配 | `"https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp"` |
| | `deploymentMode` | 否 | 部署模式，影响计费与响应延迟 | `"ultra"`（常驻）、`"basic"`（按次） |
| **插件** | `input.parameters` | 是（自定义） | OpenAPI 风格参数定义，`description` 字段直接影响模型提取准确率 | `{ "city": { "type": "string", "description": "城市名称，如'北京'" } }` |
| | `auth.type` | 是（自定义） | 鉴权方式 | `"bearer"`, `"appcode"` |
| | `auth.token` | 是（自定义） | 服务级 [Token](token.md) | `"your-api-key"` |
| **Skill** | `name` & `description`（in `SKILL.md`） | 是 | ZIP 包内必填元信息，`description` 必须清晰、无歧义、覆盖典型触发词与排除边界 | `name: "invoice-parser"`<br>`description: "解析PDF格式的增值税专用发票，提取发票代码、号码、金额、开票日期；不支持扫描件或手写票据。"` |
| **API 统一** | `agent.tools` / `agent.skills` | 是（Managed Agents API） | Agent 创建时声明的工具列表，JSON 数组格式 | `[{"tool_id": "websearch", "type": "mcp"}, {"skill_id": "pdf", "version": "1.0"}]` |

⚠️ 注意：  
- MCP 远程服务 URL 必须以 `/mcp` 结尾（Streamable HTTP）或 `/sse` 结尾（SSE），否则返回错误码 `11200058`；  
- 插件 `Object` 类型参数的子属性**不可为空**，需显式定义；  
- Skill ZIP 包大小 ≤10 MB，且 `SKILL.md` 必须位于根目录；  
- 所有工具在**子业务空间**中使用前，必须单独完成空间级授权。

## 面向开发者，简洁实用

- ✅ **优先选 MCP**：新项目统一使用 MCP 协议（Streamable HTTP），兼容性好、社区标准、易于调试（支持本地 `npx` 启动）；  
- ✅ **快速验证用插件**：直接启用 `code_interpreter` 或 `quark_search` 测试工具链通路，再逐步替换为自定义 MCP；  
- ✅ **文件处理用 Skill**：无需写代码、不暴露 API、纯语义触发，适合内部文档/报表处理场景；  
- ✅ **生产部署检查清单**：  
  ① 授权服务关联角色；  
  ② 控制台确认工具状态为「已发布」且「调试成功」；  
  ③ 智能体中检查工具是否已添加（非仅开通）；  
  ④ 工作流中确认 MCP 节点已指定 `tool_name`，插件节点已绑定 `tool_id`；  
  ⑤ Managed Agents API 调用时，`agent.tools` 列表与 `session.agent` 版本严格匹配。  

工具集成不是“连上就行”，而是**语义可理解、配置可审计、调用可追溯、失败可定位**的能力交付闭环。从定义到上线，始终围绕“模型能否正确识别意图”和“运行时能否稳定交付结果”两个核心验证。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [plug in](../guides/plug-in.md)
- [skill](../guides/skill.md)
- [managed agents api](../api/managed-agents-api.md)
- [application component api reference](../api/application-component-api-reference.md)


