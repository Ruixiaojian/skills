# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（API）集成到模型推理链路中，解决大模型在实时信息获取、精确计算、代码执行、图像生成等场景下的固有局限。开发者可选用官方插件、三方插件或自定义插件，结合智能体应用、工作流应用或 Assistant API 进行调用。所有插件均需通过服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI` 授权方可使用。

## 支持的模型/功能

百炼当前支持以下模型调用插件能力：  
- `qwen-turbo`、`qwen-plus`、`qwen-max`（文本模型）  
- `qwen-vl-plus`、`qwen-vl-max`（多模态模型）  

> **注意**：各模型对插件的兼容性存在差异，[插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md) 中列出的模型列表为截至文档发布时的兼容范围，**实际可用性请以控制台运行结果为准**；部分新模型（如 `qwen2.5` 系列）尚未明确列入该文档，需通过控制台实测验证。

插件按来源分为三类：  
- **官方插件**：预置于组件广场，开箱即用，无需配置参数。包括 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）等 [详见官方插件说明](../../raw/application-user-guide/plug-in/plugins.md)。  
- **三方插件**：来自阿里云云市场，覆盖商业服务、图像视频、教育等领域，开通后即可调用。  
- **自定义插件**：支持开发者接入自有 API，需定义插件 URL、工具路径、输入/输出参数及鉴权方式，完整流程见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 文档。

## 关键参数

插件调用依赖以下核心参数，尤其在自定义插件和 API 集成中必须准确配置：

- **工具 ID（tool_id）**：唯一标识插件下的具体工具（如 `calculator`），用于 Assistant API 或工作流节点中指定调用目标。可通过插件详情页悬浮图标复制获取。  
- **插件 URL 与工具路径**：插件 URL 为域名根地址（如 `https://myapi.example.com`），工具路径为相对路径（如 `/query`），二者拼接构成完整调用地址。  
- **输入参数（input parameters）**：  
  - `传参方式` 必须明确设为 `大模型识别`（从用户输入提取）或 `业务透传`（由外部传入，通过 `biz_params` 或 `user_defined_params` 传递）；  
  - `参数名称` 和 `参数描述` 需语义清晰，直接影响大模型参数提取准确性；  
  - `类型` 支持 `String`、`Number`、`Object`（但 Object 子属性不可为空）。  
- **输出参数（output parameters）**：定义 API 返回数据中哪些字段被大模型用于生成最终回复，需精简且层级扁平。  
- **鉴权配置**：若 API 需鉴权，支持 `Header`（如 `Authorization: Bearer <token>`）或 `Query`（如 `?api_key=xxx`）方式，`Type` 可选 `basic`/`bearer`/`appcode`。

## 使用方式

插件可通过三种方式集成：

1. **控制台可视化配置（推荐入门）**：  
   - 在 [插件市场](https://bailian.console.aliyun.com/#/plugin-market) 页面授权 `AliyunServiceRoleForSFMAccessCloudAPI` 角色（主账号直接授权；RAM 用户需先获 `ram:CreateServiceLinkedRole` 权限）；  
   - 官方/三方插件：单击“添加至智能体”，选择目标智能体应用（注意：官方插件仅支持与**同业务空间**的智能体关联）；  
   - 自定义插件：创建后需先发布为 MCP 服务，再在智能体编排页的 **MCP 区块** 中添加 [参考自定义插件文档](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。  

2. **工作流应用节点**：将插件作为独立节点拖入工作流画布，按需编排执行顺序，不依赖大模型自主决策。  

3. **API 调用**：  
   - Assistant API：在 `tools` 数组中声明工具 ID 及描述，模型自动规划调用；  
   - 智能体/工作流 API：通过 `biz_params` 传递业务透传参数或用户级鉴权 Token [详见 API 文档](https://help.aliyun.com/zh/model-studio/agent-and-workflow-application-api-reference)。

## 限制和注意事项

- **权限限制**：首次使用插件前，**必须完成 `AliyunServiceRoleForSFMAccessCloudAPI` 服务关联角色授权**，否则无法访问插件市场或调用任何插件 [详见官方和第三方插件文档](../../raw/application-user-guide/plug-in/plugins.md)。  
- **调用上限**：智能体应用最多支持添加 **10 个工具**；自定义插件中，`Object` 类型输入参数在 `GET` 请求下不被支持（仅 `POST` 允许）。  
- **功能边界**：  
  - `code_interpreter` 插件**不支持网络访问与本地文件上传**，可用依赖库已固化（如 `pandas`、`matplotlib`、`requests` 等）；  
  - `quark_search` 和 `github_search` 均**仅返回摘要、标题、链接，不支持访问网页或仓库详情页**；  
  - `text_to_image` 和 `quark_search` 为**限时免费，需单独申请开通**。  
- **调试要求**：自定义插件的工具必须经 **在线调试成功并发布为“已发布”状态** 后才能被应用调用；草稿或未启用状态的工具将导致调用失败。  
- **错误处理**：发布自定义工具时常见错误码 `130040`（参数描述缺失）、`130022`（Object 子属性为空或 GET 请求含 Object 参数）需严格按提示修正 [详见自定义插件错误码说明](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


