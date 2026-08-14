# more

`more` 是百炼平台中一组面向高级用例的扩展能力集合，涵盖服务权限管理、临时凭证生成和知识库精细化检索三大方向。这些功能不直接参与模型推理主链路，但对构建安全、可控、可观察的企业级AI应用至关重要。开发者需根据具体场景选择启用，并严格遵循最小权限原则配置相关资源。

## 支持的模型/功能

`more` 并非模型名称或独立服务，而是指代百炼平台提供的若干**辅助性基础设施能力**，主要包括：

- **服务关联角色（SLR）管理**：为工作流、数据管理、安全存储、知识库、监控等模块自动创建并托管所需云服务访问权限，例如 `AliyunServiceRoleForSFMAccessFC` 用于函数计算节点调用，`AliyunServiceRoleForSFMAccessADB` 用于知识库对接 AnalyticDB-PG [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)；
- **临时 API Key 生成**：通过后端服务调用 `/api/v1/tokens` 接口，派生具备 TTL 的短期凭证，适用于前端直连等不可信环境；
- **知识库 SearchFilters**：在 `Retrieve` 接口请求中传入结构化过滤条件，支持单值、多值、范围、模糊及标签查询，显著提升语义检索精度 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)。

> **注意**：文档中未提及任何“`more` 模型”或“`more` API”，所有能力均依附于现有服务（如工作流、知识库、监控），不存在独立的 `more` 模型调用入口。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | 有效期（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |
| SearchFilters | `searchFilters` | array of object | 否 | 过滤条件数组，每个元素为 key-value 映射或含操作符的对象 | `[{"姓名": "张三"}, {"年龄": {"gte": 20, "lte": 30}}]` |
| SearchFilters（范围查询） | `gt`, `gte`, `lt`, `lte`, `eq`, `neq` | number/string | 否 | 字段比较操作符，仅支持数值字段的区间查询及字符串/数值的等值判断 | `{"年龄": {"gte": 25}}` |
| SearchFilters（模糊查询） | `like` | string | 否 | 字符串模糊匹配，支持 `%` 通配符 | `{"岗位": {"like": "技%员"}}` |

## 使用方式

### 1. 服务关联角色（SLR）
- **自动创建**：首次启用对应功能（如发布含 FC 节点的工作流）时，系统自动创建 SLR，无需手动操作；
- **权限验证**：SLR 策略已固化，不可修改；删除前必须解除所有依赖（如断开 OSS 连接、删除 FC 节点等）[服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)；
- **查看路径**：RAM 控制台 > 角色管理 > 筛选“服务关联角色”。

### 2. 生成临时 API Key
- **前提**：已配置永久 `DASHSCOPE_API_KEY` 环境变量；
- **调用方式**：
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=300" \
       -H "Authorization: Bearer $DASHSCOPE_API_KEY"
  ```
- **响应解析**：提取 `token` 字段用于后续请求，`expires_at` 为 Unix 时间戳，需校验时效性。

### 3. 使用 SearchFilters
- **适用接口**：仅限知识库 `Retrieve` 接口（`POST /api/v1/knowledge/retrieve`）；
- **构造规则**：
  - 子分组间为 `AND` 逻辑，不可更改；
  - 单个子分组内支持混合查询类型（如 `"姓名": "张三"` + `"年龄": {"gte": 25}`）；
  - 多值查询需将数组 JSON 序列化为字符串（如 `{"姓名": "[\"张三\",\"李四\"]"}`）；
- **完整示例见** [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 中的 Python/Java 代码片段。

## 限制和注意事项

- **SLR 删除风险**：删除 `AliyunServiceRoleForSFMAccessFC` 将导致所有工作流中 FC 节点失效，且需先删除节点再发布流程——此约束在 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 文档中明确强调；
- **临时 API Key 不可撤销**：生命周期固定，到期自动失效，**不支持主动吊销**，设计时应严格控制 TTL 时长；
- **SearchFilters 字段类型强约束**：范围查询（`gt`/`gte` 等）**仅支持 `long` 或 `double` 类型字段**，对 `string` 字段使用将返回错误；模糊查询（`like`）**仅支持 `string` 字段**；
- **地域隔离**：临时 API Key 的 Endpoint 与生成所用 API Key 地域强绑定（北京/新加坡/弗吉尼亚），跨地域调用将失败；
- **权限继承**：临时 API Key 继承父密钥全部权限（含模型、知识库访问白名单），**无法降权**，敏感场景建议使用专用低权限密钥生成。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


