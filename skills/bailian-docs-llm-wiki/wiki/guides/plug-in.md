# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（API）集成到模型推理流程中，弥补其在实时信息获取、精确计算、代码执行、图像生成等场景下的固有局限。开发者可选用官方预置插件、经验证的三方插件，或完全自主定义符合业务需求的插件。插件调用由模型自主规划（智能体/Assistant API）或显式编排（工作流）驱动，最终结果经模型整合后输出。

## 支持的模型与功能

百炼当前支持在以下模型上启用插件能力：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件的兼容性可能存在差异，实际可用性请以控制台运行结果为准 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

插件按来源分为三类：
- **官方插件**：开箱即用，无需配置参数，包括 `code_interpreter`（Python执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub项目检索）等；
- **三方插件**：覆盖商业服务、图像视频、教育等领域，需在插件市场开通后使用；
- **自定义插件**：支持从零创建或从云市场导入，可灵活定义工具路径、鉴权方式、输入/输出参数及高级调用示例 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 和文档 2 均列出 `quark_search` 插件说明，但文档 2 明确指出“夸克搜索和联网搜索（`enable_search`）有本质区别”，而文档 1 未提及 `enable_search`。实际开发中应以文档 2 的区分逻辑为准：`quark_search` 是独立工具调用，返回结构化摘要；`enable_search` 是模型内部增强机制，不暴露原始搜索结果。

## 关键参数

- **工具 ID**：唯一标识插件下的具体工具（如 `calculator`），API 调用时必须传入，可在插件详情页的工具卡片上复制 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；
- **输入参数**：需明确定义名称、类型（String/Number/Object 等）、描述、传参方式（`大模型识别` 或 `业务透传`）。Object 类型子属性**不能为空**，否则发布失败；
- **输出参数**：定义 API 返回数据中哪些字段将被模型提取并用于生成最终回复，所有参数均为必填；
- **鉴权配置**：支持 Header（`Authorization: Bearer <TOKEN>`）或 Query（如 `?api_key=xxx`）方式，鉴权类型包括 `basic`、`bearer`、`appcode`；
- **高级配置（可选）**：提供用户 Query 与期望构造入参的映射示例（如 `"查询杭州明天的天气"` → `{"city": "杭州", "date": "2025-04-25"}`），显著提升模型参数识别准确率。

## 使用方式

插件可通过三种方式集成：
1. **控制台 - 智能体应用**：在插件市场选择工具 → 单击“添加至智能体” → 关联目标智能体 → 发布应用。注意：官方插件仅支持与**同业务空间**的智能体关联；
2. **控制台 - 工作流应用**：将插件作为独立节点拖入工作流画布，按需编排执行顺序；
3. **API 调用**：
   - Assistant API：在 `tools` 字段中声明工具列表，模型自动决策是否调用；
   - 工作流/旧版智能体 API：通过 `biz_params` 传递业务透传参数或用户级鉴权 [Token](../concepts/token.md)。

首次使用前，主账号或 RAM 子账号需授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`，否则无法访问插件市场 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

## 限制和注意事项

- 单个智能体应用最多支持添加 **10 个工具**；
- `code_interpreter` 插件**不支持网络访问与本地文件上传**，可用依赖版本已固化（如 `requests~=2.31.0`、`pandas`、`matplotlib` 等），详见文档 2；
- `quark_search` 和 `github_search` 均**仅返回摘要信息（标题、关键词、链接、摘要），不支持访问网页或仓库详情页**；
- 自定义插件中，GET 请求**不支持 Object 类型输入参数**；POST 请求下 Object 参数子属性必须非空，否则发布报错 `130022`；
- 删除插件或工具将导致**所有已关联的应用失效且不可恢复**，操作前须确认；
- 从云市场导入的插件，系统自动填充的出入参可能缺失，发布前需人工校验并补全（如参数描述、Object 子属性），否则因错误码 `130040` 等失败。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


