# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的实时数据访问入口。它支持结构化与非结构化数据源的接入，并通过平台托管或流处理两类模式实现数据读取与检索。开发者可基于业务场景选择适配的连接器类型，并在智能体或 API 调用中直接引用已配置的数据源。

## 支持的模型/功能

数据连接器按数据访问模式分为两类：

- **平台托管型**：适用于文件（PDF/Word/Markdown）、表格（CSV/Excel）类非结构化与轻量结构化数据。数据导入后由百炼平台统一存储、解析并构建向量索引，支持语义检索与[多模态](../concepts/multi-modal.md)理解（如图表识别需启用[大模型文档解析](https://help.aliyun.com/zh/document-mind/product-overview/overview-of-document-understanding#9a4f5fb91fpps)）。详见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中“文件连接器”与“表格连接器”章节。

- **流处理型**：适用于需实时查询的数据库与在线知识库，包括 MySQL、PostgreSQL、PolarDB-X 2.0、语雀和 OSS。此类连接器不导入数据副本，而是按需执行 SQL 查询或 API 检索，适用于动态数据场景。其中仅通过 DMS 导入方式创建的 MySQL/PostgreSQL/PolarDB-X 连接器支持 SQL 执行；自定义方式创建的同类连接器**不支持 SQL 查询**（参见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) “MySQL连接器”与“PostgreSQL连接器”说明）。

> **注意**：OSS 连接器虽属流处理型，但其 `searchOSSFile` 和 `searchOSSFileByFileName` 工具依赖向量检索服务，该服务需手动开通；而文件/表格连接器的向量索引构建则由平台自动完成，无需额外开通——二者能力边界存在差异，不可混用。

## 关键参数

| 连接器类型 | 必填参数 | 特殊要求 | 检测机制 |
|------------|----------|----------|----------|
| 文件/表格 | 连接器名称、描述、存储位置（平台存储/OSS） | 平台存储有额度限制（文件连接器限 200,000 文件/1 TB；表格连接器 1 TB 免费额度）；OSS Bucket 需添加 `bailian-connector-access` 标签（值 `ReadAndWrite`） | 无主动连通性检测，依赖上传/导入任务状态 |
| MySQL | 数据库地址、端口、用户名、密码；若为 RDS 实例则需实例 ID | 公网连接需白名单放行指定 IP 段；`wal_level` 无特殊要求 | EventBridge 服务检测 |
| PostgreSQL | 主机地址、端口、数据库名（`dbName`）、用户名、密码 | `wal_level=logical`；自建实例需配置 `listen_addresses` 允许 `100.64.0.0/16` 访问；用户需具备 `REPLICATION` 或 Superuser 权限 | DTS 服务检测 |
| PolarDB-X 2.0 | 数据库用户名、密码；仅支持私网连接 | 仅支持阿里云实例；首次使用需授权 `AliyunServiceRoleForSFMConnectorAccessDTS` 与 `AliyunServiceRoleForSFMAccessPolarDBX` 角色 | EventBridge 检测（同 MySQL） |
| 语雀 | Tenant access token | 仅支持公网语雀；[Token](../concepts/token.md) 需通过 [语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取 | [Token](../concepts/token.md) 校验接口调用 |
| OSS | Bucket 名称 | Bucket 需添加 `bailian-datahub-access` 标签（值 `read`）；不支持归档/冷归档存储类型；Referer 防盗链需白名单 `*.console.aliyun.com` | Bucket 权限与标签校验 |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击“创建连接器” → 选择类型 → 填写基本信息与连接参数 → （可选）执行连通性检测 → 确认创建。  
2. **导入数据（仅平台托管型）**：
   - 文件连接器：进入详情页 → 选择类目 → “导入数据” → 本地上传 → 选择解析方式（推荐默认设置；图表理解需选“大模型文档解析”）→ 配置标签（可选）→ 提交。
   - 表格连接器：进入详情页 → 新建或选择数据表 → 上传 Excel 或自定义表头（列名、类型必填；`image_url` 字段需确保 URL 公开可访问）→ 提交。  
3. **在应用中调用**：连接器创建成功后，可在智能体工作流中作为知识库数据源绑定，或通过 API 的 `knowledge_sources` 参数引用（格式：`{ "type": "connector", "id": "<connector_id>" }`）。具体集成方式请参考 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中“导入数据”与“在应用中使用”部分。

## 限制和注意事项

- **权限约束**：RAM 用户需主账号授予 `AliyunBailianFullAccess` 或最小化自定义策略（含 `bailian:ListConnectors`, `bailian:CreateConnector` 等动作），否则无法创建或管理连接器。
- **网络限制**：
  - MySQL/PostgreSQL 支持公网与私网；PolarDB-X 2.0 **仅支持私网**，且必须与百炼服务同地域。
  - 自建数据库需确保出方向防火墙放行百炼服务 IP 段（如 `100.64.0.0/16`）。
- **数据时效性**：
  - 平台托管型：文件/表格导入后生成静态副本，更新需重新上传；90 天内可查看历史导入记录，超期仅保留索引不可预览。
  - 流处理型：数据始终实时，但语雀/OSS/数据库查询受目标服务稳定性影响。
- **功能限制**：
  - 不支持 JSON/YAML 直接导入（表格连接器需转为 XLSX/XLS）。
  - MySQL/PostgreSQL/PolarDB-X 的 SQL 执行能力**严格依赖 DMS 导入方式**，自定义方式创建的连接器仅支持元数据同步，不可执行查询。
  - OSS 连接器的向量检索能力（`searchOSSFile`）需单独开通 [向量检索服务](https://help.aliyun.com/zh/oss/user-guide/vector-retrieval/)，否则相关工具不可用。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


