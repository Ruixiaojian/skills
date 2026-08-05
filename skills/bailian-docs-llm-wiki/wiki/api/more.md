# more

`more` 是百炼平台为增强模型服务能力、扩展数据接入与治理能力而提供的一组高级功能集合，涵盖服务关联角色（SLR）授权、临时认证机制及知识库精细化检索能力。这些功能面向需要深度集成云资源、保障调用安全或提升RAG精度的开发者场景，不直接暴露为独立API，而是通过平台组件（如工作流、知识库、监控等）按需启用。

## 支持的模型/功能

`more` 并非模型名称或独立服务，而是指代百炼平台中**依赖服务关联角色实现的扩展能力**以及**配套的高级调用控制能力**，主要包括：

- **服务集成能力**：通过预置服务关联角色（SLR），支持工作流调用函数计算（FC）、知识库/安全存储空间接入OSS/ADB-PG、数据管理对接OSS/MNS/DTS、模型监控对接SLS/CMS、用量分析对接OpenTelemetry等 [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **安全调用能力**：提供生成临时API Key的接口，用于在不可信前端环境（如浏览器、App）中安全调用模型服务，避免永久密钥泄露 [生成临时API Key (raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **知识库检索增强能力**：支持在 `Retrieve` 接口请求中传入 `searchFilters`，对语义检索结果进行结构化字段级过滤（如单值、多值、范围、模糊、标签查询），显著提升RAG结果相关性 [知识库SearchFilters (raw/application-api-reference/more/how-to-use-search-filters.md)](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档1中列出的 `AliyunServiceRoleForSFMAccessFC` 权限仅包含 `fc:ListFunctions` 和 `fc:InvokeFunction`，但实际工作流节点可能还需 `fc:GetFunction` 等元信息权限以完成配置校验；建议以控制台实际策略绑定为准，而非仅依赖文档描述。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时API Key生成 | `expire_in_seconds` | integer | 否 | TTL（秒），取值范围 `[1, 1800]`；默认60秒 | `1800` |
| 知识库检索过滤 | `searchFilters` | array of object | 否 | 检索过滤条件数组，每个元素为一个子分组（AND语义） | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| `searchFilters` 子项 | 字段名（如 `"年龄"`） | string | 是 | 知识库文档中定义的字段名 | `"年龄"` |
| `searchFilters` 子项 | 字段值 | string / number / object | 是 | 支持单值（`"张三"`）、多值（`["张三","李四"]`）、范围（`{"gte":20,"lte":30}`）、模糊（`{"like":"技%员"}`）、标签（`["A大学"]`） | `{"gte":25,"lt":35}` |

## 使用方式

- **服务关联角色**：无需手动创建。当您首次在控制台启用对应功能（如添加FC节点、创建OSS知识库、开启模型监控）时，百炼自动为您创建并绑定所需SLR。角色名称与权限策略已固化，详见 [服务关联角色 (raw/application-api-reference/more/bailian-service-linked-role.md)](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <永久API Key>` 的POST请求，可选携带 `expire_in_seconds` 查询参数。响应返回 `token`（即临时Key）和 `expires_at`（Unix时间戳）。
- **SearchFilters**：在调用 `Retrieve` 接口（路径 `/api/v1/retrieve`）的请求体中，将 `searchFilters` 作为顶层字段传入，格式为JSON数组。各子分组内支持混合字段类型，子分组间为AND逻辑。

## 限制和注意事项

- **SLR删除风险**：删除任一服务关联角色将导致其对应功能完全失效（如删除 `AliyunServiceRoleForSFMAccessFC` 后，所有工作流中的FC节点无法调用）。删除前必须先解除该角色关联的所有资源（如断开OSS连接、删除FC节点、停止DTS任务等），否则操作将被拒绝。
- **临时API Key不可撤销**：临时Key生命周期固定，到期自动失效，**不支持手动删除或提前失效**。请严格控制 `expire_in_seconds` 时长，避免过长TTL增加泄露风险。
- **SearchFilters字段约束**：仅对知识库中**已声明为可检索字段**（即建库时勾选“参与检索”的字段）生效；未声明字段即使存在于文档中也无法被过滤。多值查询需确保字段值为标准JSON数组格式（如 `["A","B"]`），字符串形式（如 `"[\"A\",\"B\"]"`）将导致匹配失败。
- **地域隔离**：临时API Key的Endpoint与永久API Key所属地域强绑定（北京/新加坡/弗吉尼亚），跨地域调用将返回 `InvalidApiKey` 错误。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


