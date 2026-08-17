# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API）封装为可被大模型识别和调用的标准化单元，解决模型在实时信息获取、精确计算、代码执行、图像生成等场景下的固有局限。插件支持官方预置、三方市场及完全自定义三种形态，开发者可根据业务需求灵活选用或组合。所有插件均需经授权、配置与发布后方可集成至智能体或工作流应用中。

## 支持的模型/功能

当前插件能力已在以下模型上验证可用：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件调用的规划能力与响应质量存在差异，**实际兼容性请以控制台运行结果为准**，不建议依赖文档静态列表做兼容性断言 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

插件按来源分为三类：
- **官方插件**：开箱即用，无需参数配置，包括 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）等 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；
- **三方插件**：覆盖商业服务、教育、音视频等领域，需在云市场开通后调用；
- **自定义插件**：支持通过控制台创建或从云市场导入，可对接任意 HTTP API，支持鉴权（Header/Query）、复杂入参（JSON Object）、业务透传参数等高级能力 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档1中称“官方插件无需配置输入输出参数”，而文档3明确要求自定义插件必须完整配置入参/出参且“所有参数均为必填项”。该差异非矛盾——官方插件因已预置标准化 Schema，故省略配置步骤；自定义插件需显式声明，二者适用不同抽象层级，开发者应严格遵循各自流程。

## 关键参数

插件调用的核心标识与行为控制依赖以下参数：

- **工具 ID（tool_id）**：唯一标识一个工具，如 `calculator`、`quark_search`，API 调用时必须准确传递。可通过插件详情页悬浮图标复制 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；
- **插件 URL 与工具路径**：自定义插件中，`plugin_url`（如 `https://example.com`）与 `tool_path`（如 `/query`）拼接构成完整请求地址；
- **鉴权配置**：支持 `Header`（如 `Authorization: Bearer <token>`）或 `Query`（如 `?api_key=xxx`）方式，类型含 `basic`/`bearer`/`appcode`；
- **输入参数（in-params）**：
  - `传参方式`：`大模型识别`（从用户 query 中抽取）或 `业务透传`（由外部通过 `biz_params` 注入）；
  - `类型`：支持 `String`/`Number`/`Object`，但 `Object` 类型下子属性**不能为空**，须手动添加 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)；
- **输出参数（out-params）**：定义 API 响应中哪些字段将被大模型提取并用于生成最终回答，描述需精简准确。

## 使用方式

插件可通过三种方式集成：
1. **控制台可视化绑定**：
   - 在[插件市场](https://bailian.console.aliyun.com/#/plugin-market)完成授权（主账号/子账号需配置 `AliyunServiceRoleForSFMAccessCloudAPI` 角色）；
   - 官方/三方插件：选择“添加至智能体”，最多关联 10 个工具；
   - 自定义插件：需先发布为 MCP 服务，再于智能体编排页的 **MCP 区块**中添加 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)；
2. **工作流节点**：将插件作为独立节点拖入工作流画布，按编排顺序执行，不依赖大模型自主决策；
3. **API 调用**：
   - Assistant API：在 `tools` 字段中声明工具列表，详见 [Assistant API 文档](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api)；
   - 智能体/工作流 API：通过 `biz_params` 透传鉴权 [Token](../concepts/token.md) 或业务参数 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 限制和注意事项

- **权限前置要求**：首次使用插件前，主账号或 RAM 子账号**必须完成服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI` 授权**，否则无法访问插件市场或导入云市场 API [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；
- **调用范围限制**：官方插件仅支持与**同业务空间内的智能体应用**关联，跨空间调用无效；
- **功能边界**：
  - `code_interpreter` 不支持网络访问与本地文件上传，依赖库版本固定（如 `matplotlib`、`pandas`、`sympy` 等）；
  - `quark_search` 和 `github_search` 仅返回网页/项目标题、摘要、链接，**不支持直接抓取网页正文或仓库代码内容**；
- **自定义插件发布强约束**：
  - 工具名称长度 ≤20 字符；
  - `GET` 方法下输入参数**不支持 `Object` 类型**；
  - 发布失败常见原因：参数描述缺失（错误码 130040）、`Object` 子属性为空（错误码 130022），须按提示修正 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)；
- **调试必要性**：所有自定义工具必须通过“测试工具”验证连通性与参数解析逻辑，**仅“已发布”且“调试成功”状态的工具才可被调用**。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


