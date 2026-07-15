# 插件机制

插件机制是百炼平台提供的核心能力扩展框架，通过标准化接口将外部工具（API、服务或计算能力）安全、可控地集成到大模型推理链路中，使模型在保持语言理解能力的同时，具备实时搜索、代码执行、图像生成、专业计算等超越纯文本推理的增强能力。

## 在百炼平台的不同场景中，这个概念如何使用

插件机制并非单一技术实现，而是贯穿多个能力层的统一抽象，其具体形态和使用方式因场景而异：

- **智能体应用（Agent）**：插件作为“可调用工具”被注入模型上下文。大模型基于用户输入语义自主规划是否调用、调用哪个插件及传入参数（如 `calculator` 计算 `237 × 48`），整个过程无需开发者编写调度逻辑。官方插件（如 `quark_search`）、三方插件（云市场服务）和自定义插件均可在此模式下启用。

- **工作流应用（Workflow）**：插件以显式节点形式存在，开发者手动拖拽、配置输入/输出连接与参数映射（如将上一节点提取的地址传给 `amap_weather` 工具）。此时插件不依赖模型决策，适用于确定性、多步骤、需精确控制的业务编排。

- **Assistant API 调用**：通过 `tools` 数组声明插件 ID 及结构化描述（含 `name`、`description`、`parameters` JSON Schema），由 SDK 或平台自动完成 function calling 的请求构造、响应解析与结果注入，实现与 OpenAI 兼容的工具调用范式。

- **MCP（Model Context Protocol）服务**：作为插件机制的协议升级形态，MCP 提供更严格的标准化通信契约（如 `streamableHttp` 协议、JSON Schema 输入校验、KMS 加密凭据管理），支持跨平台工具复用与统一治理。所有 MCP 服务（包括官方 Amap Maps、WebSearch 及自定义部署服务）在百炼中均以“插件”身份被发现、授权和调用。

> ⚠️ 注意：`Skill`（技能）虽常被类比为“插件”，但其本质不同——Skill 是预打包的、无网络调用的本地计算能力（如 CSV 清洗、PDF 解析），由百炼调度引擎基于 `description` 语义匹配触发，不涉及 HTTP 请求或外部服务授权，因此**不属于插件机制范畴**。

## 关键参数和配置

以下参数在自定义插件或 MCP 服务配置中必须准确设置，直接影响调用成功率与安全性：

| 参数 | 说明 | 开发提示 |
|------|------|----------|
| **`tool_id`（工具 ID）** | 插件内唯一标识具体工具的字符串（如 `text_to_image`），用于 Assistant API 的 `tools` 声明或工作流节点选择。可在控制台插件详情页复制。 | 避免使用空格、中文或特殊符号；同一插件内不可重复。 |
| **`url` + `path`** | 插件服务根地址（如 `https://api.example.com`）与工具路径（如 `/v1/generate`），拼接后构成完整调用 URL。MCP 中对应 `url` 字段（`type=streamableHttp` 时必填）。 | 确保 URL 可公网访问且 HTTPS 启用；路径区分大小写。 |
| **`inputSchema`（JSON Schema）** | 定义输入参数结构，直接影响模型参数提取准确性。必须包含 `type`、`properties`，推荐使用 `required` 明确必填项。 | 示例：`{"type":"object","properties":{"prompt":{"type":"string"}},"required":["prompt"]}` |
| **鉴权方式** | 支持 `Header`（如 `Authorization: Bearer <token>`）或 `Query`（如 `?api_key=xxx`）；MCP 强制要求 `Authorization` header 为 `Bearer <DASHSCOPE_API_KEY>`。 | 敏感密钥（如地图 API Key）**必须通过 KMS 加密存储**，禁止明文配置。 |
| **`output_parameters`（输出字段）** | 指定 API 返回 JSON 中哪些顶层字段供模型读取（如 `{"image_url": "string"}`），需扁平、非嵌套、非空。 | 避免返回大体积二进制或原始 HTML；仅保留模型生成回复所需的最小数据集。 |

## 面向开发者，简洁实用

- **快速起步**：优先使用控制台「插件市场」添加官方插件（如 `code_interpreter`），无需配置即可在智能体中测试；确认 `AliyunServiceRoleForSFMAccessCloudAPI` 角色已授权（主账号一键授权，RAM 用户需 `ram:CreateServiceLinkedRole` 权限）。

- **自定义插件上线三步**：  
  1. 在控制台创建插件 → 填写 `tool_id`、`url`、`path`；  
  2. 定义 `inputSchema` 和 `output_parameters`（用 JSON Schema 校验器验证）；  
  3. **在线调试通过并发布为“已发布”状态**（草稿/未启用 = 调用失败）。

- **避坑指南**：  
  - 所有插件调用均**只透传 `Authorization` header**，其他自定义 header 会被平台剥离；  
  - `Object` 类型输入参数在 `GET` 请求中不被支持（仅 `POST` 允许）；  
  - 智能体最多添加 10 个工具（含 Skill），MCP 服务上限为 5 个；  
  - 实际模型兼容性以控制台运行结果为准，文档列表可能滞后（如 `qwen2.5` 系列需实测）。

- **调试技巧**：开启 `stream=True` 查看模型思考过程（含 tool call 步骤）；检查返回错误码（如 `130040` = 参数描述缺失，`11200054` = MCP 协议解析失败），对照文档定位问题。

## 关联主题页

- [plug in](../guides/plug-in.md)
- [skill](../guides/skill.md)
- [model context protocol](../guides/model-context-protocol.md)
- [application support](../guides/application-support.md)
- [more about models](../api/more-about-models.md)


