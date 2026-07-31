# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的数据接入通道。它支持结构化与非结构化数据的接入，并通过平台托管或流处理两种模式实现数据的静态导入或实时查询。所有连接器均需满足前置权限与网络条件，且配置后可被智能体、RAG 应用等直接调用。

## 支持的模型/功能

数据连接器按数据访问方式分为两类：

- **平台托管类**：适用于离线导入场景，包括  
  - **文件连接器**：支持 PDF、Word、Markdown、图像、音视频等非结构化文档，依赖[文档理解](https://help.aliyun.com/zh/document-mind/product-overview/overview-of-document-understanding#9a4f5fb91fpps)能力进行多模态解析（如大模型文档解析、Qwen VL 解析）；  
  - **表格连接器**：支持 CSV、Excel（XLS/XLSX）等结构化数据，支持自定义表头与字段类型（含 `image_url` 类型用于以图搜图）。

- **流处理类**：适用于实时 SQL 查询或在线内容同步，包括  
  - **MySQL / PostgreSQL / PolarDB-X 2.0 连接器**：仅通过 **DMS 导入数据源** 方式创建的连接器支持执行 SQL 查询（参见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)）；  
  - **语雀连接器**：对接公网语雀知识库，依赖个人访问 [Token](../concepts/token.md)；  
  - **OSS 连接器**：访问自有 OSS Bucket 中的文件，需开通向量检索服务并配置 `bailian-datahub-access` 标签（参见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)）。

> **注意**：原始文档中对 OSS 连接器所需标签的命名存在不一致——文件/表格连接器要求 `bailian-connector-access`（值为 `ReadAndWrite`），而 OSS 连接器明确要求 `bailian-datahub-access`（值为 `read`）。请严格按各连接器类型对应标签配置，否则授权失败。该差异已在 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中分节说明，无需统一。

## 关键参数

| 连接器类型 | 必填参数 | 特殊要求 |
|------------|----------|----------|
| 文件 / 表格 | 连接器名称、描述、存储位置（平台存储 or OSS） | OSS Bucket 需添加 `bailian-connector-access: ReadAndWrite` 标签 |
| MySQL | 数据库用户名、密码、网络类型（公网/私网）、数据库实例（RDS）或地址（自建） | 公网需加白名单；仅 DMS 导入方式支持 SQL 执行 |
| PostgreSQL | 主机地址、端口、dbName、用户名、密码 | `wal_level=logical`；自建实例需开放 `100.64.0.0/16` 网段访问 |
| PolarDB-X 2.0 | 用户名、密码、所属地域（仅私网） | 仅支持阿里云实例；首次使用需授权 `AliyunServiceRoleForSFMConnectorAccessDTS` 和 `AliyunServiceRoleForSFMAccessPolarDBX` 角色 |
| 语雀 | Tenant access token | 仅支持公网语雀；[Token](../concepts/token.md) 需通过 [语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取 |
| OSS | OSS Bucket 名称 | Bucket 需开通向量检索服务；需添加 `bailian-datahub-access: read` 标签 |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击「创建连接器」→ 选择类型 → 填写基本信息与连接参数 → （可选）点击「开始检测」验证连通性 → 确认创建。  
2. **导入数据**（仅平台托管类）：  
   - 文件连接器：进入详情页 → 新建或选择类目 → 「导入数据」→ 本地上传 → 选择解析方式（推荐「大模型文档解析」以支持图表理解）→ 配置标签（可选）→ 确认；  
   - 表格连接器：进入详情页 → 新建或选择数据表 → 上传 Excel 或自定义表头（列名、类型必填，描述建议填写）→ 确保字段结构与文件完全一致 → 确认。  
3. **在应用中调用**：连接器创建成功后，可在智能体知识库配置、RAG 检索节点或 `searchOSSFile` 等工具中直接引用，无需额外开发适配层（详见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)）。

## 限制和注意事项

- **容量与时效**：  
  - 平台托管文件连接器免费额度为 200,000 个文件 / 1 TB；表格连接器为 1 TB（用尽后转按量付费）；  
  - 导入的文件仅支持查看最近 **90 天内** 的记录，超期不可见但不删除；  
  - 不支持归档、冷归档、深度冷归档类型的 OSS Bucket。

- **网络与权限**：  
  - MySQL 公网连接必须将百炼服务 IP 段加入数据库白名单；  
  - PolarDB-X 2.0 仅支持私网，且必须与实例同地域；  
  - RAM 用户需主账号授予 `AliyunBailianFullAccess` 或最小权限策略（含 `bailian:CreateConnector`, `bailian:DescribeConnectors` 等）。

- **功能边界**：  
  - MySQL/PostgreSQL/PolarDB-X 的「创建自定义数据源」方式**不支持 SQL 查询执行**，仅用于元数据同步（如表结构发现）；  
  - 语雀连接器**仅支持公网版本**，不兼容企业私有部署语雀；  
  - 文件连接器暂不支持直接导入 JSON、CSV、YAML，须先转换为 XLSX/XLS。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


