# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如计算、搜索、图像生成等 API）以标准化方式集成，弥补大模型在实时信息获取、精确计算、多模态生成等方面的固有局限。开发者可选用官方插件、三方插件或自定义插件，在智能体应用、工作流应用或 Assistant API 中按需调用。插件调用由大模型自主规划（智能体/Assistant 模式）或由用户显式编排（工作流模式）。

## 支持的模型/功能

百炼插件当前支持以下通义千问系列模型：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件的兼容性存在差异，**实际可用性请以控制台运行结果为准**，不建议依赖文档静态列表做兼容性断言 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

插件功能分为三类：
- **官方插件**：开箱即用，无需配置参数，包括 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）；
- **三方插件**：覆盖商业服务、图像视频、教育等领域，需在云市场开通后使用；
- **自定义插件**：支持通过控制台创建或从云市场导入，可对接任意符合 REST 规范的 API，并支持 Header/Query 鉴权（basic/bearer/appcode 类型）[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 和文档 2 均列出 `quark_search` 插件说明中“不支持直接访问网页详情”，但文档 2 新增了与 `enable_search` 的对比说明，明确指出夸克搜索插件返回的是结构化摘要而非原始网页内容；而文档 1 未提及该对比，易引发混淆。应以文档 2 的说明为准 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

## 关键参数

- **工具 ID（tool_id）**：唯一标识一个工具，调用时必需。可在插件详情页的“插件工具”区域或工具卡片悬停图标处复制 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **输入参数（input parameters）**：
  - `传参方式`：`大模型识别`（从用户输入中抽取）或 `业务透传`（由外部通过 `biz_params` 或 `user_defined_params` 注入）；
  - `类型`：支持 `String`、`Number`、`Boolean`、`Object`（子属性不可为空）；
  - `提交方式`：`application/json` 或 `application/x-www-form-urlencoded`；
- **输出参数（output parameters）**：必填，定义 API 返回字段的名称、描述与类型，直接影响大模型对结果的解析与重组；
- **鉴权配置**（仅自定义插件）：支持 `Header`（默认 `Authorization` 字段）或 `Query` 传参，`Type` 可选 `basic`/`bearer`/`appcode`，`Token` 为服务级或用户级凭证。

## 使用方式

1. **权限准备**：主账号或 RAM 子账号首次使用插件前，必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。RAM 用户需主账号预先授予 `ram:CreateServiceLinkedRole` 权限（含 `cloundapi-access.sfm.aliyuncs.com` 服务名限制）[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；
2. **插件接入**：
   - **官方/三方插件**：在插件市场页面单击“添加至智能体”，选择工具与目标智能体应用（注意：官方插件仅支持与**同业务空间**的智能体关联），最多添加 10 个工具；
   - **自定义插件**：需先发布为 MCP 服务，再在智能体编排页的“MCP”区块中添加；若含鉴权或业务透传参数，需在对话前通过控制台图标配置 `Token` 或变量值；
3. **调用入口**：
   - 控制台：在智能体应用对话框中直接输入自然语言指令（如“计算 12313×13232”）；
   - API：通过 Assistant API 的 `tools` 字段声明可用工具，并在 `messages` 中触发调用；工作流应用中将插件作为独立节点编排。

## 限制和注意事项

- **调用限制**：单个智能体应用最多关联 10 个工具；自定义插件的 `Object` 类型输入参数在 `GET` 请求下不被支持；
- **安全限制**：`code_interpreter` 插件禁止网络访问与本地文件上传，仅预装指定依赖（如 `pandas`、`matplotlib`、`sympy` 等）；
- **状态依赖**：所有工具必须处于“已发布”且“调试成功”状态才可被调用；删除插件将导致其下所有工具及关联应用失效；
- **错误处理**：发布自定义工具时常见错误码 `130040`（参数描述缺失）、`130022`（Object 子属性为空或 GET 含 Object 参数），需按提示修正后重新发布；
- **计费说明**：`code_interpreter`、`calculator`、`generate_qrcode`、`github_search` 免费；`text_to_image` 与 `quark_search` 为限时免费，需单独申请开通。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


