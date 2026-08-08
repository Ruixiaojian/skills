# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（API）集成到推理链路中，弥补大模型在实时信息获取、精确计算、代码执行、图像生成等方面的固有局限。插件以“工具集合”形式组织，支持官方预置、三方市场及完全自定义三种类型，可被智能体应用、工作流应用或 Assistant API 主动调用或编排执行。其设计目标是让开发者无需修改模型本身，即可安全、可控地增强应用功能。

## 支持的模型/功能

百炼当前支持插件调用的模型包括：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max` 和 `qwen-vl-plus`。各模型对插件的兼容性存在差异，**实际可用性以控制台运行结果为准**，不建议依赖文档静态列表做兼容性判断 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

插件功能分为三类：
- **官方插件**：开箱即用，无需配置参数，涵盖 Python 代码解释器（`code_interpreter`）、计算器（`calculator`）、图片生成（`text_to_image`）、夸克搜索（`quark_search`）、生成二维码（`generate_qrcode`）、GitHub 搜索（`github_search`）等 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；
- **三方插件**：来自阿里云云市场，覆盖商业服务、图像视频、教育等领域，需开通后使用；
- **自定义插件**：支持通过控制台创建或从云市场导入，允许开发者接入任意 HTTP API，并精细配置鉴权、输入/输出参数及高级调用示例 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 和文档 2 均列出 `quark_search` 插件说明，但文档 2 明确指出“夸克搜索插件目前支持检索出网页标题、关键词和摘要，但不支持直接访问网页详情”，而文档 1 仅简述为“不支持直接访问网页详情”。二者实质一致，但文档 2 表述更完整，应以此为准。

## 关键参数

插件调用的核心标识是 **工具 ID**（如 `calculator`），必须在 API 请求中准确传递。自定义插件还需关注以下关键配置项：
- **插件 URL**：工具所在服务的根域名（如 `https://myapi.example.com`），所有工具路径均以此为基准拼接；
- **工具路径**：以 `/` 开头的相对路径（如 `/query`），与插件 URL 组合成完整请求地址；
- **输入参数**：需明确定义参数名、类型（String/Number/Object 等）、描述、传参方式（`大模型识别` 或 `业务透传`）；Object 类型子属性**不能为空**，必须显式添加 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)；
- **鉴权配置**：支持 Header 或 Query 方式，鉴权类型包括 `basic`、`bearer`、`appcode`；[Token](../concepts/token.md) 值需由 API 提供方分配；
- **高级配置（Value）**：提供用户 Query 到入参 JSON 的映射示例（如 `"查询杭州明天天气" → {"city": "杭州", "date": "2025-04-25"}`），显著提升大模型参数提取准确率。

## 使用方式

插件可通过三种方式集成：
1. **控制台可视化绑定**：在插件市场页面选择工具 → 单击“添加至智能体”，关联到同业务空间的智能体应用；最多支持 10 个工具同时启用 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；
2. **工作流节点编排**：在工作流应用中将插件作为独立节点拖入画布，按需设置输入/输出连接，由人工编排而非模型自主决策；
3. **API 调用**：
   - Assistant API：在 `tools` 字段中声明工具列表，模型自动选择并触发调用；
   - DashScope SDK / HTTP 接口：通过 `biz_params` 传递业务透传参数或用户级鉴权 [Token](../concepts/token.md) [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：官方插件仅支持与**相同业务空间**内的智能体应用关联；子业务空间首次使用需单独授权 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

## 限制和注意事项

- **权限要求**：主账号或 RAM 子账号首次访问插件市场前，必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`；RAM 用户需额外授予 `ram:CreateServiceLinkedRole` 权限，否则授权失败 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；
- **自定义插件限制**：工具名称长度 ≤ 20 字符；GET 方法不支持 Object 类型输入参数；发布前必须完成在线调试且状态为“成功”；
- **功能边界**：
  - `code_interpreter` 不支持网络访问与本地文件上传，预装依赖列表详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；
  - `quark_search` 和 `github_search` 仅返回摘要信息，无法加载网页或项目详情页；
  - 多插件组合调用（如夸克搜索 + 图片生成 + 二维码）可行，但需确保各工具输出格式能被下游工具正确消费；
- **安全性**：自定义插件的鉴权逻辑完全由开发者控制，百炼平台不校验 [Token](../concepts/token.md) 有效性，仅负责透传；务必确保 API 端点具备防重放、限流等基础防护。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


