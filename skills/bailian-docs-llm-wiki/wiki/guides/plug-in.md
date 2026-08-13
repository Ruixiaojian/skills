# plug in

插件是百炼平台扩展大模型能力的核心机制，通过将外部工具（如代码执行、实时搜索、图像生成等）以标准化方式集成到大模型推理链路中，弥补其在计算精度、时效性、[多模态](../concepts/multimodal.md)输出等方面的固有局限。开发者可选用官方预置插件、三方市场插件或自定义开发插件，所有插件均需经授权、配置与发布后方可调用。插件调用由大模型自主规划（智能体/Assistant API）或显式编排（工作流）触发。

## 支持的模型/功能

百炼当前支持在以下模型上启用插件能力：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件的实际兼容性以控制台运行结果为准，[插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md) 中明确指出“最新的兼容性状态，请以控制台实际执行结果为准”。

官方插件提供开箱即用的六类基础能力：
- `code_interpreter`：执行 Python 代码（支持 `pandas`、`matplotlib`、`sympy` 等依赖，**不支持网络访问与本地文件上传**）；
- `calculator`：高精度数学计算；
- `text_to_image`：文生图（限时免费，需申请开通）；
- `quark_search`：基于夸克的实时网页摘要检索（**仅返回标题、关键词、摘要，不支持详情页访问**）；
- `generate_qrcode`：URL 转二维码；
- `github_search`：GitHub 项目检索（**仅返回项目标题、链接、摘要，不支持详情页访问**）。

三方插件覆盖商业服务、图像视频、教育等领域，需先开通；自定义插件支持通过 REST API 接入任意业务系统，详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 文档。

> **注意**：文档 1 与文档 2 均称 `quark_search` 和 `github_search` “不支持直接访问网页详情/项目详情”，但文档 1 在“夸克搜索”小节末尾额外强调“目前支持检索出网页标题、关键词和摘要”，而文档 2 未提关键词，二者描述一致但颗粒度不同，以文档 1 的完整说明为准。

## 关键参数

- **工具 ID（tool_id）**：唯一标识插件下的具体工具，API 调用时必需。可通过插件详情页的“插件工具”区域或悬浮工具名称图标复制获取（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。
- **输入参数（input parameters）**：分为 `大模型识别`（从用户输入中抽取）与 `业务透传`（由外部系统传入，需通过 `biz_params` 或 `user_defined_params` 指定）。Object 类型参数的子属性**不能为空**，必须显式添加（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。
- **鉴权配置**：自定义插件支持 Header 或 Query 方式鉴权，类型包括 `basic`、`bearer`、`appcode`；云市场导入插件自动携带 AppKey/AppSecret/AppCode，无需手动配置鉴权（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。
- **高级配置（示例 Query）**：用于提升大模型参数提取准确率，建议为复杂入参提供典型调用样例（如 `{"city": "杭州", "date": "2025-04-25"}`）。

## 使用方式

插件可通过三种方式集成：
1. **控制台可视化绑定**：在 [插件市场](https://bailian.console.aliyun.com/#/plugin-market) 添加插件至智能体应用（最多 10 个），或在应用管理 > 智能体编排页的 **MCP 区块** 添加已发布的 MCP 服务（自定义插件需先发布为 MCP）；
2. **工作流节点**：将插件作为独立节点嵌入工作流，按编排顺序执行，**不由大模型自主决策调用**；
3. **API 调用**：通过 Assistant API 的 `tools` 字段声明可用工具列表，并在 `messages` 中传递用户输入；调用时需传入 `tool_id` 及对应参数（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 中“方式三”说明）。

> **注意**：官方插件在子业务空间使用前**必须单独授权**（文档 1 明确要求“在默认业务空间调用不需要执行此步骤”，而子空间需进入插件详情页单击“授权”）；三方插件需先开通套餐；自定义插件必须完成“创建→调试→发布”全流程，且工具状态为“已发布”+“启用”才可调用。

## 限制和注意事项

- **权限前提**：主账号或 RAM 子账号首次使用插件前，必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。RAM 用户需额外被授予 `ram:CreateServiceLinkedRole` 权限（策略条件中 `ram:ServiceName` 应为 `cloundapi-access.sfm.aliyuncs.com`），否则授权失败（该细节在 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 中完全一致）。
- **调用限制**：智能体应用中最多绑定 10 个插件；自定义插件的 Object 类型入参在 GET 请求下不被支持（文档 3 错误码 130022 明确说明）。
- **安全约束**：`code_interpreter` 插件禁止网络访问与文件上传；所有插件输出均经大模型二次加工，原始 API 响应不可直接透传给用户。
- **状态依赖**：插件/工具必须处于“已发布”且“启用”状态；删除插件将导致所有关联应用失效，操作不可逆（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。

## 来源文档

- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


