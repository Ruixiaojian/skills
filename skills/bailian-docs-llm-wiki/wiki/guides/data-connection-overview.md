# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的数据接入通道。它支持结构化与非结构化数据的导入与实时访问，并通过向量化与检索机制赋能智能体在对话中引用真实业务数据。所有连接器均需显式授权与合规配置，不自动同步或持久化原始数据源变更。

## 支持的模型/功能

数据连接器按数据访问模式分为两类：

- **平台托管型**：适用于静态文件与表格数据，支持上传至百炼平台存储（限时免费）或自有 OSS Bucket。  
  - `文件`：支持 PDF、Word、Markdown 等非结构化文档，依赖[文档理解](https://help.aliyun.com/zh/document-mind/product-overview/overview-of-document-understanding#9a4f5fb91fpps)能力进行切分与向量化；解析方式包括电子文档解析、文档智能解析、大模型文档解析及 Qwen VL 解析（仅图片）[原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。  
  - `表格`：支持 CSV、Excel（XLS/XLSX），支持自定义表头与字段类型（如 `image_url`），但结构一旦创建不可修改 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

- **流处理型**：适用于实时数据库与在线知识库，数据保留在原系统，查询时按需拉取。  
  - `MySQL` / `PostgreSQL` / `PolarDB-X 2.0`：仅通过 **DMS 导入数据源** 方式创建的连接器支持执行 SQL 查询；自定义方式仅支持元数据发现，不支持直接 SQL 执行 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。  
  - `语雀`：仅支持公网版语雀，需提供 Tenant access token，不支持私有部署语雀实例。  
  - `OSS`：支持读取 Bucket 中文件，但需开通向量检索服务方可使用 `searchOSSFile` 和 `searchOSSFileByFileName` 工具。

> **注意**：MySQL 与 PostgreSQL 连接器均要求高权限账号（如 Superuser 或 REPLICATION 权限），且 PostgreSQL 必须将 `wal_level` 设置为 `logical`；而 MySQL 无此强制要求 —— 此差异在原始文档中明确列出，但未说明是否影响 DMS 导入路径下的功能一致性，建议以实际连通性检测结果为准。

## 关键参数

| 连接器类型 | 必填参数 | 特殊约束 |
|------------|----------|----------|
| 文件 / 表格 | 连接器名称、描述、存储位置（平台存储 or OSS） | OSS Bucket 需添加 `bailian-connector-access` 标签（值 `ReadAndWrite`） |
| MySQL | 数据库用户名、密码、网络类型（公网/私网）、数据库实例（RDS）或地址（自建） | 公网需白名单 `100.64.0.0/16`；私网需指定地域；仅 DMS 导入支持 SQL 执行 |
| PostgreSQL | 主机地址、端口、dbName、用户名、密码 | `wal_level=logical`；自建实例需配置 `pg_hba.conf` 允许 `100.64.0.0/16` 访问 |
| PolarDB-X 2.0 | 用户名、密码、所属地域（仅私网） | 仅支持阿里云实例；首次使用需授权 `AliyunServiceRoleForSFMConnectorAccessDTS` 和 `AliyunServiceRoleForSFMAccessPolarDBX` 角色 |
| 语雀 | Tenant access token | 仅公网语雀；[Token](../concepts/token.md) 需具备知识库读取权限 |
| OSS | Bucket 名称 | Bucket 需添加 `bailian-datahub-access` 标签（值 `read`）；不支持归档/冷归档存储类型 |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击「创建连接器」→ 选择类型 → 填写基本信息与连接参数 → （可选）点击「开始检测」验证连通性 → 确认创建。  
2. **导入数据**（仅平台托管型）：  
   - 文件连接器：进入详情页 → 选择类目 → 「导入数据」→ 本地上传 → 选择解析方式 →（可选）配置标签 → 确认。  
   - 表格连接器：进入详情页 → 新建或选择数据表 → 上传 Excel 或自定义表头 → 确保列名/类型/数量严格一致 → 确认导入。  
3. **调用数据**：在智能体或 API 调用中，通过工具（如 `searchFile`、`searchTable`、`executeSQL`）指定连接器 ID 与查询条件；标签（`tags`）可用于前置过滤提升检索效率。

## 限制和注意事项

- **容量与时效**：平台托管文件最多 200,000 个 + 1 TB（限时免费）；导入文件仅保留最近 90 天的查看入口（副本仍可用）；类目上限 500 个，超限需提工单扩容。  
- **网络与权限**：  
  - MySQL/PostgreSQL 公网连接必须将百炼服务 IP 段（`100.64.0.0/16`）加入数据库白名单；  
  - PolarDB-X 2.0 仅支持私网，且必须与实例同地域；  
  - 所有 OSS 连接需完成 RAM 授权并打标，否则无法访问。  
- **功能边界**：  
  - `executeSQL` 工具仅对 DMS 导入方式创建的 MySQL/PostgreSQL/PolarDB-X 连接器生效；  
  - OSS 连接器若未开通向量检索服务，则 `searchOSSFile` 等工具不可用；  
  - 文件连接器不支持直接导入 JSON/CSV/YAML，需转为 XLSX/XLS 后再上传。  
- **安全合规**：所有连接器均不自动同步源数据变更；导入文件为独立副本，仅限当前业务空间使用；阿里云百炼不会将数据用于商业用途或对外公开。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


