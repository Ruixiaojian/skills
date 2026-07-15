# more

`more` 是百炼平台面向开发者提供的扩展能力集合，涵盖临时凭证生成、服务关联角色管理、知识库高级检索过滤等关键功能。这些能力不直接参与模型推理，而是支撑安全调用、资源协同与精准检索等核心场景。本文档聚焦其技术细节与工程实践要点，适用于需要在可信/不可信环境集成百炼服务、构建复杂工作流或优化RAG效果的开发者。

## 支持的模型/功能

`more` 并非模型名称，而是百炼平台中一组**基础设施级扩展能力**的统称，当前包含以下三类核心功能：

- **临时API Key生成**：为浏览器、移动端等不可信客户端提供短期、可撤销的访问凭证，避免永久密钥泄露风险。该能力通过 `https://dashscope.aliyuncs.com/api/v1/tokens` 接口提供，详见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **服务关联角色（SLR）管理**：百炼在启用特定功能（如函数计算节点、OSS数据导入、ADB-PG知识库存储）时，自动创建并绑定RAM服务关联角色，以最小权限原则访问其他云服务资源。完整角色列表及权限策略见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **知识库SearchFilters**：在调用 `Retrieve` 接口时，通过结构化过滤条件对语义检索结果进行后置精筛，显著提升结构化数据（如员工表、产品目录）的召回准确率。语法支持单值、多值、范围、模糊及标签查询，详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档2中列出的 `AliyunServiceRoleForSFMAccessingMNS` 权限策略末尾存在截断（`"xtrace:Get*"` 后缺失闭合括号与完整JSON结构），实际部署应以RAM控制台中该角色绑定的最新系统策略为准；此为文档过时导致，非API行为变更。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时API Key生成 | `expire_in_seconds` | Integer | 否 | TTL有效期（秒），取值范围 `[1, 1800]`，默认60秒 | `1800` |
| SearchFilters | `searchFilters` | Array of Object | 否 | 过滤条件数组，每个Object为一个AND子分组，支持 `eq/neq/gt/gte/lt/lte/like` 等操作符 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（范围查询） | 字段值 | JSON String | 是 | 范围查询需序列化为JSON字符串，如 `{"gte": 20, "lte": 27}` | `{"gte": 20, "lte": 27}` |
| SearchFilters（模糊查询） | 字段值 | JSON String | 是 | 模糊查询需序列化为 `{"like": "技%员"}` 形式 | `{"like": "技%员"}` |

## 使用方式

- **临时API Key**：  
  在后端服务中，使用已配置的永久 `DASHSCOPE_API_KEY` 调用 `/api/v1/tokens` 接口（[生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)）。返回的 `token` 可直接用于后续模型请求的 `Authorization: Bearer <token>` 头。**切勿在前端硬编码或暴露永久密钥**。

- **服务关联角色**：  
  角色由百炼在首次启用对应功能时**自动创建**，无需手动申请。开发者需确保RAM账号具备 `AliyunRAMFullAccess` 权限以查看角色，并在删除前按文档要求清理依赖资源（如先断开OSS连接、删除函数计算节点等）。具体操作请参考 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 中各角色的“删除服务关联角色”章节。

- **SearchFilters**：  
  在 `RetrieveRequest` 请求体中直接传入 `searchFilters` 字段（[知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)）。SDK调用示例中需注意：  
  - Python/Java SDK要求将范围、模糊等复杂查询**序列化为JSON字符串**再赋值（见文档3中 `json.dumps()` 用法）；  
  - 子分组间为AND逻辑，分组内字段为AND，无法改为OR；  
  - 标签查询（`tags` 字段）中，同一分组内多个标签为OR关系，不同分组间仍为AND。

## 限制和注意事项

- **临时API Key**：  
  - 无法提前失效，仅能等待TTL过期；  
  - 继承生成者密钥的全部权限（含模型访问、知识库读写等），请严格管控生成密钥的权限粒度；  
  - 各地域Endpoint独立（北京/新加坡/弗吉尼亚），密钥不可跨地域复用。

- **服务关联角色**：  
  - 删除角色将导致对应功能完全不可用（如删除 `AliyunServiceRoleForSFMAccessFC` 后，工作流中函数计算节点将无法调用）；  
  - 部分角色（如 `AliyunServiceRoleForSFMAccessingMNS`）明确禁止手动修改或删除，违反将导致服务异常；  
  - 所有角色均需通过RAM控制台管理，百炼控制台不提供直接入口。

- **SearchFilters**：  
  - 仅对**数据查询型知识库**生效，文档型知识库不支持；  
  - 字段类型必须与知识库索引配置一致（如年龄字段需为 `double` 才能使用 `gte`）；  
  - 模糊查询（`like`）仅支持字符串字段，且 `%` 为通配符（`"技%员"` 匹配“技术员”“技师员”等）；  
  - 多值查询需将数组序列化为字符串（如 `["张三","李四"]` → `"[\\"张三\\",\\"李四\\"]"`），SDK已封装此逻辑。

> **注意**：文档3中Python示例 `multi_query()` 方法将 `names` 数组直接 `json.dumps()` 后赋值给 `search_filters`，但实际SDK（如 `alibabacloud_bailian20231229` v1.0.10+）已支持原生List传入，无需手动序列化。建议优先使用SDK最新版以避免兼容性问题。

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


