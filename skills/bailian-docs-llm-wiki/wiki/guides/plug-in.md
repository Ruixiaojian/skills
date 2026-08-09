# plug in

[插件](../concepts/plugin.md)是百炼平台扩展大模型能力的核心机制，通过将外部工具（如代码执行、实时搜索、图像生成等）以标准化方式集成到大模型工作流中，弥补其在实时信息获取、精确计算、[多模态](../concepts/multimodal.md)生成等方面的固有局限。[插件](../concepts/plugin.md)分为官方[插件](../concepts/plugin.md)、三方插件和自定义插件三类，支持在智能体应用、工作流应用及 Assistant API 中调用。所有插件调用均依赖服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI` 的权限授权。

## 支持的模型与功能

百炼当前支持插件调用的模型包括：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max` 和 `qwen-vl-plus`。各模型对插件的兼容性以控制台实际执行结果为准，建议在生产环境前进行实测验证。  
官方插件提供开箱即用能力，无需配置输入/输出参数，覆盖以下核心功能：

- `code_interpreter`：执行 Python 代码（支持 pandas、matplotlib、sympy 等依赖，**不支持网络访问与本地文件上传**）  
- `calculator`：高精度数学计算  
- `text_to_image`：文生图（限时免费，需申请开通）  
- `quark_search`：基于夸克的实时网页搜索（返回标题、关键词、摘要，**不支持访问网页详情**）  
- `generate_qrcode`：URL 转二维码  
- `github_search`：GitHub 项目检索（返回标题、链接、摘要，**不支持访问项目详情**）  

三方插件与自定义插件可扩展至商业服务、教育、音视频等领域，详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 文档。

> **注意**：文档 1 与文档 2 均列出 `quark_search` 和 `github_search` 的限制说明，但文档 1 明确指出“不支持直接访问网页详情”，而文档 2 仅复述该限制；二者一致，无矛盾。但文档 1 中 `Python代码解释器` 的依赖列表更完整（含 `pdf2image`、`pypdf` 等），文档 2 未提供，应以 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 为准。

## 关键参数

插件调用依赖以下关键标识与配置参数：

- **工具 ID**：唯一标识工具，用于 API 调用（如 `calculator`）。可在插件详情页的“插件工具”区域获取，或通过悬浮图标复制（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。  
- **插件 URL 与工具路径**：自定义插件中，`插件URL`（如 `https://example.com`）与 `工具路径`（如 `/query`）拼接构成完整 API 地址。  
- **输入参数**：  
  - `传参方式` 必须明确设为 `大模型识别`（从用户输入提取）或 `业务透传`（由外部传入，需通过 `biz_params` 或 `user_defined_params` 传递）；  
  - `参数名称` 和 `参数描述` 需语义清晰，直接影响大模型参数抽取准确率。  
- **鉴权配置**：支持 `Header` 或 `Query` 方式，`Type` 可选 `basic`/`bearer`/`appcode`；[Token](../concepts/token.md) 值需与 API 提供方一致。

## 使用方式

插件可通过三种方式集成：

1. **控制台可视化添加**：  
   - 在 [插件市场](https://bailian.console.aliyun.com/#/plugin-market) 页面，对官方/三方插件单击 **添加至智能体**，选择目标应用（**官方插件仅支持同业务空间内关联**）；  
   - 自定义插件需先发布为 MCP 服务，再在智能体编排页的 **MCP 区块** 中添加（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。  

2. **工作流应用节点**：在工作流编排中将插件作为独立节点，按预设逻辑执行，**不由大模型自主决策调用**。  

3. **API 调用**：  
   - Assistant API：在 `tools` 字段中传入工具定义，参考 [Assistant API 文档](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api)；  
   - 智能体/工作流 API：若含 `业务透传` 参数或 `用户级鉴权`，需通过 `biz_params` 传递（见 [工作流与旧版智能体应用 API](https://help.aliyun.com/zh/model-studio/agent-and-workflow-application-api-reference)）。

## 限制和注意事项

- **权限前提**：首次使用插件必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。主账号可直接授权；RAM 子账号需主账号预先授予 `ram:CreateServiceLinkedRole` 权限（策略条件中 `ram:ServiceName` 必须为 `cloundapi-access.sfm.aliyuncs.com`），否则会报错码 `140052`（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。  
- **数量限制**：单个智能体应用最多添加 10 个工具。  
- **调试要求**：自定义插件的工具必须 **测试成功并发布** 后方可调用；草稿状态或调试失败的工具不可用。  
- **安全约束**：  
  - `code_interpreter` 禁止网络访问、文件上传及系统命令执行；  
  - `quark_search` 和 `github_search` 仅返回元数据摘要，无法抓取页面正文；  
  - 自定义插件若开启鉴权，务必确保 [Token](../concepts/token.md) 有效期与权限范围匹配。  
- **错误处理**：发布工具时常见错误如 `130040`（参数描述缺失）、`130022`（Object 类型子属性为空或 GET 请求含 Object 入参），需按提示修正（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。

## 来源文档

- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


