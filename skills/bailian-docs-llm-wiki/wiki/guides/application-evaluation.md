# application evaluation

应用评测是百炼平台中用于系统化评估智能体/工作流应用输出质量的核心能力，支持自动与人工双路径评测机制。通过评测集驱动、多维度评估器打分、人工标签补充及归因分析，开发者可快速定位 RAG 流程瓶颈（如检索失效、切片不完整、模型理解偏差等），形成“评测→归因→优化→再验证”的闭环。该能力深度集成于应用观测体系，要求应用已发布且观测功能已开通。

## 支持的模型/功能

- **自动评测**：基于知识库自动生成评测集，调用 `qwen-max` 或 `qwen-plus` 模型完成端到端评分与归因分析，适用于单应用深度诊断或多应用横向对比（最多 8 个）[自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **手动评测**：支持人工构建 `.xls`/`.xlsx` 格式对话分析评测集，通过人工打标（如“较差/一般/较好”）产出定性报告，适用于业务逻辑复杂、需专家判断的场景 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。  
- **新版评测体系**：引入结构化评测集类型（智能体/工作流/自定义）、可复用评估器（LLM/Code/基于任务生成）及灵活标签体系（分类/布尔/数字/文本），支持混合自动评分与人工标注的精细化评测 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。  
- **评估器**：提供预置模板（通用质量、智能体、文本匹配等）及自定义能力，LLM 评估器依赖大模型语义理解，Code 评估器通过 Python 脚本实现确定性规则校验 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。  

> **注意**：文档 3 与文档 4 对评测集类型的定义存在差异——文档 3 将评测集分为“对话分析”和“知识问答”两类，而文档 4 新增“智能体”“工作流”“自定义”三类并强调类型创建后不可修改。实际使用应以新版控制台为准（即文档 4 和文档 5），旧版“知识问答”对应新版“智能体”类型，“对话分析”可通过“自定义”类型实现。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **评测集类型** | 决定数据结构与适用场景：`智能体`（适配智能体出入参）、`工作流`（适配工作流节点）、`自定义`（任意字段） | 创建后不可修改；旧版“知识问答”需迁移至“智能体”类型 |
| **评估器参数映射** | 将评估器变量（如 `query`, `response`, `referenceAnswer`）绑定至评测集字段或应用输出 | 所有变量必须完成映射方可保存评测任务；映射错误将导致评分失败 |
| **采样配置** | 自动评测中按任务类型（事实型/分析型/比较型/教程型）设置分类采样数，控制评测规模 | 单应用评测总样本数 = 各类型采样数之和；多应用评测共享同一采样策略 |
| **评分范围与阈值** | LLM/Code 评估器需配置 `评分范围`（如 0–1、1–5）和 `通过阈值`（如 ≥4.0 为 Pass） | 阈值建议设为范围中位数；范围越大，区分度越高但成本可能上升 |

## 使用方式

1. **准备数据**：  
   - 若用自动评测，确保应用已发布、关联知识库、开通应用观测；  
   - 若用手动/新版评测，先创建评测集：上传 `.jsonl`（知识问答）、`.xls`/`.xlsx`（对话分析）或通过“智能体/工作流”类型自动生成模板 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)；  
   - 发布评测集（草稿状态不可用于评测）。  

2. **创建评测任务**：  
   - **自动评测**：在控制台选择应用→知识库→生成评测集（仅 `qwen-max`/`qwen-plus`）→配置采样与模型→发起评测；  
   - **新版评测**：选择评测集+应用（智能体/工作流/不关联）→添加评估器（最多 10 个）并完成参数映射→配置标签→创建任务；  
   - **手动评测**：选择已发布评测集→选择应用→进入标注界面逐条打标。  

3. **分析结果**：  
   - 自动评测报告含总正确率、BadCase 归因（模型理解有误/重排不佳/检索无效/切片不完整/未获取知识）、RAG 分项得分；  
   - 新版评测任务详情页支持查看评估器自动评分、人工标签标注、指标统计（通过率/综合得分）及数据筛选。  

## 限制和注意事项

- **应用前提**：自动评测仅支持**已发布**且**配置知识库**的智能体应用；多应用横向评测要求所有应用必须关联**至少一个相同知识库**；未开通应用观测将无法执行评测 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **模型与计费**：自动评测与 LLM 评估器强制使用 `qwen-max` 或 `qwen-plus`，产生 [Token](../concepts/token.md) 费用；Code 评估器无额外调用成本；预估 [Token](../concepts/token.md) 消耗为参考值，实际以账单为准 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **评测集约束**：  
  - 知识问答类评测集必须为 `.jsonl` 格式，含 `query`、`referenceAnswer`、`fineKeywords`、`coarseKeywords` 字段；  
  - 对话分析类仅支持 `.xls`/`.xlsx`，需包含 `Prompt`、`Completion`、`SessionId`；  
  - 新版“智能体”类型评测集字段由应用出入参自动生成，不可手动修改结构。  
- **任务不可变性**：评测任务创建后，应用、评测集、评估器配置均不可修改；如需调整，须新建任务 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。  
- **权限要求**：子账号需具备 `管理员` 或 `应用评测-操作` 权限才能使用自动评测功能 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


