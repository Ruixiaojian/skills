# 插件

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（API）标准化接入大模型工作流，弥补其在实时信息获取、精确计算、代码执行、多模态生成等方面的固有局限。它以“工具集合”形式组织，支持官方预置、第三方认证及完全自定义三类来源，调用可由大模型自主规划（如智能体场景）或由开发者显式编排（如工作流场景）驱动。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent）应用**：插件作为可被大模型动态发现和调用的工具，与知识库、内置工具（如 `read`/`edit`）统一抽象为「MCP 工具」。模型基于用户意图自主选择工具、填充参数并执行，支持完整「思考-执行-反思」链路回溯。需在智能体「规划」模块中启用并配置 MCP 服务。
  
- **工作流（Workflow）应用**：插件以独立节点形式拖入画布，由开发者显式控制执行顺序、输入变量（如 `${sys.query}`）和条件分支。不依赖模型决策，适合确定性、强流程约束的业务场景。

- **高代码应用**：通过「工具」Tab 关联已发布的 MCP 服务，可在 Python 函数中直接调用插件工具（如 `tool_call("quark_search", {"query": "AI 趋势"})`），实现深度定制逻辑与系统级集成。

- **Assistant API 直接调用**：在请求体的 `tools` 字段中声明插件定义（OpenAPI Schema），通过 `tool_choice` 控制调用策略（`auto` / `required` / 具体工具 ID），适用于 SDK 或 HTTP 自主集成场景。

> ⚠️ 注意：所有插件必须处于 **已发布且启用** 状态才可被调用；删除插件将不可逆清除其下所有工具及关联应用。

## 关键参数和配置

插件配置分为**插件级**（全局）与**工具级**（单个 API）两类，均在控制台「插件管理」中设置：

### 插件级参数
| 参数 | 说明 | 示例/要求 |
|------|------|-----------|
| `插件URL` | 工具路径的根域名，所有工具路径以此为前缀拼接 | `https://api.example.com`（必须以 `https://` 开头） |
| `是否鉴权` | 启用后需配置鉴权类型、位置、参数名及 [Token](token.md) | 类型：`basic` / `bearer` / `appcode`；位置：`Header` 或 `Query`；参数名如 `Authorization` 或 `api_key` |
| `Header列表` | 非鉴权场景下可透传的自定义请求头（仅限 `Authorization` 字段有效，其余 Header 将被丢弃） | `{"X-Trace-ID": "xxx"}` → 实际仅 `Authorization` 生效 |

### 工具级参数
| 参数 | 说明 | 示例/要求 |
|------|------|-----------|
| `工具路径` | 必须以 `/` 开头的相对路径 | `/search`、`/generate/image` |
| `请求方法` | 仅支持 `GET` 或 `POST` | — |
| `提交方式` | `application/json`（推荐）或 `application/x-www-form-urlencoded` | `GET` 方法不支持 `Object` 类型输入参数 |
| `输入参数` | 明确声明：参数名、描述、类型（`String`/`Number`/`Object`）、传参方式（`大模型识别` 或 `业务透传`） | `Object` 类型子属性必须非空（否则发布失败，错误码 `130022`） |
| `输出参数` | 所有字段必填，类型与嵌套层级应尽量扁平 | 避免空子属性，如 `{ "data": {} }` 不合法，需为 `{ "data": { "title": "xxx" } }` |
| `高级配置` | 可添加调用示例（`Value` 字段），显著提升大模型参数提取准确率 | 如 `{"query": "量子计算最新进展"}` |

> ✅ **调试提示**：所有自定义工具必须先通过控制台「在线调试」验证连通性与返回格式，再发布。调试失败则调用必然失败。

## 面向开发者的关键实践建议

- **选型优先级**：优先使用官方插件（开箱即用，无需配置）；三方插件需在控制台开通；自定义插件适用于自有业务系统集成，需完整遵循 OpenAPI 规范。
- **参数透传**：若工具入参设为 `业务透传`，需通过 `biz_params`（HTTP API）或 SDK 对应参数传递；用户级/服务级鉴权 [Token](token.md) 同样走 `biz_params`。
- **[Token](token.md) 安全**：切勿硬编码 Token，应在应用「部署」→「配置」中设置环境变量，并通过 `biz_params` 动态注入。
- **计费意识**：`text_to_image` 与 `quark_search` 为限时免费（需单独申请）；其余插件按调用量计费，`GET` 请求也计入计费。
- **兼容性验证**：插件实际可用性取决于模型能力与控制台运行结果，而非静态文档列表。推荐在 `qwen-plus` 或 `qwen-max` 上先行验证。
- **错误排查**：常见失败原因包括：工具未发布、`Object` 子属性为空、`GET` 方法含 `Object` 参数、Header 透传超限（仅 `Authorization` 允许）、超时（默认 5 秒）。

## 关联主题页

- [plug in](../guides/plug-in.md)
- [llm application](../guides/llm-application.md)
- [application support](../guides/application-support.md)
- [model experience](../guides/model-experience.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


