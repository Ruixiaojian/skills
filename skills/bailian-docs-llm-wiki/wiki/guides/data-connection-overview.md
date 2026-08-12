# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的实时数据访问入口。它支持结构化与非结构化数据接入，并通过平台托管或流处理两种模式实现数据就地访问或导入处理。所有连接器均需在业务空间内创建并授权后方可被智能体或 API 调用。

## 支持的模型/功能

数据连接器按数据访问模式分为两类：

- **平台托管型**：适用于文件（PDF/Word/Markdown 等）和表格（CSV/Excel 等），数据可上传至百炼平台存储（限时免费额度）或接入自有 OSS Bucket。文件类支持多种解析方式（如文档智能解析、大模型文档解析、Qwen VL 解析等），表格类支持自动表头识别与自定义 Schema 定义。详见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

- **流处理型**：适用于 MySQL、PostgreSQL、PolarDB-X 2.0、语雀和 OSS，数据保留在原系统中，百炼通过网络连接实时查询。其中 MySQL、PostgreSQL 和 PolarDB-X 2.0 连接器**仅当通过 DMS 导入数据源方式创建时才支持执行 SQL 查询**；自定义方式创建的同类连接器不支持 SQL 执行能力 —— 此限制在 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中多次强调，开发者务必注意创建路径选择。

> **注意**：OSS 连接器虽属流处理类型，但其核心能力并非“实时查询”，而是通过 `searchOSSFile` 和 `searchOSSFileByFileName` 工具进行向量检索或文件名匹配，依赖已开通的 [向量检索服务](https://help.aliyun.com/zh/oss/user-guide/vector-retrieval/)。该前提条件在 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中明确列出，未开通则对应工具不可用。

## 关键参数

| 类型 | 必填参数 | 说明 |
|------|----------|------|
| **文件/表格** | 连接器名称、描述、存储位置（平台 or OSS） | 描述建议明确数据内容与用途，直接影响智能体调用准确度；OSS Bucket 需添加 `bailian-connector-access` 标签（值 `ReadAndWrite`） |
| **MySQL** | 数据库用户名、密码、网络类型（公网/私网）、数据库实例（RDS）或地址（自建） | 公网连接需将百炼 IP 段加入白名单；仅 DMS 导入方式支持 SQL 查询 |
| **PostgreSQL** | 主机地址、端口、dbName、用户名、密码 | `wal_level` 必须设为 `logical`；自建实例还需配置 `listen_addresses` 允许 `100.64.0.0/16` 访问 |
| **PolarDB-X 2.0** | 用户名、密码、所属地域、数据库实例（仅自定义方式）或数据源（仅 DMS 方式） | **仅支持私网**；首次使用需显式授权 DTS 与 PolarDB-X SLR 角色 |
| **语雀** | Tenant access token | 仅支持公网语雀；[Token](../concepts/token.md) 需通过 [语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取 |
| **OSS** | Bucket 名称 | Bucket 需添加 `bailian-datahub-access` 标签（值 `read`）；不支持归档/冷归档存储类型 |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 控制台 → 单击「创建连接器」→ 选择类型 → 填写基本信息与连接参数 → （可选）点击「开始检测」验证连通性 → 确认创建。

2. **导入数据（仅平台托管型）**：
   - 文件连接器：进入详情页 → 选择类目 → 「导入数据」→ 本地上传 → 选择解析方式（默认/自定义）→（可选）配置标签 → 确认。
   - 表格连接器：进入详情页 → 「数据表管理」→ 新建或选择数据表 → 上传 Excel 或自定义表头 → 确认导入。

3. **调用数据**：
   - 平台托管型：通过知识库检索（`retrieval` 工具）或 `searchFile` 等内置工具访问；
   - 流处理型：MySQL/PostgreSQL/PolarDB-X 2.0 仅限 DMS 导入方式支持 `executeSQL` 工具；语雀支持 `searchYuQueDoc`；OSS 支持 `searchOSSFile` 和 `searchOSSFileByFileName`。

## 限制和注意事项

- **权限要求**：必须为主账号或已获 `AliyunBailianDataConnectorFullAccess` 权限的 RAM 用户；RAM 用户需主账号提前授权，参见 [权限管理](https://help.aliyun.com/zh/model-studio/application-permission-management-overview)。
- **容量与时效**：
  - 文件连接器：平台存储上限 200,000 个文件 / 1 TB（限时免费）；导入文件仅可查看最近 90 天记录。
  - 表格连接器：平台存储 1 TB 免费额度，用尽后转按量付费。
- **网络与兼容性**：
  - PolarDB-X 2.0 连接器**不支持公网**，且**仅限阿里云实例**，不支持自建部署。
  - PostgreSQL 自建实例需手动配置 `pg_hba.conf` 并重载服务，否则连通性检测失败。
- **安全约束**：
  - OSS Bucket 若开启 Referer 防盗链，须将 `*.console.aliyun.com` 加入白名单。
  - 所有连接器均不支持跨业务空间共享；导入文件为独立副本，与原始数据无关联。
- **功能差异**：MySQL、PostgreSQL、PolarDB-X 2.0 的 SQL 执行能力严格绑定于「DMS 导入数据源」创建路径，此关键限制在 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中反复说明，切勿混淆创建方式。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


