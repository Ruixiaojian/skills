# 数据连接

数据连接是百炼平台统一管理外部数据源的核心基础设施能力，为智能体、工作流、RAG 应用等提供安全、可控、低侵入的数据接入通道。它抽象了异构数据源的访问细节，使开发者无需自行维护连接池、权限同步或数据同步逻辑，即可在推理过程中按需检索、引用企业自有数据库、文档系统或对象存储中的实时或静态数据。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent 2.0）中**：数据连接作为内置工具被自动注册，例如 `searchFileByContent`（文件连接器）、`searchOSSFile`（OSS 连接器）、`executeSQL`（MySQL/PostgreSQL/PolarDB-X 连接器）。智能体可根据用户问题自主规划调用，实现“查文档+跑SQL+读语雀”的多源协同推理。
- **工作流（Workflow）中**：通过「数据连接」节点显式调用，支持配置输入变量（如 SQL 查询语句、文件关键词、语雀知识库 ID），并将返回结果注入后续大模型或条件判断节点，实现确定性数据驱动流程。
- **知识库构建中**：文件类数据连接器（文件/表格）是知识库的主要数据源。上传的 PDF、Word、Excel 等文件经解析后生成向量索引，供 RAG 检索使用；OSS 连接器则可作为大规模非结构化数据的直连检索入口（启用向量检索服务后）。
- **高代码应用中**：通过 Application Component API（如 `ListFile`, `DescribeFile`, `ExecuteSQL`）编程调用，结合 SDK 实现细粒度控制，例如按标签筛选文件、分页拉取数据库结果、动态构造语雀目录树。
- **MCP 工具集成中**：数据连接器可封装为符合 MCP 协议的标准工具，暴露给第三方智能体调用，实现跨平台数据能力复用。

## 关键参数和配置

所有数据连接器均需配置以下通用参数：
- `connector_name`：连接器名称（唯一标识，不可重复）
- `description`：简要说明（用于团队协作识别）
- `workspace_id`：所属业务空间 ID（强制作用域隔离）

按类型区分的关键参数如下：

| 连接器类型 | 必填参数 | 特殊要求 | 连通性验证方式 |
|------------|----------|----------|----------------|
| **文件 / 表格** | 存储位置（平台托管 或 OSS Bucket） | OSS Bucket 需添加标签 `bailian-connector-access: ReadAndWrite` | 控制台「开始检测」触发元数据探查 |
| **MySQL** | 地址、端口、用户名、密码、数据库名（或 RDS 实例 ID） | RDS 需授权 SLR；自建需开放白名单 IP 段（含 `100.64.0.0/16`） | EventBridge 触发心跳探测 |
| **PostgreSQL** | 主机、端口、dbName、用户名、密码 | `wal_level=logical`；自建需配置 `pg_hba.conf` 允许 `100.64.0.0/16` | DTS 同步链路健康检查 |
| **PolarDB-X 2.0** | RDS 实例 ID、用户名、密码 | **仅支持私网**；首次使用需授权两个 Service Role | EventBridge 探测 |
| **语雀** | Tenant access token（从[语雀开放平台](https://www.yuque.com/yuque/developer/api)获取） | **仅支持公网语雀**；[Token](token.md) 需具备 `repo.read` 权限 | 内置 [Token](token.md) 校验 + 目录列表请求 |
| **OSS** | Bucket 名称 | Bucket 需开通[向量检索服务](https://help.aliyun.com/zh/oss/user-guide/vector-retrieval/)，并添加标签 `bailian-datahub-access: read` | 控制台自动校验 `ListObjectsV2` 和向量服务权限 |

> ⚠️ 注意：  
> - 文件连接器不支持直接导入 JSON/CSV/YAML，须转为 XLSX/XLS；表格连接器上传结构必须与预设表头严格一致。  
> - PolarDB-X 2.0 **不支持公网访问**；MySQL/PostgreSQL 若走公网，必须将百炼服务 IP 段加入白名单。  
> - 所有 OSS 连接器**不支持归档/冷归档/深度冷归档存储类型**；若启用 Referer 防盗链，需放行 `*.console.aliyun.com`。

## 面向开发者，简洁实用

- ✅ **创建即用**：控制台创建后，连接器自动注册为内置工具，无需额外编码即可在智能体或工作流中调用。  
- ✅ **API 完整覆盖**：通过 Application Component OpenAPI（`AddConnector`, `ExecuteSQL`, `ListFile`, `AddFilesFromAuthorizedOss` 等）实现全生命周期自动化管理，支持 CI/CD 集成。  
- ✅ **权限最小化**：每个连接器独立绑定 RAM 权限策略（如 `sfm:ConnectorRead`, `sfm:SQLExecute`），避免越权风险。  
- ✅ **调试友好**：控制台提供「检测连通性」按钮，失败时明确提示网络、权限或配置错误原因（如 “Bucket 标签缺失”、“[Token](token.md) 过期”、“RDS 未授权 SLR”）。  
- ✅ **生产就绪**：平台托管型数据默认加密存储于百炼专属环境，与原始数据物理隔离；流处理型保持原位不动，满足数据主权与合规审计要求。  

> 💡 提示：生产环境推荐优先使用 `session_file_id`（通过 `ApplyFileUploadLease` 获取）替代直传 URL；SQL 类连接器务必在 DMS 中完成数据源导入，否则无法执行查询。

## 关联主题页

- [data connection overview](../guides/data-connection-overview.md)
- [application component api reference](../api/application-component-api-reference.md)
- [llm application](../guides/llm-application.md)
- [knowledge base](../guides/knowledge-base.md)
- [application support](../guides/application-support.md)


