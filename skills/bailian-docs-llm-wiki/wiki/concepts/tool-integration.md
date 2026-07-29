# 工具集成

工具集成是百炼平台中将外部能力（如计算、搜索、文件处理、云服务等）以标准化方式接入智能体或工作流的核心机制，使大模型能够安全、可控地调用真实世界的服务，突破其固有的知识时效性、计算精度与执行边界限制。

## 在百炼平台的不同场景中，这个概念如何使用

工具集成不是单一技术方案，而是覆盖多层抽象、适配多种开发范式的统一能力体系，具体体现为以下三类主流形态，开发者可根据需求选择：

- **插件（Plug-in）**：面向轻量、通用能力的即插即用集成。适用于实时搜索（`quark_search`）、代码执行（`code_interpreter`）、文生图（`text_to_image`）等高频场景。模型可自主规划调用，也可在工作流中作为显式节点编排。所有插件需通过服务关联角色授权，且仅限同一子业务空间内使用。

- **Skill**：面向结构化任务处理的能力封装，强调语义驱动与零代码集成。适用于文件解析（`pdf-parser`）、数据清洗（`csv-cleaner`）等输入/输出明确的业务逻辑。通过 `SKILL.md` 中的 `description` 字段定义触发条件与能力边界，由智能体运行时自动匹配调用，无需修改提示词或流程图。

- **MCP 服务（Model Context Protocol）**：面向高扩展性、协议标准化的工具生态集成。支持官方服务（如 `Amap Maps`、`WebSearch`）和自定义部署（`npx`/`uvx` 脚本、AI 网关封装、OpenAPI 导入）。MCP 屏蔽通信细节，提供统一的工具发现（`list_tools`）与调用（`call_tool`）接口，适用于需要跨平台复用或深度定制工具链的场景。

> ⚠️ 注意：三者**不可混用**于同一调用上下文——插件与 Skill 仅支持在百炼托管智能体/工作流中使用；MCP 服务**不支持直连 `dashscope` SDK 的纯 API 调用**；而应用组件 API（如知识库、数据连接）本身属于平台基础设施，不归类为“工具”，但可被上述三类工具在运行时调用（例如 Skill 内部读取知识库检索结果）。

## 关键参数和配置

工具集成的配置围绕“标识”、“描述”、“权限”与“运行约束”四个维度展开，不同形态侧重点不同：

| 形态 | 核心标识参数 | 必填描述字段 | 权限前提 | 典型运行约束 |
|------|----------------|----------------|------------|----------------|
| **插件** | `tool_id`（如 `"calculator"`） | 无（官方插件内置描述）；自定义插件需符合 OpenAPI 规范 | `AliyunServiceRoleForSFMAccessCloudAPI` 服务关联角色 | 输入字段名严格（如 `payload__input__text`）；`code_interpreter` 禁网络/禁文件上传；依赖库白名单（`pandas`, `matplotlib` 等） |
| **Skill** | `name`（小写字母+数字+连字符，全局唯一） | `description`（必须含输入类型、支持操作、触发关键词、明确排除场景） | 无额外 IAM 权限（依赖智能体所在空间权限） | ZIP 包 ≤10 MB；`description` 质量决定调用准确率；加密 PDF 等边界场景需显式排除 |
| **MCP 服务** | `service name`（控制台识别用）、`mcpServers` 中的 key（如 `"memory"`） | `description`（控制台展示用，不影响调用逻辑） | 无独立角色，但自定义服务若访问云资源（如 RDS），需为函数计算配置 VPC 或出口 IP 白名单 | 部署模式影响计费与延迟（基础模式冷启动，极速模式常驻）；必须符合 Streamable HTTP 协议（`POST /mcp`）；不支持本地资源访问 |

> ✅ 统一要求：所有工具集成均需在**同一业务空间（Workspace）内完成注册与绑定**；跨空间调用必须先完成显式授权（插件）或服务共享配置（MCP/Skill）。

## 面向开发者，简洁实用

- **选型建议**：
  - 快速验证通用能力 → 用**插件**（控制台一键添加，API 直接传 `tools` 数组）；
  - 封装自有业务逻辑（如发票识别、合同比对）→ 用**Skill**（写好 `SKILL.md` + ZIP 上传，语义触发）；
  - 构建可复用、可跨平台（Cherry Studio/Cursor）的工具生态 → 用**MCP**（优先 `npx` 部署开源 Server，或 AI 网关封装现有 API）。

- **调试要点**：
  - 插件/Skill/MCP 均支持在智能体「对话测试窗格」中输入典型语句验证触发效果；
  - 查看调用日志：插件 → 控制台「插件市场 > 调用记录」；Skill → 「Skill 管理 > 调用统计」；MCP → 「MCP 市场 > 服务监控」；
  - 常见失败原因：权限缺失（检查服务关联角色）、输入格式错误（对照文档字段名）、环境限制（如 `code_interpreter` 无网络）、描述模糊（Skill 误触发/不触发）。

- **生产就绪检查清单**：
  - [ ] 所有工具已通过安全扫描（Skill/MCP 上传后状态为 `active`，插件已授权）；
  - [ ] `description` 字段已明确排除不支持的输入类型与边缘场景；
  - [ ] 自定义工具（插件/Skill/MCP）已通过最小可行用例验证（如传空输入、超长文本、特殊字符）；
  - [ ] 计费项已确认（如 `text_to_image` 限时免费，`WebSearch` 2000 次/月配额）；
  - [ ] 生产环境使用固定版本（Skill/MCP 指定 `version`，避免 `latest`；插件 ID 不变更）。

## 关联主题页

- [plug in](../guides/plug-in.md)
- [skill](../guides/skill.md)
- [managed agents api](../api/managed-agents-api.md)
- [model context protocol](../guides/model-context-protocol.md)
- [application component api reference](../api/application-component-api-reference.md)


