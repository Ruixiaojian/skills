# 智能体工具集成

智能体工具集成是指在百炼平台中，将外部能力（如计算、搜索、文件处理、API 服务等）以标准化方式接入智能体运行时，使其能在对话过程中自主识别任务意图、规划调用步骤、执行工具并整合结果，从而突破大模型原生能力边界的核心机制。该机制不修改模型本身，而是通过协议抽象、语义描述与运行时沙箱协同实现“模型即调度器”。

## 在百炼平台的不同场景中，这个概念如何使用

智能体工具集成在百炼平台中并非单一技术方案，而是由三类互补能力共同构成的分层集成体系，适用于不同开发阶段与控制粒度需求：

- **插件（Plug-in）**：面向快速能力复用，适用于通用高频场景（如计算器、文生图、实时搜索）。开发者无需编码，只需在智能体配置中勾选启用；模型基于用户输入自动触发调用，参数由大模型从对话中抽取或由业务系统透传。适合零/低代码构建响应式智能体。

- **Skill（技能）**：面向结构化任务自动化，聚焦文件与数据处理（如解析 PDF 表格、清洗 Excel 数据）。通过 ZIP 包封装逻辑与 `SKILL.md` 语义描述，由平台统一托管执行。智能体依据 `description` 的精确性匹配调用时机，支持开箱即用（官方 Skill）或业务定制（自定义 Skill），强调“输入-输出”行为可预期。

- **MCP（Model Context Protocol）**：面向专业集成与协议标准化，适用于需强类型约束、多工具编排或跨平台互通的场景（如高德地图路线规划、OSS 文件操作）。通过 JSON Schema 定义工具接口，支持 `streamableHttp` 等标准协议，既可用于智能体内自动调度，也可被工作流显式编排或导出至第三方 IDE。是连接百炼智能体与企业级后端服务的推荐桥梁。

> ✅ 共同前提：所有工具集成均需绑定至智能体应用（Agent 2.0），并在创建 Session 时通过 `Environment` 加载对应执行上下文（如云沙箱、预装依赖）。工具调用过程受 `react_max_steps`（默认 10）限制，超步则终止并生成最终回复。

## 关键参数和配置

| 类别 | 参数/字段 | 说明 | 必填 | 示例 |
|--------|------------|------|------|------|
| **通用控制** | `react_max_steps` | 智能体单次会话中允许的最大工具调用轮次（含规划、执行、反思） | 是（Agent 2.0） | `15` |
| | `file_processing_mode` | 决定上传文件如何参与工具链：`custom` 模式下模型可自主决策调用 Skill/MCP 处理文件 | 是（含文件场景） | `"custom"` |
| **插件** | `tool_id` | 工具唯一标识符，用于 API 声明与日志追踪 | 是（调用时） | `"calculator"` |
| | `biz_params` | 业务系统透传的结构化参数（非模型抽取），用于绕过语义理解直接驱动工具 | 否 | `{"precision": 4}` |
| **Skill** | `name`（ZIP 中 `SKILL.md`） | Skill 全局唯一标识，仅支持小写字母、数字、连字符 | 是 | `"pdf-table-extractor"` |
| | `description`（ZIP 中 `SKILL.md`） | **核心字段**：决定模型是否准确触发。需明确输入格式、支持操作、触发词及排除场景 | 是 | `"从 PDF 文件中提取表格数据为 CSV 格式；不处理扫描件或图片内嵌文字"` |
| **MCP** | `tool.name` | MCP 服务返回的工具名，模型调用时必须严格匹配 | 是（调用时） | `"maps_weather"` |
| | `inputSchema` | JSON Schema 描述工具入参结构，模型据此生成合法参数对象 | 是（自定义 MCP） | `{"type":"object","properties":{"city":{"type":"string"}}}` |
| | `mcpServers`（环境配置） | 环境中声明的 MCP 服务端点映射，格式为 `{ "service_name": { "type": "...", "url": "..." } }` | 是（启用 MCP） | `{"weather": {"type": "streamableHttp", "url": "https://xxx/mcp"}}` |

## 面向开发者，简洁实用

- **优先选型建议**：  
  - 要快 → 用 **插件**（开通即用，控制台一键添加）；  
  - 要稳 → 用 **Skill**（行为确定、版本可控、文件处理首选）；  
  - 要控 → 用 **MCP**（强 Schema、可审计、支持 VPC/凭据管理、适配工作流与外部 IDE）。

- **调试黄金法则**：  
  - 所有工具首次集成后，**必须在控制台对话面板中发送典型指令测试**（如“把附件 sales.xlsx 按部门汇总”，而非“算一下”）；  
  - 若未触发，优先检查 `description` 是否模糊、`name` 是否拼写错误、`file_processing_mode` 是否设为 `custom`；  
  - 查看 Session 事件流（SSE）中的 `tool_call` 和 `tool_result` 事件，确认工具 ID、参数、返回状态是否符合预期。

- **避坑提醒**：  
  - 删除插件/Skill/MCP 服务将导致已发布智能体**立即失效且不可恢复**，请先灰度验证再全量替换；  
  - 自定义 Skill ZIP 包中 `SKILL.md` 必须位于根目录，且 `name` 全局唯一——重复上传同名包会创建新版本，旧版本仍被历史 Session 引用；  
  - MCP 服务若需访问阿里云资源（如 OSS、RDS），必须配置函数计算 FC 的 VPC 或 IP 白名单，**不能直连本地网络**。

## 关联主题页

- [managed agents api](../api/managed-agents-api.md)
- [plug in](../guides/plug-in.md)
- [skill](../guides/skill.md)
- [model context protocol](../guides/model-context-protocol.md)
- [llm application](../guides/llm-application.md)


