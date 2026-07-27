# data connection overview

[数据连接](../concepts/data-connection.md)是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的数据接入通道。它支持结构化与非结构化数据的接入，并通过平台托管或流处理两种模式实现数据访问，是构建知识增强型智能体（Agent）和 RAG 应用的基础依赖。所有连接器均需在业务空间内创建并绑定至具体应用才能生效。

## 支持的模型/功能

[数据连接](../concepts/data-connection.md)器按数据访问模式分为两类：

- **平台托管类**：适用于文件（PDF/Word/Markdown 等）、表格（CSV/Excel 等）数据，数据被导入百炼平台或自有 OSS 存储后进行向量化索引，支持语义检索（`searchFile`、`searchTable` 等工具）。详见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中“连接器类型”表格。
- **流处理类**：适用于 MySQL、PostgreSQL、PolarDB-X 2.0、语雀、OSS 等实时数据源，数据保留在原系统，应用通过 SQL 查询或 API 调用按需拉取，支持 `executeSQL`（仅 DMS 导入方式）、`searchOSSFile` 等动态工具。该能力依赖底层服务集成，具体支持范围请参考 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 的“前置条件”章节。

> **注意**：MySQL、PostgreSQL 和 PolarDB-X 2.0 连接器中，“执行 SQL 查询”功能**仅限通过 DMS 导入数据源方式创建的连接器**；自定义数据源方式创建的连接器不支持 `executeSQL` 工具调用。该限制在 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 多处明确强调，开发者须严格遵循。

## 关键参数

| 参数 | 说明 | 必填性 | 备注 |
|------|------|--------|------|
| `connectorName` | 连接器唯一标识名称，建议语义化命名（如 `hr-policy-pdf`） | 是 | 控制台创建时必填，API 创建时亦为必需字段 |
| `description` | 描述数据内容与用途，直接影响智能体对连接器的调用准确性 | 是 | 建议包含数据范围、更新频率、关键字段说明等信息 |
| `storageType` | 平台托管类连接器特有：`platform`（百炼内置存储）或 `oss`（自有 Bucket） | 是（平台托管类） | OSS 存储需提前添加 `bailian-connector-access` 标签（值 `ReadAndWrite`） |
| `dataSourceType` | 流处理类连接器特有：`rds` / `self-built` / `dms` 等 | 是（流处理类） | PolarDB-X 2.0 仅支持 `rds`（阿里云实例），不支持自建 |
| `networkType` | 流处理类网络策略：`public` / `private` | 是（流处理类） | PolarDB-X 2.0 **仅支持 `private`**；MySQL/PostgreSQL 公网需配置白名单 IP 段 `100.64.0.0/16` |

## 使用方式

1. **控制台创建**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击“创建连接器” → 选择类型 → 填写基本信息与连接参数 → 完成授权与连通性检测 → 点击确认。  
2. **API 创建**：调用 `CreateConnector` 接口（需 RAM 权限 `bailian:CreateConnector`），请求体需按连接器类型携带对应 schema 字段（如 `mysqlConfig` 或 `ossConfig`）。完整参数定义见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) “创建连接器”各小节。  
3. **绑定应用**：创建成功后，在应用编辑页的「知识库」或「工具」模块中显式启用该连接器，方可被智能体调用。  
4. **调用工具**：在 Agent 提示词或 Function Calling 配置中引用对应工具名（如 `searchFile`、`executeSQL`），参数需符合连接器类型约束（例如 `executeSQL` 仅对 DMS 方式创建的 MySQL/PostgreSQL/PolarDB-X 连接器有效）。

## 限制和注意事项

- **容量与时效**：平台托管文件连接器中，导入文件仅保留最近 **90 天** 的查看权限（后台存储仍存在）；表格连接器无此限制，但列结构一旦创建**不可修改**（见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) “导入表格”章节）。
- **OSS 特殊要求**：使用 OSS 连接器前，目标 Bucket **必须开通向量检索服务**，否则 `searchOSSFile` 等工具将不可用；且不支持归档/冷归档/深度冷归档存储类型。
- **权限与网络**：所有流处理类连接器均依赖 SLR（服务关联角色）授权，首次创建时需完成 DTS、DMS、RDS 等多角色授权；MySQL/PostgreSQL 公网访问需将百炼服务 IP 段 `100.64.0.0/16` 加入数据库白名单。
- **解析能力边界**：文件连接器的“电子文档解析”**不支持插图与图表识别**；若需理解图像内容，必须选用“大模型文档解析”或“Qwen VL 解析”，且需应用已配置支持视觉理解的模型（如 Qwen-VL）。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


