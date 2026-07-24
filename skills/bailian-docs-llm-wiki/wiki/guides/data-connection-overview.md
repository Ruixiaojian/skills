# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心机制，为应用和智能体提供安全、可控的数据接入能力。它支持结构化与非结构化数据的导入与实时访问，并通过向量化与索引构建支撑语义检索。所有连接器均需在业务空间内创建，且权限受RAM策略约束。

## 支持的模型/功能

数据连接器按数据访问模式分为两类：**平台托管型**（文件、表格）与**流处理型**（MySQL、PostgreSQL、PolarDB-X 2.0、语雀、OSS）。  
- **平台托管型**：数据上传至百炼平台或自有OSS，经解析后构建向量知识库，供RAG类应用调用；支持文档智能解析、大模型文档解析（含Qwen-VL）、音视频解析等[多模态](../concepts/multi-modal.md)处理能力，详见[原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。  
- **流处理型**：数据保留在源端，应用通过工具（如 `searchSQL`、`searchYuque`、`searchOSSFile`）发起实时查询；其中仅通过 **DMS导入数据源方式** 创建的 MySQL/PostgreSQL/PolarDB-X 连接器支持执行 SQL 查询，自定义方式创建的连接器不支持该能力 —— 此限制在[原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)中明确强调。  
> **注意**：文档中“OSS连接器”说明其需开通向量检索服务才可使用 `searchOSSFile` 工具，但同节又指出“支持私有Bucket”，而向量检索服务对私有Bucket的访问依赖STS临时凭证与Bucket Policy配合；实际部署时请以[原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)中“添加 `bailian-datahub-access` 标签”及OSS控制台权限配置为准，避免因权限链断裂导致工具调用失败。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **通用** | 连接器名称、描述 | 名称需唯一且易识别；描述影响智能体对数据用途的理解准确度，建议包含数据内容与业务场景 |
| **文件/表格** | 存储位置（平台存储 / 自有OSS） | 平台存储提供免费额度（文件：20万文件/1TB；表格：1TB），超限后转按量付费；自有OSS需授权并打标 `bailian-connector-access: ReadAndWrite`（文件/表格）或 `bailian-datahub-access: read`（OSS） |
| **数据库类** | 网络类型、数据库地址/端口、用户名/密码、dbName（PostgreSQL必填） | MySQL/PolarDB-X 支持公网/私网（PolarDB-X 仅私网），PostgreSQL 需 `wal_level=logical`；所有数据库连接均需确保账号具备读取权限及必要系统权限（如 PostgreSQL 的 REPLICATION） |
| **语雀/OSS** | Tenant access token（语雀）、OSS Bucket（OSS） | 语雀 [Token](../concepts/token.md) 需通过[语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取；OSS Bucket 不支持归档/冷归档存储类型 |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击「创建连接器」→ 选择类型 → 填写基本信息与连接参数 → 完成授权与连通性检测。  
2. **导入数据**：  
   - 文件连接器：进入详情页 → 选择类目 → 「导入数据」→ 本地上传 → 选择解析方式（默认/自定义）→ 配置标签（可选）→ 确认。注意：JSON/CSV/YAML 需先转为 XLSX/XLS 才能导入。  
   - 表格连接器：进入详情页 → 「数据表管理」→ 新建数据表 → 选择「直接上传Excel」或「自定义表头」→ 上传文件 → 确认。表结构一旦创建不可修改。  
3. **在应用中调用**：将连接器绑定至知识库后，智能体可通过内置工具（如 `searchFile`、`searchSQL`）访问数据；调用时可通过 `tags` 参数实现基于标签的预过滤，提升检索效率，具体用法见[原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

## 限制和注意事项

- **容量与时效**：平台托管文件仅支持查看最近 90 天内导入的记录；文件解析在高并发下可能排队或超时，建议错峰操作。  
- **网络与权限**：  
  - MySQL 公网连接需将百炼服务 IP 段加入数据库白名单；  
  - PolarDB-X 仅支持私网，且实例地域必须与百炼工作空间一致；  
  - OSS Bucket 若开启 Referer 防盗链，须将 `*.console.aliyun.com` 加入白名单。  
- **功能边界**：  
  - 文件连接器不支持直接导入 JSON/CSV/YAML；  
  - 表格连接器中 `image_url` 字段要求 URL 公开可访问，否则图片索引构建失败；  
  - 所有数据库连接器均**不支持写操作**，仅限只读查询。  
- **安全合规**：导入数据作为独立副本存储于百炼平台，与原始数据无关联；百炼不会将数据用于商业用途或对外公开。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


