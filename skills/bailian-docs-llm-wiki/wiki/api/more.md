# more

`more` 是百炼平台中一组支撑性能力的统称，涵盖临时认证、服务关联角色（SLR）授权及知识库高级检索过滤等功能。这些能力不直接参与模型推理，但为安全调用、跨云服务集成和精准语义检索提供关键基础设施支持。开发者需按场景选择对应机制，并严格遵循权限最小化与生命周期管理原则。

## 支持的模型/功能

`more` 不对应具体模型，而是支撑以下三类核心功能：
- **临时 API Key 生成**：用于在不可信前端环境（如浏览器、App）安全调用模型服务，避免永久密钥泄露 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)；
- **服务关联角色（SLR）**：百炼自动创建的 RAM 角色，用于访问 FC、OSS、ADB-PG、MNS、SLS 等阿里云资源，支撑工作流、数据导入、安全存储、监控等场景 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)；
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级精确过滤，显著提升结构化数据召回准确率 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 2 中 `AliyunServiceRoleForSFMAccessFC` 的权限策略仅声明 `fc:ListFunctions` 和 `fc:InvokeFunction`，但实际工作流调用函数可能还需 `fc:GetFunction` 等元信息操作权限；建议以控制台实际授予策略为准，或参考最新版 [RAM 权限策略文档](https://help.aliyun.com/zh/ram/user-guide/permission-policy-syntax)。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|------|--------|------|------|------|----------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | [Token](../concepts/token.md) 有效期（TTL） | `[1, 1800]` 秒，默认 `60` |
| SearchFilters | `searchFilters` | array of object | 否 | 过滤子分组列表，每个子分组为 key-value 对或带操作符的对象 | 子分组间为 AND 逻辑；单个字段支持 `eq`/`neq`/`gt`/`gte`/`lt`/`lte`/`like`；多值需 JSON 序列化字符串 |
| SearchFilters（范围查询） | `{"字段名": {"gte": 20, "lte": 27}}` | object | — | 区间查询语法 | 数值类型字段专用 |

## 使用方式

- **临时 API Key**：通过后端服务向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起 POST 请求，携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，响应返回 `token` 和 `expires_at`（UNIX 时间戳）。前端需在过期前完成模型调用。
- **服务关联角色**：首次启用对应功能（如添加函数计算节点、配置 OSS 数据源）时由百炼自动创建，无需手动部署。角色名称与策略已预置，详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 表格。
- **SearchFilters**：在 `RetrieveRequest` 请求体中添加 `searchFilters` 字段，格式为 `[{ "字段A": "值1" }, { "字段B": {"gte": 10} }]`。字段名须与知识库索引时定义的字段名完全一致（区分大小写），且该字段需已配置为可过滤字段。

## 限制和注意事项

- 临时 API Key **不可撤销**，到期自动失效；其权限完全继承自生成所用的永久 API Key，务必确保该 Key 权限最小化 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- 删除服务关联角色前，必须先解除所有依赖该角色的功能（如删除函数计算节点、断开 OSS/ADB-PG 连接、停止 MNS 订阅等），否则将导致对应功能异常；删除后无法自动恢复，需重新触发功能开通流程。
- `SearchFilters` 仅作用于 `Retrieve` 接口，**不适用于 `ChatCompletion` 或 `Embedding` 等其他接口**；模糊查询（`like`）仅支持字符串字段，且 `%` 为唯一通配符；标签（`tags`）查询仅适用于文档搜索/音视频搜索类知识库。
- > **注意**：文档 3 的 Python 示例中 `multi_query()` 方法使用 `json.dumps(names)` 作为字段值，但实际 SDK 要求 `searchFilters` 中的值应为原始类型（如 `["张三","李四"]`）或标准 JSON 对象。直接传入 JSON 字符串可能导致解析失败，请以 `alibabacloud_bailian20231229` SDK 最新版文档为准。

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


