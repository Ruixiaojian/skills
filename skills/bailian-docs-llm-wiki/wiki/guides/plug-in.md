# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（API）集成到模型推理链路中，解决大模型在实时信息获取、精确计算、代码执行、图像生成等场景下的固有局限。开发者可选用官方插件、三方插件或自定义插件，结合智能体应用、工作流应用或 Assistant API 进行调用。插件调用由大模型自主规划（智能体/Assistant 模式）或显式编排（工作流模式）驱动。

## 支持的模型与功能

百炼当前支持以下模型调用插件：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件的支持能力存在差异，**实际兼容性请以控制台运行结果为准**，而非文档静态列表 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

官方插件提供开箱即用能力，包括：
- `code_interpreter`：执行 Python 代码（支持 matplotlib、pandas、sympy 等依赖，但**不支持网络访问与本地文件上传**）；
- `calculator`：复杂数学运算；
- `text_to_image`：文生图（限时免费，需申请开通）；
- `quark_search`：实时网页搜索（返回标题、关键词、摘要，**不支持访问网页详情**）；
- `generate_qrcode`：URL 转二维码；
- `github_search`：GitHub 项目检索（返回标题、链接、摘要，**不支持访问项目详情**）。

三方插件覆盖商业服务、图像视频、教育等领域，需先开通后使用；自定义插件支持完全自主开发，详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 和文档 2 均列出 `quark_search` 和 `github_search` 的能力边界（仅返回摘要，不支持详情访问），但文档 2 在“常见问题”中额外说明“夸克搜索和联网搜索（`enable_search`）有什么区别？”，指出 `enable_search` 是另一套机制，**并非插件**。该字段属于模型参数，与插件无关，开发者不应混淆二者——插件调用必须显式声明 `tools`，而 `enable_search` 是隐式增强，不可控且不返回结构化结果。

## 关键参数

插件调用依赖以下核心参数：

- **工具 ID（tool_id）**：唯一标识一个工具，如 `calculator`。必须通过控制台插件详情页复制，或在 API 请求中准确传入 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **输入参数（input parameters）**：
  - `传参方式`：分为 `大模型识别`（从用户输入中抽取）和 `业务透传`（由外部系统通过 `biz_params` 或 `user_defined_params` 注入）；
  - `类型`：支持 `String`、`Number`、`Boolean`、`Object`（Object 子属性**不能为空**，需显式添加）；
  - `必填`：勾选后，大模型未识别出该参数时将拒绝调用。
- **输出参数（output parameters）**：定义 API 返回数据中哪些字段被提取并送入大模型上下文，**所有字段均为必填项**，描述需精简准确，层级应尽量扁平。
- **鉴权配置**（自定义插件）：
  - 支持 `Header` 或 `Query` 位置；
  - `Type` 可选 `basic` / `bearer` / `appcode`，决定 Authorization 头格式；
  - `Token` 为服务级鉴权凭证，用户级鉴权需配合 `biz_params` 透传。

## 使用方式

插件可通过三种方式接入：

1. **控制台集成（推荐快速验证）**：
   - 官方/三方插件：在 [插件市场](https://bailian.console.aliyun.com/#/plugin-market) 页面单击“添加至智能体”，选择目标智能体（**官方插件仅支持同业务空间内关联**），最多添加 10 个工具；
   - 自定义插件：需先发布为 MCP 服务，再在智能体编排页的“MCP”区块中添加 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

2. **工作流应用**：将插件作为独立节点拖入画布，按需编排执行顺序，**不依赖大模型自动决策**。

3. **API 调用**：
   - Assistant API：在 `tools` 数组中声明工具定义，请求时携带 `tool_choice` 控制调用策略；
   - 智能体/工作流 API：通过 `biz_params` 传递业务透传参数或用户级鉴权 [Token](../concepts/token.md)。

> **注意**：文档 1 描述“通过智能体应用或 Assistant API 调用插件后，大模型将根据用户输入、工具名称及工具描述来判断是否调用”，而文档 3 明确要求“工具描述”需用自然语言、给出示例——这表明**工具描述质量直接影响调用准确率**，开发者须避免模糊表述。

## 限制和注意事项

- **权限前置要求**：首次使用插件前，主账号或 RAM 子账号必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。RAM 用户需主账号授予 `ram:CreateServiceLinkedRole` 权限，否则无法完成授权 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **[业务空间隔离](../concepts/workspace-isolation.md)**：官方插件仅能与**同一业务空间内的智能体应用**关联；跨空间调用需通过自定义插件 + MCP 方式实现。
- **调试与发布强约束**：自定义插件的工具必须经“测试工具”成功运行后，再点击“发布”，**草稿状态工具无法被调用**；发布失败常见原因包括参数描述缺失（错误码 130040）、Object 子属性为空（错误码 130022）或 GET 方法下误配 Object 类型入参 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **组合调用限制**：单次对话中可同时触发多个插件，但工具总数上限为 10 个（智能体模式）；工作流中无此限制，但需手动编排。
- **计费提示**：`text_to_image` 和 `quark_search` 为“限时免费，需申请开通”，其余官方插件当前免费；三方插件按所选套餐计费。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


