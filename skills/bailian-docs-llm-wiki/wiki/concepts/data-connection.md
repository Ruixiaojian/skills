# 数据连接

数据连接是阿里云百炼平台统一管理外部数据源的核心基础设施，为智能体、工作流、RAG 应用及 API 调用提供安全、可控、标准化的数据接入入口。它抽象了异构数据源的访问细节，将文件、表格、数据库、知识库等统一建模为可发现、可授权、可编排的连接器资源。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent 2.0）与工作流中**：数据连接器作为“工具”被自动注册并参与规划。例如，当用户提问“查一下上季度销售表”，Agent 可自主调用 `sql_query` 工具查询已配置的 MySQL 连接器；或调用 `knowledge_retrieval` 工具在文件类连接器的类目中进行 RAG 检索。无需硬编码，仅需在应用配置页关联对应连接器即可启用。

- **RAG 知识库构建**：文件类连接器（PDF/Word/Markdown）和表格类连接器（CSV/Excel）是知识库文档的主要来源。通过控制台导入或 API（如 `AddFile`、`AddCategory`）上传后，系统自动触发解析（支持 DOCMIND、Qwen-VL 等多引擎），生成向量化切片，供 `Retrieve` 接口实时检索。

- **API 集成开发**：通过 Application Component OpenAPI（`bailian/2023-12-29`）直接管理连接器生命周期：  
  - 创建连接器：`CreateConnector`（需指定类型与参数）；  
  - 管理数据：`AddCategory` / `AddFile`（文件类）、`AddTable`（表格类，*注：当前仅控制台支持新建表格，API 仅支持已有表格的元数据操作*）；  
  - 批量导入：`AddFilesFromAuthorizedOss` 支持从已授权 OSS Bucket 高效拉取文件。

- **高代码应用中**：开发者可通过环境变量注入连接器 ID 或 Workspace ID，在 Python 代码中调用 `dashscope` SDK 或百炼 OpenAPI，组合 `sql_query`、`searchOSSFile` 等工具实现定制化数据处理逻辑（如定时同步数据库 + 生成摘要报告）。

## 关键参数和配置

所有连接器均需配置以下基础字段，并按类型补充特定参数：

| 类型 | 必填参数 | 关键约束与说明 |
|------|----------|----------------|
| **通用** | `connector_name`、`description`、`workspace_id` | `workspace_id` 是权限与配额隔离边界，必须准确传入；名称需全局唯一且符合 `[a-zA-Z0-9_-]{1,64}` 规则 |
| **文件 / 表格（平台托管）** | `storage_type`（`PLATFORM` 或 `OSS`） | 若选 `OSS`，Bucket 必须添加标签 `bailian-connector-access: ReadAndWrite`；平台存储默认 1 TB 配额，超限需升配 |
| **MySQL / PostgreSQL / PolarDB-X 2.0** | `host`、`port`、`username`、`password`、`database_name` | ✅ 仅 DMS 方式创建的连接器支持运行时 SQL 查询；<br>✅ PostgreSQL 要求 `wal_level=logical` 且监听 `100.64.0.0/16`；<br>✅ 所有数据库需提前将百炼服务网段加入白名单 |
| **语雀** | `tenant_access_token` | [Token](token.md) 需具备目标知识库 `read` 权限；仅支持公网版语雀（`https://www.yuque.com`） |
| **OSS** | `bucket_name` | Bucket 必须添加标签 `bailian-datahub-access: read`；<br>⚠️ 不支持归档/冷归档存储类型；<br>⚠️ 开启 Referer 防盗链时，需放行 `*.console.aliyun.com` |

**解析与调用相关参数（文件类）**：  
- `parser`（API 中）：指定解析引擎，常用值：`DOCMIND`（通用文本）、`DOCMIND_LLM_VERSION`（大模型增强解析）、`DASH_QWEN_VL_PARSER`（多模态图文理解）；  
- `category_id`（API 中）：文件归属类目 ID，用于 RAG 检索范围控制；  
- `enable_vector_search`（OSS 连接器）：必须开通向量检索服务后才可用 `searchOSSFile` 工具。

## 面向开发者的重要提示

- **权限最小化**：所有连接器默认遵循最小权限原则。首次使用 DMS、OSS、PolarDB-X 等服务时，需完成对应 SLR 角色授权（如 `AliyunServiceRoleForSFMConnectorAccessDTS`），否则创建失败。
- **连接检测 ≠ 运行时可用**：“连接检测”仅验证网络连通性与基础鉴权，不保证后续 SQL 执行或文件解析成功。务必在应用中捕获工具调用异常（如 `SQLExecutionError`、`ParserTimeout`）。
- **文件生命周期注意**：控制台仅展示最近 90 天内导入的文件，但数据本身仍保留；若需长期存档，请自行备份至 OSS 或 NAS。
- **表格结构不可变**：Excel/CSV 表格一旦创建，字段名与类型锁定，修改需重建连接器。
- **推荐实践**：生产环境优先使用 `OSS + 平台托管` 混合模式——静态文档存 OSS（低成本、易管理），高频更新小表存平台（低延迟解析）；SQL 查询类场景务必通过 DMS 创建连接器以获得完整能力。

## 关联主题页

- [data connection overview](../guides/data-connection-overview.md)
- [application component api reference](../api/application-component-api-reference.md)
- [llm application](../guides/llm-application.md)
- [use cases](../guides/use-cases.md)


