# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心机制，为应用提供安全、可控的数据接入能力。它支持结构化与非结构化数据的接入，并通过平台托管或流处理两种模式实现数据访问，是构建知识增强型智能体（Agent）和 RAG 应用的基础组件。所有连接器均需在业务空间内创建并绑定至具体应用，其配置直接影响后续检索与调用行为。

## 支持的模型/功能

数据连接器按数据访问模式分为两类：

- **平台托管类**：适用于文件（PDF/Word/Markdown 等）、表格（CSV/Excel 等）数据，数据可存储于百炼平台免费空间（200,000 文件 / 1 TB）或用户自有 OSS Bucket（需添加 `bailian-connector-access` 标签）。导入后经解析生成向量索引，支持语义检索。详细解析策略见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中“导入文件”章节。

- **流处理类**：支持 MySQL、PostgreSQL、PolarDB-X 2.0、语雀、OSS 五种实时数据源。其中数据库类连接器（MySQL/PostgreSQL/PolarDB-X 2.0）仅通过 **DMS 导入数据源方式创建** 的实例才支持执行 SQL 查询；自定义方式创建的连接器仅支持元数据同步，不支持直接 SQL 执行。该限制已在 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 多次明确强调。

> **注意**：OSS 连接器虽属流处理类型，但实际不执行实时查询，而是通过 `searchOSSFile` 和 `searchOSSFileByFileName` 工具触发向量检索或文件名匹配——这依赖已开通的 [向量检索服务](https://help.aliyun.com/zh/oss/user-guide/vector-retrieval/)，未开通则对应工具不可用。相关前提条件详见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) “OSS连接器”小节。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **连接器名称 & 描述** | 必填；描述建议包含数据内容与用途，用于指导智能体调用准确度 | 名称需唯一，描述长度 ≤ 500 字符 |
| **存储位置（文件/表格）** | 平台存储（免费额度）或自有 OSS Bucket（需 SLR 授权 + `bailian-connector-access` 标签） | Bucket 必须与百炼所在地域一致 |
| **数据库地址/端口/用户名/密码（MySQL/PostgreSQL/PolarDB-X）** | 自建库需手动输入；RDS 实例自动填充（禁用手动修改） | PostgreSQL 必须填写 `dbName`；MySQL 无此字段 |
| **wal_level（PostgreSQL）** | 必须设为 `logical`（默认为 `replica`） | 否则无法建立逻辑复制通道，连通性检测失败 |
| **语雀 Tenant Access [Token](../concepts/token.md)** | 从 [语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取 | 仅支持公网语雀，[Token](../concepts/token.md) 需具备读取知识库权限 |
| **OSS Bucket 标签** | 必须为 `bailian-datahub-access: read`（注意非 `bailian-connector-access`） | 标签值区分大小写，错误将导致访问拒绝 |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击“创建连接器” → 选择类型 → 填写基本信息与连接参数 → （可选）点击“开始检测”验证连通性 → 确认创建。

2. **导入数据**：
   - *文件/表格*：进入连接器详情页 → 在类目或数据表管理下 → 选择“本地上传” → 配置解析方式（推荐默认）与标签 → 提交。
   - *数据库/语雀/OSS*：无需主动导入，连接建立后即可在应用中通过工具调用（如 `querySQL`, `searchYuQueDoc`, `searchOSSFile`）。

3. **在应用中调用**：连接器需在智能体或工作流中显式引用。平台会根据连接器类型自动注入对应工具（Tool），开发者通过 `tool_calls` 或 `function calling` 触发，无需编写底层数据访问代码。

## 限制和注意事项

- **网络限制**：PolarDB-X 2.0 连接器**仅支持私网**，不支持公网；MySQL/PostgreSQL 公网连接需将百炼服务 IP 段加入数据库白名单（具体段位见控制台提示）。
- **权限要求**：RAM 用户需被授予 `AliyunBailianFullAccess` 或最小化权限策略（含 `bailian:CreateConnector`, `bailian:InvokeConnector` 等动作）；OSS/Bucket/DMS/EventBridge/DTS/PolarDB-X 等服务的 SLR 授权必须完成，否则创建失败。
- **文件限制**：单文件最大 100 MB；不支持 JSON/YAML 直接导入（需转 XLSX/XLS）；归档/冷归档/深度冷归档类型 OSS Bucket 不支持。
- **时效性**：导入的文件仅支持查看最近 90 天记录（后台仍保留）；语雀连接器依赖 [Token](../concepts/token.md) 有效期，过期后需重新配置。
- **安全约束**：所有连接器均隔离于业务空间，跨空间不可见；平台不会将导入数据用于训练或商业用途。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


