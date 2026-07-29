# Prompt 工程

Prompt 工程是指在百炼平台上系统性设计、组织、验证与优化提示词（Prompt）的方法论与实践体系，其目标是通过结构化指令、角色设定、上下文注入、样例引导和自动化反馈等手段，显著提升大模型输出的准确性、稳定性、格式一致性与业务适配性。

## 在百炼平台的不同场景中，这个概念如何使用

- **模板化 Prompt 管理**：在「组件管理 > 提示词」中，开发者可基于 ICIO（Input-Context-Instruction-Output）、CRISPE（Capacity-Role-Insight-Statement-Personality-Experiment）或 RASCEF（Role-Action-Steps-Constraints-Examples-Format）等工程框架创建可复用模板；支持 `${variable}` 变量插值，实现跨业务动态填充（如营销文案生成、日志分析摘要），适用于文本生成、图片生成（正向/负向 Prompt 分离配置）等标准化任务。

- **智能体（LLM Application）构建**：在新版智能体（Agent 2.0）中，系统提示词（System Prompt）是 Prompt 工程的核心载体——它定义 Agent 的角色、能力边界、工具调用规范及输出格式约束。结合知识库（RAG）与 MCP 工具，Prompt 工程确保模型在多步推理中保持意图对齐与结构化响应（如始终以 JSON 输出订单状态）。

- **自动增强与反馈优化**：  
  - **自动优化**：无需人工经验，一键将原始自然语言 Prompt（如“帮我写个产品介绍”）转化为含角色注入、指令强化、安全护栏的工业级版本；不计费，且输入数据不用于训练。  
  - **反馈优化**：面向分类、结构化抽取等高精度任务，上传 5–10 条典型样例（few-shot）与 ≥20 条评测集，平台通过多轮评估-反思-重写，产出业务效果更优的 Prompt，直接支持 A/B 测试与灰度发布。

- **API 与 SDK 集成**：通过 `CreatePromptTemplate` / `GetPromptTemplate` 接口管理模板元数据；渲染后作为 `system` 或 `messages[0].content` 传入 `ChatCompletion` 等模型 API；SDK 自动处理变量注入与地域适配（仅华北2可用），开发者聚焦业务逻辑。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `promptTemplateId` | 模板唯一标识符 | 由平台生成，用于 API 获取模板内容 |
| `workspaceId` | 业务空间 ID | 必填，控制台或 `ListWorkspaces` 接口获取，决定资源隔离与鉴权范围 |
| `variables` | 模板中声明的变量名列表（JSON 数组） | 最多 64 个；语法为 `${topic}`，不支持嵌套或表达式 |
| `enable_thinking`（智能体场景） | 启用规划-执行-反思链路 | 仅对千问-Max 等支持思考模式的模型生效，用于调试 Prompt 效果 |
| `top_k` / `score_threshold`（RAG 场景） | 控制检索片段数量与相关性阈值 | 影响 Prompt 中注入的上下文质量，间接决定最终输出可靠性 |

> ⚠️ **重要限制**：  
> - 所有 Prompt 功能**仅支持华北2（北京）地域**；  
> - 控制台编辑器最大长度 **6144 字符**，实际 token 消耗需按所选模型上下文窗口（如 Qwen-Max 32K）自行校验；  
> - 图片生成模板暂不支持通过 API 创建（`CreatePromptTemplate` 接口当前仅支持文本类）；  
> - Prompt 自动优化与反馈优化过程中的用户数据**不存储、不训练、符合阿里云隐私政策**。

## 面向开发者，简洁实用

- ✅ **起步建议**：从预置模板（如“会议纪要生成”）开始，复制后修改变量与指令细节，比从零编写更高效；  
- ✅ **调试技巧**：启用 `enable_thinking=True` + `stream=True`，实时观察模型如何解析 Prompt 并规划步骤；  
- ✅ **生产最佳实践**：  
  - 对关键业务 Prompt，用反馈优化生成多个候选版本，结合线上评测集（如准确率、格式合规率）择优部署；  
  - 将 Prompt 模板 ID 与变量映射关系纳入配置中心管理，避免硬编码；  
  - 监控 `input_tokens` 增长——优化后的 Prompt 若引入大量样例或知识片段，可能推高成本，需权衡效果与开销。  
- ❌ **避免踩坑**：勿依赖已下线的 Prompt 样例库功能；新项目统一使用 RAG 表格库或反馈优化替代。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [application component api reference](../api/application-component-api-reference.md)
- [application support](../guides/application-support.md)


