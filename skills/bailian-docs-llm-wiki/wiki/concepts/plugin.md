# 插件

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如计算、搜索、图像生成、API 服务等）安全、标准化地集成到模型推理流程中，弥补大模型在实时信息获取、精确计算、确定性执行和领域操作等方面的固有局限。它不修改模型本身，而是以“可调用工具”的形式被模型自主规划或由开发者显式编排。

## 在百炼平台的不同场景中如何使用

插件能力贯穿百炼三大应用范式，但具体形态与接入方式略有差异：

- **智能体应用（Agent）**：模型基于用户输入、工具描述和上下文，自主决定是否调用插件（如 `calculator` 或 `quark_search`），调用结果自动注入上下文并参与最终回复生成。适用于需动态决策的开放型任务（如“帮我算出过去三个月销售额总和，并搜索行业最新政策”）。
  
- **工作流应用（Workflow）**：插件作为独立节点（如 MCP 工具节点或 Skill 节点）被手动拖拽、配置参数并编排执行顺序。调用时机、输入来源（变量/上一节点输出）和错误分支均由开发者显式定义，适用于路径确定、需强可控性的业务流程（如客服工单自动查单+生成摘要+发送通知）。

- **Managed Agents（托管智能体）**：插件以两种方式增强能力：
  - **内置工具**（如 `bash`、`read`、`write`）直接挂载为沙箱环境能力；
  - **外部能力**通过 MCP 服务接入（如 `amap-maps/maps_weather`），在 Agent 创建时声明，运行时按需调用。适合长时、有状态、需文件操作与环境隔离的复杂任务（如分析上传的 Excel 并调用天气 API 生成可视化报告）。

> ⚠️ 注意：`Skill` 和 `MCP 服务` 是插件能力的两种重要实现形式，但概念层级不同——  
> - **Skill** 是面向[文件处理](file-processing.md)、格式解析等特定任务的封装能力包（以 ZIP + `SKILL.md` 定义），强调语义驱动的自动识别；  
> - **MCP 服务** 是遵循 Model Context Protocol 标准的通用工具接入协议，支持任意 HTTP API 的标准化对接，更侧重跨平台兼容性与生产级托管；  
> - **传统插件（如 `code_interpreter`、`text_to_image`）** 则是平台预置的开箱即用能力，属于最简化的插件实例。三者统一归于“插件”这一横切能力抽象下，开发者可根据场景选择最适配形态。

## 关键参数和配置

无论官方、三方或自定义插件，以下参数是配置与调试的核心：

| 参数 | 说明 | 开发提示 |
|------|------|----------|
| **工具 ID / `tool_name`** | 插件内具体工具的唯一标识符（如 `calculator`, `maps_weather`），模型 function calling 时直接引用。必须与控制台/文档中完全一致。 | ✅ 从插件详情页复制，避免手输错误；多个工具共存时确保名称不冲突。 |
| **输入参数（`inputSchema` 或 控制台表单）** | 定义工具所需参数结构。推荐使用 JSON Schema（MCP）或明确配置 `参数名称`/`类型`/`传参方式`：<br>• `大模型识别`：由模型从用户输入中抽取（如城市名、数学表达式）；<br>• `业务透传`（`biz_params`）：由开发者在 API 请求中显式传入（如 API Key、会话 ID）。 | ✅ 对 `大模型识别` 参数，务必在工具描述中提供典型示例（如“输入：‘北京今天气温多少？’ → city=‘北京’”）；<br>❌ 避免 `Object` 类型参数含空子属性（易触发错误码 130022）。 |
| **输出参数（`outputSchema` 或 出参映射）** | 指定 API 返回数据中哪些字段会被提取并送入模型上下文。所有字段均为必填项，嵌套层级应尽量扁平（如 `data.temperature` → `temperature`）。 | ✅ 输出字段命名应语义清晰、无歧义（如不用 `res`，而用 `weather_summary`）；<br>✅ 复杂响应建议提前在服务端做裁剪，减少 [Token](token.md) 消耗。 |
| **鉴权配置** | 自定义插件必需。支持 Header（`Authorization: Bearer xxx`）、Query（`?token=xxx`）方式，鉴权类型包括 `basic`/`bearer`/`appcode`。[Token](token.md) 必须通过 KMS 加密存储，严禁硬编码。 | ✅ 使用百炼控制台的“环境变量”功能注入敏感凭据；<br>✅ 测试阶段可用临时 [Token](token.md)，生产环境必须轮换策略。 |
| **协议与端点** | MCP 插件必须使用 `Streamable HTTP` 协议（端点 `/mcp`），旧版 SSE 已弃用。URL 必须为 HTTPS。 | ✅ 新建 MCP 服务默认启用 Streamable HTTP；<br>✅ 外部调用时，SDK 必须使用 `streamablehttp_client`。 |

## 面向开发者：简洁实用指南

- **快速起步**：优先选用官方插件（如 `calculator`, `quark_search`），无需配置，控制台一键添加至智能体即可测试。
- **自定义接入**：  
  1. 若已有 RESTful API → 用「AI 网关导入」快速转为 MCP 工具；  
  2. 若需深度定制 → 编写符合 [MCP 规范](https://modelcontextprotocol.io/) 的 Server，部署至函数计算（FC），再在百炼控制台注册；  
  3. 若专注[文件处理](file-processing.md) → 用 Skill（ZIP + `SKILL.md`）更轻量，无需写后端。
- **调试黄金法则**：  
  ✅ 所有自定义插件必须先通过「测试工具」在线验证（检查入参解析、HTTP 状态码、JSON 响应结构）；  
  ✅ 发布前确认 `description`（Skill）或 `inputSchema`（MCP）准确覆盖典型用户表达；  
  ✅ 监控 Token 消耗——MCP 返回内容直接计入输入 Token，大响应体可能显著推高成本。
- **避坑提醒**：  
  ❌ 单个智能体最多绑定 10 个工具；  
  ❌ `code_interpreter` 沙箱禁止网络访问、本地文件上传，依赖库版本固定；  
  ❌ `quark_search` 返回结构化摘要，不支持网页抓取；  
  ❌ 文件类插件（Skill/MCP）单文件上限 10 MB，超限需前端分片或服务端预处理。

插件不是附加功能，而是百炼平台实现“模型能力可编程”的基础设施。善用它，让大模型真正成为你业务逻辑的智能执行引擎。

## 关联主题页

- [plug in](../guides/plug-in.md)
- [model context protocol](../guides/model-context-protocol.md)
- [skill](../guides/skill.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)


