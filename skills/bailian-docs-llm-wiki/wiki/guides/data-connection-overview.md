# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的实时数据访问入口。它支持结构化与非结构化数据接入，并通过向量化检索或 SQL 查询等方式赋能智能体与模型应用。所有连接器均需在业务空间内创建并授权后方可使用。

## 支持的模型/功能

数据连接器按数据访问模式分为两类：

- **平台托管型**：适用于文件（PDF/Word/Markdown等）和表格（CSV/Excel等）类非实时数据，数据可托管于百炼平台（限时免费 1 TB）或用户自有 OSS Bucket。导入后经文档解析（如[文档智能解析](https://help.aliyun.com/zh/document-mind/product-overview/overview-of-document-understanding#9a4f5fb91fpps)）生成向量索引，支持语义检索。
- **流处理型**：适用于需实时查询的数据库与在线知识库，包括 MySQL、PostgreSQL、PolarDB-X 2.0、语雀 和 OSS（启用向量检索服务后）。其中仅通过 **DMS 导入数据源**方式创建的 MySQL/PostgreSQL/PolarDB-X 连接器支持执行 SQL 查询；自定义方式创建的同类连接器仅支持元数据同步，不支持 SQL 执行 —— 此限制详见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 的“MySQL连接器”与“PostgreSQL连接器”章节。

> **注意**：OSS 连接器虽属流处理类型，但其核心能力依赖向量检索服务（[原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 明确要求开通），未开通时 `searchOSSFile` 和 `searchOSSFileByFileName` 工具不可用。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **通用** | 连接器名称、描述 | 名称需唯一且易识别；描述影响智能体调用准确度，建议明确数据内容与用途 |
| **文件/表格** | 存储位置（平台存储 / 自有 OSS） | 使用自有 OSS 时，Bucket 必须添加 `bailian-connector-access` 标签（值 `ReadAndWrite`） |
| **MySQL/PostgreSQL/PolarDB-X** | 数据库地址、端口、用户名、密码、dbName（PostgreSQL/PolarDB-X 必填） | PolarDB-X 仅支持私网连接，且仅限阿里云实例；PostgreSQL 要求 `wal_level=logical` —— 具体配置见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) |
| **语雀** | Tenant access token | 仅支持公网语雀；[Token](../concepts/token.md) 需通过[语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取 |
| **OSS** | Bucket 选择、`bailian-datahub-access` 标签（值 `read`） | 不支持归档/冷归档存储类型；Referer 防盗链需白名单 `*.console.aliyun.com` |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击「创建连接器」→ 选择类型 → 填写基本信息与连接参数 → （可选）点击「开始检测」验证连通性 → 确认创建。
2. **导入数据**：
   - *文件*：进入连接器详情页 → 选择类目 → 「导入数据」→ 本地上传 → 选择解析方式（默认/自定义）→ 配置标签（可选）→ 确认。
   - *表格*：进入连接器详情页 → 「数据表管理」→ 新建或选择数据表 → 上传 Excel 或自定义表头（列名、类型必填，结构不可修改）→ 确认。
3. **在应用中调用**：连接器创建并导入数据后，可在智能体工作流中直接引用对应知识库，或通过工具（如 `searchFile`、`searchTable`、`executeSQL`）调用；SQL 工具仅对 DMS 导入方式创建的数据库连接器生效。

## 限制和注意事项

- **权限要求**：操作者需为主账号或已获 `AliyunBailianDataConnectorFullAccess` 等相关 RAM 权限的用户；首次使用 OSS/语雀/DMS 等服务需完成 SLR 授权。
- **容量与时效**：
  - 平台托管文件：最多 200,000 个文件，1 TB 免费额度（文件导入后作为独立副本存储，无自动清理）；
  - 导入文件仅支持查看最近 90 天记录；
  - 类目上限 500 个，扩容需提交工单。
- **兼容性限制**：
  - 文件导入不支持 JSON/CSV/YAML 原生格式，需转为 XLSX/XLS；
  - PostgreSQL 自建实例需额外配置 `listen_addresses` 与 `pg_hba.conf` 允许 `100.64.0.0/16` 网段访问；
  - PolarDB-X 2.0 不支持公网连接，且不兼容自建集群。
- **安全约束**：
  - 所有自有 OSS Bucket 必须打标（`bailian-connector-access` 或 `bailian-datahub-access`）；
  - 语雀 [Token](../concepts/token.md) 为个人访问凭证，应严格保密；
  - 数据连接器作用域限定于当前业务空间，跨空间不可见。

> **注意**：MySQL 与 PostgreSQL 连接器均强调“仅 DMS 导入方式支持 SQL 查询”，但原始文档未明确说明该限制是否适用于所有版本或未来迭代。开发者应以控制台实际可用工具为准，若发现自定义方式创建的连接器意外支持 `executeSQL`，请以 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 的最新发布版本为权威依据。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


