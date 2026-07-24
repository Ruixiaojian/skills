# application evaluation

应用评测是百炼平台用于系统化评估智能体、工作流等大模型应用输出质量的核心能力，支持人工标注与自动评估双轨并行。它覆盖从评测集构建、任务编排、多维评分到归因分析的完整闭环，既可用于上线前的效果验证，也适用于迭代过程中的持续质量监控。评测结果可直接驱动 Prompt 优化、知识库切片调整及 RAG 配置调优。

## 支持的模型/功能

- **评测模式**：支持**手动评测**（基于人工打标）和**自动评测**（基于大模型或代码规则自动评分），二者可混合使用于同一任务中 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。
- **评测对象**：当前支持**智能体应用**和**工作流应用**，旧版仅限智能体；新版评测集明确扩展支持工作流与自定义类型 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。
- **评估器类型**：
  - **LLM评估器**：使用 `qwen-max` 或 `qwen-plus` 等大模型进行语义级评分，适用于相关性、幻觉、有害性等复杂判断；
  - **Code评估器**：通过 Python 脚本执行精确规则校验（如 JSON 格式、关键词匹配、数值计算），无 [Token](../concepts/token.md) 成本；
  - **预置模板**：提供通用质量、智能体能力、文本匹配、文本相似度、格式校验等分类模板，开箱即用 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **标签体系**：支持分类、布尔值、数字、文本四类标签，用于人工标注与多维统计分析，可与评估器结果联动分析 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

> **注意**：文档3（自动评测）称“仅支持已发布的智能体应用”，而文档7（评测任务）明确支持“工作流”和“不关联应用”两种模式，且文档4（新版评测集）将工作流列为一级评测集类型。此处以新版控制台能力为准，旧版限制已过时。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **评测集类型** | `对话分析`（xls/xlsx）、`知识问答`（jsonl）、`智能体`、`工作流`、`自定义` | 类型创建后不可修改；`对话分析`需含 `Prompt`/`Completion`/`SessionId` 字段；`知识问答`需含 `query`/`referenceAnswer`/`coarseKeywords`/`fineKeywords` 字段 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md) |
| **评估器参数映射** | 必须为评估器中声明的每个变量（如 `query`, `response`, `context`）指定数据源（评测集字段或应用输出） | 所有变量必须完成映射，否则无法保存评测任务 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md) |
| **评分范围与阈值** | LLM/Code评估器均需配置 `评分范围`（如 0–1、1–5、0–100）和 `通过阈值`（如 ≥4.0 判定为 Pass） | 阈值建议设为范围中位数；精细评估推荐 0–100，快速分类推荐 1–5 或 0–1 |
| **采样与规模** | 自动评测中可设置各任务类型（事实型/分析型等）的分类采样数；单次评测任务最多支持 8 个应用横向对比 | 多应用评测要求所有应用关联至少一个**相同知识库** [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md) |

## 使用方式

1. **准备评测集**  
   - 手动上传：按类型下载模板（[对话分析模板](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240123/lfrxah/应用评测-评测集-EfmApplicationdata.xlsx) 或 [知识问答 jsonl 示例](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8229463471/p937413.png)），填写后上传（单文件 ≤20MB，单次 ≤10 个）；  
   - 自动生成：基于知识库，由 `qwen-max`/`qwen-plus` 自动生成 `知识问答` 型评测集 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)；  
   - 新版支持从**应用观测**真实流量导入数据 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。

2. **创建并发布评测集**  
   - 上传后需点击**发布**，草稿状态不可用于评测任务；  
   - 支持版本管理，每次发布生成新版本，创建任务时可指定版本。

3. **配置评测任务**  
   - 选择评测集、应用（智能体/工作流/不关联）、评估器（≤10 个）及人工标签；  
   - 为每个评估器完成**参数映射**（如将 `query` 映射至评测集 `Prompt` 字段）；  
   - 支持**试运行**（单条用例预览）验证流程 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。

4. **执行与分析**  
   - 启动后查看状态（`评测中(X%)`），完成后进入详情页；  
   - **数据明细**页支持普通/快速标注模式，逐条查看输入、应用输出、评估器得分、人工标签；  
   - **指标统计**页提供综合得分仪表盘、各评估器通过率柱状图、BadCase 归因分布（如“检索无效”“切片不完整”）。

## 限制和注意事项

- **权限与依赖**：自动评测要求子账号具备 `管理员` 或 `应用评测-操作` 权限；多应用横向评测需所有应用已开通 `应用观测` 并加入观测列表 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **文件与规模限制**：评测集单文件 ≤20MB，单次上传 ≤10 个；评测任务中评估器 ≤10 个；多应用评测上限为 8 个应用。
- **模型与计费**：LLM评估器及自动评测均调用 `qwen-max`/`qwen-plus`，产生 [Token](../concepts/token.md) 费用；Code评估器无额外成本；预估 [Token](../concepts/token.md) 消耗为参考值，实际以账单为准 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **配置不可变性**：评测任务创建后，其关联的评测集、应用、评估器配置不可修改，仅可追加人工标签或新建任务 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。
- **知识库强依赖**：自动评测的评测集生成与 RAG 归因分析均依赖知识库内容完整性与切分合理性；若评测集问题在知识库中无对应答案，将导致“未获取知识”归因 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。

## 来源文档

- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)


