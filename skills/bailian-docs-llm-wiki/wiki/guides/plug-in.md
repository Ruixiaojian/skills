# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（API）集成到大模型工作流中，弥补其在实时信息获取、精确计算、代码执行、图像生成等任务上的固有局限。插件支持官方预置、三方市场及完全自定义三种类型，可被智能体应用、工作流应用或 Assistant API 主动调用或编排执行。开发者需关注模型兼容性、参数配置规范及权限授权要求。

## 支持的模型/功能

当前插件能力已在以下模型上验证可用：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件调用的规划能力与响应稳定性存在差异，**最新兼容性状态请以控制台实际执行结果为准** [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。  
插件按来源分为三类：  
- **官方插件**：开箱即用，无需配置输入/输出参数，包括 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）等；  
- **三方插件**：覆盖商业服务、图像视频、教育等领域，需在云市场开通后调用；  
- **自定义插件**：支持开发者通过 HTTP API 自主接入，支持鉴权（Header/Query）、多工具路径、复杂参数映射与在线调试 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。  

> **注意**：文档 1 与文档 2 均列出 `quark_search` 插件说明，但文档 2 明确指出“夸克搜索和联网搜索（`enable_search`）有本质区别”——前者返回结构化搜索结果供模型直接使用，后者仅为增强生成的辅助机制，不返回原始搜索内容。该差异在文档 1 中未体现，应以文档 2 为准 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

## 关键参数

插件调用依赖两类关键参数：  
- **工具 ID**：唯一标识一个工具（如 `calculator`），用于 API 请求中的 `tools` 字段或控制台工具绑定。可通过插件详情页悬浮图标复制 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；  
- **输入/输出参数**：自定义插件必须明确定义。输入参数需指定 `参数名称`、`参数描述`、`类型`（Number/String/Object 等）、`传参方式`（`大模型识别` 或 `业务透传`）；输出参数需声明 `参数名称` 和 `类型`，用于模型解析 API 响应。Object 类型子属性**不能为空**，否则发布失败 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。  
- **鉴权参数**：自定义插件若启用鉴权，需配置 `鉴权类型`（`basic`/`bearer`/`appcode`）、`位置`（Header/Query）、`参数名` 及 `Token`。例如 `bearer` 类型将自动构造 `Authorization: Bearer <TOKEN>` 头。

## 使用方式

插件可通过三种方式集成：  
1. **控制台可视化绑定**：在[插件市场](https://bailian.console.aliyun.com/#/plugin-market)页面，为智能体应用添加插件（最多 10 个工具）；或为自定义插件发布为 MCP 服务后，在智能体编排页的 **MCP 区块** 中添加；  
2. **工作流应用节点**：将插件作为独立节点拖入工作流画布，按编排顺序执行，**不由模型自主决策调用** [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)；  
3. **API 调用**：  
   - Assistant API：在请求体 `tools` 数组中传入工具定义（含 `function.name`、`function.description`、`function.parameters`），模型将生成 `tool_calls`；  
   - 智能体/工作流 API：通过 `biz_params` 传递业务透传参数或用户级鉴权 Token [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。  
所有方式均需确保插件已**发布**且处于**启用**状态，自定义插件还需完成在线调试并确认运行成功。

## 限制和注意事项

- **权限前提**：首次使用插件前，主账号或 RAM 子账号必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`，否则无法访问插件市场或导入云市场 API [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；  
- **业务空间隔离**：官方插件仅能与**同业务空间**内的智能体应用关联，跨空间需单独授权；  
- **功能限制**：  
  - `code_interpreter` 不支持网络访问与本地文件上传，依赖库版本固定（如 `matplotlib`、`pandas`、`sympy` 等）；  
  - `quark_search` 和 `github_search` 仅返回网页/项目标题、摘要、链接，**不支持访问详情页内容**；  
  - 自定义插件的 GET 请求**不支持 Object 类型输入参数**，否则发布报错 `130022`；  
- **安全与维护**：删除插件或工具将导致已关联的应用失效且**不可撤回**；修改插件 URL 或鉴权配置后，必须重新测试并发布工具 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


