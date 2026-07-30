# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（API）集成到大模型应用中，弥补其在实时信息获取、精确计算、代码执行、图像生成等方面的固有局限。插件以“工具集合”形式组织，支持官方预置、三方市场及完全自定义三种类型，可被智能体应用、工作流应用或 Assistant API 主动调用或编排执行。所有插件均需经服务关联角色（`AliyunServiceRoleForSFMAccessCloudAPI`）授权后方可使用。

## 支持的模型与功能

百炼当前支持在以下模型上启用插件能力：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max` 和 `qwen-vl-plus`。各模型对插件的兼容性存在差异，实际可用性请以控制台运行结果为准 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

官方插件提供开箱即用的常用能力，包括：
- `code_interpreter`：执行 Python 代码（支持 `matplotlib`、`pandas`、`sympy` 等依赖，**不支持网络访问与本地文件上传**）；
- `calculator`：高精度数学运算；
- `text_to_image`：文生图（限时免费，需申请开通）；
- `quark_search`：实时网络搜索（返回标题、关键词、摘要，**不支持网页详情访问**）；
- `generate_qrcode`：URL 转二维码；
- `github_search`：GitHub 项目检索（返回标题、链接、摘要，**不支持项目详情访问**）。

三方插件覆盖商业服务、图像视频、教育等场景，需在云市场开通后调用；自定义插件支持通过 REST API 接入任意业务系统，需明确定义工具路径、输入/输出参数及鉴权方式 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 与文档 2 均列出 `quark_search` 插件限制为“不支持直接访问网页详情”，但文档 2 在常见问题中补充说明“联网搜索（`enable_search`）也是基于夸克搜索”，暗示二者底层一致；而文档 1 未提及 `enable_search`。开发者应以 `quark_search` 插件显式调用为准，避免混淆 `enable_search` 这一旧版开关行为 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

## 关键参数

- **工具 ID**：唯一标识插件下的具体工具（如 `calculator`），API 调用时必需。可通过插件详情页悬浮图标复制获取。
- **插件 URL 与工具路径**：自定义插件中，`插件URL`（如 `https://example.com`）与 `工具路径`（如 `/query`）拼接构成完整请求地址。
- **输入参数配置**：
  - `传参方式`：`大模型识别`（从用户输入提取）或 `业务透传`（由外部传入，需通过 `biz_params` 或 `user_defined_params` 指定）；
  - `类型`：支持 `String`、`Number`、`Object`（Object 的子属性**不能为空**，须显式添加）；
  - `必填`：影响大模型参数构造逻辑，非必填参数可能被忽略。
- **鉴权配置**：支持 `Header`（如 `Authorization: Bearer <TOKEN>`）或 `Query`（如 `?api_key=xxx`）方式，鉴权类型包括 `basic`、`bearer`、`appcode`。

## 使用方式

1. **权限准备**：主账号或 RAM 子账号需先授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`，子账号还需额外授予 `ram:CreateServiceLinkedRole` 权限（策略条件需匹配 `cloundapi-access.sfm.aliyuncs.com`）[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
2. **插件接入**：
   - *官方/三方插件*：在插件市场页面单击“添加至智能体”，选择目标智能体（**仅限同业务空间**），最多添加 10 个工具；
   - *自定义插件*：创建后需发布为 MCP 服务，再在智能体编排页的“MCP”区块中添加；
   - *工作流应用*：将插件作为独立节点拖入流程，按需配置输入输出；
   - *Assistant API*：在 `tools` 数组中声明工具定义，调用时由模型自动规划并触发。
3. **调试与发布**：所有自定义工具必须完成在线测试（“测试工具”按钮）且状态为“成功”，再点击“发布”方可生效；草稿状态工具不可调用。

## 限制和注意事项

- 官方插件无需配置参数，但**仅限与插件所在业务空间相同的智能体应用关联**；子业务空间调用官方插件需单独授权。
- 自定义插件的 `Object` 类型输入参数在 `GET` 请求下**不支持**，仅 `POST` 允许；`Object` 的子属性必须显式定义，否则发布失败（错误码 `130022`）。
- `code_interpreter` 插件禁用网络访问、文件系统读写及敏感模块（如 `os.system`），可用依赖版本严格限定，详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- 删除插件或工具将导致**已关联的应用立即失效**，且操作不可逆；编辑插件 URL 或鉴权信息后，必须重新测试并发布所有相关工具。
- 多插件组合调用（如 `quark_search` + `text_to_image` + `generate_qrcode`）支持，但需确保各工具返回结构能被大模型正确解析与串联。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)




