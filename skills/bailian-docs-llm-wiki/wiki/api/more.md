# more

`more` 是百炼平台中一组面向高级用例与安全治理的扩展能力集合，涵盖服务权限管理、临时凭证分发、知识库精细化检索等关键功能。这些能力不直接参与模型推理主流程，但对生产环境下的权限隔离、客户端安全调用和结构化数据召回质量起决定性作用。开发者需按场景按需启用，并严格遵循各功能的权限约束与生命周期规则。

## 支持的模型/功能

`more` 不对应具体模型，而是提供三类核心支撑功能：

- **服务关联角色（SLR）管理**：为百炼子系统（如工作流、数据管理、安全存储空间、模型监控等）自动创建并托管对其他云服务（FC、OSS、ADB-PG、MNS、SLS、CMS、OpenTelemetry、内容安全、DTS、CPFS）的最小权限访问能力。详见 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)。
- **临时 API Key 生成**：支持后端服务基于永久 API Key 签发带 TTL 的短期凭证，适用于浏览器、移动端等不可信环境的安全调用，避免长期密钥泄露风险。
- **知识库 `SearchFilters` 检索过滤**：在 `Retrieve` 接口请求中嵌入结构化过滤条件，对语义检索结果进行字段级、范围级、模糊级或标签级二次筛选，显著提升结构化知识库（如员工表、产品目录）的召回精准度。

## 关键参数

| 功能 | 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|------|--------|------|------|------|-----------|
| 临时 API Key | `expire_in_seconds` | integer | 否 | 指定临时 [Token](../concepts/token.md) 有效期（秒） | `[1, 1800]`，默认 `60` |
| `SearchFilters` | `searchFilters` | array of object | 否 | 过滤条件数组，每个元素为一个子分组（AND 语义） | 子分组内支持 `{"字段": "值"}`（单值）、`{"字段": "[\"v1\",\"v2\"]"}`（多值）、`{"字段": "{\"gte\":20,\"lte\":27}\"}`（范围）、`{"字段": "{\"like\":\"技%员\"}"}`（模糊）、`{"tags": "[\"A大学\",\"学生会主席\"]"}`（标签） |

> **注意**：文档 3 中 `multi_query` 示例代码使用 `json.dumps(names)` 构造多值字符串，但实际 API 要求该字符串必须是合法 JSON 数组格式（如 `["张三","李四"]`），而非 Python 字符串表示；若传入非标准 JSON（如含单引号或未转义），将导致 400 错误。请严格按 [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md) 文档的语法说明构造。

## 使用方式

- **服务关联角色**：无需手动创建。当您首次在控制台启用某项依赖外部云服务的功能（例如在工作流中添加函数计算节点、在安全存储空间中绑定 OSS Bucket）时，百炼会自动为您创建对应 SLR。您可在 RAM 控制台的角色管理页查看与管理。删除前务必按文档要求先解除所有业务绑定。
- **临时 API Key**：通过 `POST /api/v1/tokens` 接口调用，需在 `Authorization: Bearer <permanent_api_key>` 头中携带有效永久密钥。响应返回 `token`（即临时 API Key）与 `expires_at`（UNIX 时间戳）。该 token 可直接用于后续任意百炼 API 请求（如 `/chat/completions`, `/retrieve`），权限继承自签发密钥。
- **`SearchFilters`**：在调用 `Retrieve` 接口（`POST /api/v1/retrieve`）的请求体中，于 `searchFilters` 字段传入过滤条件数组。需确保知识库已按字段类型（string/long/double）正确配置索引，且字段名与知识库元数据定义完全一致（区分大小写）。

## 限制和注意事项

- **SLR 删除风险高**：删除任一服务关联角色（如 `AliyunServiceRoleForSFMAccessFC`）将立即导致对应功能不可用（如工作流无法调用 FC 函数），且恢复需重新授权并可能触发资源重建。操作前必须按 [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md) 文档要求完成前置清理。
- **临时 API Key 不可撤销**：其生命周期由 `expire_in_seconds` 决定，到期自动失效，**不支持主动吊销或提前删除**。因此应严格控制 TTL 时长，并确保签发服务自身具备访问控制能力。
- **`SearchFilters` 依赖知识库结构**：仅对“数据查询”类型知识库及明确配置为索引字段的元数据生效；对纯文本切片的全文检索无效。多值、范围、模糊查询需字段类型匹配，否则过滤条件被静默忽略。
- **地域隔离**：临时 API Key 的签发 Endpoint 与使用 Endpoint 必须同地域（如新加坡签发的 token 不能用于北京 Endpoint），且各地域 API Key 独立管理。> **注意**：文档 2 中“以下示例使用新加坡地域的 Endpoint”表述易引发误解——实际 `https://dashscope.aliyuncs.com/api/v1/tokens` 是全局统一入口，但其签发的 token 仅能用于调用同一地域的百炼 API（如 `bailian.cn-beijing.aliyuncs.com`），此限制由服务端校验，非 DNS 或路由层面。

## 来源文档

- [服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)
- [生成临时API Key](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)
- [知识库SearchFilters](../../raw/application-api-reference/more/how-to-use-search-filters.md)


