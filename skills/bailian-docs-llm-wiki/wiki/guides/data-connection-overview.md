# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可配置的数据接入入口。通过数据连接器，应用可在对话中实时查询或引用企业数据库、文档系统及对象存储中的结构化与非结构化数据。所有连接器均支持向量化索引构建与语义检索，部分类型还支持原生SQL执行。

## 支持的模型/功能

数据连接器按数据访问模式分为两类：**平台托管型**（文件、表格）和**流处理型**（MySQL、PostgreSQL、PolarDB-X 2.0、语雀、OSS）。  
- **平台托管型**：数据导入至百炼平台或用户自有OSS，经解析后构建向量索引，供RAG类应用调用；支持文档智能解析、大模型文档解析（含Qwen-VL）、音视频解析等[多模态](../concepts/multimodal.md)处理能力，详见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)。  
- **流处理型**：数据保留在源端，运行时按需拉取；其中 MySQL、PostgreSQL 和 PolarDB-X 2.0 连接器**仅当通过 DMS 导入数据源方式创建时**才支持 SQL 查询执行；语雀与 OSS 连接器则专注于实时内容检索与文件访问。  
- 所有连接器均可与智能体（Agent 1.0）集成，并通过 `searchOSSFile`、`searchOSSFileByFileName` 等工具调用，具体能力依赖于底层服务开通状态，参见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中关于向量检索服务的要求。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **通用** | 连接器名称、描述 | 名称需唯一且易识别；描述影响智能体对数据用途的理解准确度，建议明确数据内容与业务场景。 |
| **文件/表格** | 存储位置（平台存储 / 自有OSS） | 平台存储提供免费额度（文件连接器限200,000个文件/1 TB，表格连接器限1 TB）；自有OSS需添加 `bailian-connector-access` 标签（值为 `ReadAndWrite`），详见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)。 |
| **数据库类** | 数据库地址、端口、用户名、密码、dbName（PostgreSQL/PolarDB-X 必填） | MySQL 默认端口3306，PostgreSQL 默认5432；PolarDB-X 2.0 **仅支持私网连接**，且必须选择所属地域。 |
| **语雀/OSS** | Tenant access token（语雀）、Bucket 名称（OSS） | 语雀 [Token](../concepts/token.md) 需通过[语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取；OSS Bucket 需添加 `bailian-datahub-access` 标签（值为 `read`），并开通向量检索服务。 |

> **注意**：PostgreSQL 连接器要求数据库实例 `wal_level = logical`，而 MySQL 无此要求；但两者的 DMS 导入方式均是启用 SQL 查询的**唯一前提**，该限制在原始文档中被多次强调，需严格遵循。

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击「创建连接器」→ 选择类型 → 填写基本信息与连接参数 → （可选）点击「开始检测」验证连通性 → 确认创建。  
2. **导入数据（仅平台托管型）**：  
   - 文件连接器：进入详情页 → 新建或选择类目 → 「导入数据」→ 本地上传 → 选择解析方式（默认/自定义）→ 配置标签（可选）→ 确认。注意：JSON/CSV/YAML 需先转为 XLSX/XLS 再导入。  
   - 表格连接器：进入详情页 → 新建或选择数据表 → 上传 Excel 或自定义表头（列名、类型必填，描述建议填写）→ 确认。**表结构一旦确定不可修改**。  
3. **调用数据**：在智能体或 API 调用中，通过预置工具（如 `searchFile`、`searchTable`、`executeSQL`）访问对应连接器数据；OSS 连接器需依赖已开通的向量检索服务方可使用 `searchOSSFile` 工具。

## 限制和注意事项

- **网络与权限**：MySQL/PostgreSQL/PolarDB-X 连接器需确保网络可达（公网需加白名单，私网需同地域）；RAM 用户须由主账号授予数据连接管理权限，授权方法见 [权限管理](https://help.aliyun.com/zh/model-studio/application-permission-management-overview)。  
- **功能限制**：  
  - MySQL/PostgreSQL/PolarDB-X 的 SQL 查询能力**仅限 DMS 导入方式创建的连接器**；自定义数据源方式创建的连接器不支持 `executeSQL` 工具。  
  - OSS 连接器**不支持归档、冷归档、深度冷归档存储类型的 Bucket**；开启 Referer 防盗链的 Bucket 需将 `*.console.aliyun.com` 加入白名单。  
  - 文件连接器导入的文件仅保留最近 90 天的查看记录（后台存储不受影响）；每个业务空间最多 500 个类目，超限时需提工单扩容。  
- **兼容性说明**：语雀连接器**仅支持公网版本语雀**，不支持私有化部署版本；PolarDB-X 2.0 连接器**不支持自建数据库**，仅限阿里云 PolarDB-X 2.0 实例。  
- **解析能力差异**：电子文档解析不支持插图与图表；文档智能解析可提取图中文本并生成摘要；大模型文档解析（含 Qwen-VL）支持对插图/图表内容提问——该能力细节请参考 [文档理解](https://help.aliyun.com/zh/document-mind/product-overview/overview-of-document-understanding#9a4f5fb91fpps)，亦在 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中有明确说明。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


