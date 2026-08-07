# skill

Skill 是百炼平台提供的可插拔能力包，用于扩展智能体在对话中自动处理特定任务（如文件解析、数据清洗等）的能力，无需额外编码或工具集成。开发者可通过添加官方 Skill 或上传自定义 ZIP 技能包快速赋予智能体专业功能。其核心机制依赖 `SKILL.md` 中的语义描述驱动智能体自动识别与调用，因此描述质量直接影响调用准确性 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **官方 Skill**：平台预置、开箱即用，覆盖常见文件处理场景（如 `xlsx`、`pdf`、`csv` 等），由百炼统一维护和更新，已添加的智能体会自动升级至最新版本 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。  
- **自定义 Skill**：通过 ZIP 包上传实现，适用于行业定制需求（如专有格式解析、业务规则校验等）。ZIP 包必须包含根目录下的 `SKILL.md` 文件，并满足命名唯一性、10 MB 大小限制等要求 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。  
- 不支持直接对接外部 API 或运行任意代码；所有逻辑需封装于 ZIP 包内（含可执行脚本、依赖及元信息），由平台沙箱环境安全执行。

## 关键参数

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | Skill 唯一标识符，仅允许小写字母、数字和连字符（如 `invoice-parser`），不可与同账号下已有 Skill 重名。 |
| `description` | 是 | 决定智能体是否触发该 Skill 的核心依据。必须明确说明：① 输入类型（如 `.xlsx`, JSON 表格）；② 支持操作（如“清洗缺失值”“生成透视表”）；③ 典型触发关键词（如“整理表格”“导出为 Excel”）；④ 明确排除场景（如“不处理 PDF 文字提取”）——描述模糊将导致误调用或漏调用。 |

> **注意**：`description` 的编写规范直接影响 Skill 召回率，官方示例中对触发边界（如“deliverable must be a spreadsheet file”）和排除条件的严格声明是最佳实践，而非可选建议。

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面启用。  
   - 自定义 Skill：准备 ZIP 包（含合规 `SKILL.md`），进入控制台 **组件 > Skill 管理 > 自定义 Skill > 上传**，系统自动审查（约 2 分钟）。  

2. **添加到智能体**  
   - 方式一：在 Skill 详情页点击 **添加到智能体**，选择目标应用。  
   - 方式二：在智能体 **应用配置 > 技能** 区域，点击加号从列表中选取。  

3. **测试与验证**  
   - 在应用配置页右侧对话窗格输入典型用户指令（如“把附件里的销售数据按季度汇总成表格”），观察是否自动调用并返回预期结果（如生成 `.xlsx` 文件）。

## 限制和注意事项

- ZIP 包总大小 ≤ 10 MB，且 `SKILL.md` 必须位于根目录；缺失或格式错误将导致审查失败。  
- 自定义 Skill 更新需重新上传同名 ZIP 包，旧版本仍保留，但已部署的智能体会自动切换至新版本。  
- 官方 Skill 版本由平台控制，开发者无法修改其 `description` 或逻辑；若发现官方 Skill 行为与文档不符，应以 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的最新描述为准。  
- 当前不支持跨 Skill 协同调用（如先调用 `pdf` Skill 提取文本，再交由 `data-cleaner` Skill 处理），需在单个 Skill 内完成端到端逻辑。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


