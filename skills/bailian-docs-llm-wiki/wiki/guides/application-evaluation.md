# application evaluation

应用评测是百炼平台用于系统化评估智能体、工作流等大模型应用输出质量的核心能力，支持人工打标与自动评分相结合的多维度验证方式。它既可用于上线前的效果验收，也适用于迭代过程中的回归验证和横向对比分析，覆盖从评测集构建、任务配置到结果归因与优化建议的完整闭环。

## 支持的模型/功能

- **评测模式**：支持手动评测（[手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)）与自动评测（[自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)）两类范式。手动评测依赖人工构建评测集并逐条打标；自动评测则基于知识库自动生成评测集，并利用大模型完成自动评分与归因分析。
- **应用类型支持**：当前明确支持**智能体应用**（文档1、2、4、5均强调此前提），部分新版能力（如[评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)）已扩展支持**工作流应用**及**自定义应用**，但需注意旧版流程仍仅限智能体。
- **评估器类型**：提供预置模板（通用质量、智能体、文本匹配等）及自定义能力，包括 **LLM评估器**（调用`qwen-max`/`qwen-plus`等模型）和 **Code评估器**（Python脚本规则判断），二者可组合使用以覆盖语义理解与精确校验场景（[评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)）。
- **评测集类型**：支持三种结构化形式：**对话分析**（`.xls`/`.xlsx`，含`Prompt`/`Completion`/`SessionId`字段）、**知识问答**（`.jsonl`，含`query`/`referenceAnswer`/`fineKeywords`等字段）以及新版引入的**智能体/工作流/自定义**三类结构化评测集（[评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md) 与 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)）。

> **注意**：文档4与文档3对评测集类型的定义存在不一致——文档3仅区分“对话分析”与“知识问答”，而文档4新增“智能体/工作流/自定义”分类且强调“创建后类型不可修改”。实际使用中，应以控制台最新UI为准，旧版上传逻辑（文档3）仍兼容，但新建评测集推荐采用文档4所述结构化方式。

## 关键参数

- **评测集参数**：
  - `Prompt`（或`query`）：用户输入问题/指令，必填；
  - `Completion`（或`referenceAnswer`）：标准答案，用于比对；
  - `SessionId`：多轮对话标识（仅对话分析类型）；
  - `fineKeywords`/`coarseKeywords`：细粒度与粗粒度关键词，用于完整性与主题一致性校验（知识问答类型）；
  - `queryType`：问题分类标签（如“事实型”“分析型”），影响采样与归因维度。
- **评测任务参数**：
  - **关联应用**：必须为已发布智能体（文档1、2明确要求），工作流应用需在新版任务中显式选择；
  - **评估器映射**：所有变量（如`query`、`response`、`reference`）必须完成字段映射，否则无法保存任务（[评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)）；
  - **标签配置**：支持分类、布尔值、数字、文本四类标签，用于人工补充标注（[标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)）；
  - **采样数与权重**：自动评测中可按任务类型（事实型/教程型等）设置分类采样数及维度权重（文档2）。
- **模型与计费参数**：
  - 生成评测集与执行评测均需指定模型，当前仅支持`qwen-max`和`qwen-plus`（文档2）；
  - [Token](../concepts/token.md)消耗分“预估平均消耗”（参考值）与“预估最大消耗”（硬性上限），实际费用以账单为准（文档2、5）。

## 使用方式

1. **准备评测数据**：
   - 手动方式：下载模板（[手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)），填写`.xls`/`.xlsx`文件，或按`.jsonl`格式构造知识问答集；
   - 自动方式：在自动评测流程中，基于已配置知识库生成评测集（文档2），或通过“从应用观测导入”复用真实请求数据（文档4）。
2. **创建并发布评测集**：
   - 上传后需点击“发布”，草稿状态不可用于评测（文档1、3、4）；
   - 新版支持版本管理，每次发布生成新版本，任务中可指定使用版本（文档4）。
3. **配置评测任务**：
   - 手动评测：在“手动评测”页面选择已发布应用与评测集，配置维度后启动，人工逐条打标（文档1）；
   - 自动评测：选择应用、知识库、生成评测集、设置采样规则，发起任务（文档2）；
   - 新版评测任务：支持“不关联应用”（纯人工标注）、“智能体”、“工作流”三种模式，并可叠加多个评估器与标签（文档5）。
4. **执行与分析**：
   - 手动评测完成后查看打标结果与汇总报告；
   - 自动评测产出总正确率、BadCase分析、RAG环节归因（模型理解/重排/检索/切片/知识缺失）及调优建议（文档2）；
   - 新版任务支持指标统计仪表盘、评估器得分柱状图及标签筛选（文档5、6）。

## 限制和注意事项

- **应用状态限制**：所有评测模式均要求目标应用**已发布**（文档1、2、4、5多次强调），草稿或未发布应用不可选；
- **知识库依赖**：自动评测强制要求应用已配置知识库，且多应用横向评测时所有应用必须共享至少一个知识库（文档2）；
- **权限要求**：子账号需具备`管理员`或`应用评测-操作`权限（文档2）；
- **文件限制**：上传文件仅支持`.xls`/`.xlsx`（对话分析）或`.jsonl`（知识问答），单文件≤20MB，单次≤10个（文档1、3）；
- **模型限制**：评测集生成与自动评分阶段仅支持`qwen-max`和`qwen-plus`，不支持其他模型（文档2）；
- **配置不可变性**：评测任务创建后，应用、评测集、评估器映射等核心配置不可修改，需新建任务（文档5）；
- **观测功能依赖**：自动评测需开通“应用观测”并添加目标应用至观测列表，评测期间关闭会导致失败（文档2）；
- **[Token](../concepts/token.md)消耗风险**：评测任务分步执行，任一成功步骤均产生计费，失败任务已消耗[Token](../concepts/token.md)不退还（文档2）。

## 来源文档

- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


