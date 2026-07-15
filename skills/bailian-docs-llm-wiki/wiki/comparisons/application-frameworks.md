# 应用开发框架对比：Managed Agents、Application Component 与 Toolkits

## 对比目的与背景

在百炼平台构建 AI 应用时，开发者面临多种技术路径选择：是直接调用模型能力快速验证想法？还是构建可复用、可审计的智能体系统？抑或集成知识库与数据连接能力打造企业级应用？`Managed Agents`、`Application Component` 和 `Toolkits` 是百炼平台面向不同抽象层级提供的三类核心开发框架，分别聚焦于**智能体生命周期管理**、**数据与知识基础设施编排**、以及**标准化模型能力接入**。本页旨在从技术定位、能力边界、使用约束和工程实践角度进行客观对比，帮助开发者基于业务目标、团队能力与运维要求做出理性选型决策。

---

## 关键维度对比表

| 维度 | Managed Agents | Application Component | Toolkits（[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)） |
|------|----------------|------------------------|------------------------------|
| **核心定位** | 托管式智能体运行时：统一管理会话、沙箱、工具链与事件流 | 数据与知识基础设施 API：聚焦数据连接、知识库构建、解析配置与元数据管理 | 标准化模型能力网关：提供 OpenAI 兼容协议，屏蔽底层模型差异，支持快速迁移与多模态调用 |
| **输入格式** | 结构化 JSON Event 消息数组（含 `role`/`type`/`content`），严格遵循 Session Schema；支持文本、图像 URL、文件引用（需预上传并审核通过） | 多样化资源操作请求：<br>• 文件：`AddFile` + `Parser` 指定解析器<br>• 知识库：`CreateIndex` + `SubmitIndexJob`<br>• 类目/连接器：ROA 风格参数（如 `CategoryId`, `IndexId`, `FileType`） | OpenAI 标准 REST 请求体：<br>• Chat：`messages: [{role, content}]`<br>• Vision：`messages` + `image_url` 或 `base64_image`<br>• Embedding：`input: string/array`<br>• Files：`file` + `purpose`（必填） |
| **输出格式** | SSE 流式事件（`message`, `session_status`, `tool_call` 等）或轮询历史事件；响应结构含 `event_id`, `session_id`, `output`（含 `text`, `tool_calls`, `files` 等） | ROA 风格 JSON 响应：<br>• 创建类：返回 `ResourceId`（如 `FileId`, `IndexId`）<br>• 查询类：返回完整资源对象（含状态、统计、元数据）<br>• 检索类（`Retrieve`）：返回 `chunks` 数组及 `score` | OpenAI 兼容 JSON：<br>• Chat/Responses：`choices[0].message.content` / `output_text`<br>• Embedding：`data[0].embedding`<br>• Vision：`choices[0].message.content` 或 `data[0].url`（QVQ 流式）<br>• Batch：异步 `id` + 回调通知 |
| **支持模型** | 仅百炼托管大模型（当前限 `qwen-plus` 等），模型 ID 必须为对象 `{"id": "qwen-plus"}`；不支持自定义/外部模型 | **不直接调用模型**；为模型调用提供数据支撑（如知识库检索结果作为 RAG 上下文） | 广泛支持：`qwen-plus`, `qwen3-*`, `Qwen-VL`, `QVQ`, `Qwen-OCR`, `text-embedding-v*`, `qwen-coder-turbo` 等；按接口能力隔离（如 Completions 仅支持 `qwen-coder-turbo`） |
| **API 端点** | `https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio`（如 `ws_abc.cn-beijing.maas.aliyuncs.com`） | `bailian.{region}.aliyuncs.com`（公网）或 `bailian-vpc.{region}.aliyuncs.com`（VPC）；需显式指定 `WorkspaceId` 路径参数 | 多域名策略：<br>• Chat/Vision/Embedding：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`<br>• Files/Batch（文件）：`https://dashscope.aliyuncs.com/compatible-mode/v1`（中国内地）<br>• **Batch Chat（专用）：`https://batch.dashscope.aliyuncs.com/compatible-mode/v1`** |
| **认证方式** | Bearer [Token](../concepts/token.md)（`Authorization: Bearer <api_key>`），API Key 与工作空间强绑定 | RAM AccessKey 签名（ROA），需最小权限策略（如 `AliyunBailianDataFullAccess`） | Bearer [Token](../concepts/token.md)（`Authorization: Bearer <api_key>`），**API Key 必须与 endpoint 地域一致**（北京 Key 不能用于新加坡 endpoint） |
| **计费方式** | 按 Session 运行时长（秒）+ 工具调用次数 + 文件存储（GB/月）计费；沙箱资源消耗计入 Session 成本 | 按调用次数（QPS）+ 知识库存储（GB/月）+ 文件解析/切片处理量计费；无模型推理费用（仅为数据层） | 按模型调用 token 数（输入+输出）计费；Batch 享 5 折优惠；Files 上传免费，用途相关（如 `fine-tune` 有额外费用） |
| **典型场景** | • 可复用客服智能体（带审批流、多工具协同）<br>• 合规审计型业务助手（完整事件溯源、版本快照）<br>• 需沙箱隔离的代码执行/文件分析任务 | • 构建企业级知识库（PDF/Word/Excel 自动入库+切片）<br>• 管理多源数据连接（OSS、数据库类目）<br>• 定制化文档解析策略（如合同关键字段提取） | • 快速迁移 OpenAI 应用（零代码修改）<br>• 多模态应用（图文理解、OCR、向量化）<br>• 批量推理任务（日志分析、报告生成） |

