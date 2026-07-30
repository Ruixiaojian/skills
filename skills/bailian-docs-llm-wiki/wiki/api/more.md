# more

`more` 是百炼平台中一组支撑性能力的统称，涵盖临时凭证管理、服务关联角色（SLR）授权、以及知识库高级检索过滤等功能。这些能力不直接参与模型推理，但为安全调用、跨云服务集成和精准语义检索提供关键基础设施支持。开发者需根据具体场景选择并正确配置对应机制。

## 支持的模型/功能

- **临时 API Key 生成**：用于在浏览器、移动 App 等不可信前端环境安全调用模型服务，避免永久密钥泄露。该能力独立于具体模型，适用于所有通过 `dashscope.aliyuncs.com` 或 `bailian.aliyuncs.com` 调用的百炼/通义千问模型接口。  
- **服务关联角色（SLR）**：百炼自动创建并托管的 RAM 角色，用于授权访问函数计算（FC）、OSS、ADB-PG、MNS、SLS、CMS、OpenTelemetry、内容安全、DTS、CPFS 等阿里云服务。不同角色对应不同功能模块，例如 `AliyunServiceRoleForSFMAccessFC` 支撑工作流中的函数计算节点调用 [原文标题](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- **知识库 SearchFilters**：专用于 `Retrieve` 接口的结构化过滤能力，支持在语义检索结果上叠加字段级条件（如 `{"姓名": "张三"}`），显著提升 RAG 场景下结果的相关性与准确性 [原文标题](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 关键参数

| 功能 | 参数名 | 类型 | 说明 | 取值范围/示例 |
|------|--------|------|------|----------------|
| 临时 API Key | `expire_in_seconds` | Integer | 临时 [Token](../concepts/token.md) 有效期（TTL） | `[1, 1800]` 秒，默认 `60`；示例：`?expire_in_seconds=1800` |
| SearchFilters | `searchFilters` | Array of Object | 检索过滤条件数组，每个元素为一个子分组（AND 语义） | `[{"姓名": "张三"}, {"岗位": "技术员"}]`；支持单值、多值、范围（`{"年龄": {"gte": 20, "lte": 27}}`）、模糊（`{"岗位": {"like": "技%员"}}`）、标签查询 |
| SearchFilters（范围查询） | `gt`, `gte`, `lt`, `lte`, `eq`, `neq` | String/Number | 字段比较操作符 | 仅数值字段支持 `gt`/`gte`/`lt`/`lte`；字符串和数值均支持 `eq`/`neq` |
| SearchFilters（标签查询） | `tags` | Array of String | 文档级标签匹配（OR 语义） | `{"tags": ["A大学", "学生会主席"]}`；多子分组时为 AND+OR 混合逻辑 |

> **注意**：文档 3 中 `multi_query` 示例代码使用 `json.dumps(names)` 构造多值，但实际 API 要求 `searchFilters` 中字段值应为原生 JSON 数组（如 `{"姓名": ["张三", "李四"]}`），而非字符串化数组。SDK 层需确保序列化正确，否则将导致过滤失效。请以 [原文标题](../../raw/application-api-reference/more/how-to-use-search-filters.md) 中的 JSON Schema 和实际接口行为为准。

## 使用方式

- **临时 API Key**：后端服务通过 `POST /api/v1/tokens` 调用生成（需携带 `Authorization: Bearer $DASHSCOPE_API_KEY`），获取 `token` 后透传至前端，前端在后续模型请求中使用该 `token` 替代永久密钥。地域 Endpoint 需与生成密钥一致（北京/新加坡/弗吉尼亚）[原文标题](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  
- **服务关联角色**：首次启用对应功能（如添加函数计算节点、配置 OSS 数据源）时由百炼自动创建，无需手动申请。角色权限策略已预置，**禁止修改或删除**，否则将导致相关功能中断。如确需删除，须先解除所有依赖资源（如断开 OSS 连接、删除函数计算节点等）。  
- **SearchFilters**：在 `RetrieveRequest` 请求体中直接设置 `searchFilters` 字段，配合 `indexId` 和 `query` 使用。要求知识库索引已对目标字段（如 `姓名`、`年龄`）启用结构化检索支持，且字段类型定义准确（string/double/long）。

## 限制和注意事项

- 临时 API Key **不可手动撤销**，仅能等待自然过期；其权限完全继承自生成所用的永久 API Key，包括模型访问白名单与知识库权限。  
- 所有服务关联角色均绑定特定百炼服务域名（如 `fc.sfm.aliyuncs.com`），**不可复用或跨服务授权**；删除角色前必须完成前置清理，否则操作将失败或引发功能异常。  
- `SearchFilters` 仅作用于 `Retrieve` 接口，不适用于 `ChatCompletion` 或 `Embedding`；标签（`tags`）查询仅支持文档搜索、音视频搜索类知识库；模糊查询（`like`）仅支持字符串字段，且 `%` 为唯一通配符。  
- > **注意**：文档 2 中 `AliyunServiceRoleForSFMAccessingMNS` 的权限说明末尾被截断（`"xtrace:Describe*"` 后缺失内容），实际策略应以 RAM 控制台中该角色绑定的 `AliyunServiceRolePolicyForSFMAccessingMNS` 策略内容为准，建议通过控制台校验完整权限。

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)



