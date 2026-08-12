# application evaluation

百炼平台的应用评测能力提供自动与手动两种评测路径，支持对智能体/工作流应用的输出质量进行系统化、多维度评估。核心能力包括：基于知识库自动生成评测集的自动评测、支持人工打标的手动评测、可灵活扩展的评测集类型、可复用的评估器（Grader）体系，以及面向业务场景的标签管理体系。评测结果可用于归因分析、调优建议生成和持续质量监控。

## 支持的模型/功能

- **自动评测**：依赖大模型（当前仅支持 `qwen-max` 和 `qwen-plus`）自动生成评测集并执行评分，适用于已发布且配置知识库的智能体应用 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **手动评测**：支持人工构建评测集（XLS/XLSX 格式），通过人工打标（如“较差/一般/较好”）产出评测报告，适用于需强主观判断或无标准答案的场景 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。  
- **新版评测体系**：支持三种评测集类型——**智能体**、**工作流**和**自定义**，并引入**评估器（Grader）** 与**标签（Label）** 两大核心组件，实现自动评分（LLM/Code）与人工标注协同 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。  
- **评估器类型**：  
  - *LLM评估器*：使用大模型语义理解进行评分，适用于相关性、幻觉、有害性等复杂判断；  
  - *Code评估器*：通过Python脚本执行精确规则校验（如JSON格式、关键词匹配），零[Token](../concepts/token.md)成本；  
  - *预置模板*：覆盖通用质量、智能体能力、文本匹配、相似度、格式校验等场景 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。  

> **注意**：文档1中明确限定自动评测仅支持 `qwen-max`/`qwen-plus`，而文档7中LLM评估器创建时注明“评估模型限时免费”，未限定具体型号；实际使用中应以控制台可用模型列表为准，避免因模型不可用导致评测失败。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **评测集** | `query` / `referenceAnswer` / `fineKeywords` / `coarseKeywords` | 知识问答型评测集必需字段，用于自动评分依据；`fineKeywords`为嵌套数组格式，`coarseKeywords`为1–3个主题词 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md) |
| **评测规则** | 分类采样数、评测模型、权重配置 | 自动评测中需为每类任务（事实型/分析型等）指定采样数量；权重影响最终综合得分计算 |
| **评估器** | 评分范围（如0–1、1–5）、通过阈值、参数映射 | 必须完成所有变量映射（如`query`→评测集`Prompt`字段）才能保存评测任务；评分范围需与Prompt逻辑一致 |
| **标签** | 类型（分类/布尔/数字/文本）、筛选项、标注方式 | 分类标签最多20个选项；布尔标签固定True/False；数字标签支持Double型输入；文本标签上限200字符 |

## 使用方式

1. **准备数据基础**：  
   - 创建并**发布**评测集（支持`.jsonl`知识问答、`.xls/.xlsx`对话分析，或新版智能体/工作流/自定义类型）；  
   - （可选）提前创建评估器与标签，便于后续任务复用。  

2. **创建评测任务**：  
   - *自动评测*：进入[自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)界面 → 选择已发布智能体 + 公共知识库 → 生成/选用评测集 → 配置采样与模型 → 发起评测；  
   - *新版评测任务*：选择“智能体”或“工作流”关联方式 → 绑定已发布评测集 → 添加1–10个评估器（需完成全部参数映射）→ 添加标签 → 完成创建；  
   - *手动评测*：上传XLS/XLSX评测集 → 在手动评测页选择应用与评测集 → 启动后逐条人工打标。  

3. **执行与分析**：  
   - 自动评测任务状态为“评测中(X%)”，完成后查看BadCase归因（如“检索无效”“切片不完整”）及调优建议；  
   - 新版评测任务在“数据明细”页支持**快速标注**（下拉/输入即存）与**指标统计**（各评估器通过率、标签分布）；  
   - 所有任务支持导出结果，用于离线分析或CI/CD集成。

## 限制和注意事项

- **应用前提**：自动评测要求应用**已发布**、**配置知识库**、**开通应用观测**，且子账号需具备`应用评测-操作`权限 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **数量限制**：单次自动评测最多支持8个应用横向对比；每个评测任务最多添加10个评估器；单个评测集文件≤20MB，单次上传≤10个文件。  
- **评测集兼容性**：  
  - 自动评测仅接受`.jsonl`格式的**知识问答型**评测集；  
  - 手动评测仅接受`.xls/.xlsx`格式的**对话分析型**评测集；  
  - 新版评测集类型（智能体/工作流/自定义）与旧版不互通，迁移需重新构建。  
- **费用与消耗**：  
  - 自动评测与LLM评估器调用均产生[Token](../concepts/token.md)费用，预估消耗仅为参考，以实际账单为准；  
  - Code评估器无额外[Token](../concepts/token.md)成本；  
  - 评测任务发起后配置不可修改，如需调整需新建任务。  
- **版本管理**：评测集支持版本发布，创建任务时可指定使用特定版本；评估器支持历史版本回溯与覆盖。  
- **关键风险**：  
  > **注意**：文档4（新版评测集）与文档3（旧版评测集）对评测集类型的定义存在根本差异——旧版仅分“对话分析”与“知识问答”，新版则按应用形态划分为“智能体/工作流/自定义”。二者属不同技术栈，**不可混用**。旧版自动评测流程（文档1）与新版评测任务（文档6）为并行能力，开发者需根据控制台实际入口选择对应路径，避免因类型错配导致任务失败。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


