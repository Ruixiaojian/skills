# more

`more` 是百炼平台中一组面向高级用例与安全增强能力的扩展功能集合，涵盖服务权限管理、临时凭证生成和知识库精准检索等核心能力。这些功能不直接参与模型推理调用，而是为工作流编排、数据接入、权限隔离与结果过滤等生产级场景提供支撑。开发者需结合具体业务需求，在对应模块（如工作流、知识库、监控）中按需启用。

## 支持的模型/功能

`more` 并非模型名称或推理 API，而是平台级能力集合，当前包含以下三类关键功能：

- **服务关联角色（SLR）**：用于百炼子系统（如工作流、数据管理、安全存储空间）安全访问外部云资源（FC、OSS、ADB-PG、MNS 等）。所有 SLR 均由百炼自动创建与维护，无需手动配置策略 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 生成**：通过后端服务调用 `/api/v1/tokens` 接口，基于永久 API Key 签发短期有效的临时凭证，适用于前端/移动端等不可信环境 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级精确过滤（如 `{"姓名": "张三"}`），显著提升结构化数据检索准确率 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中列出的 `AliyunServiceRoleForSFMTelemetry` 权限定义在响应体末尾被截断（`"xtrace:Read*","xtrace:Get*","xtrace:Describe*"` 后无闭合），实际策略应以控制台或最新 SDK 返回为准；建议以 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 中声明的权限范围为最小必要依据。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例值 |
|------|--------|------|------|------|--------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | TTL（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |
| SearchFilters | `searchFilters` | array of object | 否 | 检索过滤条件数组，每个对象为 Key-Value 字段约束 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（范围查询） | `gte`, `lte`, `gt`, `lt`, `eq`, `neq` | number/string | 否 | 字段比较操作符，嵌套于字段值中 | `{"年龄": {"gte": 20, "lte": 27}}` |
| SearchFilters（模糊查询） | `like` | string | 否 | 字符串模糊匹配，支持 `%` 通配符 | `{"岗位": {"like": "技%员"}}` |

## 使用方式

- **服务关联角色**：无需主动调用。当首次在控制台启用对应功能（如添加函数计算节点、配置 OSS 数据源）时，百炼自动创建所需 SLR。角色名称与权限策略已固化，不可修改 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起 `POST` 请求，`Authorization: Bearer <永久APIKey>`，可选 `?expire_in_seconds=N`。返回 `token` 和 `expires_at`（UNIX 时间戳），后续请求使用该 `token` 替代永久密钥。
- **SearchFilters**：在 `RetrieveRequest` 请求体中直接嵌入 `searchFilters` 字段。支持单值、多值、范围、模糊及标签查询；子分组间为 `AND` 逻辑，分组内字段为 `AND`；多值/范围/模糊查询需将值序列化为 JSON 字符串（如 `json.dumps({"gte": 20})`）[知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 限制和注意事项

- **SLR 删除风险**：删除任一服务关联角色（如 `AliyunServiceRoleForSFMAccessFC`）将导致依赖该角色的功能完全失效（如工作流无法调用 FC 函数），且删除前必须先清理所有关联资源（如删除函数计算节点、断开 OSS 连接等）[服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 不可撤销**：生命周期固定，到期自动失效，**不支持手动删除或提前吊销**。务必严格控制 `expire_in_seconds` 时长，避免过长 TTL 增加泄露风险 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **SearchFilters 字段类型约束**：仅支持已明确映射为 `string`、`long` 或 `double` 类型的元数据字段；未在知识库索引配置中标记为“参与检索”的字段无法被过滤 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。
- **地域隔离**：临时 API Key 的 Endpoint 与生成所用 API Key 的地域强绑定（北京、新加坡、弗吉尼亚），跨地域调用将失败；各区域 API Key 互不通用。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


