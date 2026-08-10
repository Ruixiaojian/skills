# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的实时或批量数据接入通道。它支持结构化与非结构化数据源，涵盖文件、表格、关系型数据库、知识库及对象存储等多种类型，并通过平台托管或流处理两种模式实现数据访问。所有连接器均需满足前置权限与网络条件，且配置细节直接影响后续检索与执行能力。

## 支持的模型/功能

数据连接器按数据访问模式分为两类：

- **平台托管类**：适用于离线导入场景，包括**文件连接器**（PDF/Word/Markdown等非结构化文档）和**表格连接器**（CSV/Excel等结构化数据）。数据被解析后存入百炼向量知识库，支持语义检索与智能体调用。  
- **流处理类**：适用于实时查询场景，包括**MySQL**、**PostgreSQL**、**PolarDB-X 2.0**、**语雀**和**OSS**连接器。其中前三者仅通过 [DMS导入数据源方式](../../raw/application-user-guide/data-connection-overview/data-connection.md) 创建时支持 SQL 查询执行；语雀和 OSS 连接器则分别用于知识库内容同步与对象存储文件检索。

> **注意**：原始文档中“OSS连接器”说明其需开通[向量检索服务](https://help.aliyun.com/zh/oss/user-guide/vector-retrieval/)才能使用 `searchOSSFile` 和 `searchOSSFileByFileName` 工具，但该服务开通路径未在当前文档明确指引，建议参考 [OSS向量检索官方文档](../../raw/application-user-guide/data-connection-overview/data-connection.md) 获取最新操作步骤。

## 关键参数

| 连接器类型 | 必填参数 | 特殊要求 | 检测机制 |
|------------|----------|----------|----------|
| 文件/表格 | 连接器名称、描述、存储位置（平台或自有OSS） | OSS Bucket 需添加 `bailian-connector-access` 标签（值为 `ReadAndWrite`） | 无显式连通性检测，依赖上传/解析结果反馈 |
| MySQL | 数据库地址、端口、用户名、密码；若为RDS则需实例ID | 公网连接需白名单放行指定IP段；仅DMS导入方式支持SQL执行 | EventBridge 服务检测 |
| PostgreSQL | 主机地址、端口、数据库名称（`dbName`）、用户名、密码 | `wal_level=logical`；自建实例需配置 `listen_addresses` 允许 `100.64.0.0/16` 访问 | DTS 服务检测 |
| PolarDB-X 2.0 | 数据库实例（自定义方式）或数据源（DMS方式）、用户名、密码 | **仅支持私网**；首次使用需授权 `AliyunServiceRoleForSFMConnectorAccessDTS` 和 `AliyunServiceRoleForSFMAccessPolarDBX` 角色 | EventBridge 检测（同MySQL） |
| 语雀 | Tenant access token | 仅支持公网版语雀；[Token](../concepts/token.md)需通过 [语雀开放API](https://www.yuque.com/yuque/developer/api) 获取 | [Token](../concepts/token.md)有效性校验 |
| OSS | Bucket 名称 | Bucket 需添加 `bailian-datahub-access` 标签（值为 `read`）；不支持归档/冷归档存储类型 | 授权后自动校验Bucket访问权限 |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击「创建连接器」→ 选择类型 → 填写基本信息与连接参数 → （可选）执行连通性检测 → 确认创建。  
2. **导入数据（仅平台托管类）**：  
   - 文件连接器：进入详情页 → 选择类目 → 「导入数据」→ 本地上传 → 选择解析方式（默认/自定义）→ 配置标签 → 提交。  
   - 表格连接器：进入详情页 → 新建或选择数据表 → 上传Excel 或 自定义表头（列名、类型必填，描述建议填写）→ 提交。  
3. **调用数据**：在智能体或应用中通过内置工具（如 `searchKnowledgeBase`、`executeSQL`、`searchOSSFile`）调用对应连接器，具体工具列表与参数详见 [数据连接工具参考](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

## 限制和注意事项

- **权限限制**：RAM 用户必须由主账号授予 `AliyunBailianDataConnectorFullAccess` 或等效自定义策略权限方可操作；OSS/Bucket 相关操作还需额外授予 `oss:GetBucketTagging`、`oss:ListObjects` 等细粒度权限。  
- **容量与时效**：  
  - 平台托管文件最多支持 200,000 个文件、1 TB 存储（限时免费）；表格连接器平台存储初始额度为 1 TB，用尽后转为按量付费。  
  - 导入的文件仅可在控制台查看最近 90 天内记录，超期后不可见但数据仍保留。  
- **网络与兼容性**：  
  - PolarDB-X 2.0 连接器**不支持公网**，必须通过私网访问；MySQL/PostgreSQL 公网连接需严格配置白名单。  
  - 语雀连接器仅适配公网版，不支持私有化部署语雀实例。  
- **功能差异**：  
  - MySQL/PostgreSQL/PolarDB-X 的 SQL 执行能力**仅限 DMS 导入方式**，自定义数据源方式创建的连接器无法执行 `executeSQL` 工具调用 —— 此关键限制在 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中多次强调，务必确认创建路径。  
  - 文件导入暂不支持 JSON/CSV/YAML 格式，须先转换为 XLSX/XLS；音视频解析不支持自然环境声识别。  
- **安全要求**：所有自有 OSS Bucket 必须添加指定标签（`bailian-connector-access` 或 `bailian-datahub-access`），且若启用 Referer 防盗链，需将 `*.console.aliyun.com` 加入白名单。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


