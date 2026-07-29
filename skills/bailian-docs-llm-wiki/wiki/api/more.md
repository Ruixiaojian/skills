# more

`more` 是百炼平台中一组支撑性能力的统称，涵盖临时凭证生成、服务关联角色管理、知识库高级检索过滤等关键基础设施功能。这些能力不直接面向模型推理，而是为安全调用、跨云服务集成和结构化数据精准检索提供底层支持。开发者需根据具体场景选择并正确配置对应组件。

## 支持的模型/功能

`more` 并非模型类别，而是平台级支撑能力集合，当前包含三类核心功能：

- **临时 API Key 生成**：用于在前端（浏览器、App）等不可信环境安全调用模型服务，避免永久密钥泄露 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)  
- **服务关联角色（SLR）**：百炼自动创建的 RAM 角色，用于访问 FC、OSS、ADB-PG、MNS、SLS 等外部云服务资源，支撑工作流、数据管理、安全存储、监控等场景 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)  
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级精确过滤（如 `{"姓名": "张三"}`），显著提升结构化数据检索精度 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)  

> **注意**：文档 2 中列出的 `AliyunServiceRoleForSFMAccessingMNS` 权限说明存在截断（末尾 JSON 不完整），实际策略应以 RAM 控制台中该角色绑定的 `AliyunServiceRolePolicyForSFMAccessingMNS` 策略内容为准；其他 SLR 策略描述均完整可用。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | TTL（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |
| SearchFilters | `searchFilters` | array of object | 否 | 每个 object 为一个 AND 分组，支持单值、多值、范围、模糊、标签查询 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（范围查询） | `gte`, `lte`, `gt`, `lt`, `eq`, `neq` | number/string | 否 | 字段比较操作符，需嵌套在字段值中（如 `{"年龄": "{\"gte\": 20, \"lte\": 30}\"}`） | `{"age": "{\"gte\": 25}"}` |
| SearchFilters（模糊查询） | `like` | string | 否 | 值格式为 `{"like": "张%"}`，`%` 表示通配符 | `{"岗位": "{\"like\": \"技%员\"}"}` |

## 使用方式

- **临时 API Key**：通过 `POST https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800` 调用，需在 `Authorization` Header 中携带后端持有的永久 `DASHSCOPE_API_KEY`。返回的 `token` 可直接用于后续模型请求的 `Authorization: Bearer <token>`。  
- **服务关联角色**：首次启用对应功能（如添加函数计算节点、配置 OSS 数据源）时由百炼自动创建，无需手动调用 API；角色权限已预置，禁止修改其策略内容。  
- **SearchFilters**：在 `RetrieveRequest` 请求体中作为顶层字段传入，与 `indexId`、`query` 同级；SDK 中通过 `retrieve_request.search_filters = [...]` 设置（Python/Java SDK 示例见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)）。

## 限制和注意事项

- 临时 API Key **不可主动删除**，仅能等待过期自动失效；其权限完全继承自签发用的永久 API Key，务必确保后者权限最小化。  
- 所有服务关联角色均受 **RAM 服务关联角色约束**：删除前必须先解除其依赖（如删除函数计算节点、断开 OSS 连接、停止 MNS 订阅等），否则删除失败；`AliyunServiceRoleForSFMAccessingMNS` 明确禁止手动修改或删除 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- SearchFilters 仅作用于 **已成功索引且参与检索的字段**；若字段未在知识库创建时勾选“参与检索”，则无法被 `searchFilters` 过滤；多值查询需使用 `json.dumps(["val1", "val2"])` 格式传递字符串数组，而非原生数组。  
- > **注意**：文档 3 的 Python 示例中 `multi_query()` 方法将 `names` 数组 `json.dumps` 后赋值给字段，但实际 SDK（如 `alibabacloud_bailian20231229` v1.0.11+）已支持原生 list 传参，推荐直接使用 `{"姓名": ["张三", "李四"]}`，避免手动序列化引发格式错误。

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


