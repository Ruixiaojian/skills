# application evaluation

application evaluation 是百炼平台用于系统化评估智能体/工作流应用输出质量的核心能力，支持自动与人工双路径评测。它通过结构化评测集驱动模型推理、多维度评估器打分及人工标签标注，实现从数据准备、任务执行到归因分析的闭环。该能力深度集成知识库、应用观测与RAG调优建议，适用于版本迭代验证、线上质量监控和Prompt工程优化等典型开发者场景。

## 支持的模型/功能

- **自动评测**：基于大模型（当前仅支持 `qwen-max` 和 `qwen-plus`）自动生成评测集并执行端到端评分，适用于已发布且配置知识库的智能体应用 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **手动评测**：支持人工构建 `.xls`/`.xlsx` 格式对话分析类评测集，并通过人工打标（如“较差/一般/较好”）产出报告，适用于需强主观判断的业务场景 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。  
- **新版评测体系**：提供统一评测任务框架，支持关联智能体/工作流应用、灵活组合 LLM/Code 评估器（最多10个）、以及分类/布尔/数字/文本四类人工标签，覆盖自动+人工混合评测需求 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。  
- **评估器类型**：预置通用质量、智能体能力、文本匹配等模板；支持自定义 LLM 评估器（需指定模型与 Prompt）和 Code 评估器（Python 脚本校验），其中 LLM 评估器调用产生 [Token](../concepts/token.md) 费用，Code 评估器无额外费用 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。  

> **注意**：文档1明确限定自动评测仅支持 `qwen-max` 和 `qwen-plus`，而文档7中“创建LLM评估器”步骤提到“评估模型限时免费”，未限定具体型号——实际使用中请以文档1为准，避免因模型不兼容导致评测失败。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **评测集** | `queryType`、`referenceAnswer`、`fineKeywords`、`coarseKeywords` | 知识问答型评测集必需字段，用于自动评分归因；`fineKeywords` 必须为嵌套数组格式（如 `[["信息点1"],["信息点2"]]`）[评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md) |
| **评测规则** | 分类采样数（事实型/教程型/比较型/分析型）、评测模型、各维度权重（0~1） | 控制评测样本规模与侧重点；权重调整直接影响最终综合得分计算逻辑 |
| **评估器** | `评分范围`（如 0-1 或 1-5）、`通过阈值`、参数映射（如 `query`→评测集`question`字段） | 映射错误将导致评估器无法获取输入数据；所有变量必须完成映射才能保存任务 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md) |
| **标签** | 类型（分类/布尔/数字/文本）、筛选项（如“回答质量：较差/一般/较好”） | 分类标签最多支持20个选项；布尔值标签固定为 `True`/`False`，常用于“是否正确”等二元判断 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md) |

## 使用方式

1. **准备评测集**：  
   - 自动场景：在[自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)流程中，选择知识库后由 `qwen-max`/`qwen-plus` 自动生成 `.jsonl` 格式知识问答集；  
   - 手动场景：下载 Excel 模板填写 `Prompt`/`Completion`/`SessionId`，上传后需**发布**才可使用；  
   - 新版体系：支持智能体/工作流/自定义三类评测集，创建时需指定类型且不可修改，推荐优先选用 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。  

2. **创建评测任务**：  
   - 自动评测：进入控制台 → 创建任务 → 选应用（≤8个）→ 选知识库 → 生成/复用评测集 → 配置采样数与模型 → 发起评测；  
   - 新版评测：在[评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)页面 → 关联已发布评测集与智能体/工作流 → 添加评估器（配置参数映射）→ 添加标签 → 完成创建；  
   - 手动评测：上传评测集并发布后 → 进入手动评测页 → 选应用与评测集 → 选内置/自定义维度 → 开始评测 → 人工逐条打标。  

3. **分析与迭代**：  
   - 自动评测报告提供总正确率、BadCase 归因（如“检索无效”“切片不完整”）及调优建议；  
   - 新版评测任务详情页支持查看评估器自动评分、人工标签标注结果，并通过“指标统计”页进行多维聚合分析；  
   - 建议将评测融入开发闭环：知识库/Prompt/模型变更后立即触发，定期回归验证 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  

## 限制和注意事项

- **应用前提**：自动评测仅支持**已发布**且**配置知识库**的智能体应用；必须开通`应用观测`功能并将目标应用加入观测列表，否则评测任务可能失败或结果不准 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **数量限制**：单次自动评测最多支持8个应用横向对比；单个评测任务最多添加10个评估器；单次上传评测集文件不超过10个，单文件≤20MB。  
- **权限要求**：子账号需具备`管理员`或`应用评测-操作`权限，否则无法访问评测功能 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **评测集兼容性**：自动评测仅接受 `.jsonl` 格式知识问答集；手动评测仅接受 `.xls`/`.xlsx` 格式对话分析集；新版评测体系中，智能体/工作流类型评测集需按应用出入参自动生成模板，不可混用 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。  
- **费用提示**：自动评测、新版评测任务中调用 LLM 评估器均产生 [Token](../concepts/token.md) 费用；Code 评估器无额外费用；预估 [Token](../concepts/token.md) 消耗为参考值，实际以账单为准 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


