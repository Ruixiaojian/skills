# application evaluation

application evaluation 是阿里云百炼平台用于系统化评估智能体（Agent）与工作流应用输出质量的核心能力，支持自动与手动两种评测范式。它通过评测集驱动、多维度评估器打分、人工标签标注及归因分析，帮助开发者量化效果、定位问题并闭环优化。该能力深度集成于应用观测体系，要求应用已发布且配置知识库（自动评测）或已开通观测（部分场景），是 RAG 应用调优和质量保障的关键环节。

## 支持的模型/功能

- **自动评测**：基于大模型与知识库自动生成评测集，支持单应用深度评测与最多 8 个应用的横向对比，适用于知识问答类场景 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **手动评测**：支持人工构建对话分析或知识问答类评测集，通过人工打标产出报告，适用于需主观判断或高精度校验的场景 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。  
- **新版评测体系**：引入“智能体”“工作流”“自定义”三类评测集类型，并支持从应用观测真实流量导入数据 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。  
- **评估器（Grader）**：提供预置模板（通用质量、智能体、文本匹配等）及自定义 LLM/Code 评估器，支持多评估器组合评分，覆盖语义理解与规则校验双路径 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。  
- **标签管理**：支持分类、布尔值、数字、文本四类标签，用于人工标注与多维指标统计，可同步应用于评测任务与应用观测 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

> **注意**：文档 1（自动评测）与文档 4（新版评测集）在评测集类型定义上存在差异——前者仅明确区分“对话分析”与“知识问答”，后者新增“智能体”“工作流”“自定义”三级分类；实际使用中应以控制台最新界面为准，旧版自动评测功能已逐步迁移至新版评测任务框架。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **评测集** | `queryType`、`referenceAnswer`、`fineKeywords`、`coarseKeywords` | 知识问答型必备字段，用于大模型自动评分；`fineKeywords` 必须为嵌套数组格式，`coarseKeywords` 限 1–3 个主题词 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md) |
| **模型选择** | `qwen-max`、`qwen-plus` | 自动评测中生成评测集与执行评测均仅支持此两类模型；新版评估器支持更广模型选型，但自动评测流程仍受限于此 |
| **采样与权重** | 分类采样数（事实型/教程型/比较型/分析型）、各维度权重（0–1） | 控制评测覆盖广度与重点；多应用评测时权重影响综合得分计算逻辑 |
| **评估器配置** | 评分范围（如 0–1、1–5）、通过阈值、参数映射（`query`→评测集`Prompt`等） | 映射错误将导致评估失败；所有变量必须完成映射方可保存评测任务 |

## 使用方式

1. **准备数据**：  
   - 自动评测：确保应用已发布、关联知识库、开通应用观测；  
   - 手动/新版评测：上传 `.xls`/`.xlsx`（对话分析）或 `.jsonl`（知识问答）评测集，或通过“从应用观测导入”获取真实请求；  
   - 创建标签与评估器（可选），用于后续多维分析。

2. **创建任务**：  
   - 自动评测：在控制台“自动评测”页依次完成“选择应用→选择知识库→生成/选择评测集→配置采样与模型→发起评测”；  
   - 新版评测任务：在“评测任务”页选择评测集、关联应用（智能体/工作流/不关联）、添加评估器（需完成参数映射）及标签；  
   - 手动评测：在“手动评测”页选择已发布评测集与应用，进入标注流程逐条打标。

3. **执行与分析**：  
   - 自动评测结果含总正确率、BadCase 归因（模型理解有误/重排不佳/检索无效/切片不完整/未获取知识）及调优建议；  
   - 新版任务支持“数据明细”（含评估器自动评分+人工标签）与“指标统计”（综合得分、通过率柱状图）；  
   - 所有评测任务支持下载原始结果（JSON/Excel 格式）。

## 限制和注意事项

- **应用状态限制**：自动评测仅支持**已发布**的智能体应用；手动评测与新版评测任务虽支持“不关联应用”，但调用模型评测时仍需应用处于发布状态。  
- **知识库依赖**：自动评测强制要求应用配置知识库，且多应用横向评测时所有应用必须共享至少一个知识库 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **[Token](../concepts/token.md) 消耗不可逆**：评测集生成、试运行、正式评测均为离线任务，每一步成功执行即消耗 [Token](../concepts/token.md) 并计费，失败步骤已消耗 [Token](../concepts/token.md) 不退还。  
- **配置不可修改**：评测任务创建后，应用、评测集、评估器映射等核心配置不可编辑；如需调整，必须新建任务。  
- **版本兼容性**：文档 6（评测任务）与文档 7（评估器）明确提示“左上角可返回旧版”，表明新旧两套评测体系并存；开发者应确认当前控制台默认启用版本，避免混用旧版文档操作新版界面。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


