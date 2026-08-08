# more

`more` 是百炼平台面向高级用例提供的扩展能力集合，涵盖临时凭证生成、服务关联角色管理、知识库精细化检索等关键功能。这些能力主要用于增强安全性、实现跨云服务集成、提升RAG检索精度，适用于对权限控制、资源联动和语义过滤有明确需求的开发者场景。所有功能均需通过API调用或SDK集成使用，不提供独立控制台入口。

## 支持的模型/功能

`more` 并非单一模型，而是平台级能力模块，当前包含三类核心功能：

- **临时API Key生成**：为不可信前端环境（如浏览器、App）提供短期有效的访问凭证，避免永久密钥泄露风险。该能力继承源API Key的全部权限范围，包括模型调用与知识库访问限制 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- **服务关联角色（SLR）管理**：百炼自动创建并维护一系列RAM服务关联角色，用于安全访问其他阿里云服务（如FC、OSS、ADB-PG、MNS、SLS等）。每个SLR对应特定业务场景（如工作流调用函数计算、数据管理导入OSS、安全存储空间连接ADB-PG），其权限策略严格限定于最小必要范围 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **知识库SearchFilters**：在`Retrieve`接口中支持结构化过滤条件，可对语义检索结果按字段进行单值、多值、范围、模糊及标签查询，显著提升RAG结果相关性，尤其适用于员工信息、产品目录等结构化数据场景 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档2中 `AliyunServiceRoleForSFMAccessingMNS` 的权限说明在末尾被截断（`"xtrace:Describe*"` 后缺失闭合括号及后续内容），实际策略应以RAM控制台或最新版策略文档为准；建议调用 `GetPolicy` API 获取完整策略定义。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时API Key | `expire_in_seconds` | integer | 否 | TTL有效期（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |
| SearchFilters | `searchFilters` | array of object | 否 | 过滤条件数组，每个元素为键值对对象，子分组间为AND逻辑 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SearchFilters（范围查询） | `gte`, `lte`, `gt`, `lt`, `eq`, `neq` | number/string | 否 | 字段比较操作符，需嵌套在字段值中（JSON字符串化） | `{"年龄": "{\"gte\":20,\"lte\":27}\"}` |
| SearchFilters（模糊查询） | `like` | string | 否 | 模糊匹配值，支持 `%` 通配符 | `{"岗位": "{\"like\":\"技%员\"}\"}` |

## 使用方式

- **临时API Key**：通过HTTP POST请求调用 `https://dashscope.aliyuncs.com/api/v1/tokens`（新加坡地域）或对应地域Endpoint，携带 `Authorization: Bearer <永久API Key>`。响应返回 `token`（临时Key）和 `expires_at`（UNIX时间戳）。该[Token](../concepts/token.md)可直接用于后续所有百炼API调用的鉴权头。
- **服务关联角色**：无需手动创建。当首次启用对应功能（如在工作流中添加FC节点、在安全存储空间中绑定ADB-PG实例）时，系统自动创建SLR。开发者仅需确保主账号具备 `AliyunRAMFullAccess` 权限，并在RAM控制台确认角色已存在。
- **SearchFilters**：在调用 `bailian20231229.Retrieve` 接口时，将过滤条件作为 `searchFilters` 字段传入请求体。注意：字段名必须与知识库索引时定义的字段名完全一致（区分大小写）；数值字段需确保类型匹配（如`年龄`为`double`，不可传入字符串`"25"`）；多值、范围、模糊查询需将条件对象JSON序列化后作为字段值传入（见[完整代码示例](../../raw/application-api-reference/more/how-to-use-search-filters.md)）。

## 限制和注意事项

- 临时API Key **无法提前撤销**，仅能等待自然过期。生成后即生效，无刷新机制 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。
- 所有服务关联角色均绑定特定服务主体（如 `datahub.sfm.aliyuncs.com`），**禁止手动修改其策略或删除角色**，否则将导致对应功能完全不可用。如确需删除，必须先解除所有依赖资源（如删除工作流中的FC节点、断开OSS连接等），再通过RAM控制台操作 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- SearchFilters 仅作用于 `Retrieve` 接口，**不适用于`Chat`或`Complete`等生成式接口**；过滤字段必须已在知识库索引配置中声明为“参与检索”，否则无效；标签查询（`tags`）仅支持文档搜索/音视频搜索类知识库，不支持通用文本搜索 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。
- 临时API Key 的地域Endpoint与源API Key所属地域强绑定，跨地域调用将返回 `InvalidApiKey` 错误；各Region的Endpoint需严格匹配（北京：`dashscope.aliyuncs.com`，新加坡：`dashscope.aliyuncs.com`，弗吉尼亚：`dashscope.us-east-1.aliyuncs.com`）。

## 来源文档

- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


