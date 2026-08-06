# plug in

插件是百炼平台扩展大模型能力的核心机制，通过将外部工具（如代码执行、网络搜索、图像生成等）以标准化方式接入，弥补大模型在实时信息获取、精确计算、[多模态](../concepts/multimodal.md)输出等方面的固有局限。开发者可直接调用官方插件、开通三方插件，或基于自有 API 创建自定义插件。所有插件均需通过服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI` 授权访问云资源，主账号与 RAM 用户的授权流程存在差异。

## 支持的模型与功能

百炼插件支持以下模型（按官方文档明确列出）：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件的兼容性以控制台实际执行结果为准，[插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md) 文档指出“最新的兼容性状态，请以控制台实际执行结果为准”。

- **官方插件**（免配置）：包括 `code_interpreter`（Python 代码执行）、`calculator`（复杂数学计算）、`text_to_image`（文生图）、`quark_search`（夸克搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）。详细功能与计费方案见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件**：覆盖商业服务、图像视频、教育等领域，需在插件市场开通后使用。
- **自定义插件**：支持通过控制台创建个性化插件，定义插件 URL、鉴权方式（Header/Query，支持 basic/bearer/appcode 类型），并为每个工具配置路径、请求方法（GET/POST）、输入/输出参数（含类型、描述、传参方式）及高级调用示例。完整流程详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 与文档 3 均要求 RAM 用户需先获得 `ram:CreateServiceLinkedRole` 权限才能完成插件授权，但文档 1 的权限策略 Condition 中 `"ram:ServiceName": "cloundapi-access.sfm.aliyuncs.com"` 存在拼写错误（应为 `cloudapi-access`），而文档 3 的脚本中该值为正确拼写 `"cloudapi-access.sfm.aliyuncs.com"`。请以文档 3 的脚本为准。

## 关键参数

- **工具 ID**：唯一标识插件下的具体工具（如 `calculator`），API 调用时必需。可通过插件详情页的工具卡片或悬浮图标复制获取（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。
- **输入参数**：
  - `传参方式`：`大模型识别`（从用户输入中抽取）或 `业务透传`（由外部 SDK/HTTP 请求通过 `biz_params` 透传）；
  - `类型`：支持 `String`、`Number`、`Object` 等，`Object` 类型下子属性**不能为空**，需手动添加；
  - `参数描述`：必须填写，用于指导大模型准确提取参数值。
- **输出参数**：所有参数均为必填，大模型依据其定义对 API 返回结果进行筛选与重组。
- **鉴权配置**（仅自定义插件）：支持 Header 或 Query 方式，`Type` 可选 `basic`/`bearer`/`appcode`；`Token` 为服务级鉴权凭据。

## 使用方式

插件可通过三种方式集成：
1. **控制台智能体应用**：在插件市场页面单击“添加至智能体”，选择目标智能体；或在智能体编排页的 **MCP 区块** 添加已发布的 MCP 服务（自定义插件需先发布为 MCP）；
2. **工作流应用**：将插件作为独立节点拖入画布，按需编排执行顺序；
3. **API 调用**：
   - Assistant API：在请求 `tools` 字段中传入工具定义，详见 [Assistant API 文档](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api)；
   - 应用 API：若含 `业务透传` 参数或 `用户级鉴权`，需通过 `biz_params` 传递对应值（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。

> **注意**：官方插件在**非默认业务空间**中调用前，必须先在插件市场对该子业务空间单独授权（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）；而自定义插件无此限制，但需确保其工具状态为“已发布”且“启用”。

## 限制和注意事项

- **权限限制**：主账号可直接授权 `AliyunServiceRoleForSFMAccessCloudAPI`；RAM 用户需主账号预先授予 `ram:CreateServiceLinkedRole` 权限（Condition 中 `ram:ServiceName` 必须为 `cloudapi-access.sfm.aliyuncs.com`）。
- **功能限制**：
  - `code_interpreter` 不支持网络访问与本地文件上传，依赖库版本固定（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）；
  - `quark_search` 与 `github_search` 仅返回网页/项目标题、关键词/摘要，**不支持访问详情页内容**；
  - 单个智能体应用最多关联 **10 个工具**。
- **调试与发布**：自定义插件的工具必须**在线调试成功**并**发布**后方可调用；发布失败常见原因包括参数描述缺失（错误码 130040）、`Object` 类型子属性为空（错误码 130022）或 GET 请求误配 `Object` 输入参数（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。
- **计费说明**：`code_interpreter`、`calculator`、`generate_qrcode`、`github_search` 为免费；`text_to_image` 与 `quark_search` 为限时免费，需申请开通。

## 来源文档

- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


