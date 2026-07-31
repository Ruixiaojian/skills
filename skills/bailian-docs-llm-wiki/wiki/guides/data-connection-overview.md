# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的数据接入通道。它支持结构化与非结构化数据的接入，并通过平台托管或流处理两种模式实现数据访问，是构建知识增强型智能体和实时数据驱动应用的基础组件。所有连接器均需在业务空间内创建并绑定至具体应用，其配置直接影响后续检索、SQL 查询及向量化效果。

## 支持的模型/功能

数据连接器按数据访问模式分为两类：

- **平台托管类**：适用于文件（PDF/Word/Markdown等）和表格（CSV/Excel等）连接器，数据导入后由百炼平台统一存储与向量化，支持全文检索、语义搜索及[多模态](../concepts/multi-modal.md)解析（如 Qwen-VL 图像理解）。详见 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中“文件连接器”与“表格连接器”章节。
- **流处理类**：适用于 MySQL、PostgreSQL、PolarDB-X 2.0、语雀和 OSS 连接器，数据保留在源端，百炼通过实时连接执行查询或拉取元数据。其中仅通过 **DMS 导入数据源方式** 创建的 MySQL/PostgreSQL/PolarDB-X 连接器支持 SQL 执行；自定义方式创建的同类连接器仅支持元数据同步，不支持 `SELECT` 等运行时查询 —— 此限制已在 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 的各数据库连接器说明中明确标注。

> **注意**：文档中提及“文件导入后作为独立副本存储在平台提供的免费空间中，当前无容量限制”，但该描述与“平台托管文件连接器提供最大 200,000 个文件，1 TB 存储额度，限时免费”存在矛盾。实际配额以控制台实时显示为准，建议以 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中“前置条件”与“创建连接器”章节的配额说明为准。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **通用** | 连接器名称、描述 | 名称需唯一且可识别；描述用于指导 LLM 理解数据用途，影响检索准确率，建议包含数据范围与业务场景。 |
| **平台托管** | 存储位置（平台存储 / 自有OSS）、类目（文件）、数据表结构（表格） | 平台存储有配额约束；自有 OSS 需添加 `bailian-connector-access` 标签（值 `ReadAndWrite`）；类目上限 500 个；表格表结构一旦创建不可修改。 |
| **流处理** | 数据库地址/端口/用户名/密码（MySQL/PostgreSQL/PolarDB-X）、dbName（PostgreSQL 必填）、Tenant access token（语雀）、Bucket 名（OSS） | PostgreSQL 要求 `wal_level=logical`；PolarDB-X 仅支持私网且必须完成 DTS + PolarDB-X SLR 授权；OSS Bucket 需开通向量检索服务并添加 `bailian-datahub-access` 标签（值 `read`）。 |

## 使用方式

1. **创建连接器**：进入 [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md) 页面 → 单击“创建连接器” → 选择类型 → 填写基本信息与连接参数 → 完成授权与连通性检测（如适用）→ 确认创建。
2. **导入数据（仅平台托管）**：
   - 文件连接器：进入详情页 → 选择类目 → “导入数据” → 本地上传 → 选择解析方式（推荐“大模型文档解析”以支持图表理解）→ 可选配置标签 → 提交。
   - 表格连接器：进入详情页 → 新建或选择数据表 → 上传 Excel 或自定义表头（列名、类型必填，描述建议填写）→ 提交。
3. **调用数据**：
   - 平台托管数据：通过 `searchKnowledgeBase` 工具（文件）或 `searchTable` 工具（表格）在智能体中调用；
   - 流处理数据：MySQL/PostgreSQL/PolarDB-X 通过 `executeSQL` 工具（仅 DMS 方式支持）；语雀通过 `searchYuQue`；OSS 通过 `searchOSSFile` 或 `searchOSSFileByFileName`（需已开通向量检索服务）。

## 限制和注意事项

- **网络与权限**：MySQL/PostgreSQL 公网连接需将百炼服务 IP 段加入数据库白名单；PolarDB-X 仅支持私网；所有自建数据库需确保 `100.64.0.0/16` 网段可达（PostgreSQL 显式要求）；RAM 用户需主账号授予 `AliyunBailianFullAccess` 或最小权限策略。
- **格式与兼容性**：平台托管不支持直接导入 JSON/YAML/纯 CSV（需转 XLSX/XLS）；OSS 不支持归档/冷归档存储类型；语雀仅支持公网版，[Token](../concepts/token.md) 需具备 `knowledge.read` 权限。
- **生命周期**：平台托管文件仅可查看最近 90 天内导入记录；导入后文件与源端无关联，更新需重新上传；表格数据表结构不可变更，字段类型错误将导致导入失败。
- **安全合规**：自有 OSS Bucket 必须显式添加对应标签才能被百炼访问；语雀 [Token](../concepts/token.md) 和数据库凭据均加密存储，不落盘；所有连接器数据隔离于业务空间，不跨空间共享。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


