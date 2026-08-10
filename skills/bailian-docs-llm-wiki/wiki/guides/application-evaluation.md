# application evaluation

应用评测是百炼平台用于系统化评估大模型应用（如智能体、工作流）输出质量的核心能力，支持人工打标与自动化评估相结合的多维度验证方式。它覆盖从评测集构建、任务执行到归因分析与调优建议的完整闭环，适用于上线前验证、版本迭代对比及日常质量监控等典型场景。

## 支持的模型/功能

- **评测模式**：提供手动评测（[手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)）与自动评测（[自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)）两类路径。手动评测依赖人工构建评测集并逐条打标；自动评测基于知识库自动生成评测集，并利用大模型完成评分与归因分析。
- **评测对象**：支持智能体应用、工作流应用及自定义应用（见[新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)），但旧版手动评测仅限已发布的智能体应用（> **注意**：文档1明确限定“当前仅支持选择已发布的**智能体应用**”，而文档4和文档6已扩展支持工作流与自定义类型，表明平台能力已演进，旧文档存在范围过时问题）。
- **评估器类型**：提供预置模板（通用质量、智能体、文本匹配等）及自定义能力，包括LLM评估器（调用`qwen-max`/`qwen-plus`等模型）和Code评估器（Python脚本规则校验），详见[评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **标签体系**：支持分类、布尔值、数字、文本四类标签，用于人工标注与多维统计分析（[标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)）。

## 关键参数

- **评测集字段**：
  - 对话分析类型（`.xls`/`.xlsx`）：必需 `Prompt`（用户输入）、`Completion`（参考答案）、`SessionId`（会话标识）；
  - 知识问答类型（`.jsonl`）：必需 `query`、`referenceAnswer`、`coarseKeywords`、`fineKeywords`、`queryType`（见[评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)）。
- **评估器配置**：
  - LLM评估器：需指定模型（如`qwen-max`）、Prompt规则、评分范围（如0–5或0–100）及通过阈值；
  - Code评估器：需定义入参（如`query`, `response`）、Python函数逻辑及评分范围。
- **评测任务参数**：支持最多8个应用横向对比（自动评测）、最多10个评估器组合使用（[评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)），分类采样数可按任务类型（事实型/分析型等）独立设置。

## 使用方式

1. **准备评测集**：  
   - 手动上传：下载模板（如`应用评测-评测集-EfmApplicationdata.xlsx`），按字段填充后上传（支持`.xls`/`.xlsx`/`.jsonl`，单文件≤20MB）；  
   - 自动生成：基于知识库选择任务类型（事实型、教程型等），由大模型生成`.jsonl`格式评测集（仅限知识问答类型）。

2. **创建评测任务**：  
   - 手动评测：在“应用批量评测”中选择已发布智能体应用 + 已发布评测集 → 配置维度 → 开始评测 → 人工打标（“较差/一般/较好”或1–5分）；  
   - 自动评测：选择应用（需已发布且配置知识库）→ 选择知识库 → 生成/复用评测集 → 配置采样数与评测模型 → 发起任务；  
   - 新版评测任务：支持“不关联应用”（纯人工标注）、智能体、工作流三种关联方式，可灵活组合评估器与标签。

3. **执行与分析**：  
   - 人工标注：在任务详情页进入“标注”视图，逐条比对应用输出与参考答案；  
   - 自动评估：系统输出总正确率、BadCase分析（含归因：模型理解有误/重排不佳/检索无效等）、RAG各环节得分及调优建议；  
   - 结果查看：支持下载评测结果、按标签筛选数据、查看[Token](../concepts/token.md)消耗明细。

## 限制和注意事项

- **权限与前提**：自动评测要求子账号具备`管理员`或`应用评测-操作`权限；需开通`应用观测`功能并添加目标应用至观测列表（[自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)）；知识库为自动评测必要条件。
- **文件与规模限制**：评测集单次上传最多10个文件，单文件≤20MB；自动评测最多支持8个应用横向对比；每个评测任务最多添加10个评估器。
- **模型与计费**：评测过程调用模型（如`qwen-max`/`qwen-plus`）产生[Token](../concepts/token.md)s费用，按实际用量计费；公共资源部署产生费用，独占资源不收费（[手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)）。
- **状态约束**：草稿状态的评测集不可用于评测任务，必须发布后方可选用；评测任务创建后配置不可修改，需新建任务调整参数（[评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)）。
- > **注意**：文档2称“自动评测将基于知识库自动生成评测集”，而文档3明确指出自动生成仅支持“知识问答”类型；文档4新增“智能体”“工作流”“自定义”三类评测集，但未说明其是否支持自动生成——实践中应以控制台实际能力为准，避免依赖过时文档描述。

## 来源文档

- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)


