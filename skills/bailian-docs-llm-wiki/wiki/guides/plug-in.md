# plug in

[插件](../concepts/plugin.md)是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（API）集成到大模型工作流中，弥补其在实时信息获取、精确计算、代码执行、多模态生成等方面的固有局限。[插件](../concepts/plugin.md)以“工具集合”形式组织，支持官方预置、第三方认证及完全自定义三类来源，调用由大模型自主规划或工作流显式编排驱动。其设计目标是为开发者提供可插拔、可调试、可鉴权的标准化工具接入能力。

## 支持的模型与功能

百炼当前支持在以下模型上启用[插件](../concepts/plugin.md)能力：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max` 和 `qwen-vl-plus`。各模型对插件调用的推理逻辑、工具选择准确率及上下文处理深度存在差异，**实际兼容性请以控制台运行结果为准**，而非静态列表 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。  
插件功能按来源分为三类：
- **官方插件**：开箱即用，无需配置参数，包括 `code_interpreter`（Python执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub项目检索）等；
- **三方插件**：经效果验证的商业/垂直领域插件，开通后即可调用；
- **自定义插件**：开发者可基于自有API创建，支持完整生命周期管理（创建、调试、发布、鉴权、删除），详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 中称“夸克搜索插件目前支持检索出网页标题、关键词和摘要，但不支持直接访问网页详情”，而最新控制台实测已支持返回结构化摘要及部分可点击链接；该描述已过时，请以实际 API 返回字段为准。

## 关键参数

插件配置核心参数分为**插件级**与**工具级**两类：

- **插件级参数**：
  - `插件URL`：工具路径的根域名（如 `https://example.com`），所有工具路径均以此为前缀拼接；
  - `是否鉴权`：启用后需配置鉴权类型（`basic`/`bearer`/`appcode`）、位置（`Header` 或 `Query`）、参数名（如 `Authorization` 或 `api_key`）及 `Token`；
  - `Header列表`：非鉴权场景下可透传自定义请求头。

- **工具级参数**：
  - `工具路径`：必须以 `/` 开头的相对路径（如 `/query`）；
  - `请求方法`：仅支持 `GET` 或 `POST`；
  - `提交方式`：`application/json`（推荐）或 `application/x-www-form-urlencoded`；
  - `输入参数`：需明确 `参数名称`、`参数描述`、`类型`（`String`/`Number`/`Object` 等）、`传参方式`（`大模型识别` 或 `业务透传`）；
  - `输出参数`：所有参数必填，类型与嵌套层级应尽量扁平，避免空子属性（[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 明确要求 Object 类型子属性不能为空）；
  - `高级配置`：可添加调用示例（`Value` 字段），提升大模型参数提取准确率。

## 使用方式

插件可通过三种方式集成：
1. **智能体应用**：在编排页面的 **MCP 区块** 添加插件（需先发布为 MCP 服务），支持对话式测试与鉴权 [Token](../concepts/token.md) 配置；
2. **工作流应用**：将插件作为独立节点拖入流程，由用户显式编排执行顺序，不依赖大模型自动决策；
3. **Assistant API**：在 `tools` 参数中传入工具定义，通过 `tool_choice` 控制调用策略，详见 [Assistant API 文档](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api)。

调用时，若工具入参设为 `业务透传`，需通过 `biz_params`（HTTP API）或 SDK 对应参数传递；用户级/服务级鉴权 [Token](../concepts/token.md) 同样通过 `biz_params` 透传。工具 ID 可在插件详情页悬浮工具名称后复制获取。

## 限制和注意事项

- **发布约束**：工具名称长度 ≤20 字符；`GET` 方法不支持 `Object` 类型输入参数；`Object` 类型参数的子属性必须非空，否则发布失败（错误码 `130022`）；
- **状态依赖**：仅 `已发布` 且 `启用` 状态的工具方可被调用；删除插件将**不可逆地清除其下所有工具及关联应用**；
- **RAM 用户权限**：子账号从云市场导入插件前，需主账号授予 `ram:CreateServiceLinkedRole` 权限，并限定 `ServiceName` 为 `cloundapi-access.sfm.aliyuncs.com`；
- **调试必要性**：所有自定义工具必须通过 **在线调试** 验证连通性与返回格式，再发布，否则调用必然失败；
- **计费说明**：官方插件中 `text_to_image` 与 `quark_search` 为限时免费，需单独申请开通；其余官方及三方插件按调用量计费，详情见控制台定价页。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


