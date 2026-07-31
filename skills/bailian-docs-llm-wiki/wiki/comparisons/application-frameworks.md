# 应用开发框架对比：Managed Agents、Application Components与Toolkits

本文旨在帮助开发者在百炼平台中进行技术选型，清晰区分三类核心开发范式的能力边界、适用阶段与集成成本。随着大模型应用从单次推理走向复杂工作流、从静态知识检索迈向动态智能体协作，百炼平台提供了分层演进的抽象能力：**Managed Agents** 面向高自治性、长生命周期的智能体系统；**Application Components** 聚焦可复用、可编排的数据与工程化能力底座；**Toolkits & Frameworks** 则提供轻量、标准、快速迁移的 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)层。理解三者的定位差异，是构建稳定、可维护、可扩展 AI 应用的前提。

## 关键维度对比

| 维度 | Managed Agents | Application Components | Toolkits & Frameworks |
|------|----------------|------------------------|------------------------|
| **核心定位** | 托管式智能体运行时（Agent + Environment + Session 三位一体） | 应用级基础能力组件（数据连接、知识库、Prompt 工程） | OpenAI 兼容协议工具包（标准化模型调用与扩展能力） |
| **输入格式** | 事件驱动：`POST /sessions/{id}/events`，`input` 为消息数组（含 `role`, `type`, `content`, `file_id`）；支持多模态文件引用 | RESTful 资源操作：如 `AddFile`（需 `LeaseId` + `Parser`）、`Retrieve`（`query` 文本）、`CreatePromptTemplate`（JSON 模板结构） | OpenAI 标准请求体：`messages` 数组（Chat）、`input` 字符串/数组（Embedding）、`image_url` 对象（Vision）等 |
| **输出格式** | SSE 流式事件流：含 `session_status`（`running`/`idle`/`terminated`）、`content`（文本/工具调用结果/文件引用）、`tool_calls` 等结构化事件 | 同步 JSON 响应：如 `ListIndices` 返回索引列表、`Retrieve` 返回 `chunks` 数组及 `score`、`CreateIndex` 返回 `index_id` | OpenAI 兼容响应：`chat/completions` 返回 `choices[0].message.content`；`responses` 返回带 `id`/`output`/`tool_calls` 的对象；`embeddings` 返回 `data[0].embedding` |
| **支持模型** | 仅百炼托管模型：`qwen-plus` 等（硬编码模型 ID，不支持自定义或外部模型） | **不直接调用模型**：作为数据/知识/Prompt 能力供给方，供其他模块（如 Managed Agents 或 Toolkits）消费 | 广泛支持：Qwen 全系列（`qwen3-plus`, `qwen-vl-plus`, `qwen-ocr`）、三方模型（DeepSeek, Kimi, GLM）、专用模型（`text-embedding-v4`, `qwen-coder-turbo`）；部分模型有协议限制（如 Qwen-Audio 不支持 OpenAI 协议） |
| **API 端点** | `https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`（`region` 固定为 `cn-beijing`） | `https://bailian.{region}.aliyuncs.com`（如 `bailian.cn-beijing.aliyuncs.com`），基于 ROA 签名 | `https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`（地域支持北京/新加坡/弗吉尼亚/东京/法兰克福） |
| **计费方式** | 按 **Session 运行时长** + **工具调用次数** + **文件存储（GB/天）** 计费；Agent/Environment/Skill 创建免费 | 按 **API 调用次数**（如 `Retrieve`、`SubmitIndexJob`） + **知识库存储容量（GB/月）** + **文件解析用量** 计费；无会话级资源消耗 | 按 **模型 [Token](../concepts/token.md) 消耗量**（输入+输出）计费；`files`/`batch`/`conversations` 等能力按调用次数或文件大小计费；与模型调用强绑定 |
| **状态管理** | 强状态机：Session 严格遵循 `idle → running → idle/terminated`；仅 `idle` 可接收新事件；状态变更通过 SSE 通知 | 弱状态依赖：多数操作无状态流转（如 `ListCategory`），但知识库需 `FINISH` 状态才可检索；文件需 `PARSE_SUCCESS` 才可关联索引 | 无内置会话状态：`chat/completions` 为无状态请求；`conversations` 和 `responses` 提供显式会话/上下文管理能力（`previous_response_id`, `conversation_id`） |
| **扩展性与定制** | 高定制：通过 ZIP Skill 封装自定义工具（Python/Shell），沙箱环境隔离执行；支持版本化挂载与安全扫描 | 中定制：支持自定义解析器（`Parser`）、知识库切片策略、Prompt 模板变量注入；不支持运行任意代码 | 低定制：协议层兼容，模型能力由服务端决定；可通过 `enable_thinking`、`stream_options` 等参数微调行为；不支持注入自定义工具或沙箱 |
| **典型场景** | 客服对话机器人（需多轮状态保持、调用订单查询/退款工具）、自动化数据分析助手（需执行 SQL/Python 脚本）、合规审批 Agent（需文件审核+人工介入节点） | 构建企业知识库（PDF/Excel 解析+向量化+检索）、统一 Prompt 管理中心（A/B 测试模板）、多源数据接入网关（OSS/数据库连接器） | 快速迁移现有 OpenAI 应用、批量文本生成（`completions`）、多模态理解（`vision`）、向量化服务（`embedding`）、异步批量任务（`batch`） |

