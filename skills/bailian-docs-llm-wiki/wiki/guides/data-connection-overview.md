# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的实时或批量数据接入通道。它支持结构化与非结构化数据源，涵盖文件、表格、关系型数据库、[知识库](../concepts/knowledge-base.md)及对象存储等多种类型，并通过平台托管或流处理两种模式实现数据访问。所有连接器均需在业务空间内创建并授权后方可被智能体或 API 调用。

## 支持的模型/功能

- **平台托管类连接器**：适用于离线导入与向量化检索场景  
  - `文件`：支持 PDF、Word、Markdown 等非结构化文档，依赖[文档理解](https://help.aliyun.com/zh/document-mind/product-overview/overview-of-document-understanding#9a4f5fb91fpps)能力进行多模态解析（含大模型文档解析、Qwen VL 解析等）[原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)  
  - `表格`：支持 CSV、Excel（XLS/XLSX），自动识别表头或支持自定义 Schema；字段类型支持 `image_url`（需公开可访问 URL）以启用以图搜图能力  

- **流处理类连接器**：适用于实时 SQL 查询或动态内容拉取  
  - `MySQL` / `PostgreSQL` / `PolarDB-X 2.0`：仅通过 **DMS 导入数据源**方式创建的连接器支持执行 SQL 查询；自定义方式仅支持元数据同步，不支持查询执行 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)  
  - `语雀`：对接语雀开放 API，依赖 Tenant Access Token 访问[知识库](../concepts/knowledge-base.md)内容，**仅支持公网版本语雀**  
  - `OSS`：支持读取 Bucket 中文件，但需提前开通[向量检索服务](https://help.aliyun.com/zh/oss/user-guide/vector-retrieval/)才能使用 `searchOSSFile` 和 `searchOSSFileByFileName` 工具 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)  

> **注意**：MySQL 与 PostgreSQL 连接器均要求数据库账号具备读取权限，但 PostgreSQL 还需额外满足 `wal_level=logical` 及 `listen_addresses` 配置（自建实例），而 MySQL 无此强制要求 —— 此差异已在原始文档中明确，无需额外协调。

## 关键参数

| 连接器类型 | 必填参数 | 特殊约束 |
|------------|----------|----------|
| 文件 / 表格 | 连接器名称、描述、存储位置（平台存储 or OSS） | OSS Bucket 需添加 `bailian-connector-access` 标签（值 `ReadAndWrite`） |
| MySQL | 数据库用户名、密码、网络类型（公网/私网）、数据库实例（RDS）或地址（自建） | 公网连接需将百炼 IP 段加入白名单；仅 DMS 导入方式支持 SQL 执行 |
| PostgreSQL | 主机地址、端口、dbName、用户名、密码 | `wal_level` 必须设为 `logical`；自建实例需配置 `pg_hba.conf` 允许 `100.64.0.0/16` 访问 |
| PolarDB-X 2.0 | 用户名、密码、所属地域（强制私网）、数据库实例（SLR 授权后下拉选择） | 仅支持阿里云 PolarDB-X 2.0 实例；首次使用需授权 `AliyunServiceRoleForSFMConnectorAccessDTS` 和 `AliyunServiceRoleForSFMAccessPolarDBX` 角色 |
| 语雀 | Tenant Access Token | Token 需通过[语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取 |
| OSS | Bucket 名称 | Bucket 需添加 `bailian-datahub-access` 标签（值 `read`）；不支持归档/冷归档存储类型 |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击「创建连接器」→ 选择类型 → 填写基本信息与连接参数 → （可选）点击「开始检测」验证连通性 → 确认创建  
2. **导入数据（仅平台托管类）**：  
   - 文件连接器：进入详情页 → 选择类目 → 「导入数据」→ 本地上传 → 选择解析方式（默认/自定义）→ 配置标签（可选）→ 确认  
   - 表格连接器：进入详情页 → 新建或选择数据表 → 上传 Excel 或自定义表头 → 确保列名与类型严格匹配 → 确认导入  
3. **调用连接器**：  
   - 平台托管类：通过智能体工具（如 `searchFile`、`searchTable`）或 API 的 `knowledge_retrieval` 参数触发向量检索  
   - 流处理类：MySQL/PostgreSQL/PolarDB-X 仅在 DMS 导入方式下可通过 `executeSQL` 工具执行查询；语雀/OSS 通过专用工具（如 `searchYuQueDoc`、`searchOSSFile`）调用  

## 限制和注意事项

- **容量与生命周期**：  
  - 平台托管文件：免费额度为 200,000 个文件 + 1 TB 存储；导入文件仅可查看最近 90 天记录，超期后不可见但不删除  
  - 平台托管表格：1 TB 免费额度，用尽后转按量付费  
  - 类目上限：每个业务空间最多 500 个类目，扩容需[提交工单](https://smartservice.console.aliyun.com/service/create-ticket)  

- **网络与权限**：  
  - MySQL 公网连接必须配置白名单；PolarDB-X 2.0 **仅支持私网**，且地域必须与实例一致  
  - 所有连接器均需主账号或已获 RAM 授权的用户操作；OSS/Bucket 访问依赖 SLR 授权与标签策略  

- **功能限制**：  
  - 不支持直接导入 JSON、CSV、YAML 格式文件（表格连接器除外）；文件连接器需转换为 XLSX/XLS 后再导入  
  - 语雀连接器不支持内网部署版；OSS 连接器若开启 Referer 防盗链，须将 `*.console.aliyun.com` 加入白名单  
  - 流处理类连接器中，**仅 DMS 导入方式支持 SQL 执行**，该限制在 MySQL、PostgreSQL、PolarDB-X 三类连接器中保持一致 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)  

- **安全合规**：  
  - 导入数据作为独立副本存储于百炼平台，与源数据无关联；阿里云不会将数据用于商业用途或对外公开  
  - 所有连接器均遵循最小权限原则，建议为数据库账号分配只读权限，避免敏感操作风险

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


