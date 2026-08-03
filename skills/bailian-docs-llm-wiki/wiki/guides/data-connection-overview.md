# data connection overview

[数据连接](../concepts/data-connection.md)是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的数据接入通道。通过创建不同类型的[数据连接](../concepts/data-connection.md)器，开发者可将企业自有数据库、文档系统及对象存储中的数据实时接入百炼应用，在对话或智能体推理中按需检索与引用。所有连接器均支持在控制台可视化配置，并可通过 API 集成到自动化工作流中。

## 支持的模型/功能

[数据连接](../concepts/data-connection.md)器按数据访问模式分为两类：**平台托管型**（文件、表格）和**流处理型**（MySQL、PostgreSQL、PolarDB-X 2.0、语雀、OSS）。  
- **平台托管型**：数据导入百炼平台或自有 OSS 后进行向量化索引，适用于非结构化文档（PDF/Word/Markdown）和结构化表格（CSV/Excel），支持全文检索、语义搜索及标签过滤。详细能力见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)。  
- **流处理型**：保持数据原位不动，通过实时连接执行查询或拉取内容。其中 MySQL、PostgreSQL 和 PolarDB-X 2.0 连接器**仅当通过 DMS 导入数据源方式创建时才支持 SQL 查询执行**；语雀和 OSS 连接器则分别用于知识库内容同步与对象存储文件检索。该限制已在 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中明确标注。  
> **注意**：语雀连接器**仅支持公网版本语雀**，不兼容私有化部署实例；该约束在 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中已强调，但未说明替代方案（如自建知识库对接需使用 OSS 或文件连接器）。

## 关键参数

| 连接器类型 | 必填参数 | 特殊要求 | 检测服务 |
|------------|----------|----------|----------|
| 文件 / 表格 | 连接器名称、描述、存储位置（平台或 OSS） | OSS Bucket 需添加 `bailian-connector-access` 标签（值 `ReadAndWrite`） | — |
| MySQL | 数据库地址、端口、用户名、密码、数据库实例（RDS）或 dbName（自建） | RDS 实例需 SLR 授权；自建需开放白名单 IP 段 | EventBridge |
| PostgreSQL | 主机地址、端口、dbName、用户名、密码 | `wal_level=logical`；自建需配置 `pg_hba.conf` 允许 `100.64.0.0/16` 访问 | DTS |
| PolarDB-X 2.0 | 数据库实例（仅 RDS）、用户名、密码 | **仅支持私网**；首次使用需授权 `AliyunServiceRoleForSFMConnectorAccessDTS` 和 `AliyunServiceRoleForSFMAccessPolarDBX` | EventBridge |
| 语雀 | Tenant access token | [Token](../concepts/token.md) 需从 [语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取 | 内置 [Token](../concepts/token.md) 验证 |
| OSS | Bucket 名称 | Bucket 需开通[向量检索服务](https://help.aliyun.com/zh/oss/user-guide/vector-retrieval/)，并添加 `bailian-datahub-access` 标签（值 `read`） | 控制台自动校验权限 |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击「创建连接器」→ 选择类型 → 填写基础信息与连接参数 → （可选）点击「开始检测」验证连通性 → 确认提交。  
2. **导入数据（仅平台托管型）**：  
   - 文件连接器：进入详情页 → 选择类目 → 「导入数据」→ 本地上传 → 选择解析方式（推荐「大模型文档解析」以支持图表理解）→ 配置标签 → 确认。  
   - 表格连接器：进入详情页 → 新建或选择数据表 → 上传 Excel 或自定义表头（列名、类型必填，结构不可修改）→ 确认。  
3. **调用数据**：在应用或智能体中通过内置工具（如 `searchFileByContent`、`searchOSSFile`、`executeSQL`）调用，具体参数与返回格式参见对应连接器的 API 文档。

## 限制和注意事项

- **容量与时效**：平台托管文件连接器默认提供 1 TB 免费额度（用完转按量），且仅支持查看最近 **90 天内导入的文件**；表格连接器同样适用该时效限制。  
- **网络与权限**：  
  - MySQL/PostgreSQL/PolarDB-X 2.0 连接器若使用公网，**必须将百炼服务 IP 段加入数据库白名单**；PolarDB-X 2.0 **强制私网访问**，不支持公网。  
  - 所有 OSS 连接器均**不支持归档、冷归档、深度冷归档存储类型**的 Bucket；若启用 Referer 防盗链，需将 `*.console.aliyun.com` 加入白名单。  
- **功能边界**：  
  - 文件连接器**不支持直接导入 JSON/CSV/YAML**，需先转换为 XLSX/XLS；表格连接器上传文件结构必须与预设表头严格一致，否则失败。  
  - PostgreSQL 自建实例需手动配置 `listen_addresses` 和 `pg_hba.conf`，而 RDS 实例无需此操作——该差异在 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中已明确，但未提供 RDS 参数检查清单。  
- **安全合规**：导入文件作为独立副本存储于百炼平台，**与原始数据无关联**；所有数据仅限当前业务空间使用，阿里云不会用于商业用途或对外公开。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


