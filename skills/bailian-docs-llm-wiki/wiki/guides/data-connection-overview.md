# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的数据接入入口。通过创建不同类型的数据连接器，开发者可将企业自有数据库、文档系统或对象存储中的数据实时接入百炼应用，在对话或智能体执行中按需检索与引用。该能力支持结构化与非结构化数据的混合接入，并兼顾平台托管与流式直连两种模式。

## 支持的模型/功能

数据连接器按数据访问模式分为两类：**平台托管型**（文件、表格）和**流处理型**（MySQL、PostgreSQL、PolarDB-X 2.0、语雀、OSS）。  
- **平台托管型**：数据导入百炼平台或自有OSS后，经向量化处理构建知识库，支持语义检索（如 `searchFile`、`searchTable` 工具），适用于静态或低频更新场景。  
- **流处理型**：数据保留在源端，运行时实时查询（如 MySQL 的 `executeSQL`），适用于高时效性需求；但注意，[原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 明确指出：**仅通过 DMS 导入方式创建的 MySQL/PostgreSQL/PolarDB-X 连接器才支持 SQL 执行**，自定义数据源方式创建的连接器不支持该能力。  
- 各连接器均支持与智能体（Agent 1.0）及 API 应用集成，调用时可通过 `tags` 参数实现基于标签的过滤检索。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **通用** | 连接器名称、描述 | 名称需唯一且可识别；描述用于指导模型理解数据用途，影响检索准确率，建议明确数据范围与业务含义。 |
| **文件/表格** | 存储位置（平台存储 / 自有OSS） | 平台存储提供免费额度（文件连接器限 200,000 文件 + 1 TB；表格连接器 1 TB 免费），超限转按量付费；自有OSS需添加 `bailian-connector-access` 标签（值 `ReadAndWrite`）[原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。 |
| **数据库类** | 网络类型、SLR 授权、wal_level（PostgreSQL）、dbName（PostgreSQL） | MySQL 默认端口 3306，PostgreSQL 必填 `dbName` 且需 `wal_level=logical`；PolarDB-X 2.0 **仅支持私网**，且首次使用需显式授权 `AliyunServiceRoleForSFMConnectorAccessDTS` 和 `AliyunServiceRoleForSFMAccessPolarDBX` 角色 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。 |
| **语雀/OSS** | Tenant access token（语雀）、Bucket 选择（OSS） | 语雀仅支持公网版本；OSS Bucket 需开通向量检索服务，且必须添加 `bailian-datahub-access` 标签（值 `read`），否则无法使用 `searchOSSFile` 等工具。 |

> **注意**：文档中关于 OSS Bucket 标签的键名存在不一致——文件/表格连接器要求 `bailian-connector-access`，而 OSS 连接器要求 `bailian-datahub-access`。请严格按对应连接器类型配置，否则授权失败。

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 控制台 → 单击“创建连接器” → 选择类型 → 填写基本信息与连接参数 → 完成 SLR 授权（如需）→ 测试连通性 → 确认创建。  
2. **导入数据（仅平台托管型）**：  
   - 文件连接器：在详情页选择类目 → “导入数据” → 本地上传 PDF/Word/Excel 等 → 选择解析方式（推荐“大模型文档解析”以支持图表理解）→ 配置标签（可选）→ 提交。  
   - 表格连接器：在详情页新建数据表 → 选择“直接上传Excel”或“自定义表头” → 上传 CSV/Excel → 注意列名、类型、描述需严格匹配，`image_url` 字段需为公开可访问 URL。  
3. **调用连接器**：在智能体工作流或 API 请求中，通过预置工具（如 `searchFile`、`executeSQL`）传入 `connectorId` 及查询参数；标签过滤需在请求 `tags` 字段中指定。

## 限制和注意事项

- **容量与时效**：平台托管文件仅保留最近 90 天导入记录（不可查看但未删除）；文件解析可能因高峰排队延迟数小时，偶发超时需重试。  
- **格式限制**：文件连接器**不支持直接导入 JSON/CSV/YAML**，需先转为 XLSX/XLS；表格连接器上传文件结构必须与定义的表结构完全一致，否则失败。  
- **权限与网络**：RAM 用户需主账号授予数据连接管理权限；数据库连接需确保白名单包含百炼服务 IP 段（如公网需加 `100.64.0.0/16`），私网连接需同地域且网络互通。  
- **OSS 特殊要求**：不支持归档/冷归档存储类型；若 Bucket 开启 Referer 防盗链，须将 `*.console.aliyun.com` 加入白名单。  
- **功能差异**：MySQL/PostgreSQL/PolarDB-X 的 SQL 执行能力**强依赖 DMS 导入方式**，自定义方式创建的连接器仅支持元数据同步，不可执行查询——此限制在 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中多次强调，开发时务必确认创建路径。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


