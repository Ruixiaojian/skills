# more

`more` 是百炼平台提供的扩展能力集合，涵盖服务权限管理、安全认证机制与高级检索控制三大方向。它不直接提供模型推理能力，而是支撑工作流编排、知识库精准检索、监控可观测性等关键场景的底层基础设施。开发者需结合具体功能模块按需启用和配置。

## 支持的模型/功能

`more` 本身**不提供独立模型**，而是为以下核心功能提供支撑能力：

- **服务关联角色（SLR）**：自动创建并管理百炼访问其他阿里云服务所需的最小权限角色，覆盖函数计算（FC）、OSS、ADB-PG、MNS、OpenTelemetry、内容安全、SLS、CMS、DTS、CPFS 等十余类资源 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。  
- **临时 API Key 生成**：用于在不可信前端环境（如浏览器、App）中安全调用模型服务，避免永久密钥泄露。  
- **知识库 `searchFilters` 高级过滤**：在 `Retrieve` 接口请求中传入结构化过滤条件，对语义检索结果进行字段级精确筛选，显著提升 RAG 场景下结构化数据的召回准确性 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档 1 中列出的 `AliyunServiceRoleForSFMAccessFC` 权限仅包含 `fc:ListFunctions` 和 `fc:InvokeFunction`，但实际工作流节点可能还需 `fc:GetFunction` 等元信息权限以支持动态发现。建议以控制台实际策略为准，或参考最新 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 文档中的策略定义。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | TTL（秒），取值范围 `[1, 1800]`，默认 `60` | `?expire_in_seconds=1800` |
| `searchFilters` | `searchFilters` | array of object | 否 | 检索过滤子分组列表，每个子分组内为 `key: value` 或 `key: {operator: value}` 形式 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| `searchFilters`（范围查询） | `gte`, `lte`, `gt`, `lt`, `eq`, `neq` | number/string | 否 | 字段操作符，用于数值或字符串等值/区间过滤 | `{"年龄": {"gte": 20, "lte": 27}}` |
| `searchFilters`（模糊查询） | `like` | string | 否 | 字符串模糊匹配，支持 `%` 通配符 | `{"岗位": {"like": "技%员"}}` |

## 使用方式

### 1. 服务关联角色（SLR）
- **自动创建**：首次在控制台启用对应功能（如函数计算节点、OSS 数据导入）时，系统自动创建 SLR，无需手动操作。  
- **手动查看/删除**：前往 [RAM 控制台 → 角色管理](https://ram.console.aliyun.com/)，筛选服务关联角色；删除前**必须**先解除相关功能依赖（如删除工作流中的 FC 节点、断开 OSS 连接等），否则将导致功能异常 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。

### 2. 生成临时 API Key
- **调用方式**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发送带 `Authorization: Bearer <永久APIKey>` 的 POST 请求。  
- **地域适配**：Endpoint 因地域而异（北京、新加坡、弗吉尼亚），需使用对应地域的 API Key 和 Endpoint。  
- **鉴权继承**：临时 [Token](../concepts/token.md) 继承源 API Key 的全部权限（含模型白名单、知识库访问限制等）。

### 3. `searchFilters` 使用
- **请求位置**：作为 `RetrieveRequest` 的字段，与 `query`、`indexId` 同级传入。  
- **语法规则**：
  - 子分组间为 **AND** 逻辑（不可更改）；
  - 单个子分组内支持单值、多值、范围、模糊、标签五种查询类型；
  - 多值查询需将数组 `json.dumps` 后作为字符串值传递（见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 示例代码）。

## 限制和注意事项

- **SLR 删除风险**：删除任一 SLR 将直接导致其关联功能不可用（如删 `AliyunServiceRoleForSFMAccessFC` → 工作流 FC 节点失效），且无自动恢复机制。务必按文档要求前置清理依赖。  
- **临时 API Key 不可撤销**：生命周期固定，到期自动失效，**不支持手动删除或提前吊销** [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。  
- **`searchFilters` 兼容性**：仅适用于知识库类型为 **数据查询** 的索引；文档搜索、音视频搜索类知识库仅支持 `tags` 查询，其他字段过滤无效。  
- **权限最小化原则**：SLR 策略已按功能最小化设计，**禁止修改或复用其策略**；若需自定义权限，请创建独立 RAM 角色并显式授权。  
- **地域隔离**：临时 API Key、知识库 `Retrieve` 接口均严格绑定地域，跨地域调用将返回鉴权失败。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


