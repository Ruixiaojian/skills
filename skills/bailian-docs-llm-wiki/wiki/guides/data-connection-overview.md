# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心机制，为应用提供安全、可控的数据接入能力。它支持将企业自有数据库、文档系统、对象存储等异构数据源接入百炼环境，并在对话或智能体执行过程中实时检索与引用。所有连接器均通过统一控制台创建与配置，权限由RAM策略集中管控。

## 支持的模型/功能

数据连接器按数据访问模式分为两类：

- **平台托管型**：适用于非结构化与结构化静态数据，包括：
  - `文件`：支持 PDF、Word、Markdown 等格式，依赖[文档理解](https://help.aliyun.com/zh/document-mind/product-overview/overview-of-document-understanding#9a4f5fb91fpps)能力进行向量化（详见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 中“导入文件”章节）；
  - `表格`：支持 CSV、Excel（XLS/XLSX），支持自定义表头与字段类型（如 `image_url` 字段触发图片向量索引生成）。

- **流处理型**：适用于实时查询动态数据，包括：
  - `MySQL`、`PostgreSQL`、`PolarDB-X 2.0`：仅通过 **DMS 导入数据源** 方式创建的连接器支持 SQL 查询执行（[原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) 明确指出“创建自定义数据源方式不支持直接执行SQL”）；
  - `语雀`：对接语雀知识库，需公网版 [Token](../concepts/token.md)；
  - `OSS`：访问对象存储中文件，依赖向量检索服务实现 `searchOSSFile` 等工具调用（参见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) “OSS连接器”说明）。

> **注意**：`PolarDB-X 2.0` 连接器**仅支持私网接入**，且不支持自建实例；而 `MySQL` 和 `PostgreSQL` 均支持公网/私网双模式，但后者要求 `wal_level=logical` —— 此配置差异在原始文档中被明确列出，无矛盾。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **通用** | 连接器名称、描述 | 名称需唯一可识别；描述影响智能体调用准确度，建议注明数据范围与用途 |
| **平台托管** | 存储位置（平台存储 / 自有OSS） | 平台存储提供限时免费额度（文件：200,000个/1TB；表格：1TB）；自有OSS需添加 `bailian-connector-access` 标签（值 `ReadAndWrite`） |
| **流处理（DB类）** | 数据库地址、端口、用户名、密码、dbName（PostgreSQL/PolarDB-X 必填） | MySQL 默认端口 3306，PostgreSQL 默认 5432；PolarDB-X 仅支持私网，且数据库地址/端口自动填充 |
| **语雀/OSS** | Tenant access token（语雀）、Bucket 名称（OSS） | 语雀 [Token](../concepts/token.md) 需从[语雀开放 API](https://www.yuque.com/yuque/developer/api) 获取；OSS Bucket 需添加 `bailian-datahub-access` 标签（值 `read`），并开通向量检索服务 |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 控制台 → 单击“创建连接器” → 选择类型 → 填写基本信息与连接参数 → （可选）点击“开始检测”验证连通性 → 确认提交。
2. **导入数据**：
   - 文件/表格连接器：进入连接器详情页 → 选择类目或数据表 → 上传本地文件或配置表结构 → 设置解析方式（如大模型文档解析）与标签 → 提交。
   - DB 类连接器：无需手动导入，数据保留在原库，应用通过 SQL 工具（如 `queryMySQL`）实时查询。
3. **在应用中调用**：在智能体或 API 调用中，通过预置工具（如 `searchFile`、`queryPostgreSQL`）指定连接器 ID 与查询条件，平台自动路由至对应数据源。

## 限制和注意事项

- **权限前提**：必须由主账号或已授权 RAM 用户操作；涉及 SLR 授权（如 DMS、DTS、PolarDB-X 角色）时需显式同意（见 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md) “前置条件”与各连接器章节）。
- **存储限制**：
  - 文件连接器：仅可查看最近 90 天内导入的文件（文件副本独立存储，不与源同步）；
  - OSS 连接器：**不支持归档、冷归档、深度冷归档类型 Bucket**；开启 Referer 防盗链时，须将 `*.console.aliyun.com` 加入白名单。
- **功能限制**：
  - MySQL/PostgreSQL/PolarDB-X 的 SQL 执行能力**严格绑定 DMS 导入方式**，自定义数据源方式仅支持元数据同步，不可查；
  - 表格连接器中 `image_url` 字段要求链接**公开可访问**，否则图片抓取失败；
  - 文件导入暂不支持 JSON/CSV/YAML 格式，需转为 XLSX/XLS 后再上传。
- **网络与配置**：
  - PostgreSQL 自建实例需额外配置 `listen_addresses` 允许 `100.64.0.0/16` 网段访问；
  - PolarDB-X 2.0 连接器**仅支持私网**，且必须与实例同地域。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


