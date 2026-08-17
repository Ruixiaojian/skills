# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、低延迟的数据接入通道。它支持结构化与非结构化数据的纳管，并通过平台托管或流处理两种模式实现数据就绪与实时访问。所有连接器均需在业务空间内创建，且其生命周期与权限受RAM策略严格管控。

## 支持的模型/功能

数据连接器按数据访问模式分为两类：

- **平台托管型**：适用于文件（PDF/Word/Markdown等）和表格（CSV/Excel等）类非实时数据。数据被导入至百炼平台存储或用户自有OSS，经向量化后支持语义检索。解析方式包括电子文档解析、文档智能解析、大模型文档解析及Qwen VL解析（详见[文档理解](https://help.aliyun.com/zh/document-mind/product-overview/overview-of-document-understanding#9a4f5fb91fpps)），具体能力请参考 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中“导入文件”章节。
  
- **流处理型**：适用于需实时查询的数据库与知识库，包括 MySQL、PostgreSQL、PolarDB-X 2.0、语雀 和 OSS。其中仅通过 **DMS 导入数据源** 方式创建的 MySQL/PostgreSQL/PolarDB-X 连接器支持执行 SQL 查询；自定义方式创建的同类连接器仅支持元数据同步，不支持直接 SQL 调用 —— 此限制在 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 的各数据库小节中明确强调。

> **注意**：OSS 连接器虽归类为流处理型，但实际不执行实时 SQL，而是通过 `searchOSSFile` 和 `searchOSSFileByFileName` 工具进行向量/关键词检索，其能力依赖于已开通的[向量检索服务](https://help.aliyun.com/zh/oss/user-guide/vector-retrieval/) —— 该前提在 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) “OSS连接器”说明中强制要求，不可省略。

## 关键参数

| 参数类别       | 必填项                                                                 | 说明 |
|----------------|------------------------------------------------------------------------|------|
| **通用**       | 连接器名称、描述                                                       | 描述建议明确数据内容与用途，直接影响智能体调用准确度 |
| **文件/表格**  | 存储位置（平台存储 或 自有OSS）、OSS Bucket 标签（`bailian-connector-access`） | 平台存储有额度限制（文件连接器限200,000个文件/1TB，表格连接器1TB免费）；自有OSS需手动添加标签并完成RAM授权 |
| **MySQL**      | 数据库用户名、密码、网络类型（公网/私网）、数据库实例ID（RDS）或地址（自建） | 公网需放行百炼指定IP段；私网需匹配地域；仅 DMS 导入方式支持 SQL 执行 |
| **PostgreSQL** | 用户名、密码、dbName、`wal_level=logical`、`listen_addresses`（自建） | 自建实例必须配置 `100.64.0.0/16` 网段白名单；连通性检测使用 DTS 服务 |
| **PolarDB-X**  | 用户名、密码、所属地域（仅私网）、SLR 授权（`AliyunServiceRoleForSFMConnectorAccessDTS` 等） | 不支持公网与自建；SLR 授权为硬性前置条件，未授权将无法创建 |
| **语雀**       | Tenant access token                                                    | 仅支持公网语雀；[Token](../concepts/token.md) 需通过[语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取 |
| **OSS**        | Bucket 名称、Bucket 标签（`bailian-datahub-access`）、向量检索服务开通状态 | 不支持归档/冷归档存储类型；开启 Referer 防盗链时须将 `*.console.aliyun.com` 加入白名单 |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击“创建连接器” → 选择类型 → 填写基本信息与连接参数 → （可选）点击“开始检测”验证连通性 → 单击“确认”。

2. **导入数据**：
   - **文件/表格连接器**：进入连接器详情页 → 在“类目”或“数据表管理”下新建类目/数据表 → 选择“本地上传” → 配置解析方式与标签 → 提交。
   - **流处理连接器**：无需手动导入，连接成功后即可在应用中调用对应工具（如 `queryMySQL`、`searchYuQueDoc`）。

3. **在应用中调用**：在智能体（Agent 1.0）或工作流中，通过预置工具（如 `searchFile`、`queryPostgreSQL`）传入自然语言查询或 SQL 语句，平台自动路由至对应连接器执行。

## 限制和注意事项

- **容量与时效**：平台托管文件仅保留最近 90 天的导入记录（可查看），超期后不可见但不删除；文件连接器平台存储上限为 200,000 个文件 / 1 TB，表格连接器为 1 TB 免费额度（用尽后转按量付费）。
  
- **网络与权限**：
  - MySQL/PostgreSQL 公网连接必须将百炼服务 IP 段加入数据库白名单；
  - PolarDB-X 仅支持私网，且必须与实例同地域；
  - 所有自有 OSS Bucket 必须添加指定标签（`bailian-connector-access` 或 `bailian-datahub-access`），否则授权失败。

- **功能边界**：
  - 文件连接器**不支持直接导入 JSON/CSV/YAML**，需先转换为 XLSX/XLS；
  - 表格连接器数据表结构（列名、类型）**创建后不可修改**；
  - PostgreSQL 自建实例需显式配置 `pg_hba.conf` 允许 `100.64.0.0/16` 访问，此要求在 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中明确列出，但部分旧版文档未强调，务必以本文为准。

- **安全合规**：导入文件仅限当前业务空间内使用，百炼不会用于商业用途或对外公开；所有连接器操作均需主账号或具备 `AliyunBailianDataConnectorFullAccess` 权限的 RAM 用户执行。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


