# plug in

插件是百炼平台扩展大模型能力的核心机制，通过将外部工具（如代码执行、网络搜索、图像生成等）以标准化方式接入，弥补大模型在实时信息获取、精确计算、多模态输出等方面的固有局限。开发者可直接调用官方插件、开通三方插件，或创建自定义插件，所有插件均通过统一的工具调用协议与智能体/工作流/Assistant API 集成。插件能力依赖服务关联角色授权及模型兼容性，需按规范配置参数并完成发布。

## 支持的模型/功能

百炼插件支持以下模型（截至当前文档版本）：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件的调用支持度可能存在差异，**实际兼容性请以控制台运行结果为准** [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

插件按来源分为三类：
- **官方插件**：预置于组件广场，开箱即用，无需配置输入/输出参数。包括 `code_interpreter`（Python代码执行）、`calculator`（复杂数学计算）、`text_to_image`（文生图）、`quark_search`（夸克搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub项目检索）等 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件**：来自阿里云云市场，覆盖商业服务、图像视频、教育等领域，开通后即可调用。
- **自定义插件**：支持开发者导入云市场API或自主开发HTTP服务，通过定义插件URL、工具路径、鉴权方式及结构化I/O参数实现深度集成 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档1中称“官方插件只能与位于相同的业务空间里的智能体应用关联”，而文档2未提此限制；但文档3明确要求自定义插件需先“发布为MCP服务”再添加至智能体，且强调“已发布且启用状态的工具才能用于后续调用”。因此，**所有插件（含官方）的实际调用均以“已发布”状态为前提，业务空间隔离是默认行为，非例外规则**。

## 关键参数

插件调用依赖以下核心参数：

- **工具ID（tool_id）**：唯一标识一个工具，API调用时必需。可在插件详情页的“插件工具”区域或工具卡片悬停图标处获取 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **输入参数（input parameters）**：
  - `传参方式`：`大模型识别`（从用户Query中抽取）或`业务透传`（由外部通过 `biz_params` 或 `user_defined_params` 传入）；
  - `类型`：支持 `String`、`Number`、`Boolean`、`Object`（子属性必填）；
  - `参数描述`：必须填写，直接影响大模型参数提取准确性（缺失将导致发布失败，错误码 `130040`）。
- **输出参数（output parameters）**：定义API返回数据中需被大模型提取并用于生成回复的关键字段，类型与描述同样为必填项。
- **鉴权配置**（自定义插件）：
  - `是否鉴权`：可选开启；
  - `鉴权类型`：`basic` / `bearer` / `appcode`；
  - `位置`：`Header`（默认字段 `Authorization`）或 `Query`（如 `?api_key=xxx`）。

## 使用方式

插件可通过三种方式集成：

1. **控制台可视化集成**：
   - 在[插件市场](https://bailian.console.aliyun.com/#/plugin-market)页面，为官方/三方插件完成授权或开通；
   - 对自定义插件，需先创建插件→添加工具→调试→发布；再通过“发布为MCP服务”→在智能体编排页的“MCP”区块中添加；
   - 最多支持单个智能体关联10个工具 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

2. **工作流应用节点**：
   - 将插件作为独立节点拖入工作流画布，按需编排执行顺序，**不依赖大模型自动规划**，适用于确定性任务链路。

3. **API调用**：
   - Assistant API：在请求 `tools` 字段中传入工具定义（含 `tool_id`, `description`, `parameters`），模型将自主决策是否调用；
   - 工作流/旧版智能体API：通过 `biz_params` 传递业务透传参数或用户级鉴权[Token](../concepts/token.md) [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 限制和注意事项

- **权限前置要求**：主账号或RAM子账号首次使用插件前，**必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`**。RAM子账号需额外授予 `ram:CreateServiceLinkedRole` 权限（策略条件 `ram:ServiceName = "cloundapi-access.sfm.aliyuncs.com"`），否则无法进入插件市场或导入云市场API [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **功能边界**：
  - `code_interpreter` 不支持网络访问、本地文件上传，依赖库版本固定（如 `pandas`, `matplotlib`, `requests~=2.31.0`）；
  - `quark_search` 和 `github_search` 仅返回网页/项目标题、关键词、摘要，**不支持访问原始网页或仓库详情页**；
  - `text_to_image` 和 `generate_qrcode` 均为限时免费，需单独申请开通。
- **配置强约束**：
  - 自定义插件的 `Object` 类型参数子属性不能为空（错误码 `130022`）；
  - GET 请求方法下禁止使用 `Object` 类型输入参数；
  - 工具名称长度不可超过20字符（超长将阻断发布）。
- **生命周期管理**：删除插件将**级联删除其下所有工具，且已关联该插件的应用立即失效**，操作不可逆 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 来源文档

- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