## 各方案的适用场景建议

### ✅ 选择 **Managed Agents** 当：
- 你需要构建一个**具备自主决策、工具调用、状态记忆与沙箱执行能力的完整智能体**；
- 业务逻辑涉及**跨系统协同**（如调用内部 API、读写数据库、执行 Shell 命令），且要求安全隔离；
- 对**会话生命周期、错误恢复、审计追踪**有强诉求（如客服场景需记录每轮工具调用详情）；
- 团队具备 Python/Shell 工具开发能力，并愿意接受 ZIP 打包、安全扫描等额外流程；
- 模型选型可接受百炼托管模型（`qwen-plus` 等），无需接入私有或第三方模型。

> ⚠️ 注意：不适合简单问答、单次推理或需要极致低延迟的场景；不适用于需频繁切换模型或动态加载 Prompt 的轻量服务。

### ✅ 选择 **Application Components** 当：
- 你的核心需求是**构建和管理应用的数据基础设施**：例如将数百份合同 PDF 自动解析入库、为销售团队搭建专属产品知识库、统一管理营销话术 Prompt 模板；
- 需要**解耦模型调用与数据准备**：先用 `AddFile` + `SubmitIndexJob` 构建知识库，再由 Toolkits 的 `Retrieve` 或 Managed Agents 的 Skill 调用该知识库；
- 追求**细粒度权限控制与资源治理**：通过 `WorkspaceId` + RAM 策略实现数据连接器、知识库、Prompt 模板的独立授权与审计；
- 项目处于**中台化建设阶段**，目标是沉淀可复用、可编排的“能力资产”，而非单点应用。

> ⚠️ 注意：它本身**不执行模型推理**，不能直接返回答案；必须与其他模块（如 Toolkits 的 `chat/completions` 或 Managed Agents）组合使用。

### ✅ 选择 **Toolkits & Frameworks** 当：
- 你已有基于 OpenAI SDK 的代码，希望**零改造或最小改造迁移至百炼**；
- 需要**快速验证模型能力**（如测试 `qwen3-vl-plus` 的图文理解效果）或构建 MVP；
- 场景以**标准化、无状态调用为主**：批量生成报告、文档摘要、向量检索、OCR 识别、代码补全；
- 对**协议一致性、生态兼容性、开发效率**优先级高于深度定制（如不需沙箱、不需自定义工具链）；
- 需要利用百炼特有能力（如 `responses` 的自动思考链、`QVQ` 的流式视觉理解）但不想引入复杂资源模型。

> ⚠️ 注意：不适用于需要长期会话状态管理（除非显式使用 `conversations`）、复杂工具编排（需自行实现 orchestration 逻辑）或高安全沙箱执行的场景。

## 技术选型参考指南（面向开发者）

| 你的问题 | 推荐方案 | 理由简述 |
|----------|----------|----------|
| “我想把现有 ChatGPT 应用迁到百炼，改多少代码？” | ✅ Toolkits | 仅需替换 `base_url` 和 `model`，OpenAI SDK 可直接复用 |
| “我要做一个能查订单、改地址、发短信的客服机器人” | ✅ Managed Agents | 内置工具协调、沙箱执行、会话状态机，开箱即用 |
| “我们有 1000 份产品手册 PDF，想让销售随时提问获取答案” | ✅ Application Components + Toolkits | 用 Components 构建知识库，用 Toolkits 的 `Retrieve` + `chat/completions` 实现 RAG |
| “需要定时跑一批 Excel 数据，用 LLM 生成分析结论并邮件发送” | ✅ Toolkits（`batch`） | 异步批量接口天然适配定时任务，避免长连接维护 |
| “我们要统一管理所有业务线的 Prompt 模板，并支持灰度发布” | ✅ Application Components | `CreatePromptTemplate`/`UpdatePromptTemplate` 支持版本与状态管理 |
| “算法团队训练了私有模型，必须部署在 VPC 内并调用” | ❌ 三者均不直接支持 | 需使用百炼 **Model Studio 自定义模型部署** + **原生 DashScope API**，非本文范畴 |
| “用户上传图片后，既要 OCR 又要识图分类，还要生成描述” | ✅ Toolkits（`qwen-ocr` + `qwen3-vl-plus`） | 多模态模型原生支持混合输入，协议统一易编排 |

**组合使用是常态**：  
绝大多数生产级应用采用分层架构——  
🔹 **底层**：用 *Application Components* 构建知识库、管理数据连接、沉淀 Prompt；  
🔹 **中层**：用 *Toolkits* 实现模型调用、向量化、批量处理等原子能力；  
🔹 **顶层**：用 *Managed Agents* 编排上述能力，注入业务逻辑与工具链，形成端到端智能体。  

请根据当前项目阶段（PoC / MVP / Production）、团队技能栈（是否熟悉 OpenAI 生态 / 是否具备工具开发能力）、以及核心 KPI（上线速度 / 安全合规 / 可维护性）综合决策。必要时，可先用 Toolkits 快速验证，再逐步迁移到 Managed Agents 实现深度智能化。

## 被对比主题页

- [managed agents api](../api/managed-agents-api.md)
- [application component api reference](../api/application-component-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


