# 插件

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API、计算服务或生成服务）封装为标准化、可被大模型识别与调用的接口，弥补模型在实时信息获取、精确计算、代码执行、图像生成等场景下的固有局限。插件本身不依赖特定模型推理逻辑，而是作为“能力代理”被智能体自主调度或在工作流中显式编排。

## 在百炼平台的不同场景中如何使用

- **智能体应用（Agent 2.0）**：插件以 MCP（Model Calling Protocol）服务形式接入，在对话过程中由大模型基于用户意图、工具名称与描述自动决策调用（例如：“算一下 123 × 456” → 自动触发 `calculator`；“生成一只穿宇航服的猫” → 触发 `text_to_image`）。需在智能体配置页的 **MCP 区块** 添加插件，并确保所选模型支持该插件类型（如 `qwen-max` 支持 `code_interpreter`，`qwen-vl-max` 支持 `text_to_image`）。

- **工作流应用（Workflow）**：插件作为独立节点拖入画布，无需模型参与决策。开发者可手动配置输入参数映射（如将 `${sys.query}` 映射为搜索关键词）、设置失败重试策略，并直接连接下游节点处理返回结果，适用于确定性、高可控性的业务流程（如“用户提问 → 调用 `quark_search` → 提取摘要 → 生成摘要卡片”）。

- **Assistant API 调用**：在请求体的 `tools` 字段中声明插件 ID（如 `"calculator"`）及完整工具定义（含名称、描述、参数 schema），平台将自动注入工具上下文并返回调用结果。若插件需业务级参数（如用户 ID、会话上下文）或动态鉴权凭证，须通过 `biz_params` 字段传入。

- **高代码应用**：通过 SDK 或 HTTP Client 直接调用插件后端服务（URL 可在插件详情页获取），适用于需要深度定制请求逻辑、混合多插件响应或对接内部认证体系的场景。此时插件退化为标准 REST API，不再经过大模型调度层。

> ⚠️ 注意：插件调用受 `ReAct 最大轮次`（默认 10，可配 1–50）限制；单次会话中所有插件调用总次数超限时，模型将终止调用并生成最终回复。

## 关键参数和配置

插件配置分为两个层级，均在控制台插件管理页或 API 创建时定义：

### 插件级参数（全局配置）
| 参数 | 类型 | 说明 |
|------|------|------|
| `plugin_url` | String | 插件服务的基础域名（如 `https://api.example.com/v1`），不包含路径。 |
| `is_auth_enabled` | Boolean | 是否启用鉴权，默认 `false`。启用后需配置以下字段。 |
| `auth_type` | Enum | 鉴权方式：`basic`（HTTP Basic）、`bearer`（Bearer [Token](token.md)）、`appcode`（阿里云 AppCode）。 |
| `auth_location` | Enum | 凭证位置：`Header`（推荐）或 `Query`。 |
| `auth_param_name` | String | 凭证 Header Key 或 Query Param 名（如 `Authorization`、`X-API-Key`）。 |
| `auth_token` | String | 服务级固定 [Token](token.md)（仅 `bearer`/`basic` 类型需填；`appcode` 类型由平台自动注入）。 |

### 工具级参数（每个工具独立配置）
每个插件可包含多个工具（如一个搜索插件含 `web_search` 和 `news_search`），每项工具需定义：

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `name` | 是 | String（≤20 字符） | 工具唯一标识，用于模型识别和 API 引用，不可含空格或特殊符号。 |
| `description` | 是 | String | **核心字段**：清晰说明工具用途、输入约束、输出格式及典型触发语句（如 `"根据城市名和日期查询天气，返回温度、湿度、天气状况，不支持历史数据"`）。质量直接影响模型调用准确率。 |
| `parameters` | 是 | Object Schema | OpenAPI 3.0 兼容的参数定义，支持 `String`/`Number`/`Boolean`/`Object` 类型。`Object` 类型子属性必须显式声明且非空（否则发布失败，错误码 `130022`）；GET 请求不支持 `Object` 类型参数。 |
| `passing_method` | 是 | Enum | `model_recognition`（由大模型解析提取）或 `biz_transmission`（由业务系统透传，不经过模型理解，适合敏感/结构化参数）。 |
| `output_description` | 是 | String | 精简描述 API 响应体结构（如 `"JSON 对象，含 url 字段（图片地址）和 width/height 字段"`），用于指导模型解析结果。 |

> ✅ 推荐实践：对 `model_recognition` 类型参数，提供 `user_input → payload` 映射示例（如 `"画一只红色熊猫"` → `{"prompt": "red panda", "style": "realistic"}`），显著提升参数提取准确率。

## 面向开发者的重要提示

- **模型兼容性请以控制台为准**：文档列出的支持模型（如 `qwen-turbo`, `qwen-vl-plus`）仅为参考，实际可用性取决于插件类型与当前控制台版本。创建插件后，请在目标模型下测试调用。
- **自定义插件调试建议**：先用 `curl` 直接调用 `plugin_url` + 工具路径验证服务可用性与鉴权逻辑，再接入平台；利用 `biz_params` 传递运行时变量（如用户 token、session_id），避免硬编码。
- **安全红线**：RAM 子账号需主账号授予 `ram:CreateServiceLinkedRole` 权限方可使用插件市场；生产环境严禁使用主账号 AccessKey 调用 API。
- **错误排查重点**：  
  - `130022` 错误 → 检查 `Object` 参数子属性是否为空或 GET 请求误用 `Object`；  
  - 工具未被调用 → 检查 `description` 是否模糊、是否缺少否定约束（如“不支持 PDF 解析”）、模型是否支持该插件；  
  - 鉴权失败 → 核对 `auth_location` 与实际请求头/Query 位置是否一致，`auth_param_name` 是否拼写正确。

## 关联主题页

- [plug in](../guides/plug-in.md)
- [skill](../guides/skill.md)
- [llm application](../guides/llm-application.md)
- [application component api reference](../api/application-component-api-reference.md)


