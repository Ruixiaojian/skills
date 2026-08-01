# plug in

插件是百炼平台扩展大模型能力的核心机制，通过将外部工具（如代码执行、实时搜索、图像生成等）以标准化方式集成到大模型推理流程中，弥补其在实时信息获取、精确计算、多模态输出等方面的固有局限。插件分为官方插件、三方插件和自定义插件三类，支持在智能体应用、工作流应用及 Assistant API 中调用。所有插件均需通过服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI` 授权访问云资源，该授权是使用前提 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

## 支持的模型与功能

百炼当前支持插件调用的模型包括：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max` 和 `qwen-vl-plus`。各模型对插件的兼容性以控制台实际执行结果为准，建议在目标模型下进行端到端验证 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

**官方插件（开箱即用，无需配置参数）**：
- `code_interpreter`：执行 Python 代码（支持 pandas、matplotlib、sympy 等依赖，**不支持网络访问与文件上传**）
- `calculator`：高精度数学计算
- `text_to_image`：文生图（限时免费，需申请开通）
- `quark_search`：基于夸克的实时网页搜索（返回标题、关键词、摘要，**不支持访问网页详情**）
- `generate_qrcode`：URL 转二维码
- `github_search`：GitHub 项目检索（返回标题、链接、摘要，**不支持访问项目详情**）

**三方插件**：覆盖商业服务、图像视频、教育等领域，需在插件市场开通后直接调用。

**自定义插件**：支持通过 REST API 接入任意业务系统，需明确定义插件 URL、工具路径、输入/输出参数及鉴权方式 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 与文档 2 均列出 `quark_search` 和 `github_search` 的能力边界（仅返回摘要，不支持详情页访问），但文档 1 在“常见问题”中称“联网搜索（enable_search）也是基于夸克搜索”，而文档 2 未提及 `enable_search` 参数。该参数不属于插件体系，而是独立的模型侧开关，**不应与插件混淆**；插件调用必须显式声明 `tools` 列表。

## 关键参数

- **工具 ID（tool_id）**：唯一标识插件下的具体工具，API 调用时必需。可在插件详情页的“插件工具”区域或工具卡片悬停图标处复制。
- **输入参数（input parameters）**：
  - `传参方式` 必须明确设为 `大模型识别`（从用户输入提取）或 `业务透传`（由外部传入，通过 `biz_params` 或 `user_defined_params` 传递）。
  - `参数名称` 和 `参数描述` 需语义清晰，直接影响大模型参数提取准确率。
- **输出参数（output parameters）**：定义 API 返回数据中哪些字段被送入大模型用于最终回答，所有字段均为必填，嵌套层级应尽量扁平。
- **鉴权配置**（仅自定义插件）：
  - 支持 `Header`（如 `Authorization: Bearer <token>`）或 `Query`（如 `?api_key=xxx`）方式。
  - `Type` 可选 `basic` / `bearer` / `appcode`，决定 token 前缀。

## 使用方式

1. **控制台集成（推荐快速验证）**：
   - 官方/三方插件：进入 [插件市场](https://bailian.console.aliyun.com/#/plugin-market)，开通并单击“添加至智能体”，选择同业务空间的智能体应用即可。
   - 自定义插件：创建并发布工具后，需先“发布为 MCP 服务”，再在智能体编排页的 **MCP 区块** 中添加 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
2. **API 集成**：
   - Assistant API：在 `tools` 数组中传入工具定义（含 `tool_id`、`description` 等），请求时自动触发规划与调用。
   - 工作流应用：将插件作为独立节点编排，不依赖大模型自主决策。
3. **权限前置要求**：
   - 主账号：首次访问插件页需授权 `AliyunServiceRoleForSFMAccessCloudAPI` 角色。
   - RAM 子账号：需主账号授予 `ram:CreateServiceLinkedRole` 权限（策略条件中 `ram:ServiceName` 必须为 `cloundapi-access.sfm.aliyuncs.com`），否则授权失败 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

## 限制和注意事项

- **数量限制**：单个智能体应用最多关联 10 个插件工具。
- **业务空间隔离**：官方插件仅能与**同一业务空间**内的智能体关联；子业务空间需单独授权。
- **自定义插件调试要求**：工具必须经“测试工具”验证成功且状态为“已发布”，否则无法调用。
- **安全约束**：
  - `code_interpreter` 禁止网络访问、本地文件读写及敏感模块（如 `os.system`）。
  - 自定义插件若启用鉴权，`biz_params` 中的 token 将被透传，需确保传输链路安全。
- **错误处理**：发布自定义工具时常见错误码 `130040`（参数描述缺失）、`130022`（Object 类型子属性为空或 GET 请求含 Object 入参），需按提示修正 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **计费说明**：官方插件中 `text_to_image` 和 `quark_search` 为“限时免费，需申请开通”，其余为免费；三方插件按所选套餐计费。

## 来源文档

- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


