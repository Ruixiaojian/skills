# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如代码执行、实时搜索、图像生成等）以标准化方式集成到大模型工作流中，弥补其在实时性、精确计算、多模态输出等方面的固有局限。插件支持官方预置、三方市场及完全自定义三种形态，可被智能体应用、工作流应用或 Assistant API 主动调用或自动规划调用。开发者需关注模型兼容性、参数配置规范及权限授权要求。

## 支持的模型/功能

当前插件能力已在以下模型上验证可用：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件调用的规划能力与响应稳定性存在差异，**最新兼容性状态请以控制台实际执行结果为准**，不建议依赖文档静态列表做兼容性断言。  
插件按来源分为三类：  
- **官方插件**：组件广场预置，开箱即用，无需配置输入/输出参数，包括 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）等。详情见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。  
- **三方插件**：来自阿里云云市场，覆盖商业服务、图像视频、教育等领域，需开通后使用，且部分插件需额外鉴权。  
- **自定义插件**：开发者可基于自有 API 创建，支持完整参数映射、鉴权（Header/Query，含 bearer/basic/appcode 类型）、在线调试与发布流程。详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 和文档 2 均列出 `quark_search` 插件说明，但文档 2 明确指出“夸克搜索和联网搜索（`enable_search`）有本质区别”——前者返回结构化搜索结果供模型直接引用，后者仅辅助内容生成而不返回原始结果；而文档 1 未提及此关键区分。开发者应以 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 中的说明为准。

## 关键参数

- **工具 ID（tool_id）**：唯一标识插件下的具体工具，API 调用时必需。可通过插件详情页悬浮工具名称图标复制获取。  
- **输入参数（input parameters）**：  
  - `传参方式` 必须明确设为 `大模型识别`（从用户输入提取）或 `业务透传`（由外部传入，如 `biz_params`）。  
  - `类型` 支持 `String`/`Number`/`Object` 等，**Object 类型子属性不能为空**，需手动添加（见文档 3 错误码 130022）。  
  - GET 请求下**禁止使用 Object 类型入参**（文档 3 明确限制）。  
- **输出参数（output parameters）**：所有字段必填，描述需精简准确，层级尽量扁平，直接影响模型对 API 返回结果的解析质量。  
- **鉴权配置**：自定义插件支持 Header 或 Query 方式，`Type` 可选 `bearer`（自动加 `Bearer ` 前缀）、`basic` 或 `appcode`；[Token](../concepts/token.md) 值由 API 提供方发放。

## 使用方式

1. **权限准备**：主账号或 RAM 子账号首次使用插件前，必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。RAM 用户需主账号预先授予 `ram:CreateServiceLinkedRole` 权限（策略条件中 `ram:ServiceName` 应为 `cloundapi-access.sfm.aliyuncs.com`），否则无法进入插件市场或导入云市场 API —— 此流程在 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 中均有详细说明。  
2. **插件接入**：  
   - **官方/三方插件**：在插件市场页面单击“添加至智能体”，选择目标智能体应用（注意：官方插件仅支持与**同业务空间**的智能体关联）；最多可添加 10 个工具。  
   - **自定义插件**：需先发布为 MCP 服务，再在智能体编排页的 **MCP 区块**中添加；若含用户级/服务级鉴权或业务透传参数，需在对话前通过控制台图标配置 `biz_params`。  
3. **API 调用**：通过 Assistant API 时，在 `tools` 字段中声明工具 ID 及描述；工作流应用中将插件作为独立节点编排。所有方式均依赖模型根据用户输入、工具描述自动决策是否调用及如何构造参数。

## 限制和注意事项

- **模型限制**：`qwen-vl-*` 系列模型虽支持插件调用，但对多模态输入与插件输出的协同处理能力尚未完全优化，复杂图文混合任务建议优先验证 `qwen-plus` 或 `qwen-max`。  
- **功能限制**：  
  - `code_interpreter` 插件**不支持网络访问与本地文件上传**，可用依赖版本已固化（见文档 2 列表），不可自定义安装新包。  
  - `quark_search` 和 `github_search` 均**仅返回摘要、标题、链接等元信息，不支持抓取网页正文或项目源码**（文档 1 和文档 2 均强调此点）。  
- **配置风险**：  
  - 自定义插件发布前必须完成**在线调试并确保运行成功**，否则应用调用将失败；发布后修改 URL 或鉴权配置需重新测试。  
  - 删除插件或工具将导致**所有关联应用立即失效且不可恢复**（文档 3 明确标注为“重要”）。  
- **计费提示**：`text_to_image` 与 `quark_search` 为“限时免费，需申请开通”，其余官方插件当前免费；三方插件按所选套餐计费。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


