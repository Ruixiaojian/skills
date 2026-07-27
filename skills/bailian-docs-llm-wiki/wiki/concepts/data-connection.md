# 数据连接

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为智能体（Agent）、工作流（Workflow）和高代码应用提供安全、可控、按需访问结构化与非结构化数据的标准化通道。它不是简单的数据库配置，而是融合了身份鉴权、网络策略、解析引擎与工具协议的端到端数据接入抽象层。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent 2.0）场景**：数据连接作为可调度工具（Tool）被显式启用。例如，绑定一个 `hr-policy-pdf` 文件连接器后，Agent 可自动调用 `searchFile` 工具进行语义检索；绑定 DMS 导入的 MySQL 连接器后，可调用 `executeSQL` 执行动态查询。工具调用行为由模型自主规划，无需硬编码 SQL 或路径。
  
- **工作流（Workflow）场景**：在「工具」节点中选择已创建的数据连接器，配置输入参数（如 `query` 或 `file_name`），将结果以变量形式（如 `${connector_result}`）传递给下游节点，实现确定性数据驱动流程。

- **高代码应用（Rich Code）场景**：通过 SDK 调用 `bailian.ApplicationComponent.AddConnector` 等 API 动态创建/管理连接器，并在 Python 逻辑中直接引用其 ID，结合 `bailian.ApplicationComponent.Retrieve` 或自定义 MCP 客户端完成数据拉取与处理。

- **知识库（RAG）构建场景**：文件类数据连接器（PDF/Excel/OSS）是知识库数据源的主要入口。上传文件 → 触发向量化索引 → 构建可检索知识库，整个链路由连接器生命周期驱动，而非独立知识库导入操作。

> ⚠️ 注意：所有数据连接器必须在**业务空间内创建**，并**显式绑定至具体应用**（在应用编辑页的「知识库」或「工具」模块中启用），否则无法被任何组件调用。

## 关键参数和配置

| 参数 | 类型 | 说明 | 必填性 | 开发提示 |
|------|------|------|--------|----------|
| `connectorName` | string | 连接器唯一标识，建议含业务语义（如 `finance-2024-q1-report`） | 是 | 控制台与 API 均强制校验唯一性；命名将出现在工具名中（如 `searchFile_finance-2024-q1-report`） |
| `description` | string | 描述数据内容、更新频率、关键字段等，直接影响 Agent 工具选择准确性 | 是 | 建议包含“数据范围：2024年Q1销售报表；更新频率：每日凌晨同步；主键：order_id”等信息 |
| `storageType`（平台托管类） | `platform` \| `oss` | 指定文件存储位置 | 是（平台托管类） | 选 `oss` 时，目标 Bucket 必须已添加标签 `bailian-connector-access: ReadAndWrite` 且开通向量检索服务 |
| `dataSourceType`（流处理类） | `rds` \| `dms` \| `self-built` | 数据源部署形态 | 是（流处理类） | PolarDB-X 2.0 仅支持 `rds`；MySQL/PostgreSQL 的 `executeSQL` 工具**仅对 `dms` 类型有效** |
| `networkType`（流处理类） | `public` \| `private` | 网络访问策略 | 是（流处理类） | 公网访问需将百炼服务 IP 段 `100.64.0.0/16` 加入数据库白名单；PolarDB-X 2.0 **强制 `private`** |
| `parser`（文件类 API） | string | 解析策略，如 `DOCMIND_LLM_VERSION`, `DASH_QWEN_VL_PARSER` | 否（API 默认 `AUTO_SELECT`） | 需图像理解时，必须显式指定 `DASH_QWEN_VL_PARSER` 并确保应用已配置 VL 模型 |

## 面向开发者的关键实践

- **创建优先级**：优先使用控制台创建并验证连通性，再通过 API 批量管理；API 创建需严格匹配 schema（如 `mysqlConfig` 含 `host/port/username/password/database`，`ossConfig` 含 `bucket/region/prefix`）。
- **权限最小化**：RAM 策略应限定 `bailian:CreateConnector`、`bailian:GetConnector` 等细粒度动作，并绑定 `WorkspaceId` 资源 ARN。
- **工具调用约束**：
  - `executeSQL` 仅对 DMS 方式创建的 MySQL/PostgreSQL/PolarDB-X 连接器生效；
  - `searchOSSFile` 要求 OSS Bucket 已开通向量检索，且不支持归档存储类型；
  - 文件连接器导入的文档，90 天后控制台不可查看（后台仍存），但不影响 API 检索。
- **调试技巧**：在 Agent 调试页开启 `enable_thinking`，观察模型是否准确识别 `description` 并选择对应工具；若工具未出现，检查是否已绑定应用、`description` 是否缺失关键语义词（如“员工手册”“销售报表”）。

## 关联主题页

- [data connection overview](../guides/data-connection-overview.md)
- [application component api reference](../api/application-component-api-reference.md)
- [llm application](../guides/llm-application.md)
- [knowledge base](../guides/knowledge-base.md)
- [use cases](../guides/use-cases.md)


