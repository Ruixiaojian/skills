# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的实时数据访问入口。它支持结构化与非结构化数据的接入，并通过平台托管或流处理两类模式实现数据就位（data-at-rest）或数据就绪（data-in-motion）场景下的灵活集成。所有连接器均需在业务空间内创建并授权后方可被智能体或 API 调用。

## 支持的模型/功能

数据连接本身不直接调用大模型，但为以下两类能力提供数据底座：

- **知识库检索**：文件、表格、OSS、语雀连接器支持向量化索引构建，供 `searchFile`、`searchTable` 等工具执行语义检索；
- **实时 SQL 查询**：仅 MySQL、PostgreSQL、PolarDB-X 2.0 连接器在**通过 DMS 导入数据源方式创建时**支持 `executeSQL` 工具执行查询（参见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中“MySQL连接器”章节说明）；
- **[多模态](../concepts/multimodal.md)解析**：文件连接器支持电子文档解析、文档智能解析、大模型文档解析及 Qwen VL 解析等模式，详见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 的“导入文件”小节。

> **注意**：`executeSQL` 功能**不适用于**通过“创建自定义数据源”方式添加的 MySQL/PostgreSQL/PolarDB-X 连接器——该限制在 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 多处明确强调，且与部分旧版文档中模糊表述存在冲突，请以本文档为准。

## 关键参数

| 参数类别       | 必填项                     | 说明                                                                 |
|----------------|----------------------------|----------------------------------------------------------------------|
| **通用**       | 连接器名称、描述           | 名称需唯一；描述影响智能体对数据用途的理解，建议包含数据范围与业务含义 |
| **文件/表格**  | 存储位置（平台存储 / OSS） | 平台存储有免费额度（1 TB），OSS 需提前打标 `bailian-connector-access`（值 `ReadAndWrite`） |
| **MySQL**      | 数据库用户名、密码、实例ID（RDS）或地址（自建） | RDS 场景下端口自动填充为 3306；公网连接需放行白名单 IP 段             |
| **PostgreSQL** | dbName、用户名、密码、`wal_level=logical` | 自建实例还需配置 `listen_addresses` 允许 `100.64.0.0/16` 访问         |
| **PolarDB-X**  | 数据库用户名、密码、私网地域 | 仅支持私网；首次使用需显式授权 `AliyunServiceRoleForSFMConnectorAccessDTS` 等 SLR 角色 |
| **语雀**       | Tenant access token        | 仅支持公网语雀；[Token](../concepts/token.md) 需通过 [语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取 |
| **OSS**        | Bucket 名称                | Bucket 需打标 `bailian-datahub-access`（值 `read`），且已开通 [向量检索服务](https://help.aliyun.com/zh/oss/user-guide/vector-retrieval/) |

## 使用方式

1. **创建连接器**：进入 [数据连接控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list)，单击“创建连接器”，按类型填写参数并完成连通性检测；
2. **导入数据（仅文件/表格）**：
   - 文件连接器：在详情页选择类目 → “导入数据” → 本地上传（支持 PDF/Word/Markdown/图片/音视频等）→ 选择解析方式；
   - 表格连接器：在详情页新建数据表 → 上传 Excel 或自定义表头（列名、类型必填，结构不可变）；
3. **绑定至应用**：在智能体或 API 应用配置中，将连接器关联至知识库或工具集；
4. **调用数据**：
   - 知识库场景：通过 `searchFile`、`searchTable`、`searchOSSFile` 等工具触发检索；
   - 实时查询场景：仅 DMS 导入的数据库连接器可调用 `executeSQL` 工具（参见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中各数据库连接器的“说明”段落）。

## 限制和注意事项

- **类目与容量限制**：文件连接器单业务空间最多 500 个类目；平台存储文件默认保留 90 天（仅可查看），超期文件不删除但不可见；
- **格式限制**：文件连接器不支持直接导入 JSON/CSV/YAML，需转为 XLSX/XLS；OSS 连接器**不支持归档、冷归档、深度冷归档存储类型**；
- **网络与权限**：
  - MySQL/PostgreSQL 公网连接需手动配置白名单；
  - PolarDB-X 2.0 **仅支持私网**，且必须与百炼服务同地域；
  - 所有 OSS 连接器需目标 Bucket 添加指定标签并完成 RAM 授权；
- **安全要求**：
  - PostgreSQL 自建实例必须配置 `wal_level=logical` 和 `pg_hba.conf` 访问规则；
  - 语雀 [Token](../concepts/token.md) 为高权限凭证，应严格保密；
- **功能边界**：`executeSQL` 仅返回查询结果，**不支持写操作（INSERT/UPDATE/DELETE）或 DDL**；流处理类连接器（数据库/OSS/语雀）的数据始终保留在源端，平台不持久化副本。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


