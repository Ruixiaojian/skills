# Prompt 工程

Prompt 工程是百炼平台上系统化设计、管理与优化提示词（Prompt）的方法论与技术实践，旨在通过结构化模板、数据驱动优化和可复用配置，将业务意图精准转化为大模型的稳定、可控、可评估输出。它不是一次性指令编写，而是涵盖定义、测试、迭代、部署全生命周期的工程化能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **模板化复用**：在「组件管理 > 提示词」中创建文本生成类 Prompt 模板（支持 `qwen3.7-plus` 等主流文本模型），使用 `${variable}` 占位符实现动态注入（如 `${product_name}`、`${tone}`），配合 ICIO/CRISPE/RASCEF 等框架规范提示结构，确保跨应用一致性和可维护性。

- **智能体（Agent 2.0）与工作流编排**：系统提示词（System Prompt）作为智能体的核心“角色设定”，直接影响其规划、工具调用与反思行为；工作流中的大模型节点也支持直接引用已发布 Prompt 模板 ID，避免硬编码，提升流程可读性与版本管理能力。

- **反馈驱动优化（推荐路径）**：针对关键业务场景（如客服问答、营销文案生成），在控制台「提示词 > 反馈优化」中上传初始 Prompt + 5–10 条高质量样例（覆盖典型输入类别）+ ≥20 条评测数据集，平台自动执行多轮评估-反思-重写闭环，生成效果更优、鲁棒性更强的新 Prompt，并支持一键保存为模板复用。

- **API 集成调用**：通过 `GetPromptTemplate` 接口（需 `workspaceId` 和 `promptTemplateId`）获取模板内容，运行时填充 `variables` 后，作为 `input.messages[0].content` 传入目标模型 API（如 `qwen3.7-plus`），实现服务端 Prompt 动态组装与下发。

> ⚠️ 注意：Prompt 样例库（Few-shot 样例注入）功能**已正式下线**，不再维护。请勿在新项目中依赖该能力；历史存量应用须按指引迁移至 RAG 表格库实现上下文增强。

## 关键参数和配置

| 参数 | 说明 | 使用建议 |
|------|------|----------|
| `workspaceId` | 所有 Prompt 相关操作的必需路径参数，标识业务空间隔离边界 | 必须提前在控制台或通过 API 获取，格式如 `llm-3z7uw7fwz0vexxxx` |
| `promptTemplateId` | 模板唯一标识符，用于 `GetPromptTemplate` 接口精确拉取 | 创建模板后自动生成，建议在代码中常量管理或配置中心存储 |
| `variables` | 运行时需填充的变量列表（JSON 数组），如 `["topic", "audience", "length"]` | 填充前务必校验字段完整性，缺失变量会导致模板渲染失败 |
| 模板长度上限 | 控制台编辑器最大支持 **6144 字符**（含占位符） | 超长 Prompt 建议拆分为系统提示 + 用户输入 + RAG 检索片段组合方式 |
| 地域约束 | **仅支持华北2（北京）地域**（`cn-beijing`） | SDK 或 API 调用必须指定对应 endpoint：`bailian.cn-beijing.aliyuncs.com` |

## 面向开发者，简洁实用

- ✅ **优先使用反馈优化**：相比纯文本自动优化，反馈优化基于真实样例与评测数据，效果更可靠；投入少量高质量数据即可获得显著提升。
- ✅ **模板即代码**：将 Prompt 模板视为基础设施代码，纳入 CI/CD 流程——例如通过 `CreatePromptTemplate` API 自动化部署，配合 Git 版本管理。
- ✅ **解耦提示与模型调用**：永远通过 `GetPromptTemplate` 获取内容并动态填充，避免在业务代码中拼接字符串或硬编码提示逻辑。
- ❌ **禁用已弃用功能**：`has_thoughts=true`、样例库关联、召回片段数配置等均属下线能力，SDK 中无需预留兼容逻辑。
- 🔒 **安全合规**：Prompt 自动优化过程不存储用户输入，但反馈优化任务中上传的样例与评测数据属于业务敏感信息，请确保符合内部数据治理要求。

> 提示词不是魔法咒语，而是可测试、可度量、可迭代的软件资产。在百炼平台，把它当作一个需要单元测试（评测集）、版本控制（模板ID）、灰度发布（A/B测试不同模板）的核心组件来对待。

## 关联主题页

- [prompt](../guides/prompt.md)
- [application component api reference](../api/application-component-api-reference.md)
- [llm application](../guides/llm-application.md)
- [model experience](../guides/model-experience.md)


