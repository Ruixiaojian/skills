# more

`more` 是百炼平台面向开发者提供的扩展能力集合，涵盖服务权限管理、知识库高级检索、安全认证机制等关键功能模块。这些能力不直接参与模型推理主流程，但为构建生产级应用提供必要的基础设施支持，如跨云服务访问授权、结构化数据精准过滤、前端调用安全隔离等。开发者需根据具体场景按需启用并配置相关组件。

## 支持的模型/功能

`more` 并非模型名称或独立服务，而是百炼平台中一组**支撑性功能模块**的统称，主要包括：

- **服务关联角色（SLR）**：为百炼集成外部云服务（如 FC、OSS、ADB-PG、MNS、SLS 等）自动创建和管理的 RAM 角色，实现最小权限访问控制 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)；
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中使用的结构化过滤语法，支持单值、多值、范围、模糊及标签查询，用于对语义检索结果进行后置精准筛选 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)；
- **临时 API Key 生成**：通过后端调用 `/api/v1/tokens` 接口，基于永久 API Key 签发短期有效的凭证，适用于浏览器或移动端等不可信环境 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

> **注意**：文档 1 中列出的 `AliyunServiceRoleForSFMAccessFC` 等 SLR 名称均以 `AliyunServiceRoleFor...` 开头，但文档 2 和文档 3 均未提及任何模型名称或 `more` 对应的模型 ID。这表明 `more` 不代表某类模型，而是功能聚合标识 —— 此处无矛盾，但需避免误认为 `more` 是可调用的模型类型。

## 关键参数

| 功能模块 | 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|----------|--------|------|------|------|-----------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | 临时 [Token](../concepts/token.md) 有效期（秒） | `[1, 1800]`，默认 `60` |
| SearchFilters | `searchFilters` | array of object | 否 | 过滤条件数组，每个对象为一个 AND 分组 | 每个分组内支持 `eq`/`neq`/`gt`/`gte`/`lt`/`lte`/`like` 等操作符，详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) |
| SLR 权限 | — | — | — | 各 SLR 绑定的系统策略（如 `AliyunServiceRolePolicyForSFMAccessFC`）已固化，**不可自定义修改** | 详见各 SLR 的 JSON 权限策略声明 |

## 使用方式

- **服务关联角色**：首次启用对应功能（如工作流中添加函数计算节点、知识库接入 ADB-PG）时，百炼后台**自动创建**所需 SLR；无需手动调用 API，但需确保主账号具备 `ram:CreateServiceLinkedRole` 权限。
- **SearchFilters**：在调用 `POST /api/v1/retrieve` 接口时，将 `searchFilters` 字段作为 JSON 数组嵌入请求体，例如：  
  ```json
  {
    "indexId": "o73yjlxxxx",
    "query": "张三",
    "searchFilters": [{"姓名": "张三"}, {"岗位": "技术员"}]
  }
  ```
- **临时 API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <永久Key>` 的 POST 请求，可选附加 `?expire_in_seconds=1800` 查询参数。

## 限制和注意事项

- **SLR 删除风险高**：删除任一 SLR（如 `AliyunServiceRoleForSFMAccessFC`）将导致依赖该角色的功能**立即失效**（如工作流无法调用 FC 函数），且删除前必须先清理所有关联资源（如移除流程中的 FC 节点）[服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **SearchFilters 依赖知识库字段类型**：仅当知识库索引字段明确声明为 `string` 或 `double`/`long` 类型时，对应查询（如 `like` 或 `gte`）才生效；未声明类型的字段不支持过滤。
- **临时 API Key 不可撤销**：一旦签发，只能等待其自然过期（最长 30 分钟），**不支持主动吊销**；因此应严格控制 `expire_in_seconds` 时长，并确保后端服务对签发行为有审计日志。
- **地域隔离**：临时 API Key 接口 Endpoint 与永久 API Key 所属地域强绑定（北京/新加坡/弗吉尼亚），跨地域调用将返回 `InvalidApiKey` 错误 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)


