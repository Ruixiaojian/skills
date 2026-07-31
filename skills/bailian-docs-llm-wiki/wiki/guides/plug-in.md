# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API）集成到推理流程中，弥补大模型在实时信息获取、精确计算、代码执行、图像生成等方面的固有局限。插件以“工具”为最小可调用单元，支持官方预置、三方市场及完全自定义三种来源，可在智能体应用、工作流应用或 Assistant API 中按需启用。其核心价值在于将任务规划与[工具调用](../concepts/tool-use.md)解耦，由大模型自主决策是否及如何调用。

## 支持的模型/功能

百炼当前支持在以下模型上启用插件能力：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件的兼容性存在差异，**实际可用性请以控制台运行结果为准**，不建议依赖文档静态列表。插件功能覆盖三大类：

- **官方插件**：开箱即用，无需配置参数，包括 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）。详细说明见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。
- **三方插件**：来自阿里云云市场，覆盖商业服务、图像视频、教育等垂直领域，开通后即可调用，无需额外配置。授权与开通流程详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **自定义插件**：支持用户通过控制台创建或从云市场导入，可对接任意 HTTP API，并精细配置鉴权（Header/Query、Bearer/AppCode 等）、输入/输出参数、高级调用示例。完整开发流程参见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 和文档 2 均列出 `quark_search` 插件，但文档 2 明确指出其“目前支持检索出网页标题、关键词和摘要，但不支持直接访问网页详情”，而文档 1 仅模糊表述为“不支持直接访问网页详情”。此处以文档 2 的明确限定为准。

## 关键参数

插件调用依赖两类关键参数：

- **工具 ID（tool_id）**：唯一标识一个工具，如 `calculator`、`text_to_image`。必须在 API 请求或应用配置中准确传递。获取方式：在插件详情页悬浮工具名称图标后复制（[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。
- **输入参数（input parameters）**：由大模型从用户输入中提取（传参方式设为“大模型识别”）或由业务系统透传（设为“业务透传”，需通过 `biz_params` 传递）。参数需明确定义名称、类型（String/Number/Object）、描述及必填性；Object 类型子属性**不能为空**，否则发布失败（[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。
- **鉴权参数**：若插件开启鉴权，需配置 Header 或 Query 中的 [Token](../concepts/token.md) 及 Type（`basic`/`bearer`/`appcode`）。例如 `bearer` 类型将自动拼接为 `Authorization: Bearer <TOKEN>`。

## 使用方式

插件可通过三种方式集成：

1. **控制台可视化集成**：
   - 在 [插件市场](https://bailian.console.aliyun.com/#/plugin-market) 页面，为智能体应用添加工具（最多 10 个），要求官方插件与目标智能体**位于同一业务空间**（[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。
   - 自定义插件需先发布为 MCP 服务，再在智能体编排页面的 **MCP 区块**中添加（[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。

2. **工作流应用节点**：将插件作为独立节点编排进工作流，按预设逻辑执行，**不由大模型自主决策调用时机**（[插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)）。

3. **API 调用**：
   - Assistant API：在请求 `tools` 字段中声明工具列表，大模型将返回 `tool_calls` 指令，客户端需执行调用并回传结果（[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。
   - 应用 API：若含业务透传参数或用户级鉴权，需通过 `biz_params` 传递（[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。

## 限制和注意事项

- **权限前提**：首次使用插件前，主账号或 RAM 子账号**必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`**。RAM 用户需主账号预先授予 `ram:CreateServiceLinkedRole` 权限（[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。
- **功能限制**：
  - `code_interpreter` 不支持网络访问与本地文件上传，仅限预装依赖（如 pandas、matplotlib、sympy）（[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。
  - `quark_search` 与 `github_search` 均仅返回摘要信息，**不支持获取网页或项目详情页内容**（[插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)、[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。
- **发布要求**：自定义插件下的工具必须处于 **“已发布”且“启用”状态** 才能被调用；调试失败或参数配置错误（如 Object 子属性为空、GET 请求含 Object 参数）将导致发布失败（[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。
- **计费提示**：`text_to_image` 和 `quark_search` 为“限时免费，需申请开通”，其余官方插件免费；三方插件按所选套餐计费（[插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)）。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


