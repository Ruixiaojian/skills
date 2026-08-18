# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可配置的数据接入入口。通过数据连接器，应用可在对话中实时查询或引用企业数据库、文档系统及对象存储中的结构化与非结构化数据。所有连接器均支持向量化索引与语义检索，是构建 RAG 应用和智能体知识库的基础组件。

## 支持的模型/功能

数据连接器按数据访问模式分为两类：

- **平台托管型**：适用于文件（PDF/Word/Markdown 等）和表格（CSV/Excel 等），数据可托管于百炼平台（免费额度：200,000 文件 / 1 TB）或用户自有 OSS Bucket。文件类支持多种解析方式（电子文档解析、文档智能解析、大模型文档解析、Qwen VL 解析、音视频解析）；表格类支持自动表头识别或自定义 Schema 定义，字段类型包括 `string`、`number`、`boolean`、`image_url` 等。  
- **流处理型**：适用于需实时查询的数据库与 SaaS 服务，包括 MySQL、PostgreSQL、PolarDB-X 2.0、语雀 和 OSS（仅限文件元数据与内容读取）。其中，**仅通过 DMS 导入数据源方式创建的 MySQL/PostgreSQL/PolarDB-X 连接器支持执行 SQL 查询**；其余方式（如自定义数据源）仅支持元数据同步与向量索引构建，不支持运行时 SQL 执行。该限制详见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

> **注意**：OSS 连接器在原始文档中被归类为“流处理”，但其实际行为更接近平台托管——它不执行实时 SQL，而是通过 `searchOSSFile` 和 `searchOSSFileByFileName` 工具进行向量/关键词检索。该分类逻辑与 MySQL/PostgreSQL 的流式 SQL 查询存在语义偏差，建议以功能为准，而非类型标签。详见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **通用** | 连接器名称、描述 | 名称需唯一且可识别；描述将参与 LLM 检索路由决策，**必须明确说明数据内容与业务用途**。 |
| **文件/表格** | 存储位置（平台存储 / 自有 OSS） | 使用自有 OSS 时，Bucket 必须添加 `bailian-connector-access` 标签（值为 `ReadAndWrite`）；OSS 连接器则需 `bailian-datahub-access`（值为 `read`）。[原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中明确区分了两类标签用途。 |
| **MySQL/PostgreSQL/PolarDB-X** | 网络类型、SLR 授权、wal_level（PostgreSQL）、dbName（PostgreSQL）、实例地域（PolarDB-X） | MySQL 默认端口 3306，PostgreSQL 默认 5432；PostgreSQL 要求 `wal_level=logical`；PolarDB-X **仅支持私网**且必须选择所属地域；所有数据库连接均需具备读权限，PostgreSQL 还需 Superuser 或 REPLICATION 权限。 |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击「创建连接器」→ 选择类型 → 填写基本信息与连接参数 → （可选）点击「开始检测」验证连通性 → 确认创建。  
2. **导入数据**（仅平台托管型）：  
   - **文件**：进入连接器详情页 → 选择类目 → 「导入数据」→ 本地上传 → 选择解析方式（推荐「大模型文档解析」以支持图表理解）→ 配置标签（可选，用于 API 调用时过滤）→ 确认。  
   - **表格**：进入连接器详情页 → 「数据表管理」→ 新建数据表 → 选择「直接上传 Excel」（自动推导 Schema）或「自定义表头」（手动定义列名、类型、描述）→ 上传文件 → 确认。  
3. **调用数据**：在智能体或应用中，通过内置工具（如 `searchFile`、`searchTable`、`executeSQL`）调用对应连接器；API 请求中可通过 `tags` 参数指定文件标签，提升检索精度。

## 限制和注意事项

- **容量与时效**：平台托管文件仅保留最近 90 天的导入记录（不可见但未删除）；单业务空间最多 500 个文件类目，超限需提工单扩容。  
- **格式限制**：文件连接器**不支持直接导入 JSON/CSV/YAML**，需转为 XLSX/XLS；OSS 连接器**不支持归档/冷归档/深度冷归档存储类型**的 Bucket。  
- **网络与权限**：  
  - MySQL 公网连接需将百炼服务 IP 段加入数据库白名单；  
  - PostgreSQL 自建实例需配置 `listen_addresses` 允许 `100.64.0.0/16` 访问；  
  - PolarDB-X 仅支持私网，且首次使用需显式授权 `AliyunServiceRoleForSFMConnectorAccessDTS` 与 `AliyunServiceRoleForSFMAccessPolarDBX` 角色。  
- **功能边界**：  
  - `executeSQL` 工具仅对 DMS 导入方式创建的 MySQL/PostgreSQL/PolarDB-X 连接器可用；  
  - OSS 连接器的 `searchOSSFile` 工具依赖向量检索服务开通，未开通则不可用；  
  - 语雀连接器**仅支持公网版语雀**，且需 Tenant Access Token（非个人 Token）。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


