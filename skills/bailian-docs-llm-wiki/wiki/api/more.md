# more

`more` 是百炼平台面向高级用例提供的扩展能力集合，涵盖服务权限管理、知识库精准检索、临时凭证生成等关键功能。这些能力不直接参与模型推理主流程，但对构建安全、可控、可观察的企业级AI应用至关重要。开发者需根据具体场景按需启用，并严格遵循最小权限原则。

## 支持的模型/功能

`more` 并非模型名称，而是百炼平台中一组**支撑性功能模块**的统称，当前主要包括：
- **服务关联角色（SLR）管理**：为工作流、数据管理、安全存储、模型监控等子系统自动创建并托管云资源访问权限，例如 `AliyunServiceRoleForSFMAccessFC` 用于函数计算节点调用 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)；
- **知识库检索过滤（SearchFilters）**：在 `Retrieve` 接口请求中嵌入结构化过滤条件，实现语义检索结果的字段级精筛，适用于数据查询型知识库 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)；
- **临时API Key生成**：通过后端服务调用 `/tokens` 接口签发短期有效的访问令牌，用于前端或移动端等不可信环境的安全调用 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

> **注意**：文档1中列出的 `AliyunServiceRoleForSFMTelemetry` 权限策略内容被截断（末尾缺失 `}`），且其 `log:Get*` 等权限范围未明确限定 project 前缀是否支持通配符；实际部署时请以控制台最新策略定义或 OpenAPI 返回为准。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 示例 |
|------|--------|------|------|------|------|
| 临时API Key | `expire_in_seconds` | integer | 否 | 有效期（秒），取值范围 `[1, 1800]`，默认 `60` | `1800` |
| SearchFilters | `searchFilters` | array of object | 否 | 过滤条件数组，每个对象为一个AND分组，支持单值、多值、范围、模糊、标签查询 | `[{"姓名": "张三"}, {"岗位": "技术员"}]` |
| SLR 删除 | — | — | — | 无显式参数，但删除前必须满足前置条件（如断开OSS连接、删除FC节点等） | — |

## 使用方式

- **服务关联角色**：首次启用对应功能（如发布含FC节点的工作流）时由系统**自动创建**，无需手动调用API；查看与管理需前往 [RAM控制台](https://ram.console.aliyun.com/) 的角色管理页。
- **SearchFilters**：在调用 `Retrieve` 接口时，将过滤条件作为 `searchFilters` 字段传入请求体，详见 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 中的完整代码示例。
- **临时API Key**：向 `https://dashscope.aliyuncs.com/api/v1/tokens` 发起带 `Authorization: Bearer <永久AK>` 的 POST 请求，可选添加 `expire_in_seconds` 查询参数。

## 限制和注意事项

- **SLR 删除风险高**：删除任一服务关联角色（如 `AliyunServiceRoleForAccessOSS`）将导致依赖该角色的功能（如安全存储空间）**立即失效**，且删除前必须完成所有前置清理（如断开连接、删除任务），否则操作会被拒绝 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **SearchFilters 依赖知识库配置**：仅当知识库类型为“数据查询”且索引设置中已声明相关字段（如 `姓名`、`年龄`）时，`searchFilters` 才生效；文本型知识库不支持此特性。
- **临时API Key 权限继承**：生成的临时[Token](../concepts/token.md)**完全继承**签发所用永久API Key 的全部权限（含模型白名单、知识库访问限制等），无法做细粒度降权。
- **地域隔离**：临时API Key 的Endpoint与永久API Key 地域强绑定（北京/新加坡/弗吉尼亚），跨地域调用会返回 `InvalidApiKey` 错误 [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)


