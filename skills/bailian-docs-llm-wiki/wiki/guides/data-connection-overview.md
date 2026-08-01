# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的数据接入通道。它支持结构化与非结构化数据的接入，并通过平台托管或流处理两种模式实现数据读取与实时查询。开发者可基于业务场景选择合适的连接器类型，并在应用中调用对应工具（如 `searchOSSFile`、`queryMySQL`）完成数据检索或 SQL 执行。

## 支持的模型/功能

数据连接器按数据访问模式分为两类：

- **平台托管型**：适用于文件（PDF/Word/Markdown）、表格（CSV/Excel）等静态数据，数据被导入百炼平台或自有 OSS 后进行向量化与索引构建，支持语义检索；
- **流处理型**：适用于 MySQL、PostgreSQL、PolarDB-X 2.0、语雀、OSS 等实时数据源，数据保留在原系统，应用通过工具触发即时查询或同步拉取。

> **注意**：仅通过 **DMS 导入数据源** 方式创建的 MySQL、PostgreSQL 和 PolarDB-X 2.0 连接器才支持执行 SQL 查询；自定义方式创建的连接器不支持该能力 —— 此限制在 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中多次强调，需严格遵循。

各连接器支持的功能如下：
- 文件/表格连接器：支持文档智能解析、大模型文档解析（含图表理解）、音视频解析（语音识别+帧提取+剧情解析）；
- MySQL/PostgreSQL/PolarDB-X 2.0：支持 SQL 查询（限 DMS 导入方式），其中 PostgreSQL 要求 `wal_level=logical`，PolarDB-X 2.0 仅支持私网连接；
- 语雀连接器：支持公网语雀知识库访问，依赖个人访问 Token；
- OSS 连接器：支持 `searchOSSFile`（语义搜索）和 `searchOSSFileByFileName`（精确匹配），但需提前开通 [向量检索服务](https://help.aliyun.com/zh/oss/user-guide/vector-retrieval/) —— 详见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

## 关键参数

| 参数 | 说明 | 必填性 | 备注 |
|------|------|--------|------|
| 连接器名称 | 建议使用业务语义化命名（如 `hr-policy-files`） | ✅ | 影响调试与日志识别 |
| 描述 | 用于指导模型理解数据用途，建议包含数据范围与典型查询意图 | ⚠️ 推荐 | [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 明确指出描述“会用于指导智能体调用的准确度” |
| 存储位置（文件/表格） | 平台存储（免费额度）或自有 OSS Bucket | ✅ | OSS Bucket 需添加 `bailian-connector-access` 标签（值为 `ReadAndWrite`） |
| 数据库地址/端口（MySQL/PostgreSQL/PolarDB-X） | 自建数据库需手动填写；RDS 实例由平台自动填充 | ✅（自建）/❌（RDS） | PolarDB-X 2.0 仅支持私网，且仅限阿里云实例 |
| dbName（PostgreSQL） | 必填字段，指定目标数据库名 | ✅ | MySQL 无此字段，见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 对比表 |
| Tenant access token（语雀） | 公网语雀开放 API 获取的个人 Token | ✅ | 仅支持公网语雀，不支持企业内网部署版 |
| OSS Bucket 名称 | 从下拉列表选择已授权 Bucket | ✅ | Bucket 需添加 `bailian-datahub-access` 标签（值为 `read`），且不支持归档类存储类型 |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击「创建连接器」→ 选择类型 → 填写基本信息与连接参数 → 完成授权与连通性检测；
2. **导入数据（仅平台托管型）**：
   - 文件连接器：在详情页选择类目 → 「导入数据」→ 本地上传 → 选择解析方式（推荐默认设置，复杂图表选「大模型文档解析」）→ 可选配置标签；
   - 表格连接器：在详情页新建或选择数据表 → 上传 Excel 或自定义表头（列名、类型、描述）→ 注意表结构不可修改；
3. **调用连接器**：
   - 平台托管型：在智能体或工作流中调用 `searchFile` / `searchTable` 工具，支持 `tags` 参数过滤；
   - 流处理型：调用 `queryMySQL` / `queryPostgreSQL` / `queryPolarDBX` 等工具，传入 SQL 语句（仅 DMS 导入方式有效）；语雀/OSS 工具无需 SQL，直接传入关键词或文件名。

## 限制和注意事项

- **权限要求**：RAM 用户需主账号授予 `AliyunBailianFullAccess` 或最小化自定义策略（含 `bailian:CreateConnector` 等动作），详见 [权限管理](https://help.aliyun.com/zh/model-studio/application-permission-management-overview)；
- **网络限制**：
  - MySQL/PostgreSQL 公网连接需将百炼服务 IP 段加入数据库白名单；
  - PolarDB-X 2.0 **仅支持私网**，且必须与百炼所在地域一致；
- **OSS 特殊要求**：
  - 开启 Referer 防盗链的 Bucket，须将 `*.console.aliyun.com` 加入白名单；
  - 不支持归档、冷归档、深度冷归档存储类型；
- **文件/表格容量**：
  - 平台存储文件上限为 200,000 个文件 + 1 TB（限时免费）；
  - 导入文件仅保留最近 90 天的查看记录（后台仍可用）；
- **PostgreSQL 配置强依赖**：`wal_level` 必须设为 `logical`，自建实例还需配置 `listen_addresses` 允许 `100.64.0.0/16` 网段访问；
- **解析限制**：电子文档解析不支持插图与图表；音视频解析暂不识别环境音（如雷声、钟声）。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


