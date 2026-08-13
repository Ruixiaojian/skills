# application evaluation

application evaluation 是阿里云百炼平台用于系统化评估智能体与工作流应用输出质量的核心能力，支持自动与手动两种评测范式。它通过评测集、评估器、标签和观测数据的协同，实现从数据构建、规则定义、自动打分到人工标注的完整闭环，帮助开发者持续验证和优化应用效果。

## 支持的模型/功能

- **自动评测**：基于知识库自动生成评测集，利用大模型（当前仅支持 `qwen-max` 和 `qwen-plus`）对智能体回答进行语义级评分，并提供归因分析与调优建议 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **手动评测**：支持人工构建 `.xls`/`.xlsx` 格式的对话分析评测集，通过人工打标（如“较差/一般/较好”）完成效果评估 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。  
- **新版评测体系**：引入结构化评测集类型（智能体/工作流/自定义）、可复用的评估器（LLM/Code/基于任务生成）及多维度标签体系，支持更灵活的业务场景建模 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。  
- **评估器能力**：预置通用质量、智能体、文本匹配等模板；支持自定义 LLM 评估器（需配置 Prompt 与评分范围）和 Code 评估器（Python 脚本校验）；亦可通过历史人工标注任务反向生成 LLM 评估器 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。  

> **注意**：文档 1 和文档 4–7 描述的是两套并行演进的评测体系——旧版（以知识库驱动的自动评测为主）与新版（以评测集+评估器+标签为架构）。新版不依赖知识库配置，且明确支持工作流与自定义应用类型；而旧版自动评测强制要求应用已发布、配置知识库并开通应用观测 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。开发者应根据控制台实际界面（是否显示“返回旧版”按钮）选择对应文档路径。

## 关键参数

- **评测集字段**：知识问答型需 `query`、`referenceAnswer`、`coarseKeywords`、`fineKeywords`、`queryType`（JSONL 格式）；对话分析型需 `Prompt`、`Completion`、`SessionId`（XLS/XLSX 格式）[评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。  
- **评估器参数映射**：所有变量（如 `query`, `response`, `context`）必须显式映射至评测集字段或应用输出，否则任务无法保存 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。  
- **采样与权重**：旧版自动评测中，分类采样数（事实型/分析型等）决定各类型问题抽取数量；新版支持在评测任务中为每个评估器独立配置评分范围（如 0–5 或 0–100）与通过阈值 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **标签类型**：支持分类（多选枚举）、布尔值（True/False）、数字（精确打分）、文本（自由描述）四类，直接影响指标统计维度 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。  

## 使用方式

1. **准备数据**：  
   - 旧版：确保智能体已发布、关联知识库、开通应用观测；新版：直接创建评测集（支持上传 XLS/XLSX/JSONL 或从应用观测导入）。  
2. **构建评测逻辑**：  
   - 选择或创建评估器（LLM 或 Code），完成参数映射；  
   - 可选添加标签用于人工补充维度（如“错误类型”“情感倾向”）。  
3. **发起评测**：  
   - 旧版：在自动评测页面按“创建任务→设置评测集→配置规则→执行”四步流程操作；  
   - 新版：在评测任务页面选择评测集、应用、评估器与标签，一键创建。  
4. **分析结果**：  
   - 查看自动评分（BadCase 归因、RAG 环节定位）、人工标注结果及多维指标统计（通过率、综合得分仪表盘）。  

## 限制和注意事项

- **应用约束**：旧版自动评测仅支持已发布的智能体应用，且多应用横向评测要求所有应用共享至少一个知识库；新版评测任务支持“不关联应用”，适用于纯人工标注场景 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **文件限制**：评测集上传单文件 ≤ 20 MB，格式严格限定（XLS/XLSX 用于对话分析，JSONL 用于知识问答）；新版自定义评测集允许编辑表结构，但类型创建后不可修改 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。  
- **权限与计费**：子账号需 `应用评测-操作` 权限；所有调用大模型的环节（评测集生成、自动评分）均产生 [Token](../concepts/token.md) 消耗，预估消耗仅为参考，实际以账单为准 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **版本兼容性**：新版评估器不支持试运行（基于评测任务创建的评估器）；旧版评测报告中的“追加评测”功能在新版中由“多评估器组合”替代，二者逻辑不同，不可混用。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)


