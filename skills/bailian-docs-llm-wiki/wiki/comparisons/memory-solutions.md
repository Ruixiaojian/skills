# [长期记忆](../concepts/long-term-memory.md)方案对比：Long Term Memory New 与 Memory Library Overview

## 对比目的与背景

百炼平台当前提供两套面向[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）能力的技术方案：**Long Term Memory New**（以下简称 *LTM New*）和 **Memory Library Overview**（以下简称 *Memory Library*）。二者名称相近、功能重叠，但定位层级、设计哲学、接口抽象程度及适用阶段存在显著差异，易导致开发者在技术选型时产生混淆。

本对比旨在厘清二者本质关系——**Memory Library 是面向业务场景的顶层能力概览与使用指南，而 LTM New 是其背后统一、标准化、可编程的底层 API 实现**。换言之，*Memory Library Overview* 是“怎么用”，*LTM New* 是“怎么写代码调用”。本文从开发者视角出发，系统梳理关键维度差异，明确各方案的适用边界与集成路径，助力高效、准确地完成技术决策与工程落地。

---

## 关键维度对比

| 维度 | Long Term Memory New | Memory Library Overview |
|------|----------------------|--------------------------|
| **定位与性质** | **底层 API 规范**：定义了 `AddMemory`/`SearchMemory` 等核心接口的精确请求结构、参数语义、错误码及行为契约，是平台级标准能力契约。 | **上层能力指南**：以用户视角组织的综合性文档，涵盖能力介绍、典型流程、插件集成（如 OpenClaw）、控制台操作指引及最佳实践，不定义具体接口细节。 |
| **输入格式** | 严格区分 `messages`（最多 50 条对话消息，支持[多模态](../concepts/multi-modal.md) content array）与 `custom_content`（≤512 字符纯文本），二者互斥必填；`messages` 中每条 `content` 超长将被截断。 | 描述更宽泛：支持“对话消息”或“直接内容”，未明确条数与长度限制；强调可通过 `autoCapture` 自动捕获，但未规定自动捕获的具体输入解析逻辑。 |
| **输出格式** | 返回结构化 JSON，含 `memory_node_id`、`content`、`timestamp`、`meta_data` 及 `score`（检索时）等字段；所有字段语义明确、类型固定，符合 OpenAPI Schema。 | 不定义具体响应体结构，仅示意性描述“返回匹配的记忆片段列表”或“返回结构化用户画像”，依赖读者跳转至底层 API 文档获取细节。 |
| **支持模型** | **无独立模型依赖**：全部能力由平台专用记忆模型（非通用大模型）统一支撑，无需用户选择或部署模型；模型能力内置于 API 行为中（如自动抽取、重排、改写）。 | 同样不暴露模型选择项，但文档中强调“基于预定义 Schema 抽取”“多轮渐进式填充”等高级语义能力，隐含对底层专用模型的调用，未说明模型可替换性。 |
| **API 端点** | 明确且唯一：<br>`POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add`<br>`POST https://dashscope.aliyuncs.com/api/v2/apps/memory/search`<br>（其他操作同理，路径统一前缀 `/api/v2/apps/memory/`） | **无独立端点**：所有 API 调用均指向同一组底层接口（即 LTM New 的端点），文档中仅给出通用示例（如 `AddMemory`），未声明专属 URL。 |
| **计费方式** | 按调用次数计费（QPM 限流体现资源消耗）：<br>- `AddMemory`：计入写入调用量<br>- `SearchMemory`：计入检索调用量<br>费用归属 `DASHSCOPE_API_KEY` 所属阿里云账号。 | **不涉及计费逻辑**：作为能力概览文档，不描述计费模型；实际计费完全由底层 LTM New API 调用触发并计量。 |
| **典型场景** | - 需精细控制记忆生命周期（如按业务事件主动 `UpdateMemory`）<br>- 要求高确定性输入/输出（如金融、医疗类强合规场景）<br>- 集成至自研 Agent 框架，需异步/流式处理响应<br>- 需启用 `enable_rerank`/`enable_judge` 等高级搜索开关 | - 快速验证[长期记忆](../concepts/long-term-memory.md)效果（通过控制台或 OpenClaw 插件）<br>- 构建低代码/无代码智能体（依赖 `autoCapture`/`autoRecall` 自动化）<br>- 多应用共享同一记忆库，关注数据隔离而非接口细节<br>- 用户画像驱动的个性化服务（如电商推荐、客服知识库） |
| **SDK 支持** | 提供 `agentscope-runtime>=1.1.5` 官方 SDK 封装（`AddMemory`, `SearchMemory`, `ListMemory`），但 `UpdateMemory` 需直调 HTTP；Python 示例与文档存在细微不一致，**以 API 参考文档为准**。 | 未提供独立 SDK；OpenClaw 插件封装了完整记忆流程（`memory_store`, `memory_search` 工具），但属于框架层抽象，非通用 SDK。 |
| **扩展性与定制** | 高：支持 `profile_schema_id` 显式绑定画像模板；`meta_data` 支持任意业务键值；`custom_content` 允许绕过对话解析直接注入结构化文本。 | 中：通过 `profile_schema` 参数支持画像抽取，但未暴露 `enable_*` 类高级搜索开关；强调“双模态接入”，但未说明如何定制[多模态](../concepts/multi-modal.md)解析逻辑。 |

---

## 各方案的适用场景建议

### ✅ 推荐选用 **Long Term Memory New** 当：
- 你正在开发一个**高度定制化的智能体（Agent）**，需要精确控制记忆的写入时机、内容结构、检索策略（如强制启用重排或语义改写）；
- 你的应用对**数据一致性、可追溯性、错误处理**有严格要求（例如需记录 `request_id` 进行审计，或需根据 `code` 字段做精细化降级）；
- 你已具备成熟的 Python/Node.js 工程栈，希望**直接集成标准 REST API 或官方 SDK**，避免中间层抽象带来的黑盒风险；
- 你需要构建**跨平台、跨语言的通用记忆适配器**，要求接口契约稳定、文档完备、行为可预测。

### ✅ 推荐参考 **Memory Library Overview** 当：
- 你是**产品负责人、解决方案架构师或初级开发者**，目标是快速理解“长期记忆能做什么”，评估是否满足业务需求；
- 你计划使用 **OpenClaw 等百炼官方 Agent 框架**，希望利用 `autoCapture`/`autoRecall` 插件实现“零代码”记忆接入；
- 你需要在**控制台可视化管理记忆库、规则、画像 Schema**，或协调多个应用共享同一记忆空间；
- 你正在编写面向业务方的**技术方案书或用户操作手册**，需用通俗语言解释能力价值，而非技术实现细节。

> ⚠️ 重要提示：二者**不是互斥选项，而是协同关系**。  
> **Memory Library Overview 是 LTM New 的“说明书”与“快捷入口”，LTM New 是 Memory Library Overview 的“引擎”与“执行标准”**。  
> 实际项目中，通常先通过 Memory Library Overview 快速验证能力，再基于 LTM New API 进行生产级集成。

---

## 面向开发者的技术选型参考

| 选型考量 | 建议动作 |
|----------|----------|
| **首次接入？想快速验证效果？** | ✅ 优先阅读 *Memory Library Overview*，在控制台创建记忆库 → 启用 OpenClaw 插件 → 观察自动捕获效果；无需写一行代码即可验证核心价值。 |
| **进入开发阶段？需对接自有 Agent？** | ✅ 立即切换至 *LTM New* 文档，精读 [API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)，确认 `user_id` 隔离策略、`top_k`/`min_score` 默认值、错误响应格式等关键契约。 |
| **是否必须用 SDK？** | ✅ 若使用 Python 且接受 `UpdateMemory` 需手动调用，推荐 `agentscope-runtime>=1.1.5`；否则建议直接使用 `requests`/`fetch` 调用标准 REST API，避免 SDK 版本滞后风险。 |
| **如何处理[多模态](../concepts/multi-modal.md)？** | ⚠️ 二者均声明支持多模态 `messages.content`（含 `image_url`），但**当前仅对文本内容进行语义解析**。图像内容不会被提取为记忆，仅作元数据存储。若需图像理解，请另行调用多模态大模型 API。 |
| **如何管理记忆生命周期？** | ⚠️ **二者均不提供自动过期机制**。文档中提及的“默认规则有效期 180 天”仅为规则配置项，**不触发物理删除**。业务方必须自行实现定时清理（如通过 `ListMemory` + `DeleteMemory`）或设计 TTL 元数据字段。 |
| **遇到问题如何排查？** | ✅ 无论通过哪种文档接入，**所有请求均返回 `request_id`**。务必在日志中记录该 ID，并在提工单时提供，这是平台侧定位问题的唯一依据。 |

--- 

> **最后提醒**：百炼平台的长期记忆能力持续演进。`LTM New` 是当前主推的标准化接口，`Memory Library Overview` 将随其迭代同步更新。请始终以 [LTM New API 参考文档](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 为最终权威依据，其他文档均为辅助性解读。

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)


