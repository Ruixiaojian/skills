# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可配置的数据接入通道。通过数据连接器，开发者可将企业自有数据库、文档系统、对象存储等异构数据源接入百炼，支撑知识库构建、实时SQL查询与智能体上下文增强等场景。所有连接器均基于最小权限原则设计，支持平台托管与流处理两类访问模式。

## 支持的模型/功能

数据连接器按数据访问方式分为两大类：

- **平台托管类**：文件、表格连接器。数据上传至百炼平台或自有OSS后，由平台完成解析、切分与向量化，供RAG类应用调用。支持文档智能解析、大模型文档解析（含Qwen VL）、音视频解析等多种解析策略 [数据连接 (raw/application-user-guide/data-connection-overview/data-connection.md)](../../raw/application-user-guide/data-connection-overview/data-connection.md)。
  
- **流处理类**：MySQL、PostgreSQL、PolarDB-X 2.0、语雀、OSS 连接器。数据保留在源端，应用在运行时按需发起实时查询或检索。其中，**仅通过 DMS 导入数据源方式创建的 MySQL/PostgreSQL/PolarDB-X 连接器支持执行 SQL 查询**；自定义方式创建的同类连接器仅支持元数据发现，不支持 `SELECT` 等执行能力 [数据连接 (raw/application-user-guide/data-connection-overview/data-connection.md)](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

此外，**定时数据同步规则**作为文件连接器的扩展能力，支持从 OSS、飞书、钉钉、语雀、SharePoint 等来源自动拉取新增/更新文件，实现近实时知识库增量更新 [定时数据同步指南 (raw/application-user-guide/data-connection-overview/data-sync-guide.md)](../../raw/application-user-guide/data-connection-overview/data-sync-guide.md)。

> **注意**：文档1中称“OSS连接器用于访问对象存储中的文件”，但未明确其是否支持流式读取；而文档2明确将OSS列为同步来源之一，并强调其支持“增量同步”和“文件更新检测”。结合二者，OSS连接器实际具备双重角色：既可作为**流处理连接器**（直接访问OSS对象并调用`searchOSSFile`等工具），也可作为**同步来源**（通过同步规则拉取文件到平台托管知识库）。该能力差异未在文档1中体现，属信息缺失，建议以文档2的同步机制说明为准。

## 关键参数

| 连接器类型 | 必填参数 | 特殊要求 | 权限/标签 |
|------------|----------|----------|-----------|
| **文件/表格** | 连接器名称、描述、存储位置（平台/OSS） | 平台存储：免费额度200,000文件/1TB；OSS需添加`bailian-connector-access`标签（值`ReadAndWrite`） | RAM用户需被授予`AliyunBailianDataConnectorFullAccess`或等效权限 |
| **MySQL** | 数据库地址、端口、用户名、密码（自建）；或实例ID（RDS） | RDS需SLR授权；自建需开放公网/IP白名单；DMS导入方式才支持SQL执行 | Bucket标签同上；数据库用户需`SELECT`权限 |
| **PostgreSQL** | 主机地址、端口、数据库名（`dbName`）、用户名、密码 | `wal_level=logical`；自建实例需配置`listen_addresses`允许`100.64.0.0/16`网段访问 | 同上；用户需`REPLICATION`或Superuser权限 |
| **PolarDB-X 2.0** | 数据库地址、端口、用户名、密码；或实例ID（自定义方式） | **仅支持私网**；首次使用需授权`AliyunServiceRoleForSFMConnectorAccessDTS`与`AliyunServiceRoleForSFMAccessPolarDBX`角色 | 同上 |
| **语雀** | Tenant access token | 仅支持公网语雀；[Token](../concepts/token.md)需具备知识库读取权限 | 无Bucket标签要求 |
| **OSS（同步规则）** | OSS Bucket、对象路径、同步周期 | 需添加`bailian-datahub-access`标签（值`read`）；**不支持归档/冷归档存储类型** | 同上；且需开通[向量检索服务](https://help.aliyun.com/zh/oss/user-guide/vector-retrieval/) |

## 使用方式

1. **创建连接器**：在[数据连接控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) → “创建连接器”，按向导选择类型并填写参数。MySQL/PostgreSQL/PolarDB-X 的 DMS 导入方式需提前在 DMS 中完成数据源录入与 SLR 授权 [数据连接 (raw/application-user-guide/data-connection-overview/data-connection.md)](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

2. **导入/同步数据**：
   - 文件/表格：进入连接器详情页 → “导入数据”，支持本地上传或OSS路径批量导入。
   - 定时同步：仅适用于**文件连接器**，在文件管理页点击“同步数据规则” → 创建规则，指定来源（OSS/飞书/钉钉/语雀/SharePoint）、路径、周期（1分钟/1小时/1天）及标签 [定时数据同步指南 (raw/application-user-guide/data-connection-overview/data-sync-guide.md)](../../raw/application-user-guide/data-connection-overview/data-sync-guide.md)。

3. **在应用中调用**：
   - 平台托管类：通过知识库检索工具（如`searchKnowledgeBase`）调用；
   - 流处理类：MySQL/PostgreSQL/PolarDB-X 使用`executeSQL`工具；语雀/OSS 使用`searchYuQueDoc`/`searchOSSFile`等专用工具。

## 限制和注意事项

- **容量与时效**：平台托管文件仅支持查看最近90天内导入的文件（副本仍保留）；解析耗时受流量高峰影响，可能达数小时 [数据连接 (raw/application-user-guide/data-connection-overview/data-connection.md)](../../raw/application-user-guide/data-connection-overview/data-connection.md)。
  
- **网络与地域**：PolarDB-X 2.0 连接器**仅支持私网**，且实例必须与百炼服务同地域；MySQL/PostgreSQL 公网连接需将百炼出口IP加入数据库白名单 [数据连接 (raw/application-user-guide/data-connection-overview/data-connection.md)](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

- **同步行为**：所有同步规则拉取的文件均为**独立副本**，源文件删除不影响百炼中已同步数据；需手动删除百炼侧副本 [定时数据同步指南 (raw/application-user-guide/data-connection-overview/data-sync-guide.md)](../../raw/application-user-guide/data-connection-overview/data-sync-guide.md)。

- **权限隔离**：每个连接器仅对所属业务空间可见；RAM 用户需主账号显式授权`AliyunBailianDataConnectorFullAccess`策略方可操作 [数据连接 (raw/application-user-guide/data-connection-overview/data-connection.md)](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

- **OSS特殊限制**：使用`searchOSSFile`等工具前，**必须开通OSS向量检索服务**；若Bucket开启Referer防盗链，须将`*.console.aliyun.com`加入白名单 [数据连接 (raw/application-user-guide/data-connection-overview/data-connection.md)](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)
- [定时数据同步指南](../../raw/application-user-guide/data-connection-overview/data-sync-guide.md)


