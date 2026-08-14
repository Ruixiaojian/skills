# plug in

[插件](../concepts/plugin.md)是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API）封装为可被大模型识别和调用的标准化接口，解决模型在实时信息获取、精确计算、代码执行、图像生成等场景下的固有局限。[插件](../concepts/plugin.md)支持官方预置、三方集成与完全自定义三种形态，可无缝接入智能体应用、工作流应用及 Assistant API。其调用由大模型基于用户输入、工具名称与描述自主决策，或由工作流显式编排。

## 支持的模型/功能

百炼[插件](../concepts/plugin.md)当前支持以下模型（以控制台实际可用性为准）：  
- `qwen-turbo`、`qwen-plus`、`qwen-max`（文本模型）  
- `qwen-vl-max`、`qwen-vl-plus`（多模态模型）  

> **注意**：文档 1 中列出的模型兼容性表格未说明是否支持所有插件类型（如 `text_to_image` 在 VL 模型中可能冗余），而文档 3 的组合示例明确展示了 `quark_search` + `text_to_image` + `generate_qrcode` 跨类型协同，表明多模型协同调用已实现场景化验证。建议以 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md) 中的模型列表为初始参考，但务必在控制台中验证具体插件与目标模型的兼容性。

插件按来源分为三类：  
- **官方插件**：开箱即用，无需配置参数，包括 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）。详情见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。  
- **三方插件**：来自云市场，覆盖商业服务、教育、音视频等领域，开通后即可调用，无需额外配置。  
- **自定义插件**：开发者可基于自有 API 创建，支持完整鉴权（Header/Query、basic/bearer/appcode）、复杂参数（含 Object 嵌套）、多工具聚合。创建流程详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 关键参数

插件调用依赖两类关键参数配置：  
- **插件级参数**：在创建插件时定义，包括 `plugin_url`（基础域名）、`is_auth_enabled`（是否开启鉴权）、`auth_type`（`basic`/`bearer`/`appcode`）、`auth_location`（`Header` 或 `Query`）、`auth_param_name`（如 `api_key`）、`auth_token`（服务级 [Token](../concepts/token.md)）。  
- **工具级参数**：每个工具独立配置，分为：  
  - **输入参数**：`param_name`（如 `city`）、`description`（如 `城市名称，中文，例如"杭州"`）、`type`（`String`/`Number`/`Object`）、`passing_method`（`大模型识别` 或 `业务透传`）。`Object` 类型子属性**必须非空**，否则发布失败（错误码 `130022`）。  
  - **输出参数**：`param_name` 与 `description` 需精简准确，用于指导大模型解析 API 返回结果；所有出参均为必填。  
  - **高级配置**（可选）：提供 `user_input` → `payload` 的映射示例（如 `"查询杭州明天天气"` → `{"city": "杭州", "date": "2025-04-25"}`），显著提升参数提取准确率。

## 使用方式

插件可通过以下方式集成：  
- **控制台（智能体应用）**：  
  1. 将插件发布为 MCP 服务（或直接从插件页添加）；  
  2. 在智能体编排页面的 **MCP 区块** 添加该服务；  
  3. 若含鉴权或业务透传参数，需在对话前通过配置按钮传入 `biz_params`（[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 中详述）；  
  4. 测试通过后发布应用。  
- **API 调用**：  
  - 通过 Assistant API，在 `tools` 字段中传入工具 ID（如 `"calculator"`）及工具定义；  
  - 工具 ID 可在插件详情页悬浮工具名称图标复制（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）；  
  - 含 `业务透传` 参数或用户级鉴权时，需通过 `biz_params` 传递（[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 明确要求）。  
- **工作流应用**：将插件作为独立节点拖入画布，按需配置输入/输出映射，不依赖大模型自动规划。

## 限制和注意事项

- **权限限制**：主账号首次访问插件市场需授权 `AliyunServiceRoleForSFMAccessCloudAPI` 角色；RAM 用户（子账号）需主账号预先授予 `ram:CreateServiceLinkedRole` 权限（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 中的 RAM 授权步骤）。  
- **功能限制**：  
  - `code_interpreter` 不支持网络访问与本地文件上传，仅限白名单依赖（如 `pandas`, `matplotlib`, `requests~=2.31.0`）；  
  - `quark_search` 与 `github_search` 仅返回网页/项目标题、摘要、链接，**不支持访问原始网页或仓库详情页**；  
  - `text_to_image` 与 `generate_qrcode` 为限时免费，需单独申请开通。  
- **配置限制**：  
  - 工具名称长度 ≤ 20 字符（超长将阻断发布）；  
  - GET 请求下输入参数**不支持 `Object` 类型**（错误码 `130022`）；  
  - `Object` 类型参数的子属性**必须显式添加且非空**（否则发布失败）。  
- **运维风险**：删除插件将**不可逆地移除其下所有工具**，并导致已关联的应用失效；编辑插件 URL 或鉴权配置后，必须重新测试并发布工具。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)


