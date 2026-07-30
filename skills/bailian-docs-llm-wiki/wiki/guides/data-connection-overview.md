# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的数据接入通道。它支持将企业自有数据库、文档系统、对象存储等异构数据源接入百炼，实现对话中实时查询与知识引用。所有连接器均基于统一权限模型与网络隔离策略设计，开发者可按需选择托管式或流处理式接入方式。

## 支持的模型/功能

数据连接器分为两类：**平台托管型**（文件、表格）和**流处理型**（MySQL、PostgreSQL、PolarDB-X 2.0、语雀、OSS）。  
- **平台托管型**：数据导入百炼平台或自有OSS，经解析后构建向量知识库，供RAG类应用调用；支持文档智能解析、大模型文档解析（含图表理解）、音视频[多模态](../concepts/multi-modal.md)解析等能力，详见 [文档理解](https://help.aliyun.com/zh/document-mind/product-overview/overview-of-document-understanding#9a4f5fb91fpps)。  
- **流处理型**：数据保留在源端，通过实时连接执行查询或检索。其中 MySQL、PostgreSQL 和 PolarDB-X 2.0 连接器**仅当通过 DMS 导入数据源方式创建时才支持 SQL 查询**；语雀和 OSS 连接器则提供知识库级检索能力（如 `searchOSSFile` 工具），但需提前开通[向量检索服务](https://help.aliyun.com/zh/oss/user-guide/vector-retrieval/)。  
> **注意**：原始文档中对“文件连接器”和“表格连接器”的存储额度描述存在不一致——前者称平台存储“限时免费”，后者称“1 TB 免费额度，额度用完后自动转为按量付费”。该差异已在 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中明确体现，建议以控制台实时配额为准。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **通用** | 连接器名称、描述 | 名称需唯一且易识别；描述影响智能体调用准确度，建议说明数据内容与业务用途 |
| **文件/表格** | 存储位置（平台存储 / 自有OSS） | 使用自有OSS需完成RAM授权，并为目标Bucket添加 `bailian-connector-access` 标签（值为 `ReadAndWrite`） |
| **MySQL/PostgreSQL/PolarDB-X** | 网络类型（公网/私网）、数据库地址、端口、用户名、密码 | MySQL 默认端口 3306，PostgreSQL 默认 5432；PolarDB-X **仅支持私网**；PostgreSQL 必须设置 `wal_level=logical` |
| **语雀** | Tenant access token | 仅支持公网语雀，[Token](../concepts/token.md) 需从 [语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取 |
| **OSS** | Bucket 选择、`bailian-datahub-access` 标签 | Bucket 需设为 `read` 权限标签；不支持归档/冷归档存储类型 |

## 使用方式

1. **创建连接器**：访问 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击“创建连接器” → 选择类型 → 填写基本信息与连接参数 → 完成授权与连通性检测。  
2. **导入数据**（仅文件/表格）：进入连接器详情页 → 选择类目（文件）或数据表（表格）→ 上传本地文件或配置表结构 → 选择解析方式（推荐默认设置，复杂图表建议选“大模型文档解析”）→ 提交任务。  
3. **调用数据**：在智能体或API调用中，通过工具名（如 `searchOSSFile`、`queryMySQL`）触发对应连接器能力；标签（`tags`）可用于过滤文件范围，提升检索效率，具体参见 [应用调用指南](https://help.aliyun.com/zh/model-studio/application-calling-guide#4100253b7chc3)。  
> 注意：文件导入后作为独立副本存储，**仅支持查看最近90天内导入的文件**；超过时间仍可被知识库检索，但控制台不可见。

## 限制和注意事项

- **权限要求**：必须由主账号或已授予 `AliyunBailianDataConnectorFullAccess` 权限的 RAM 用户操作；DMS 相关连接器首次使用需完成 EventBridge、DTS 及对应数据库服务的 SLR 授权。  
- **网络与兼容性**：  
  - MySQL/PostgreSQL 自建实例需确保 `100.64.0.0/16` 网段可达（PostgreSQL 还需配置 `pg_hba.conf`）；  
  - PolarDB-X 2.0 **不支持自建实例**，且仅限私网访问；  
  - OSS Bucket 若启用 Referer 防盗链，须将 `*.console.aliyun.com` 加入白名单。  
- **功能限制**：  
  - 文件连接器**不支持直接导入 JSON/CSV/YAML**，需先转为 XLSX/XLS；  
  - 表格连接器的数据表结构（列名、类型）**创建后不可修改**；  
  - image_url 字段要求链接**公开可访问**，否则图片索引构建失败。  
- **资源约束**：平台托管文件连接器提供最多 200,000 个文件、1 TB 存储（限时免费）；表格连接器平台存储为 1 TB 免费额度（用尽后按量计费），详见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


