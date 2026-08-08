# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的数据接入通道。它支持结构化与非结构化数据的接入，并通过平台托管或流处理两种模式实现数据读取与实时查询。所有连接器均需在业务空间内创建，且依赖明确的权限与网络配置。

## 支持的模型/功能

数据连接器按数据访问模式分为两类：

- **平台托管型**：适用于文件（PDF/Word/Markdown等）和表格（CSV/Excel等）类非实时数据，数据被导入百炼平台或自有OSS后构建向量索引，供RAG检索使用。  
- **流处理型**：适用于需实时查询的数据库与在线服务，包括 MySQL、PostgreSQL、PolarDB-X 2.0、语雀 和 OSS，支持通过 SQL 或 API 实时拉取原始数据（具体执行能力见[原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)中“说明”部分）。

> **注意**：MySQL、PostgreSQL 和 PolarDB-X 2.0 连接器仅通过 **从 DMS 导入数据源** 方式创建时才支持执行 SQL 查询；自定义方式创建的连接器不支持该能力 —— 此限制在[原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)中多次强调，开发者务必确认创建路径。

## 关键参数

| 连接器类型 | 必填参数 | 特殊要求 | 检测服务 |
|------------|----------|----------|----------|
| 文件 / 表格 | 连接器名称、描述、存储位置（平台或 OSS） | OSS Bucket 需添加 `bailian-connector-access` 标签（值 `ReadAndWrite`） | 无（上传即生效） |
| MySQL | 数据库用户名、密码、网络类型（公网/私网）、实例 ID（RDS）或地址（自建） | 公网需加白名单；RDS 推荐 SLR 授权 | EventBridge |
| PostgreSQL | 主机地址、端口、dbName、用户名、密码 | `wal_level=logical`；自建需开放 `100.64.0.0/16` 网段 | DTS |
| PolarDB-X 2.0 | 用户名、密码、地域、实例（自定义）或 DMS 数据源（导入） | **仅支持私网**；首次需授权 `AliyunServiceRoleForSFMConnectorAccessDTS` 等 SLR 角色 | EventBridge |
| 语雀 | Tenant access token | 仅支持公网语雀；[Token](../concepts/token.md) 需通过[语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取 | 内置 [Token](../concepts/token.md) 验证 |
| OSS | Bucket 名称 | Bucket 需开通[向量检索服务](https://help.aliyun.com/zh/oss/user-guide/vector-retrieval/)；标签为 `bailian-datahub-access: read` | 无（授权后自动校验） |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击「创建连接器」→ 选择类型 → 填写基本信息与连接参数 → （可选）点击「开始检测」验证连通性 → 确认创建。  
2. **导入数据（仅平台托管型）**：
   - 文件连接器：在详情页选择类目 → 「导入数据」→ 本地上传 → 选择解析方式（推荐默认）→（可选）配置标签 → 确认。  
   - 表格连接器：在详情页新建数据表 → 选择「直接上传 Excel」或「自定义表头」→ 上传文件 → 确认。  
3. **调用数据**：在智能体或 API 应用中，通过内置工具（如 `searchFile`、`searchTable`、`executeSQL`）或知识库检索触发数据访问。具体工具签名与参数详见[原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)中各连接器章节。

## 限制和注意事项

- **容量与时效**：平台托管文件最多 200,000 个、1 TB 免费额度（用完转按量）；导入文件仅支持查看最近 90 天记录。  
- **网络与权限**：
  - MySQL/PostgreSQL 公网连接必须将百炼服务 IP 段加入数据库白名单；
  - PolarDB-X 2.0 **不支持公网**，仅限私网；
  - 所有 OSS 连接器要求目标 Bucket 开通向量检索服务，否则 `searchOSSFile` 等工具不可用。  
- **格式与兼容性**：
  - 文件连接器**不支持直接导入 JSON/CSV/YAML**，需先转为 XLSX/XLS；
  - 表格连接器自定义表头后，列名、类型、数量不可修改，且上传文件结构必须严格一致；
  - OSS 不支持归档、冷归档、深度冷归档存储类型；开启 Referer 防盗链的 Bucket 需将 `*.console.aliyun.com` 加入白名单。  
- **安全约束**：语雀连接器仅支持公网版本；所有连接器均需主账号或具备 `AliyunBailianDataConnectorFullAccess` 权限的 RAM 用户操作。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


