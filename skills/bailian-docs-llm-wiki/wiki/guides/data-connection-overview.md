# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可控的数据接入通道。通过创建不同类型的连接器，开发者可将企业自有数据库、文档系统、对象存储等数据源接入百炼，支撑对话中实时查询、知识检索与智能推理。所有连接器均遵循最小权限原则，支持平台托管与流处理两类架构模式。

## 支持的模型/功能

数据连接器按数据访问方式分为两类：

- **平台托管型**：适用于非结构化与结构化静态数据，包括：
  - **文件连接器**：支持 PDF、Word、Markdown 等格式，依赖[文档理解](https://help.aliyun.com/zh/document-mind/product-overview/overview-of-document-understanding#9a4f5fb91fpps)能力进行[多模态](../concepts/multi-modal.md)解析（如大模型文档解析、Qwen VL 解析）；详情见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。
  - **表格连接器**：支持 CSV、Excel 等结构化数据，支持 `image_url` 字段类型以生成图片向量索引，用于以图搜图等场景。

- **流处理型**：适用于实时、动态数据源，支持 SQL 查询（**仅限 DMS 导入方式创建的连接器**）：
  - **MySQL / PostgreSQL / PolarDB-X 2.0**：需满足特定前置条件（如 PostgreSQL 要求 `wal_level=logical`），连通性检测分别依赖 EventBridge 或 DTS 服务；具体配置差异详见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。
  - **语雀**：仅支持公网语雀，需提供 Tenant access token。
  - **OSS**：需开通向量检索服务，并为 Bucket 添加 `bailian-datahub-access` 标签（值为 `read`）；该要求与文件/表格连接器使用的 `bailian-connector-access` 标签不同，注意区分 —— [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中明确指出二者标签名与权限值均不一致。

> **注意**：MySQL、PostgreSQL、PolarDB-X 2.0 连接器均明确说明“仅通过**从DMS导入数据源**方式创建的连接器支持执行SQL查询”，而自定义方式创建的连接器**不支持 SQL 执行**。该限制在三类数据库连接器描述中完全一致，无矛盾。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **通用** | 连接器名称、描述 | 名称需唯一且易识别；描述影响智能体调用准确度，建议明确数据内容与用途 |
| **文件/表格** | 存储位置（平台存储 / 自有 OSS） | 平台存储提供免费额度（文件连接器限 200,000 文件 + 1 TB，表格连接器 1 TB）；自有 OSS 需添加 `bailian-connector-access` 标签（值 `ReadAndWrite`） |
| **数据库类** | 数据库地址、端口、用户名、密码、dbName（PostgreSQL/PolarDB-X 必填） | MySQL 默认端口 3306，PostgreSQL 默认 5432；PolarDB-X 2.0 **仅支持私网**，且不支持自建实例 |
| **语雀/OSS** | Tenant access token（语雀）、Bucket 选择（OSS） | 语雀 [Token](../concepts/token.md) 需通过[语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取；OSS Bucket 不支持归档/冷归档存储类型 |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击 **创建连接器** → 选择类型 → 填写基本信息与连接参数 → （可选）点击 **开始检测** 验证连通性 → 确认创建。
2. **导入数据**：
   - 文件连接器：进入详情页 → 选择类目 → **导入数据** → 本地上传 → 选择解析方式（默认/自定义）→ 配置标签（可选）→ 确认。
   - 表格连接器：进入详情页 → 在**数据表管理**下新建或选择数据表 → 上传 Excel 或自定义表头（列名、类型必填，结构不可修改）→ 确认导入。
3. **调用能力**：连接器创建并导入数据后，可在智能体应用中通过内置工具（如 `searchOSSFile`、`searchTableData`）或 RAG 检索链路调用数据；具体工具使用请参考对应连接器的 API 文档。

## 限制和注意事项

- **权限要求**：RAM 用户需主账号授予数据连接管理权限；首次使用 OSS、DMS、PolarDB-X 等服务时，需完成 SLR 授权（如 `AliyunServiceRoleForSFMConnectorAccessDTS`）。
- **网络限制**：
  - MySQL 支持公网/私网，但公网需将指定 IP 段加入白名单；
  - PolarDB-X 2.0 **仅支持私网**，且必须与百炼服务同地域；
  - PostgreSQL 自建实例需配置 `listen_addresses` 允许 `100.64.0.0/16` 网段访问。
- **数据时效性**：平台托管型（文件/表格）导入后生成独立副本，与原始数据无关联；流处理型（数据库/OSS/语雀）为实时访问，无缓存。
- **文件限制**：文件连接器仅支持最近 90 天内导入的文件预览；不支持直接导入 JSON/CSV/YAML，需转为 XLSX/XLS 后再导入。
- **标签差异**：OSS 连接器要求 Bucket 标签为 `bailian-datahub-access: read`，而文件/表格连接器要求 `bailian-connector-access: ReadAndWrite` —— 二者不可混用。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)



