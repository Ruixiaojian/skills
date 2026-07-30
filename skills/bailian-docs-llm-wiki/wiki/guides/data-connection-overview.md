# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的数据接入通道。它支持结构化与非结构化数据的接入，并通过平台托管或流处理两种模式实现数据的静态导入或实时查询。所有连接器均需满足前置权限与网络条件，且配置后可被智能体、RAG 应用等直接调用。

## 支持的模型/功能

数据连接器按数据访问模式分为两类：

- **平台托管类**：适用于离线导入场景，包括  
  - **文件连接器**：支持 PDF、Word、Markdown、图像、音视频等非结构化文档（详见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)）；  
  - **表格连接器**：支持 CSV、Excel（XLS/XLSX）等结构化数据，自动识别表头或支持自定义 Schema。

- **流处理类**：适用于实时 SQL 查询或在线内容检索，包括  
  - **MySQL / PostgreSQL / PolarDB-X 2.0 连接器**：仅通过 **DMS 导入数据源** 方式创建的连接器支持执行 SQL 查询（[数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 明确指出该限制）；  
  - **语雀连接器**：对接语雀[知识库](../concepts/knowledge-base.md)，支持公网版语雀文档的实时检索；  
  - **OSS 连接器**：访问自有 OSS Bucket 中的文件，依赖向量检索服务实现 `searchOSSFile` 等工具调用（[数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 要求开通该服务）。

> **注意**：原始文档中“文件连接器”和“表格连接器”的存储位置说明存在不一致表述——前者称平台存储“限时免费”，后者称“1 TB 免费额度，额度用完后自动转为按量付费”。实际计费策略以控制台最新提示为准，建议以 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中“表格连接器”描述为当前有效规则。

## 关键参数

| 连接器类型 | 必填参数 | 特殊要求 | 检测机制 |
|------------|----------|----------|----------|
| 文件/表格（平台托管） | 连接器名称、描述、存储位置（平台/OSS） | OSS Bucket 需打 `bailian-connector-access` 标签（值 `ReadAndWrite`） | 无显式连通性检测，依赖上传/解析结果反馈 |
| MySQL | 数据库地址、端口、用户名、密码、数据库实例（RDS）或主机（自建） | RDS 场景下自动填充地址/端口；自建需手动配置白名单；仅 DMS 导入方式支持 SQL 执行 | EventBridge 连通性检测 |
| PostgreSQL | 主机地址、端口、dbName、用户名、密码 | `wal_level=logical`；自建需配置 `listen_addresses` 允许 `100.64.0.0/16` 访问 | DTS 连通性检测 |
| PolarDB-X 2.0 | 数据库实例（自定义）或数据源（DMS）、用户名、密码 | 仅支持私网；必须完成 DTS + PolarDB-X SLR 授权；DMS 方式还需 DMS 角色授权 | EventBridge 检测（同 MySQL） |
| 语雀 | Tenant access token | 仅支持公网语雀；[Token](../concepts/token.md) 需通过 [语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取 | [Token](../concepts/token.md) 校验（无网络连通性检测） |
| OSS | Bucket 名称 | Bucket 需打 `bailian-datahub-access` 标签（值 `read`）；不支持归档/冷归档存储类型 | 授权后自动校验 Bucket 权限 |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击「创建连接器」→ 选择类型 → 填写基本信息与连接参数 → （可选）点击「开始检测」或「连接检测」验证 → 单击「确认」。
2. **导入数据（仅平台托管类）**：
   - 文件连接器：进入详情页 → 选择类目 → 「导入数据」→ 本地上传 → 选择解析方式（默认/文档智能/大模型/Qwen VL/音视频）→（可选）配置标签 → 确认。
   - 表格连接器：进入详情页 → 「数据表管理」→ 新建数据表 → 选择「直接上传 Excel」或「自定义表头」→ 上传文件 → 确认。
3. **调用数据**：
   - 平台托管类：在智能体 Knowledge Retrieval 或 RAG 应用中绑定对应连接器，系统自动切分、向量化并建立索引；
   - 流处理类：通过 `querySQL`（MySQL/PG/PolarDB-X）、`searchYuQueDoc`（语雀）、`searchOSSFile`（OSS）等内置工具在 Function Calling 中调用。

## 限制和注意事项

- **权限限制**：RAM 用户需主账号授予 `AliyunBailianDataConnectorFullAccess` 或最小化自定义策略权限，否则无法创建/管理连接器（参见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 的前置条件章节）。
- **网络限制**：
  - MySQL/PostgreSQL 支持公网/私网，但公网需将百炼出口 IP 段加入数据库白名单；
  - PolarDB-X 2.0 **仅支持私网**，且必须与实例同地域；
  - 语雀、OSS 依赖公网访问，无内网 VPC 支持。
- **功能限制**：
  - MySQL/PostgreSQL/PolarDB-X 的 SQL 执行能力**严格依赖 DMS 导入方式**，自定义数据源方式创建的连接器不可执行 SQL（该限制在三类连接器文档中重复强调，具有一致性）；
  - 文件连接器不支持直接导入 JSON/CSV/YAML，须转为 XLSX/XLS；
  - 表格连接器一旦确定列名与类型，**不可修改**；
  - OSS 连接器启用 `searchOSSFileByFileName` 工具前，必须已开通向量检索服务。
- **容量与生命周期**：
  - 文件连接器仅可查看最近 **90 天内导入的文件**（过期不可见，但数据未删除）；
  - 平台托管文件上限为 **200,000 个文件 + 1 TB 存储**（文件连接器）；表格连接器平台存储为 **1 TB 免费额度**（见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)）；
  - 类目数量上限为 **500 个**，扩容需提交工单。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


