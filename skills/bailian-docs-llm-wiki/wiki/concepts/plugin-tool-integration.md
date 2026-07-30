# 插件与工具集成

插件与工具集成是百炼平台统一的外部能力接入机制，指将大模型无法原生完成的确定性任务（如实时搜索、代码执行、图像生成、API调用等）封装为标准化、可识别、可调度的工具单元，并通过声明式配置或编程接口注入智能体、工作流或托管运行时中，由模型自主规划或流程显式编排触发执行。

## 在百炼平台的不同场景中，这个概念如何使用

插件与工具集成并非单一技术实现，而是覆盖多层抽象、适配多种运行范式的统一能力扩展体系，具体按场景分为三类：

- **智能体（Agent）场景**：以“自主决策”为核心。大模型基于用户输入和系统提示词，自动识别任务意图、选择合适工具、构造参数并调用；结果返回后参与推理链闭环。适用于动态路径、模糊需求的对话式应用（如“帮我查北京今天天气并画成折线图”）。支持插件（Plugin）、MCP服务、Skill、内置沙箱工具四类能力，统一纳入ReAct规划循环（Agent 2.0），最大调用轮次可通过 `ReAct 最大轮次` 参数控制（1–50）。

- **工作流（Workflow）场景**：以“确定性编排”为核心。工具作为独立节点拖入画布，输入参数由前置节点（如大模型、变量提取器）显式传递，输出结果映射至后续节点变量。不依赖模型自主判断，适合固定流程、高可靠要求的自动化任务（如“先搜索竞品报告 → 再解析PDF → 最后生成摘要”）。支持插件节点、MCP节点、Skill节点及自定义HTTP节点。

- **托管智能体（Managed Agents）场景**：以“长时沙箱执行”为核心。工具在隔离的云端容器中运行，支持多步交互、文件读写、命令执行与依赖安装。除内置 `bash`/`read`/`write` 等7个工具外，还可挂载 Skill 或接入 MCP 服务，形成端到端的自主任务执行环境（如“下载网页 → 提取表格 → 用 pandas 清洗 → 保存为 CSV”）。需显式创建 `environment_id` 并绑定 `agent.id` 启动会话。

> ✅ 统一原则：所有工具均需**发布后才可被调用**（草稿状态不可用）；同一智能体应用最多添加 10 个插件，最多集成 5 个 MCP 服务；所有调用均受账号级权限（如 `AliyunServiceRoleForSFMAccessCloudAPI` 角色）和业务空间配额约束。

## 关键参数和配置

| 类别 | 参数 | 说明 | 必填 | 备注 |
|------|------|------|------|------|
| **通用标识** | `tool_id` / `name` | 工具唯一标识符（如 `calculator`, `text_to_image`, `amap_weather`），用于模型识别与API引用 | 是 | 官方插件/MCP/Skill 的 ID 由平台预置；自定义插件需开发者定义，仅支持小写字母、数字、连字符，≤64字符 |
| **调用协议** | `type` | 工具通信协议类型 | 是 | 常见值：`plugin`（传统插件）、`mcp`（Model Context Protocol）、`skill`（ZIP包能力）、`builtin`（沙箱内置工具） |
| **输入定义** | `parameters` | JSON Schema 格式，描述参数名、类型（String/Number/Object）、描述、是否必需 | 是（自定义工具） | Object 类型子属性必须显式声明；`description` 需精简准确，直接影响模型参数生成质量 |
| **输出定义** | `output_schema` / `response_format` | 指导模型解析返回结果的结构化描述 | 是（自定义工具） | 应尽量扁平，避免深层嵌套；MCP 服务默认返回标准 JSON，无需额外配置 |
| **鉴权配置** | `auth` | 认证方式与凭据 | 否（官方工具无需） | 支持 `Header`（`Authorization: Bearer xxx`）或 `Query`（`?appcode=xxx`）；[Token](token.md) 必须通过 KMS 加密，禁止明文 |
| **网络与部署** | `url` / `command` / `env` | 自定义工具的服务地址、启动命令或环境变量 | 是（自定义工具） | `url` 用于插件/MCP；`command` + `env` 用于脚本部署的 MCP；敏感信息（如 API Key）必须加密 |
| **高级控制** | `tool_choice`（API） | 调用策略：`auto`（模型自主决定）、`required`（强制调用）、`{"type": "function", "function": {"name": "xxx"}}`（指定工具） | 否 | Assistant API 中使用，影响调用确定性 |

## 面向开发者，简洁实用

- **快速起步**：优先选用官方插件（如 `calculator`, `quark_search`）或官方 MCP 服务（如 `websearch`, `amap_maps`），零配置即用；调试时直接在控制台对话面板测试。
- **自定义接入三步走**：
  1. **定义**：明确工具功能边界，编写精准 `parameters` 和 `output_schema`（参考官方插件 Schema）；
  2. **配置**：在控制台创建工具，填入 `url`/`command`、`auth`、`env`，点击“测试工具”验证连通性与返回格式；
  3. **集成**：添加至智能体/工作流，或在 Assistant API 的 `tools` 数组中传入完整定义，发布后生效。
- **避坑指南**：
  - 自定义插件不支持透传除 `Authorization` 外的任何 HTTP Header；
  - MCP 服务协议类型（`sse`/`streamableHttp`）必须与端点路径（`/sse`/`/mcp`）严格匹配，否则报错 `11200058`；
  - Skill 的 `description` 是触发关键，务必覆盖用户口语化表达（如“那个Excel”、“把PDF转成表格”），而非仅写技术术语；
  - 所有工具返回内容计入模型输入 [Token](token.md)，复杂响应需评估 [Token](token.md) 开销。
- **调试建议**：启用 `stream=True` 查看工具调用中间过程；使用控制台右侧“卡片流”模式观察 Agent 规划步骤；对失败调用，复制 `RequestId` 提交工单并附带 `tools` 配置快照。

## 关联主题页

- [plug in](../guides/plug-in.md)
- [skill](../guides/skill.md)
- [model context protocol](../guides/model-context-protocol.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)
- [application support](../guides/application-support.md)


