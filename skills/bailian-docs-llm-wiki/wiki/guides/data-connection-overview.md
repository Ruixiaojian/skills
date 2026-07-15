# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的数据接入通道。它支持结构化与非结构化数据的接入，并通过平台托管或流处理两种模式实现数据访问，是构建知识增强型智能体（Agent）和 RAG 应用的基础组件。所有连接器均需在业务空间内创建并绑定至具体应用，其配置直接影响后续检索与调用行为。

## 支持的模型/功能

数据连接器按数据访问方式分为两类：

- **平台托管类**：适用于静态文件与表格数据，包括  
  - `文件`：支持 PDF、Word、Markdown 等非结构化文档，依赖[文档理解](https://help.aliyun.com/zh/document-mind/product-overview/overview-of-document-understanding#9a4f5fb91fpps)能力进行解析（详见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中“导入文件”章节）；  
  - `表格`：支持 CSV、Excel 等结构化数据，支持自定义表头与字段类型（如 `image_url`），但表结构一旦确定不可修改。

- **流处理类**：适用于实时数据库与在线服务，包括  
  - `MySQL`、`PostgreSQL`、`PolarDB-X 2.0`：仅通过 **DMS 导入数据源** 方式创建的连接器支持执行 SQL 查询；自定义方式创建的连接器仅支持元数据同步，不支持直接查询（该限制在 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 的各数据库连接器说明中反复强调）；  
  - `语雀`：对接语雀知识库，依赖个人访问 Token，**仅支持公网版本语雀**；  
  - `OSS`：访问对象存储中的文件，需开通向量检索服务方可使用 `searchOSSFile` 和 `searchOSSFileByFileName` 工具（参见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) “OSS连接器”章节）。

> **注意**：`MySQL` 与 `PostgreSQL` 连接器均要求数据库账号具备高权限（如 REPLICATION 或 Superuser），且 PostgreSQL 必须将 `wal_level` 设置为 `logical`；而 PolarDB-X 2.0 **仅支持私网连接**，不支持公网，且不兼容自建实例——这些关键差异已在原始文档中明确区分，开发者需严格遵循。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **通用** | 连接器名称、描述 | 名称需唯一且易识别；描述影响智能体调用准确度，建议明确数据内容与用途 |
| **文件/表格** | 存储位置（平台存储 / 自有 OSS） | 平台存储提供免费额度（文件连接器限 200,000 文件 / 1 TB，表格连接器限 1 TB）；自有 OSS 需添加 `bailian-connector-access` 标签（值为 `ReadAndWrite`） |
| **数据库类** | 数据库地址、端口、用户名、密码、dbName（PostgreSQL/PolarDB-X 必填） | MySQL 默认端口 3306，PostgreSQL 默认 5432；PolarDB-X 仅支持私网，且数据库地址/端口由实例自动填充 |
| **语雀/OSS** | Tenant access token（语雀）、Bucket 选择（OSS） | 语雀 Token 需从 [语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取；OSS Bucket 需添加 `bailian-datahub-access` 标签（值为 `read`），且**不支持归档/冷归档存储类型** |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击 **创建连接器** → 选择类型 → 填写基本信息与连接参数 → （可选）点击 **开始检测** 或 **连接检测** 验证连通性 → 确认创建。  
2. **导入数据**：  
   - 文件连接器：进入详情页 → 选择类目 → **导入数据** → 本地上传 → 配置解析方式（默认/自定义）与标签 → 确认；  
   - 表格连接器：进入详情页 → 在 **数据表管理** 下新建或选择数据表 → 上传 Excel 或自定义表头 → 确保列名与类型严格匹配；  
   - 数据库/OSS/语雀类连接器无需手动导入，数据实时访问。  
3. **绑定应用**：在应用配置中显式关联已创建的数据连接器，方可启用对应检索能力（如 `searchFile`、`querySQL` 等工具）。

## 限制和注意事项

- **权限约束**：RAM 用户需主账号授予 `AliyunBaiLianFullAccess` 或最小化权限策略（含 `bailian:ListConnectors`、`bailian:CreateConnector` 等动作），详见 [权限管理](https://help.aliyun.com/zh/model-studio/application-permission-management-overview)。  
- **网络与白名单**：MySQL 公网连接需将百炼服务 IP 段加入数据库白名单；PostgreSQL 自建实例需配置 `pg_hba.conf` 允许 `100.64.0.0/16` 访问；PolarDB-X 仅支持私网，必须同地域部署。  
- **解析与时效性**：文件导入后生成独立副本，**仅支持查看最近 90 天内导入的文件**；高峰时段解析可能延迟数小时，偶现超时，建议错峰操作。  
- **功能边界**：  
  - `MySQL`/`PostgreSQL`/`PolarDB-X 2.0` 的 SQL 执行能力**仅对 DMS 导入方式生效**，自定义方式不支持（原始文档多次强调，勿混淆）；  
  - OSS 连接器若未开通向量检索服务，则 `searchOSSFile` 等工具不可用；  
  - 文件连接器**不支持直接导入 JSON/CSV/YAML**，需先转为 XLSX/XLS 格式。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


