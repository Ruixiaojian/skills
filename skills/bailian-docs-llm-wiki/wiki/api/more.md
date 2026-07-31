# more

`more` 是百炼平台面向高级功能与扩展能力的统一入口，涵盖服务权限治理、安全凭证管理、知识库检索增强等关键能力。它不提供独立模型服务，而是通过服务关联角色（SLR）、临时 API Key 机制和结构化检索过滤器（SearchFilters）等底层能力，支撑工作流编排、安全存储、数据同步、监控分析及 RAG 场景的精细化控制。开发者需按需组合使用，确保权限最小化、凭证时效可控、检索结果精准。

## 支持的模型/功能

`more` 本身不对应具体模型，而是为以下核心功能提供基础设施支持：

- **服务集成与资源访问**：通过预置服务关联角色（SLR），授权百炼访问 FC、OSS、ADB-PG、MNS、SLS、CMS、OpenTelemetry、内容安全、DTS、CPFS 等阿里云服务。例如，`AliyunServiceRoleForSFMAccessFC` 用于工作流中调用函数计算节点，`AliyunServiceRoleForSFMAccessADB` 用于知识库对接 AnalyticDB for PostgreSQL [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时身份认证**：支持后端服务生成短期有效的临时 API Key，适用于前端或移动端等不可信环境的安全调用 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **知识库语义检索增强**：在 `Retrieve` 接口上支持 `searchFilters` 参数，实现基于字段的精确过滤（单值、多值、范围、模糊、标签查询），显著提升结构化数据检索准确率 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中 `AliyunServiceRoleForSFMTelemetry` 的策略定义被截断（末尾缺失 `}` 和完整权限项），实际部署时应以控制台或最新版 RAM 策略为准；同时，其权限声明中混用了 `log:*`、`arms:*` 和未完成的 `xtrace:*`，需确认 `xtrace` 权限是否已弃用或迁移至 ARMS/OpenTelemetry 统一接口。

## 关键参数

| 参数名 | 类型 | 说明 | 示例/约束 |
|--------|------|------|-----------|
| `expire_in_seconds` | integer | 临时 API Key 有效期（秒） | 范围 `[1, 1800]`，默认 `60` |
| `searchFilters` | array of object | 知识库检索过滤条件，每个 object 为一个 AND 子分组 | 最多支持 10 个子分组；子分组内支持 `eq`/`neq`/`gt`/`gte`/`lt`/`lte`/`like` 及 `tags` 字段；字段值需与知识库 Schema 类型严格匹配（如 `age` 为 `double` 时不可传字符串 `"25"`） |
| `indexId` | string | 知识库索引 ID | 必填，需与 `Retrieve` 请求体一致 |

## 使用方式

- **服务关联角色**：首次启用对应功能（如工作流中添加 FC 节点、安全存储空间绑定 OSS）时，系统自动创建 SLR；无需手动创建，但需确保 RAM 权限允许 `ram:CreateServiceLinkedRole`。角色名称与策略均固定，不可修改 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：通过 `POST /api/v1/tokens` 接口调用，需携带永久 API Key 的 `Authorization: Bearer <key>` 头；响应返回 `token`（前缀 `st-`）与 `expires_at`（Unix 时间戳）；该 token 可直接用于后续所有百炼 API 请求（如 `chat/completions`、`retrieve`）。
- **SearchFilters**：在 `RetrieveRequest` 请求体中直接嵌入 `searchFilters` 字段，格式为 `[{ "field1": "value1" }, { "field2": { "gte": 20, "lte": 30 } }]`；多值查询需对数组 `json.dumps` 后作为字符串传入（如 `{"姓名": "[\"张三\",\"李四\"]"}`）；模糊查询使用 `{"岗位": "{\"like\": \"技%员\"}"}` [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **SLR 删除风险**：删除任一 SLR 将导致对应功能完全失效（如删 `AliyunServiceRoleForAccessOSS` 后，安全存储空间无法读写 OSS）。删除前必须先解除所有依赖资源（如断开 OSS 连接、删除 FC 节点、停止 DTS 任务等），否则操作将失败 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 不可撤销**：生命周期由 `expire_in_seconds` 决定，到期自动失效，**不支持主动吊销或提前删除**；建议严格控制 TTL 时长，并避免在客户端硬编码。
- **SearchFilters 兼容性**：仅对 `indexType = "data_query"` 的知识库生效；`tags` 查询仅适用于文档搜索、音视频搜索类知识库；字段名须与知识库建模时定义的 `field_name` 完全一致（区分大小写）；数值字段不支持 `like` 模糊查询。
- **地域隔离**：临时 API Key 的生成 Endpoint 与永久 API Key 所属地域强绑定（北京/新加坡/弗吉尼亚），跨地域调用将返回 `InvalidApiKey` 错误 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


