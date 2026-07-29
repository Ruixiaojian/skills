# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的实时数据访问入口。通过创建不同类型的连接器，开发者可将企业自有数据库、文档系统、对象存储等数据源接入百炼，支撑智能体在对话中动态检索、引用和处理结构化与非结构化数据。该能力不依赖数据迁移，支持平台托管与流处理两类模式，兼顾灵活性与实时性。

## 支持的模型/功能

数据连接器按数据访问模式分为两大类：

- **平台托管型**：适用于文件（PDF/Word/Markdown）、表格（CSV/Excel）类非结构化与轻量结构化数据。数据可托管于百炼平台（免费额度：200,000 文件 / 1 TB）或用户自有 OSS Bucket（需添加 `bailian-connector-access` 标签）[原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。  
- **流处理型**：适用于实时查询场景，包括 MySQL、PostgreSQL、PolarDB-X 2.0、语雀、OSS。数据保留在源端，百炼通过网络直连执行查询或同步索引。其中，**仅通过 DMS 导入方式创建的 MySQL/PostgreSQL/PolarDB-X 连接器支持 SQL 查询**；自定义方式创建的同类连接器仅支持元数据发现与向量化检索 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

> **注意**：原始文档中对 OSS 连接器的标签要求存在不一致——文件/表格连接器要求 `bailian-connector-access`（值 `ReadAndWrite`），而 OSS 连接器明确要求 `bailian-datahub-access`（值 `read`）[原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。请严格按连接器类型配置对应标签，否则授权失败。

## 关键参数

| 连接器类型 | 必填参数 | 特殊要求 |
|------------|----------|----------|
| **文件/表格** | 连接器名称、描述、存储位置（平台/OSS） | 描述字段直接影响智能体调用准确度；OSS Bucket 需打标且开通向量检索服务 |
| **MySQL** | 数据库用户名、密码、实例ID（RDS）或地址+端口（自建） | RDS 场景自动填充地址/端口；公网连接需白名单放行指定 IP 段；仅 DMS 导入支持 SQL 执行 |
| **PostgreSQL** | 主机地址、端口、数据库名（`dbName`）、用户名、密码 | `wal_level` 必须设为 `logical`；自建实例需配置 `pg_hba.conf` 允许 `100.64.0.0/16` 网段访问 |
| **PolarDB-X 2.0** | 用户名、密码、实例（自定义方式）或 DMS 数据源（DMS 方式） | **仅支持私网**；首次使用需显式授权 DTS 和 PolarDB-X SLR 角色 |
| **语雀** | Tenant access token | 仅支持公网语雀；[Token](../concepts/token.md) 需通过 [语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取 |
| **OSS** | Bucket 名称 | Bucket 不支持归档/冷归档存储类型；若启用 Referer 防盗链，需将 `*.console.aliyun.com` 加入白名单 |

## 使用方式

1. **创建连接器**：进入 [数据连接控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list)，点击「创建连接器」，按向导选择类型并填写参数。  
2. **验证连通性**：MySQL/PostgreSQL/PolarDB-X 支持「开始检测」（MySQL 用 EventBridge，PostgreSQL 用 DTS）；语雀/OSS 提供「连接检测」按钮；文件/表格无需网络检测。  
3. **导入数据**：  
   - 文件连接器：在详情页按类目上传，支持多种解析方式（如大模型文档解析支持图表理解）；  
   - 表格连接器：新建数据表后上传 Excel 或自定义表头（列名、类型、描述不可修改）；  
   - 流处理连接器：无需导入，直接在应用中调用对应工具（如 `searchOSSFile`、`executeSQL`）。  
4. **在应用中调用**：连接器创建后，可在智能体工作流中作为工具节点使用，或通过 API 请求参数 `tags` 指定标签进行过滤检索。

## 限制和注意事项

- **权限约束**：RAM 用户需主账号授予 `AliyunBaiLianDataConnectorFullAccess` 或自定义策略，详见 [权限管理](https://help.aliyun.com/zh/model-studio/application-permission-management-overview)。  
- **容量与时效**：平台托管文件仅保留最近 90 天的导入记录（可查看），但数据副本长期有效；表格连接器平台存储额度用尽后转为按量付费。  
- **网络与安全**：  
  - PolarDB-X 2.0 **强制私网**，不支持公网；  
  - 自建 PostgreSQL/MySQL 需确保百炼服务 IP 段（如 `100.64.0.0/16`）可达；  
  - OSS Bucket 若开启 Referer 防盗链，必须放行 `*.console.aliyun.com`。  
- **功能边界**：  
  - 文件连接器**不支持直接导入 JSON/CSV/YAML**，需转为 XLSX/XLS；  
  - `image_url` 字段要求 URL 公开可访问，百炼将主动抓取生成图片向量索引；  
  - 语雀连接器**仅适配公网版**，不支持私有部署语雀。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


