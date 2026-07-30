# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（API）集成到推理流程中，弥补大模型在实时信息获取、精确计算、代码执行、图像生成等方面的固有局限。开发者可选用官方插件、三方插件或自定义插件，结合智能体应用、工作流应用或 Assistant API 实现自动化任务编排与执行。插件调用由大模型自主规划（智能体/Assistant 模式）或显式编排（工作流模式）驱动。

## 支持的模型/功能

百炼当前支持以下模型调用插件能力：

| 模型名称         | 模型标识符     |
|------------------|----------------|
| 通义千问-Turbo   | `qwen-turbo`   |
| 通义千问-Plus    | `qwen-plus`    |
| 通义千问-Max     | `qwen-max`     |
| 通义千问VL-Max   | `qwen-vl-max`  |
| 通义千问VL-Plus  | `qwen-vl-plus` |

> **注意**：各模型对插件的实际兼容性可能存在差异，[插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md) 明确指出“最新的兼容性状态，请以控制台实际执行结果为准”，建议在目标模型上实测验证。

官方插件提供开箱即用能力，包括：
- `code_interpreter`：执行 Python 代码（数学计算、数据分析、可视化等），依赖已预置（如 `pandas`, `matplotlib`, `sympy`），**不支持网络访问与本地文件上传**；
- `calculator`：复杂数学运算；
- `text_to_image`：文生图（限时免费，需申请开通）；
- `quark_search`：实时网络搜索（返回标题、关键词、摘要，**不支持访问网页详情**）；
- `generate_qrcode`：URL 转二维码；
- `github_search`：GitHub 项目检索（返回标题、链接、摘要，**不支持访问项目详情**）。

三方插件覆盖商业服务、图像视频、教育等领域，需在云市场开通后使用；自定义插件支持完全自主开发，详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 文档。

## 关键参数

插件调用依赖以下核心参数配置：

- **工具 ID（`tool_id`）**：唯一标识工具，用于 API 请求和模型决策。可在插件详情页悬浮工具名称图标复制（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。
- **输入参数（`input_params`）**：
  - `传参方式`：`大模型识别`（从用户输入提取）或 `业务透传`（由外部传入，需通过 `biz_params` 或 `user_defined_params` 传递）；
  - `类型`：支持 `String`、`Number`、`Object` 等，**Object 类型子属性不能为空**（需手动添加）；
  - `必填`：影响模型调用可靠性，非必填参数可能被忽略。
- **输出参数（`output_params`）**：定义 API 返回字段如何映射至模型上下文，**所有参数均为必填项**，描述需精简准确，层级宜扁平。
- **鉴权配置**（自定义插件）：
  - `鉴权类型`：`basic` / `bearer` / `appcode`；
  - `位置`：`Header`（默认 `Authorization` 字段）或 `Query`（如 `?api_key=xxx`）；
  - `Token`：服务级鉴权凭据，用户级鉴权需在对话前通过 UI 配置或 `biz_params` 传入。

## 使用方式

插件可通过三种方式集成：

1. **控制台集成（智能体应用）**：
   - 官方/三方插件：在 [插件市场](https://bailian.console.aliyun.com/#/plugin-market) 页面单击“添加至智能体”，选择工具与目标应用（**同一业务空间内**），最多支持 10 个工具；
   - 自定义插件：需先发布为 MCP 服务，再在智能体编排页的 **MCP 区块** 中添加（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。

2. **工作流应用**：
   - 将插件作为独立节点拖入画布，按需编排执行顺序，**不依赖模型自主决策**，适用于确定性任务流。

3. **API 调用**：
   - Assistant API：在请求 `tools` 字段中声明工具列表，模型自动选择并调用（参考 [Assistant API 文档](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api)）；
   - 应用 SDK/HTTP 接口：若含 `业务透传` 参数或用户级鉴权，必须通过 `biz_params` 传递对应值。

> **注意**：RAM 子账号首次使用插件（含自定义插件导入）需主账号授予 `ram:CreateServiceLinkedRole` 权限（策略条件限定 `cloundapi-access.sfm.aliyuncs.com`），否则授权失败（详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。

## 限制和注意事项

- **权限限制**：主账号可直接授权 `AliyunServiceRoleForSFMAccessCloudAPI` 角色；RAM 用户必须预先获得创建服务关联角色的权限，否则无法访问插件市场或导入云市场插件。
- **功能限制**：
  - `code_interpreter` 禁止网络访问、文件上传，依赖库版本固定（如 `requests~=2.31.0`, `pillow~=9.4.0`）；
  - `quark_search` 和 `github_search` 均仅返回摘要信息，**不支持跳转或解析原始网页/仓库内容**；
  - 同一插件下多个工具共享域名，路径由 `工具路径`（如 `/query`）拼接 `插件URL` 构成。
- **配置风险**：
  - Object 类型输入参数在 GET 请求下不被支持（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 错误码 `130022`）；
  - 工具名称超 20 字符、参数描述缺失（错误码 `130040`）将导致发布失败；
  - 删除插件或工具会导致关联应用失效，且操作不可逆。
- **调试要求**：所有自定义工具必须通过“测试工具”验证连通性并成功发布，草稿状态无法调用。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


