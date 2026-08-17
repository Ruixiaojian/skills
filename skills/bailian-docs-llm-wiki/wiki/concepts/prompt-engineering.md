# Prompt 工程

Prompt 工程是百炼平台中系统化设计、管理与优化大模型输入指令（Prompt）的方法论与技术实践，旨在通过结构化模板、样例驱动和自动化迭代等手段，将模糊的业务意图稳定、可复现地转化为高质量模型输出。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent 2.0）应用**：System Prompt 是核心控制入口，定义角色、任务边界与约束；支持变量插值（如 `${query}`）与 Few-shot 样例注入（需迁移至 RAG 表格库），直接影响规划、工具调用与知识检索行为。  
- **工作流（Workflow）应用**：大模型节点支持独立配置 Prompt 模板（文本生成类），可绑定变量（如 `${sys.query}`）、启用 ICIO/CRISPE 等结构化框架，并与上下文变量、历史对话联动，实现确定性流程中的精准输出控制。  
- **高代码应用**：开发者可通过 API 动态加载 `GetPromptTemplate` 返回的模板内容，在 Python 服务中完成变量渲染与参数组装，再传入模型推理接口，实现 Prompt 与业务逻辑的深度耦合。  
- **[多模态](multi-modal.md)生成任务**：图片生成类 Prompt 模板严格区分正向 Prompt（描述应呈现的内容）与负向 Prompt（排除不期望元素），二者分别计长且均支持变量插值与结构化提示词框架。  
- **评估与调优闭环**：Prompt 工程与 `application evaluation` 深度协同——反馈优化依赖评测集（≥20 条）与样例集（5–10 条）驱动多轮反思生成；自动评测结果（如“检索无效”“指令歧义”）直接反哺 Prompt 结构重构建议。

> ⚠️ 注意：Prompt 样例库功能已正式下线，所有存量样例请迁移至 RAG 表格库；不再支持通过 API 创建文生图 Prompt 模板。

## 关键参数和配置

| 参数 | 说明 | 约束与建议 | 使用位置 |
|------|------|-------------|-----------|
| `promptTemplateId` | 模板唯一标识符 | 字符串，长度无显式限制；用于 API 调用与控制台引用 | 所有模板操作（创建/获取/调用） |
| `workspaceId` | 业务空间 ID | 必填；所有 Prompt 操作均需绑定该上下文 | 控制台与 API 全局必需 |
| `type` | 模板类型 | `TEXT_GENERATION`（默认）或 `IMAGE_GENERATION`；后者需在控制台显式选择 | `CreatePromptTemplate` API / 控制台创建页 |
| 模板内容长度 | `content` 字段总字符数 | ≤ 6144 字符；图片生成模板中正向/负向 Prompt 分别计长 | 控制台编辑器实时校验 / API 请求校验 |
| 变量语法 | 运行时插值占位符 | `${variableName}`；变量名需在调用时通过 `variables` 对象传入（如 `{"topic": "AI安全"}`） | 模板内容中任意位置 / API `variables` 字段 |
| 样例集规模（反馈优化） | 输入-输出对数量 | 建议 5–10 条，覆盖典型场景与边界 case | 反馈优化任务上传文件 |
| 评测集规模（反馈优化） | 用于评估优化效果的测试样本 | 建议 ≥20 条，含多样性 query 与标准答案 | 反馈优化任务上传文件 |

## 面向开发者，简洁实用

- ✅ **优先用模板，而非硬编码 Prompt**：通过 `CreatePromptTemplate` API 或控制台创建可复用模板，避免在代码中拼接字符串；变量插值能力天然支持多环境（dev/staging/prod）差异化配置。  
- ✅ **文本生成模板推荐结构化框架**：在控制台选择“基于 Prompt 工程创建”，快速套用 ICIO（Input-Context-Instruction-Output）、CRISPE（Capacity-Roles-Insight-Statement-Personality-Experiment）等模板，提升指令清晰度与鲁棒性。  
- ✅ **图片生成务必分离正负向 Prompt**：正向描述主体、风格、构图；负向明确排除模糊、畸变、水印等干扰项；二者均支持 `${}` 变量，但不可混用在同一字段。  
- ✅ **反馈优化是生产级调优首选**：比单次自动优化更可靠——上传真实业务样例（5–10 条）+ 评测集（≥20 条），启动后平台返回多个候选 Prompt，支持人工筛选与 A/B 测试。  
- ❌ **不要依赖已下线能力**：`Prompt 样例库` 已停用；`API 创建图片生成模板` 暂不支持；跨地域（非华北2）调用 Prompt 接口将失败。  
- 📌 **调试技巧**：在智能体/工作流的“文本对话体验”面板中，开启「显示完整 Prompt」开关，可实时查看变量渲染后的最终输入，快速定位插值错误或长度截断问题。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [application component api reference](../api/application-component-api-reference.md)
- [start using](../guides/start-using.md)
- [application evaluation](../guides/application-evaluation.md)


