# more

`more` 是百炼平台中一组面向高级用例的扩展能力集合，涵盖服务权限管理、安全凭证分发和知识库精细化检索等关键功能。这些能力不直接参与模型推理主链路，但为生产环境下的权限隔离、前端安全调用和结构化数据过滤提供了必要支撑。开发者需结合具体场景按需启用，并严格遵循各功能的权限约束与生命周期规则。

## 支持的模型/功能

`more` 并非模型名称或独立服务，而是指代百炼平台中若干**非核心推理类扩展能力**，主要包括：
- **服务关联角色（SLR）管理**：为工作流、数据导入、知识库、监控等模块自动创建并托管对 FC、OSS、ADB-PG、MNS 等云服务的最小权限访问角色；
- **临时 API Key 生成**：用于在不可信客户端（如浏览器、App）中安全调用模型 API，避免永久密钥泄露；
- **知识库 `searchFilters` 检索过滤**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级精确筛选，适用于结构化数据场景。

> **注意**：文档中未提及任何“`more` 模型”，也无对应模型 ID 或推理接口。该术语仅作为能力分类标识，详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 和 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | TTL（秒），范围 `[1, 1800]`，默认 `60` | `?expire_in_seconds=1800` |
| `searchFilters` | `searchFilters` | array of object | 否 | 每个 object 为一个 AND 子分组，支持单值、多值、范围、模糊、标签查询 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| `searchFilters`（范围查询） | `gte`, `lte`, `gt`, `lt`, `eq`, `neq` | number/string | 否 | 字段比较操作符，需嵌套在字段值中 | `{"年龄": {"gte": 20, "lte": 27}}` |
| `searchFilters`（模糊查询） | `like` | string | 否 | 值为 `{"like": "技%员"}` 形式 | `{"岗位": {"like": "技%员"}}` |

## 使用方式

### 1. 服务关联角色（SLR）
- **触发时机**：首次在控制台启用对应功能（如添加函数计算节点、配置 OSS 数据源、启用 ADB-PG 知识库）时，系统**自动创建** SLR；
- **查看路径**：RAM 控制台 > 角色管理 > 筛选“服务关联角色”；
- **策略绑定**：每个 SLR 绑定唯一系统策略（如 `AliyunServiceRolePolicyForSFMAccessFC`），权限已固化，**不可修改**；
- **删除前提**：必须先解除所有依赖该 SLR 的资源绑定（如删除函数计算节点、断开 OSS/ADB-PG 连接、停止 MNS 订阅），否则删除失败。详情见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。

### 2. 临时 API Key
- **调用方式**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发送带 `Authorization: Bearer <永久APIKey>` 的 POST 请求；
- **地域隔离**：北京、新加坡、弗吉尼亚地域 endpoint 不互通，API Key 需匹配对应地域；
- **权限继承**：生成的 `st-***` [Token](../concepts/token.md) 完全继承源 API Key 的所有权限（含模型白名单、知识库访问限制）；
- **生命周期**：仅可设置 TTL，**不支持手动撤销**，到期自动失效。参见 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

### 3. `searchFilters`
- **适用接口**：仅限知识库 `Retrieve` 接口（`POST /api/v1/retrieve`）；
- **语法要求**：
  - 多个子分组（array 元素）间为 **AND** 逻辑；
  - 单个子分组内多个字段为 **AND** 逻辑；
  - 字段值支持字符串、数值、JSON 对象（如范围/模糊查询）；
- **前置条件**：知识库需为“数据查询”类型，且字段已正确映射为 `string`/`long`/`double` 类型；子账号需具备 `AliyunBailianDataFullAccess` 权限并加入对应业务空间。

## 限制和注意事项

- **SLR 权限不可定制**：所有 SLR 的策略由百炼预定义，开发者无法增删权限或修改 Resource 范围。例如 `AliyunServiceRoleForAccessOSS` 仅允许访问打有 `bailian-safe-workspace-oss-access: ReadAndWrite` 标签的 OSS Bucket，无法绕过该标签限制。
- **临时 API Key 无刷新机制**：TTL 一旦设定即不可延长，客户端需在过期前重新请求新 [Token](../concepts/token.md)；错误响应（如 `InvalidApiKey`）表明源 API Key 无效或已禁用。
- **`searchFilters` 与语义检索协同工作**：`searchFilters` 是在向量检索返回的候选集上做**后过滤**，不影响向量相似度计算本身；若过滤后无结果，将返回空 `nodes` 数组，而非报错。
- **跨功能依赖风险**：`AliyunServiceRoleForSFMTelemetry` 的策略片段在文档 1 中被截断（末尾缺失 `}` 和后续内容），实际权限范围应以 RAM 控制台中该策略的完整 JSON 为准。> **注意**：该截断问题已在 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 中体现，使用前请务必在控制台核验策略完整性。
- **地域一致性要求**：临时 API Key 的生成 endpoint 与模型调用 endpoint 必须同地域；知识库 `Retrieve` 接口的 `indexId` 与业务空间 ID 也需属同一地域。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


