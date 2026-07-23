# application evaluation

application evaluation 是百炼平台提供的系统化应用质量评估能力，支持通过人工标注与自动评估相结合的方式，对智能体、工作流等大模型应用的输出效果进行多维度、可复现的量化分析。其核心流程包括评测集构建、评测任务创建、评估器配置与标签管理，覆盖从数据准备到结果分析的完整闭环。

## 支持的模型/功能

- **应用类型支持**：当前明确支持**智能体**和**工作流**两类应用的评测；[手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)文档特别强调“当前仅支持选择已发布的**智能体应用**”，但[新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)和[评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)文档均明确列出对“工作流”类型的支持，表明功能已扩展。
- **评测模式**：支持**自动评估**（基于预置或自定义评估器）与**人工标注**（通过结构化标签）双轨并行；[评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)文档指出知识问答类型适用于自动评测，而对话分析类型适用于人工评测，体现了能力分层设计。
- **评估器类型**：提供预置模板（通用质量、智能体、文本匹配等）及两种自定义方式：**LLM评估器**（基于大模型语义理解）和**Code评估器**（基于Python规则判断），满足灵活与精确的不同需求。

> **注意**：文档 1（手动评测）中“当前仅支持选择已发布的**智能体应用**”的描述与文档 3、4 中明确支持“工作流”应用存在矛盾。根据发布时间和上下文一致性，应以[新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)和[评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)为准，该限制已解除。

## 关键参数

- **评测集字段**：不同评测集类型要求不同字段。`对话分析`需 `Prompt`、`Completion`、`SessionId`；`知识问答`需 `query`、`referenceAnswer`、`fineKeywords`、`coarseKeywords`；`智能体/工作流`类型则依据所选应用的出入参自动生成字段结构。
- **评估器参数映射**：所有变量必须完成映射才能保存评测任务。常见参数如 `query`（用户输入）、`response`（应用输出）、`referenceAnswer`（标准答案）需准确绑定至评测集对应字段或应用输出。
- **评分配置**：
  - `评分范围`：决定打分尺度（如 0–1、1–5、0–100），影响评估器 Prompt 的生成逻辑；
  - `通过阈值`：用于判定 Pass/Fail（如 ≥ 0.8 判定为通过）；
  - `标签类型`：分类、布尔值、数字、文本四类，直接影响标注方式与后续统计维度。

## 使用方式

1. **准备评测集**：  
   - 选择类型（智能体/工作流/自定义），下载模板并填充数据；  
   - 支持 `.xls`/`.xlsx`（对话分析）、`.jsonl`（知识问答）格式，单文件 ≤20MB；  
   - 必须**发布**后才可用于评测任务（草稿状态不可用）。

2. **创建评测任务**：  
   - 选择已发布的评测集及版本；  
   - 指定关联应用（智能体/工作流/不关联）；  
   - 添加评估器（最多 10 个），完成全部参数映射；  
   - 可选添加人工标签（支持分类、布尔值、数字、文本四类）。

3. **执行与标注**：  
   - 任务发起后自动调用应用获取响应；  
   - 进入任务详情页，在“数据明细”中使用**普通模式**或**快速标注**进行人工标注；  
   - “指标统计”页实时展示综合得分、评测进度、各评估器通过率等。

## 限制和注意事项

- **评测集类型不可修改**：创建时选定“智能体”“工作流”或“自定义”后，无法变更类型。
- **评测任务不可编辑**：创建完成后，应用、评测集、评估器配置均不可修改；如需调整，必须新建任务。
- **费用说明**：自动评估调用大模型产生的 Tokens 将正常计费；使用公共资源部署模型会产生费用，独占资源部署不收费（详见[手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)中的费用说明）。
- **评估器依赖约束**：被评测任务引用的评估器无法删除；基于评测任务创建的评估器**不支持试运行**，需在实际任务中验证效果。
- **字段兼容性**：使用预置评估器前，务必确认评测集包含其必选字段（如“问答相关性”评估器要求 `query` 和 `response` 字段），否则映射失败。

## 来源文档

- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


