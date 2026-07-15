# more

`more` 是百炼平台面向高级用例提供的扩展能力集合，涵盖服务权限管理、知识库精准检索、临时凭证生成等关键功能。这些能力不直接参与模型推理主流程，但对构建安全、可控、可观察的企业级AI应用至关重要。开发者需结合具体场景按需启用，并严格遵循最小权限原则。

## 支持的模型/功能

`more` 不对应特定模型，而是提供以下三类基础设施级功能：

- **服务关联角色（SLR）管理**：为百炼各子功能（如工作流调用函数计算、知识库对接ADB-PG、数据同步访问OSS等）自动创建并托管云资源访问权限。详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **知识库高级检索（SearchFilters）**：在 `Retrieve` 接口请求中嵌入结构化过滤条件，支持单值、多值、范围、模糊及标签查询，显著提升语义检索结果的相关性。该能力仅适用于已配置字段索引的数据查询型知识库。
- **临时API Key生成**：通过后端服务调用 `/tokens` 接口，基于永久密钥签发短期有效的访问令牌，适用于前端直连等不可信环境。详见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

> **注意**：文档 1 中列出的 `AliyunServiceRoleForSFMTelemetry` 权限策略在末尾被截断（`"xtrace:Read*", "xtrace:Get*"` 后缺失完整内容），实际策略应以控制台或最新版RAM策略文档为准；同时，文档 2 中 `tag_query2()` 示例代码在末尾被截断，完整逻辑需参考SDK示例仓库。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|------|--------|------|------|------|----------|
| 临时API Key | `expire_in_seconds` | integer | 否 | 令牌有效期（秒） | `[1, 1800]`，默认 `60` |
| SearchFilters | `searchFilters` | array of object | 否 | 过滤条件数组，每个对象为一个AND分组 | 最多支持 5 个分组；每个分组内Key-Value对数量无硬限制，但总请求体大小 ≤ 1 MB |

## 使用方式

- **服务关联角色**：系统在首次启用对应功能（如发布含FC节点的工作流）时**自动创建**，无需手动调用API。角色名称与权限策略已固化，不可修改。删除前必须先解除所有依赖该角色的业务配置（如断开OSS连接、删除FC节点等），否则将导致功能异常。
- **SearchFilters**：在 `RetrieveRequest` 请求体中直接传入 `searchFilters` 字段。例如：
  ```json
  {
    "indexId": "o73yjlxxxx",
    "query": "公司中姓名为张三的员工",
    "searchFilters": [
      {"姓名": "张三"},
      {"岗位": "技术员", "年龄": {"gte": 20, "lte": 27}}
    ]
  }
  ```
  具体语法与字段类型约束请参考 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。
- **临时API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <permanent_key>` 的 POST 请求，可选添加 `?expire_in_seconds=N` 查询参数。响应中的 `token` 字符串可直接用于后续模型API调用的 `Authorization` 头。

## 限制和注意事项

- 所有服务关联角色均绑定特定百炼服务域名（如 `fc.sfm.aliyuncs.com`），**不可复用或跨服务授权**。手动修改其策略或删除角色将导致对应功能完全失效。
- `SearchFilters` 仅对**数据查询型知识库**生效，文档型知识库不支持字段级过滤；多值查询需使用 `json.dumps(["val1","val2"])` 序列化为字符串传递；模糊查询 `like` 值中 `%` 为通配符。
- 临时API Key 继承源密钥的全部权限（含模型白名单、知识库访问限制等），且**无法提前撤销**，仅能等待过期。生产环境务必严格控制 `expire_in_seconds` 时长，避免设置过长TTL。
- 文档 1 中 `AliyunServiceRoleForSFMAccessingMNS` 明确声明“请勿修改、删除，或将其授予除服务关联角色之外的任何RAM身份”，此为强制安全要求，违反将导致数据同步中断且难以恢复。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)


