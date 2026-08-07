# more

`more` 是百炼平台中一组支撑性能力的统称，涵盖临时认证、知识库高级检索过滤及服务关联角色管理三大核心方向。它不直接提供模型推理能力，而是为安全调用、精准检索和云资源协同提供底层支持。开发者需结合具体场景选择对应能力，并注意权限继承与生命周期约束。

## 支持的模型/功能

`more` 本身不对应具体大模型，而是提供以下三类基础设施能力：

- **临时 API Key 生成**：用于在不可信前端（如浏览器、App）安全调用模型服务，避免永久密钥泄露 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)  
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级精确过滤，适用于结构化数据场景 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)  
- **服务关联角色（SLR）**：百炼自动创建并托管的 RAM 角色，用于授权访问 FC、OSS、ADB-PG、MNS 等阿里云服务资源，支撑工作流、数据导入、安全存储等功能 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)

> **注意**：文档 2 中提到的 `searchFilters` 仅适用于知识库 `Retrieve` 接口（即 RAG 检索阶段），**不适用于模型 `chat` 或 `completions` 接口**；且其语法与 Elasticsearch 或 OpenSearch 的 query DSL 不兼容，必须严格遵循百炼定义的 JSON 结构。

## 关键参数

| 能力类型 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|----------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | TTL（秒），取值范围 `[1, 1800]`，默认 `60` | `?expire_in_seconds=300` |
| SearchFilters | `searchFilters` | array of object | 否 | 每个 object 为一个 AND 分组，支持单值、多值、范围、模糊、标签查询 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（范围查询） | `gte`, `lte`, `gt`, `lt`, `eq`, `neq` | number/string | 否 | 字段内嵌操作符，需通过 `json.dumps()` 序列化后传入（见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 中 Python 示例） | `{"年龄": "{\"gte\": 20, \"lte\": 27}\"}` |
| SearchFilters（模糊查询） | `like` | string | 否 | 值中 `%` 表示通配符，需封装为 `{"like": "技%员"}` 并序列化 | `{"岗位": "{\"like\": \"技%员\"}\"}` |

## 使用方式

- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起 POST 请求，携带 `Authorization: Bearer <永久APIKey>`，地域 Endpoint 需与密钥所在地域一致（北京/新加坡/弗吉尼亚）  
- **SearchFilters**：在 `RetrieveRequest` 请求体中直接添加 `searchFilters` 字段，**无需额外鉴权或开启开关**，但要求知识库已按字段类型（string/double）正确配置索引 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)  
- **服务关联角色**：**无需手动创建**，当首次启用对应功能（如添加函数计算节点、配置 OSS 数据源）时由百炼自动创建；角色策略已预置，禁止修改  

## 限制和注意事项

- 临时 API Key 继承生成者密钥的全部权限（含模型访问、知识库读写等），且**无法提前撤销，仅能等待过期**；有效期最长 1800 秒（30 分钟）  
- `searchFilters` 中各分组间为 **AND 逻辑，不可更改**；同一分组内多字段也为 AND；标签（`tags`）查询中，同一数组内为 OR，不同数组间仍为 AND  
- 所有服务关联角色均绑定特定服务场景，**删除角色将导致对应功能完全失效**（如删除 `AliyunServiceRoleForSFMAccessFC` 后，工作流中函数计算节点无法调用）；删除前必须清理依赖资源（如已发布的应用、OSS 连接、ADB-PG 实例绑定等）  
- > **注意**：文档 3 中 `AliyunServiceRoleForSFMAccessingMNS` 的权限说明末尾被截断（缺失 `xtrace` 权限的 closing brace），实际策略以 RAM 控制台中该角色绑定的 `AliyunServiceRolePolicyForSFMAccessingMNS` 策略为准，建议通过控制台校验完整内容。

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)


