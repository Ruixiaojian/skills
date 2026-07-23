# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（API）集成到大模型应用中，弥补其在实时信息获取、精确计算、代码执行、图像生成等场景下的固有局限。插件以“工具集合”形式组织，支持官方预置、三方市场及完全自定义三种类型，可被智能体应用、工作流应用或 Assistant API 主动调用或自动规划调用。

## 支持的模型/功能

当前插件能力已覆盖以下通义千问系列模型：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件的兼容性存在差异，**实际可用性请以控制台运行结果为准**，而非静态列表 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。  
插件功能分为三类：
- **官方插件**：开箱即用，无需配置参数，包括 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）；
- **三方插件**：来自云市场，覆盖商业服务、图像视频、教育等领域，需开通后使用；
- **自定义插件**：用户自主定义插件 URL、工具路径、鉴权方式及输入/输出参数，支持从零创建或从云市场导入 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 和文档 2 均列出 `quark_search` 插件说明，但文档 2 明确指出其“目前支持检索出网页标题、关键词和摘要，但不支持直接访问网页详情”，而文档 1 仅简述为“查找公开的网络知识和信息”。应以文档 2 的限定描述为准，避免误判能力边界。

## 关键参数

插件调用依赖以下核心参数：
- **工具 ID**：唯一标识工具（如 `calculator`），用于 API 请求中指定目标工具，获取方式见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；
- **输入参数**：由大模型从用户输入中识别提取（`传参方式 = 大模型识别`）或由业务系统透传（`传参方式 = 业务透传`），需明确定义名称、类型（String/Number/Object）、描述及必填性；
- **输出参数**：定义 API 返回数据中哪些字段将被大模型用于生成最终回复，所有出参均为必填项，嵌套层级应尽量扁平；
- **鉴权配置**：针对自定义插件，支持 Header 或 Query 方式传递 [Token](../concepts/token.md)，鉴权类型包括 `basic`、`bearer`、`appcode`；云市场插件通常自动注入 AppKey/AppSecret，无需手动配置。

## 使用方式

插件可通过三种方式接入：
1. **控制台可视化集成**：在 [插件市场](https://bailian.console.aliyun.com/#/plugin-market) 页面，为智能体应用添加工具（最多 10 个），或通过“发布为 MCP 服务”后在智能体编排页的 MCP 区块中引入；
2. **工作流应用节点**：将插件作为独立节点编排进工作流，按预设逻辑顺序执行，不依赖大模型自主决策；
3. **API 调用**：通过 Assistant API 的 `tools` 字段声明可用工具，并在 `tool_choice` 中控制调用策略；若含业务透传参数或用户级鉴权，需通过 `biz_params` 传递 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

> **注意**：官方插件仅支持与**同业务空间内的智能体应用**关联；子账号（RAM 用户）首次使用插件前，必须由主账号授予 `ram:CreateServiceLinkedRole` 权限，否则授权失败（错误码 140052），详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

## 限制和注意事项

- **权限约束**：主账号或 RAM 子账号需具备 `AliyunServiceRoleForSFMAccessCloudAPI` 服务关联角色权限，否则无法访问插件市场或导入云市场 API；
- **功能限制**：`code_interpreter` 不支持网络访问与本地文件上传，可用依赖库已固化（如 `pandas`、`matplotlib`、`requests` 等）；`quark_search` 和 `github_search` 均仅返回摘要信息，不支持跳转详情页；
- **配置要求**：自定义插件的 Object 类型参数**子属性不能为空**，否则发布失败（错误码 130022）；GET 请求方法下**禁止配置 Object 类型入参**；
- **生命周期管理**：删除插件将导致其下所有工具及关联应用失效；工具修改后必须重新测试并发布才生效；
- **计费提示**：`text_to_image` 与 `quark_search` 为限时免费且需单独申请开通，其余官方插件默认免费；三方插件按所选套餐计费。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


