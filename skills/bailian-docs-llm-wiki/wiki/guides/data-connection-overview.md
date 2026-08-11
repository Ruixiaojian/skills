# data connection overview

数据连接是阿里云百炼平台统一管理外部数据源的核心能力，为应用提供安全、可配置的数据接入入口。通过数据连接器，应用可在对话中实时查询或引用企业数据库、文档系统及对象存储中的结构化与非结构化数据。所有连接器均支持向量化索引构建与语义检索，部分类型还支持原生SQL执行。

## 支持的模型/功能

数据连接器按数据访问模式分为两类：**平台托管型**（文件、表格）和**流处理型**（MySQL、PostgreSQL、PolarDB-X 2.0、语雀、OSS）。  
- **平台托管型**：数据导入至百炼平台或用户自有OSS，经解析后构建向量索引，供RAG类应用调用；支持文档智能解析、大模型文档解析（含图表理解）、音视频[多模态](../concepts/multi-modal.md)解析等 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。  
- **流处理型**：数据保留在源端，连接器仅建立实时访问通道；其中 MySQL、PostgreSQL 和 PolarDB-X 2.0 连接器**仅当通过 DMS 导入数据源方式创建时**才支持 SQL 查询执行，自定义数据源方式创建的实例不支持该能力 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。  
- **语雀与 OSS 连接器**：分别对接语雀知识库与 OSS Bucket，支持基于内容或文件名的向量检索（如 `searchOSSFile` 工具），但需提前开通 OSS 向量检索服务 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

> **注意**：原始文档中关于 PostgreSQL 的 `wal_level` 配置要求（必须设为 `logical`）与 MySQL/PolarDB-X 的说明逻辑一致，但 MySQL 实际无需此配置；该差异属数据库自身机制导致，非文档矛盾，开发者应严格按各数据库类型独立校验前置条件。

## 关键参数

| 参数类别       | 关键字段/约束                                                                 | 说明 |
|----------------|-------------------------------------------------------------------------------|------|
| **通用参数**   | 连接器名称、描述                                                              | 名称需唯一且易识别；描述将影响智能体对数据用途的理解准确度，建议明确数据内容与业务场景。 |
| **存储位置**   | 平台存储（免费额度：文件≤200,000个/1 TB，表格1 TB限时免费）、自有OSS         | 使用自有OSS需授权并添加 `bailian-connector-access` 标签（值 `ReadAndWrite`）；OSS连接器则需 `bailian-datahub-access`（值 `read`）。 |
| **数据库连接** | 地址、端口、用户名、密码、dbName（PostgreSQL/PolarDB-X 必填）、实例ID（RDS） | MySQL 默认端口3306，PostgreSQL 默认5432；PolarDB-X 仅支持私网，不支持公网连接。 |
| **认证凭证**   | 语雀 Tenant access token、DMS 数据源 ID、SLR 授权角色（DTS/RDS/PolarDB-X/DMS） | SLR 授权为首次使用必需步骤，涉及 `AliyunServiceRoleForSFMConnectorAccessDTS` 等角色。 |

## 使用方式

1. **创建连接器**：进入 [数据连接](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list) 页面 → 单击「创建连接器」→ 选择类型 → 填写基本信息与连接参数 → 完成授权与连通性检测。  
2. **导入数据（仅平台托管型）**：  
   - 文件连接器：在详情页选择类目 → 「导入数据」→ 本地上传（支持 PDF/Word/Markdown/图像/音视频等）→ 选择解析方式（推荐「大模型文档解析」以支持图表理解）→ 配置标签（可选，用于 API 调用时过滤）。  
   - 表格连接器：在详情页新建数据表 → 选择「直接上传Excel」或「自定义表头」→ 严格匹配列名与类型（`image_url` 字段需填公开可访问 URL）→ 提交导入。  
3. **调用数据**：在智能体或 API 请求中通过工具（如 `searchOSSFile`、`querySQL`）触发连接器能力；标签（`tags`）可用于缩小检索范围 [原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

## 限制和注意事项

- **容量与时效**：平台托管文件仅保留最近 90 天的导入记录（不可查看但未删除）；类目上限 500 个，需扩容请提交工单。  
- **格式限制**：平台不支持直接导入 JSON/CSV/YAML 表格文件，须转为 XLSX/XLS；OSS 不支持归档/冷归档/深度冷归档存储类型。  
- **网络与权限**：  
  - MySQL 公网连接需将百炼指定 IP 段加入 RDS 白名单；  
  - PostgreSQL 自建实例需配置 `listen_addresses` 允许 `100.64.0.0/16` 访问；  
  - 开启 Referer 防盗链的 OSS Bucket，须将 `*.console.aliyun.com` 加入白名单。  
- **功能边界**：  
  - 所有流处理型连接器的 SQL 执行能力**完全依赖 DMS 导入路径**，自定义数据源方式创建的实例无此能力；  
  - 文件连接器导入后生成独立副本，与原始文件无同步关系；  
  - 音视频解析不支持识别音乐或环境声（如雷声、钟声）[原文标题](../../raw/application-user-guide/data-connection-overview/data-connection.md)。

## 来源文档

- [数据连接](../../raw/application-user-guide/data-connection-overview/data-connection.md)


