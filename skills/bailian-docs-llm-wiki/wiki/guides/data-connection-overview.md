# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心机制，为应用提供安全、可控的数据接入能力。它支持结构化与非结构化数据的接入，并通过平台托管或流处理两种模式实现数据的存储与实时访问。所有连接器均需在业务空间内创建，且其生命周期与权限受RAM策略约束，详见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

## 支持的模型/功能

数据连接器按数据访问模式分为两类：

- **平台托管类**：适用于文件（PDF/Word/Markdown等）和表格（CSV/Excel等）连接器。数据可存储于百炼平台免费空间（文件上限 200,000 个，总容量 1 TB；表格含 1 TB 免费额度），或接入自有 OSS Bucket（需添加 `bailian-connector-access` 标签）。  
- **流处理类**：支持 MySQL、PostgreSQL、PolarDB-X 2.0、语雀、OSS 连接器。数据保留在源端，应用通过工具（如 `searchSQL`、`searchYuqueDoc`、`searchOSSFile`）发起实时查询。其中，**仅通过 DMS 导入方式创建的 MySQL/PostgreSQL/PolarDB-X 连接器支持执行 SQL 查询**；自定义数据源方式创建的同类连接器仅支持元数据同步，不支持运行时 SQL 执行 —— 此限制在 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中明确强调。

> **注意**：OSS 连接器虽属流处理类型，但实际依赖向量检索服务实现语义搜索（`searchOSSFile`）和文件名匹配（`searchOSSFileByFileName`），未开通该服务将导致对应工具不可用，该要求在 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 的“OSS连接器”小节中强制说明。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **通用** | 连接器名称、描述 | 名称需唯一且易识别；描述影响智能体调用准确率，建议包含数据内容与用途（见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)） |
| **文件/表格** | 存储位置（平台存储 / 自有OSS） | 平台存储享免费额度；自有OSS需完成授权并打标（`bailian-connector-access: ReadAndWrite`） |
| **MySQL/PostgreSQL/PolarDB-X** | 数据来源方式、网络类型、数据库地址/端口/用户名/密码 | MySQL/PolarDB-X 支持 SLR 授权自动填充连接信息；PostgreSQL 必填 `dbName`；PolarDB-X 仅支持私网；PostgreSQL 要求 `wal_level=logical` |
| **语雀** | Tenant access token | 仅支持公网语雀，[Token](../concepts/token.md) 需通过 [语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取 |
| **OSS** | Bucket 选择、标签（`bailian-datahub-access: read`） | Bucket 需已开通向量检索服务；不支持归档/冷归档存储类型 |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击“创建连接器” → 选择类型 → 填写基本信息与连接参数 → （可选）点击“开始检测”验证连通性 → 确认创建。  
2. **导入数据（仅平台托管类）**：  
   - 文件连接器：进入详情页 → 新建或选择类目 → “导入数据” → 本地上传 → 选择解析方式（默认/文档智能/大模型/Qwen VL/音视频）→ 配置标签（可选）→ 确认。  
   - 表格连接器：进入详情页 → 新建或选择数据表 → 上传 Excel 或自定义表头（列名、类型必填，描述建议填写）→ 确认。  
3. **调用数据**：在智能体或 API 调用中，通过预置工具（如 `searchFile`、`searchSQL`、`searchYuqueDoc`）传入 query 参数触发检索；支持通过 `tags` 参数按标签过滤文件（见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) “导入文件”章节说明）。

## 限制和注意事项

- **权限限制**：仅主账号或被授予 `AliyunBailianDataConnectorFullAccess` 或自定义数据连接权限的 RAM 用户可操作；授权方法参见 [权限管理](https://help.aliyun.com/zh/model-studio/application-permission-management-overview)。  
- **地域与网络**：PolarDB-X 2.0 连接器仅支持私网，且实例必须与百炼服务同地域；MySQL/PostgreSQL 公网连接需将百炼服务 IP 段加入数据库白名单。  
- **解析与容量**：文件连接器仅支持最近 90 天内导入的文件预览；单业务空间最多 500 个类目（扩容需提工单）；表格连接器表结构一旦创建不可修改。  
- **兼容性限制**：  
  - 文件连接器不支持直接导入 JSON/CSV/YAML，须转为 XLSX/XLS；  
  - OSS 连接器若开启 Referer 防盗链，须将 `*.console.aliyun.com` 加入白名单；  
  - PostgreSQL 自建实例需额外配置 `listen_addresses` 允许 `100.64.0.0/16` 网段访问。  
- **功能差异**：MySQL 与 PostgreSQL 连通性检测分别依赖 EventBridge 和 DTS；PolarDB-X 不支持自建库，且 SLR 授权涉及 DTS + PolarDB-X 双角色（DMS 方式还需 DMS 角色）。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


