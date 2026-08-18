# application evaluation

应用评测是百炼平台用于系统化评估智能体/工作流应用输出质量的核心能力，支持自动与人工双路径评测机制。通过评测集、评估器、标签三大组件协同，开发者可实现从数据构建、规则定义、自动打分到人工标注的完整评测闭环，支撑模型迭代、RAG调优与上线前验证等关键场景。

## 支持的模型/功能

- **自动评测**：基于知识库自动生成评测集，支持单应用深度评测与最多 8 个应用的横向对比；当前仅支持 `qwen-max` 和 `qwen-plus` 模型用于评测集生成与最终评分 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。  
- **手动评测**：依赖人工构建评测集（XLS/XLSX 格式），通过人工打标完成效果评估，适用于需强业务语义判断或无标准答案的场景 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。  
- **新版评测体系**：引入结构化评测集类型（智能体/工作流/自定义）、可复用评估器（LLM/Code/预置模板）及多类型标签（分类/布尔/数字/文本），支持更灵活的评测维度建模与混合评估 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。  
> **注意**：文档 1 与文档 4–7 描述的是两套并存但不兼容的评测体系——文档 1 对应旧版“自动评测”（仅限智能体+知识库驱动），而文档 4–7 共同构成新版统一评测框架（支持智能体/工作流/自定义应用，且评测集、评估器、标签解耦）。两者控制台入口、权限模型与数据结构均不同，不可混用。

## 关键参数

- **评测集字段要求**：  
  - 知识问答类（自动评测）必须包含 `query`、`referenceAnswer`、`coarseKeywords`、`fineKeywords`、`queryType` 字段，格式为 `.jsonl` [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)；  
  - 对话分析类（手动评测）需 `Prompt`、`Completion`、`SessionId` 字段，格式为 `.xls`/`.xlsx`；  
  - 新版评测集支持自定义表结构，字段名需与评估器参数映射严格一致。  
- **评估器配置**：  
  - LLM评估器需明确定义 `评分范围`（如 0–5 或 0–100）与 `通过阈值`，且 Prompt 中须与范围保持逻辑一致；  
  - Code评估器函数签名必须匹配入参设置，返回数值型 score 并在范围内；  
  - 所有评估器参数（如 `query`, `response`, `context`）必须完成字段映射，否则任务创建失败 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。  
- **标签类型约束**：分类标签最多 20 个选项；数字标签支持 Double 类型；文本标签上限 200 字符 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

## 使用方式

1. **准备评测数据**：  
   - 旧版：为自动评测配置已发布且含知识库的智能体；为手动评测下载模板并填充 XLS/XLSX 文件；  
   - 新版：在[评测集](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=evalSet)页面选择“智能体/工作流/自定义”类型，上传文件或从应用观测导入真实流量。  

2. **定义评估逻辑**：  
   - 选用预置评估器（如“问答相关性”）或自定义 LLM/Code 评估器，确保其必选参数与评测集字段对齐；  
   - 为人工维度创建标签（如“回答质量：较差/一般/较好”），并在评测任务中添加 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。  

3. **发起评测任务**：  
   - 旧版：在“自动评测”或“手动评测”独立页面创建任务，绑定应用、知识库、评测集；  
   - 新版：在[评测任务](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=task)统一入口创建，关联评测集、应用（智能体/工作流/不关联）、评估器（≤10 个）及标签。  
   > **注意**：新版评测任务创建后配置不可修改，如需调整需新建任务；旧版自动评测支持“追加评测”新增应用，但总数仍限 8 个 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。

## 限制和注意事项

- **权限与依赖**：  
  - 自动评测要求子账号具备 `管理员` 或 `应用评测-操作` 权限，且目标应用必须已开通 `应用观测` 并加入观测列表 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)；  
  - 新版评测任务中，若选择“智能体”或“工作流”关联方式，则对应应用必须已发布；“不关联应用”模式仅支持纯人工标注。  

- **技术限制**：  
  - 旧版自动评测仅支持智能体应用，不支持工作流；新版支持三类应用，但工作流评测需其 API 入参/出参与评测集结构兼容；  
  - 评测集文件单次上传 ≤10 个，单个 ≤20 MB；JSONL 格式无 Excel 行数限制，但过大会导致导入超时；  
  - 基于评测任务创建的 LLM 评估器不支持试运行，需在真实任务中验证效果 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。  

- **计费与稳定性**：  
  - 所有调用大模型的环节（评测集生成、LLM评估器执行）均按实际 Token 消耗计费，预估消耗仅为参考值，以账单为准 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)；  
  - 评测任务为离线异步执行，排队期间进度显示 0%，任务失败时已完成步骤的 Token 仍计费；  
  - 评测期间请勿关闭应用观测，否则可能导致数据丢失或报告异常。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)