---

## 各方案适用场景建议

### ✅ 优先选用 **Managed Agents**
- 需要**端到端智能体生命周期管理**：如会话状态机（`idle`→`running`→`terminated`）、中断恢复、工具调用审批、事件流订阅。
- 要求**强安全与合规控制**：沙箱环境隔离、Skill ZIP 包安全扫描、文件审核机制、版本锁定（禁止 `latest`）。
- 构建**可复用、可归档、可审计**的智能体资产：Agent 版本化、Environment 复用、Session 快照追溯。
- 场景示例：金融理财顾问（需风控工具调用+会话留痕）、HR 招聘助手（简历解析+面试问答+合规提示）。

### ✅ 优先选用 **Application Component**
- 核心需求是**数据与知识基础设施建设**：如将数百份 PDF 合同自动构建知识库、对接内部 OSS 存储、定制化解析规则。
- 需要**精细化管理知识库元数据**：如按部门/项目分类管理 Index、动态追加文档、删除错误切片、监控索引质量。
- 业务逻辑依赖**结构化数据连接**：如将 CRM 表格数据作为 RAG 上下文源（注意：`AddTable` 为受限功能，推荐控制台操作）。
- 场景示例：法务合同审查系统（OSS 批量导入+法律条款切片+高精度检索）、产品文档中心（多格式解析+版本化更新）。

### ✅ 优先选用 **Toolkits（[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)）**
- 追求**开发效率与生态兼容性**：已有 OpenAI SDK 代码，希望最小改动接入百炼模型。
- 需要**灵活组合多模态能力**：如同时调用 `Chat`（对话）、`Vision`（图片理解）、`Embedding`（向量检索）构建多阶段流水线。
- 执行**大规模批量任务**：如每日 10 万条用户反馈情感分析（Batch Chat 5 折）、千万级文本向量化（Embedding Batch）。
- 场景示例：SaaS 客户支持[插件](../concepts/plugin.md)（OpenAI SDK 直接切换 endpoint）、电商商品图搜系统（Qwen-VL + Embedding）、AI 写作助手（qwen3.7-plus + qwen-coder-turbo 协同）。

---

## 技术选型参考指南（面向开发者）

| 选型考量因素 | 推荐方案 | 说明 |
|--------------|----------|------|
| **是否需要模型推理以外的能力（如知识库、文件解析）？** | → 若需：**Application Component**<br>→ 若仅需模型调用：继续评估 | Application Component 是数据层基石，Toolkits/Managed Agents 均可消费其产出（如知识库检索结果传入 Agent 的 `input`）。 |
| **是否必须保证会话状态一致性与工具链可审计？** | → 是：**Managed Agents**<br>→ 否：考虑 Toolkits | Managed Agents 提供唯一具备完整状态机与事件溯源的框架；Toolkits 的 `Conversations` 仅提供轻量会话 ID 管理，无状态持久化保障。 |
| **团队是否已使用 OpenAI 生态（SDK、Prompt 工程规范）？** | → 是：**Toolkits**（首选）<br>→ 否：评估学习成本 | Toolkits 最小化迁移成本；Managed Agents 需理解 Agent/Environment/Session 三层抽象；Application Component 需熟悉 ROA 签名与资源生命周期。 |
| **是否涉及敏感数据处理（如客户隐私文件）？** | → 是：**Managed Agents**（沙箱隔离）或 **Application Component**（私有 VPC endpoint）<br>→ 否：均可 | Managed Agents 的 `cloud` 沙箱提供进程级隔离；Application Component 支持 VPC endpoint 避免公网传输；Toolkits 默认走公网（需确认合规策略）。 |
| **是否需要未来扩展自定义模型或外部服务集成？** | → 是：**Toolkits**（开放模型列表）或 **Application Component + 自研服务**<br>→ 否：Managed Agents 更省心 | Managed Agents 当前**不支持自定义模型**；Toolkits 持续扩展模型支持；Application Component 可通过连接器对接自研服务。 |
| **运维复杂度要求（CI/CD、监控、告警）？** | → 低：**Toolkits**（标准 HTTP 接口）<br>→ 中：**Application Component**（需管理 Index/Category 状态）<br>→ 高：**Managed Agents**（需监控 Session 状态机、Skill 安全扫描、文件审核） | Toolkits 接口行为最接近传统 REST；Managed Agents 引入更多异步状态（如 `session_status` 变更），需适配 SSE 或轮询。 |

> **联合使用建议**：实际生产中三者常组合使用——  
> **Application Component** 构建知识库 → 输出 `IndexId` 与检索结果；  
> **Toolkits**（`Embedding` + `Retrieve`）实现快速原型验证；  
> **Managed Agents** 封装最终交付形态，将知识库检索结果、工具调用、用户会话统一编排为可发布智能体。  
> 此分层架构兼顾敏捷性、可维护性与企业级治理要求。

## 被对比主题页

- [managed agents api](../api/managed-agents-api.md)
- [application component api reference](../api/application-component-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


