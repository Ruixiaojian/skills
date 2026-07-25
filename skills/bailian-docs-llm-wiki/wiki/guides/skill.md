# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，支持无需编码即可为智能体赋予文件处理、数据分析等专业功能。它通过语义匹配自动触发，开发者可选用平台预置的官方 Skill，或基于 ZIP 包定义自定义 Skill。所有 Skill 均需通过 `SKILL.md` 描述其能力边界，该描述直接影响智能体调用的准确性 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **官方 Skill**：由平台统一维护，覆盖常见文件处理场景（如 `.xlsx`、`.csv` 解析与生成），开箱即用，无需配置；版本更新后已添加的应用将自动升级 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。  
- **自定义 Skill**：通过上传符合规范的 ZIP 包创建，适用于行业定制需求（如特定格式发票解析、内部数据清洗流程）。其行为完全由 `SKILL.md` 中的 `description` 字段驱动，不依赖代码逻辑或外部 API 集成。  
- **当前限制**：Skill 仅支持同步式文件处理任务（输入为用户上传文件或结构化数据，输出为文件或结构化结果），**不支持**长时运行、流式响应、数据库直连或第三方服务调用。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` 根级字段 | 是 | Skill 全局唯一标识，仅允许小写字母、数字和连字符（如 `pdf-summarizer`）；重名上传将被拒绝。 |
| `description` | `SKILL.md` 根级字段 | 是 | **核心参数**：决定智能体是否触发该 Skill。必须明确说明适用输入类型、支持操作、典型触发关键词及明确排除的场景 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。描述模糊将导致高误触发率或漏触发。 |
| ZIP 包大小 | 上传时校验 | — | ≤ 10 MB；超限将直接失败，不进入审查流程。 |

> **注意**：文档中“官方 Skill 持续更新中”与实际控制台行为存在差异——部分旧版官方 Skill（如 `docx`）在控制台已下线但文档未同步标注弃用状态。建议以 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面实时列表为准。

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：无需创建，在 Skill 管理页直接使用。  
   - 自定义 Skill：准备 ZIP 包（含根目录 `SKILL.md`），在 **组件 > Skill 管理 > 自定义 Skill > 上传** 完成提交；审查约 2 分钟，通过后出现在自定义标签页。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击 **添加到智能体**，选择目标应用。  
   - 方式二：在智能体 **应用配置 > 技能** 区域点击 `+`，勾选所需 Skill。  
   > 添加后，智能体在对话中依据 `description` 语义匹配自动调用，**无需**在提示词中显式指令（如“请调用 xlsx Skill”）。

3. **测试与验证**  
   在应用配置页右侧对话窗格中发送典型请求（如 `把附件里的销售数据按季度汇总成表格`），观察是否生成预期文件。若未触发，优先检查 `description` 是否覆盖该触发意图。

## 限制和注意事项

- **版本管理**：官方 Skill 自动更新；自定义 Skill 更新需重新上传同名 ZIP 包，旧版本仍保留在历史记录中，但新部署的应用默认使用最新版。  
- **描述质量强依赖**：`description` 是 Skill 的唯一“接口契约”。示例中 xlsx Skill 的详尽描述（含支持格式、操作、触发词、排除场景）是最佳实践，简写如 `"处理 Excel 文件"` 将导致不可靠调用 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。  
- **调试手段有限**：无运行时日志或调用链追踪；若 Skill 未触发，仅能通过修改 `description` 并重新测试迭代优化。  
- **安全约束**：ZIP 包内禁止包含可执行文件（`.py`、`.sh` 等）、脚本或网络请求逻辑；所有处理均在平台沙箱内完成，无法访问外部资源。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


