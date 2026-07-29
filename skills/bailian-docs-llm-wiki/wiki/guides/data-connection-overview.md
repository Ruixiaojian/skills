# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的数据接入通道。它支持结构化与非结构化数据的接入，并通过平台托管或流处理两种模式实现数据访问与实时查询。所有连接器均需在控制台创建并配置权限后方可被智能体或API调用。

## 支持的模型/功能

数据连接器按数据访问方式分为两类：

- **平台托管型**：适用于文件（PDF/Word/Markdown等）和表格（CSV/Excel等）类非实时数据。数据导入后由百炼平台统一向量化并构建知识库索引，支持语义检索、标签过滤及多模态解析（如[文档理解](https://help.aliyun.com/zh/document-mind/product-overview/overview-of-document-understanding#9a4f5fb91fpps)中描述的Qwen VL解析、音视频解析等）。详见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中“导入文件”与“导入表格”章节。

- **流处理型**：适用于需实时访问的数据库与在线服务，包括 MySQL、PostgreSQL、PolarDB-X 2.0、语雀和 OSS。其中仅通过 **DMS 导入数据源** 方式创建的 MySQL/PostgreSQL/PolarDB-X 连接器支持执行 SQL 查询；其余方式（如自定义数据源）仅支持元数据发现与基础连接验证。OSS 连接器需开通[向量检索服务](https://help.aliyun.com/zh/oss/user-guide/vector-retrieval/)才可使用 `searchOSSFile` 等工具。该设计细节在 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 的各连接器说明中明确区分。

> **注意**：语雀连接器**仅支持公网版本语雀**，不兼容私有部署版；OSS 连接器**不支持归档、冷归档或深度冷归档存储类型**的 Bucket —— 这些限制在 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) “OSS连接器”小节末尾有明确标注，开发者须提前校验存储类型。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **通用** | 连接器名称、描述 | 名称需唯一且易识别；描述影响智能体调用准确度，建议包含数据内容与用途（如“财务部2024Q1销售报表”）。 |
| **平台托管（文件/表格）** | 存储位置（平台存储 / 自有OSS） | 平台存储提供免费额度（文件：200,000个/1TB；表格：1TB），超限后转按量付费；自有OSS需添加 `bailian-connector-access` 标签（值 `ReadAndWrite`）。 |
| **流处理（数据库）** | 数据库地址、端口、用户名、密码、dbName（PostgreSQL必填） | MySQL 默认端口 3306，PostgreSQL 默认 5432；PolarDB-X 2.0 **仅支持私网**，且必须选择所属地域。 |
| **流处理（语雀/OSS）** | Tenant access token（语雀）、Bucket 名称（OSS） | 语雀 [Token](../concepts/token.md) 需从[语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取；OSS Bucket 需添加 `bailian-datahub-access` 标签（值 `read`），并确保当前账号具备访问权限。 |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击“创建连接器” → 选择类型 → 填写基本信息与连接参数 → （可选）点击“开始检测”或“连接检测”验证连通性 → 确认创建。

2. **导入数据（仅平台托管型）**：
   - 文件连接器：进入详情页 → 选择类目 → “导入数据” → 本地上传 → 选择解析方式（默认/自定义）→ 配置标签（可选）→ 确认。
   - 表格连接器：进入详情页 → 数据表管理 → 新建或选择数据表 → 上传 Excel 或自定义表头（列名、类型必填，描述建议填写）→ 确认。

3. **调用数据**：
   - 平台托管型：通过知识库检索接口（如 `retrieveFromKnowledgeBase`）或智能体内置工具自动触发；
   - 流处理型：MySQL/PostgreSQL/PolarDB-X 需通过 DMS 导入方式创建后，方可使用 `executeSQL` 工具；语雀/OSS 使用对应工具（如 `searchYuQueDoc`、`searchOSSFile`）。

完整操作流程与界面指引见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

## 限制和注意事项

- **权限要求**：RAM 用户需主账号授予 `AliyunBailianFullAccess` 或最小权限策略（含 `bailian:CreateConnector`、`bailian:DescribeConnectors` 等动作），授权方法参见[权限管理](https://help.aliyun.com/zh/model-studio/application-permission-management-overview)。
- **网络与配置依赖**：
  - PostgreSQL 必须将 `wal_level` 设置为 `logical`，且自建实例需配置 `listen_addresses` 允许 `100.64.0.0/16` 访问；
  - MySQL/PolarDB-X 自建实例需确保网络可达，并将百炼服务 IP 段加入白名单；
  - PolarDB-X 2.0 **不支持公网连接**，且仅限阿里云实例。
- **文件处理限制**：
  - 不支持直接导入 JSON、CSV、YAML；需先转为 XLSX/XLS；
  - 导入文件仅保留最近 90 天的查看记录（但数据本身不删除）；
  - 电子文档解析不支持插图与图表识别；如需图文理解，必须选用“大模型文档解析”或“Qwen VL解析”。
- **OSS 特别说明**：若 Bucket 启用 Referer 防盗链，须将 `*.console.aliyun.com` 加入白名单 Referer，否则连接失败。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


