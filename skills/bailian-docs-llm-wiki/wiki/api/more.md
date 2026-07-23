# more

`more` 是百炼平台面向高级用例提供的扩展能力集合，涵盖临时认证、服务集成授权与知识库精细化检索三大核心方向。它不构成独立 API 服务，而是作为模型调用、工作流编排和 RAG 场景的支撑机制存在，适用于需兼顾安全性、跨云服务协同及结构化数据过滤的生产级应用。

## 支持的模型/功能

`more` 不直接对应特定模型，而是为以下功能提供底层支持：

- **临时 API Key 生成**：用于在浏览器、移动端等不可信环境安全调用模型服务（如 `qwen-max`、`qwen-plus` 等），避免永久密钥泄露 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)；
- **服务关联角色（SLR）自动管理**：支撑百炼与函数计算（FC）、OSS、ADB-PG、MNS、OpenTelemetry 等阿里云服务的受控集成，覆盖工作流节点、数据导入、安全存储、用量监控等场景 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)；
- **知识库 `SearchFilters` 检索过滤**：在 `Retrieve` 接口调用中对语义检索结果进行结构化字段级过滤（如 `姓名: "张三"`、`年龄: {"gte": 20, "lte": 27}`），显著提升 RAG 输出精度 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 2 中 `AliyunServiceRoleForSFMTelemetry` 的权限策略示例被截断（末尾缺失 `}`），实际部署时请以 RAM 控制台中该策略的完整 JSON 为准；同时，其关联的 `proj-xtrace-*` Logstore 命名规则与当前百炼控制台默认项目命名不一致，建议通过 [用量监控与性能分析](https://help.aliyun.com/zh/model-studio/application-observation) 页面确认实际 Project 名称。

## 关键参数

| 功能 | 参数名 | 类型 | 说明 | 取值范围/示例 |
|------|--------|------|------|----------------|
| **临时 API Key** | `expire_in_seconds` | Integer | Token 有效期（TTL） | `[1, 1800]` 秒，默认 `60`；示例：`?expire_in_seconds=1800` |
| **SearchFilters** | `searchFilters` | Array of Object | 过滤条件数组，每个 Object 为一个 AND 分组 | `[{"姓名": "张三"}, {"岗位": "技术员"}]`；支持单值、多值、范围（`gt`/`gte`/`lt`/`lte`/`eq`/`neq`）、模糊（`like`）和标签（`tags`）查询 |
| **SearchFilters（范围查询）** | 字段值格式 | String (JSON) | 范围条件需序列化为 JSON 字符串 | `"年龄": "{\"gte\": 20, \"lte\": 27}\"` |

## 使用方式

- **临时 API Key**：通过 `POST https://dashscope.aliyuncs.com/api/v1/tokens` 发起请求，需在 `Authorization` Header 中携带主账号的永久 `DASHSCOPE_API_KEY`；响应返回 `token`（前缀 `st-`）与 `expires_at`（Unix 时间戳）。该 token 可直接用于后续模型 API 调用的 `Authorization: Bearer <token>`。
- **服务关联角色**：无需手动创建。当您在百炼控制台首次启用对应功能（如添加 FC 节点、配置 OSS 数据源、开通安全存储空间等）时，系统自动创建并绑定 SLR。角色删除需先解除所有依赖资源（如删除工作流中的 FC 节点、断开 OSS 连接等），再通过 RAM 控制台操作。
- **SearchFilters**：在 `Retrieve` 请求体中直接传入 `searchFilters` 字段（非 Query 参数）。需确保知识库索引已将目标字段（如 `姓名`、`年龄`）配置为可检索字段；多值查询需将数组 `json.dumps` 后作为字符串传入字段值；模糊查询使用 `{"字段名": "{\"like\": \"值%\"}\"}` 格式。

## 限制和注意事项

- 临时 API Key **不可撤销**，仅能等待自然过期；其权限完全继承自签发所用的永久 API Key，包括模型访问白名单与知识库权限 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- 所有服务关联角色均含 `ram:DeleteServiceLinkedRole` 权限，但**删除后将导致对应功能完全不可用**（如删 `AliyunServiceRoleForSFMAccessFC` 后无法调用 FC 节点），且恢复需重新触发功能开通流程 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- `SearchFilters` 仅作用于 `Retrieve` 接口，**不改变向量索引本身**；过滤发生在语义检索之后，因此仍需保证原始检索召回质量；标签（`tags`）查询仅支持文档搜索、音视频搜索类知识库，且多个 `tags` 数组间为 OR 关系 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。
- 各地域（北京/新加坡/弗吉尼亚）的临时 Token Endpoint 和 DashScope API Endpoint **不互通**，必须使用与主 API Key 相同地域的 Endpoint。

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


