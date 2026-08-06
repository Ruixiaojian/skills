# application evaluation

application evaluation 是阿里云百炼平台用于系统化评估智能体、工作流等应用输出质量的核心能力，支持自动与手动两种评测范式。它通过评测集驱动、多维度评估器（LLM/Code）与人工标签协同，实现从数据构建、任务执行到归因分析的完整闭环，帮助开发者持续优化 RAG 流程与 Prompt 工程。

## 支持的模型与功能

- **自动评测**：基于知识库自动生成评测集，支持单应用深度评测与最多 8 个应用的横向对比；依赖 `qwen-max` 或 `qwen-plus` 模型生成评测集及执行评分 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **手动评测**：支持人工构建并上传 `.xls`/`.xlsx` 格式的对话分析评测集，或 `.jsonl` 格式的知识问答评测集，适用于需强业务语义判断的场景 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。  
- **新版评测体系**：引入「智能体」「工作流」「自定义」三类评测集，并支持通过「评估器」（LLM 或 Code 类型）和「标签」（分类/布尔/数字/文本）实现多维度自动化+人工混合评测 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。  
> **注意**：文档 1 和文档 4/5 存在功能演进关系——文档 1 描述的是旧版自动评测流程（仅面向智能体、强耦合知识库），而文档 4/5 定义的新版评测体系已扩展至工作流、支持不关联应用的纯人工标注，并解耦了评测集类型与应用类型。实际开发中应优先采用新版能力。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **评测集类型** | `对话分析`（.xls/.xlsx）、`知识问答`（.jsonl）、`智能体`/`工作流`/`自定义`（新版） | 旧版仅支持前两者；新版创建后类型不可修改 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md) |
| **评估器模型** | LLM 评估器支持 `qwen-max`、`qwen-plus` 等（评估模型限时免费）；Code 评估器无模型依赖 | 自动评测阶段固定为 `qwen-max`/`qwen-plus`；新版评估器可自由选型 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md) |
| **采样与权重** | 分类采样数（如事实型、分析型各采 N 条）、各评估器权重（0~1）、通过阈值（如 ≥0.8 判定 Pass） | 旧版自动评测中分类采样数影响总用例量；新版支持为每个评估器独立配置阈值 |
| **标签类型** | 分类（多选枚举）、布尔（True/False）、数字（Double）、文本（String） | 标签需在评测任务中显式添加并映射，否则不参与统计 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md) |

## 使用方式

1. **准备评测数据**  
   - 若使用旧版自动评测：确保智能体已发布、配置知识库、开通应用观测；知识库将用于生成 `.jsonl` 格式评测集 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
   - 若使用新版体系：可手动上传 `.xls`/`.xlsx`（对话分析）或 `.jsonl`（知识问答），或选择「从应用观测导入」真实流量数据 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。  

2. **创建评测任务**  
   - 旧版：在「自动评测」界面依次完成「创建任务→设置评测集→配置规则→执行评测」四步；试运行仅支持单应用预览。  
   - 新版：在「评测任务」页面选择评测集、关联智能体/工作流（或选「不关联应用」）、添加 1–10 个评估器并完成字段映射（如 `query`→`Prompt`）、配置标签；所有变量映射必须完成方可保存 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。  

3. **执行与分析**  
   - 自动评测结果含总正确率、BadCase 归因（模型理解有误/重排不佳/检索无效等）及调优建议；  
   - 新版任务支持「数据明细」查看每条评估器评分与人工标签、「指标统计」查看综合得分与各评估器通过率；  
   - 所有评测均产生 [Token](../concepts/token.md) 消耗，可在控制台查看明细，费用按实际调用计费 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。

## 限制与注意事项

- **应用状态限制**：旧版自动评测仅支持已发布的智能体应用，且多应用横向评测要求所有应用必须关联至少一个相同知识库；新版评测任务中「智能体」类型评测集也要求应用已发布。  
- **评测集格式强约束**：知识问答类 `.jsonl` 文件必须包含 `query`、`referenceAnswer`、`coarseKeywords`、`fineKeywords` 字段；字段缺失或格式错误将导致评测失败 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。  
- **权限与资源**：子账号需具备 `管理员` 或 `应用评测-操作` 权限；自动评测依赖应用观测功能，评测期间关闭观测将导致任务失败或报告不准 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **不可逆操作**：评测任务创建后，应用、评测集、评估器映射等核心配置不可修改；如需调整，必须新建任务。  
- **[Token](../concepts/token.md) 消耗提示**：预估平均消耗仅为参考值，实际用量以账单为准；预估最大消耗是硬性成本上限，但实际消耗通常显著低于该值 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)


