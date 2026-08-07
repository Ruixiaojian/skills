# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的实时数据访问入口。它支持结构化与非结构化数据接入，并通过平台托管或流处理两类模式实现数据就位（data-at-rest）或数据就绪（data-in-motion）的灵活集成。所有连接器均需在业务空间内创建并授权后方可被智能体或API调用。

## 支持的模型/功能

数据连接器按数据访问范式分为两类：

- **平台托管型**：适用于文件（PDF/Word/Markdown等）、表格（CSV/Excel等）类非结构化与轻量结构化数据。数据可存储于百炼平台免费空间（上限 200,000 文件 / 1 TB），或用户自有 OSS Bucket（需添加 `bailian-connector-access` 标签）[原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。  
- **流处理型**：支持 MySQL、PostgreSQL、PolarDB-X 2.0、语雀、OSS 等实时数据源。其中数据库类连接器（MySQL/PostgreSQL/PolarDB-X 2.0）仅当通过 **DMS 导入数据源**方式创建时才支持执行 SQL 查询；自定义方式创建的连接器仅支持向量检索，不支持直接 SQL 执行 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。  
- **解析能力差异**：文件连接器支持多种解析策略（电子文档解析、文档智能解析、大模型文档解析、Qwen VL 解析、音视频解析），不同策略对图表、插图、语音/视频内容的支持程度不同，详见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **通用** | 连接器名称、描述 | 名称需唯一且易识别；描述用于指导模型理解数据用途，影响检索准确率 |
| **文件/表格** | 存储位置（平台存储 / 自有 OSS） | 平台存储限时免费；OSS 需完成 RAM 授权并打标（`bailian-connector-access: ReadAndWrite`） |
| **MySQL/PostgreSQL/PolarDB-X** | 数据库地址、端口、用户名、密码、dbName（PostgreSQL 必填） | MySQL 默认端口 3306，PostgreSQL 默认 5432；PolarDB-X 仅支持私网连接且必须选择所属地域 |
| **语雀** | Tenant access token | 仅支持公网语雀；[Token](../concepts/token.md) 需通过 [语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取 |
| **OSS** | Bucket 选择、`bailian-datahub-access` 标签 | Bucket 必须开通向量检索服务，且不支持归档/冷归档存储类型 |

> **注意**：PostgreSQL 连接器要求 `wal_level = logical`，而 MySQL 无此限制；但两者均要求 DMS 导入方式才支持 SQL 查询 —— 此处原始文档中“仅 DMS 方式支持执行 SQL”的表述一致，无矛盾 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

## 使用方式

1. **创建连接器**：进入 [数据连接控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list)，单击「创建连接器」，按类型填写配置；
2. **验证连通性**：
   - MySQL 使用 EventBridge 检测；
   - PostgreSQL 使用 DTS 检测；
   - 语雀、OSS、文件/表格连接器提供「连接检测」或「开始检测」按钮；
3. **导入数据**：
   - 文件连接器：在详情页按类目导入，支持标签配置（用于 API 调用时过滤）；
   - 表格连接器：新建或选择数据表，上传 Excel 或自定义表头（结构一旦确定不可修改）；
4. **调用数据**：在智能体工作流或 API 请求中，通过 `searchFile`、`searchTable`、`executeSQL`（仅 DMS 创建的数据库连接器）等工具调用。

## 限制和注意事项

- **权限依赖**：RAM 用户需主账号授予 `AliyunBailianDataConnectorFullAccess` 或最小化自定义策略，否则无法创建/管理连接器；
- **网络限制**：
  - PolarDB-X 2.0 仅支持私网，不支持公网；
  - MySQL 公网连接需将百炼服务 IP 段加入数据库白名单；
  - 自建 PostgreSQL 需配置 `listen_addresses` 允许 `100.64.0.0/16` 网段访问；
- **存储与生命周期**：
  - 平台托管文件仅可查看最近 90 天导入记录，超期不可见但未删除；
  - OSS Bucket 若启用 Referer 防盗链，须将 `*.console.aliyun.com` 加入白名单；
- **功能边界**：
  - 不支持 JSON/YAML 直接导入表格连接器（需转为 XLSX/XLS）；
  - `image_url` 字段要求 URL 公开可访问，否则向量化失败；
  - 语雀连接器仅支持公网版本，不兼容企业私有部署语雀。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


