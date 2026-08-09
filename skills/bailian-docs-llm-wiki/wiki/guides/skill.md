# skill

Skill 是百炼平台提供的可插拔能力包，用于扩展智能体在对话中自动处理特定任务的能力（如文件解析、数据清洗等），无需开发者编写集成代码。官方 Skill 由平台预置并维护，自定义 Skill 则通过符合规范的 ZIP 包上传实现。其核心机制依赖 `SKILL.md` 中的语义描述驱动智能体自动识别与调用，因此描述质量直接影响调用准确率 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **官方 Skill**：覆盖常见文件处理场景（如 `xlsx`、`pdf`、`csv` 等），开箱即用，无需配置，版本由平台统一更新 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。  
- **自定义 Skill**：支持用户上传 ZIP 包实现业务定制能力，适用于行业专属格式解析、私有 API 封装等场景。ZIP 包必须包含根目录下的 `SKILL.md` 文件，且整体大小 ≤ 10 MB [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。  
- **不支持模型绑定**：Skill 本身不关联或依赖特定大模型，其调用由智能体运行时根据 `description` 的语义匹配触发，与底层模型无关。

## 关键参数

所有 Skill 的行为由 `SKILL.md` 中的两个必填字段定义：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | Skill 唯一标识符，仅允许小写字母、数字和连字符（如 `invoice-parser`），同一账号下不可重名。 |
| `description` | 是 | 决定 Skill 是否被调用的核心字段。需明确说明：① 输入类型（如 `.xlsx`, JSON）；② 支持操作（如“读取、计算公式、导出为 CSV”）；③ 触发关键词（如“整理表格”、“生成报表”）；④ **不适用场景**（如“不处理 PDF 表单填写”），避免误触发。 |

> **注意**：`description` 不是 UI 展示文案，而是供智能体推理的语义指令。模糊或遗漏排除条件将导致高频误调用——参考 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中 xlsx Skill 的完整示例，其明确排除了产出 Word/HTML/Python 脚本等场景。

## 使用方式

1. **添加 Skill**  
   - 方式一：在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面点击 Skill 卡片 → “添加到智能体” → 选择目标应用。  
   - 方式二：进入智能体应用的 **应用配置** → 左侧“技能”区域 → 点击 `+` → 从列表勾选。  

2. **测试验证**  
   在应用配置页右侧对话窗格中发送典型请求（如 `把附件里的销售数据按季度汇总成表格`），观察是否触发对应 Skill 并返回预期结果（如生成 .xlsx 文件）。  

3. **更新自定义 Skill**  
   修改本地 ZIP 包内 `SKILL.md`（尤其优化 `description`）后，重新上传同名包即可创建新版本；已接入该 Skill 的智能体将自动使用最新版。

## 限制和注意事项

- **审查机制**：自定义 Skill 上传后需约 2 分钟人工/自动审查，失败时需根据提示修正 `SKILL.md` 后重传。  
- **名称冲突**：同一账号下 `name` 全局唯一，重复上传同名包会创建新版本，但不会覆盖旧版历史记录。  
- **无状态执行**：Skill 运行时不保留上下文或用户会话状态，每次调用均为独立任务。  
- **调试建议**：若 Skill 未被触发，优先检查 `description` 是否缺失触发关键词或未排除干扰场景；若被误触发，需强化 `description` 中的否定条件表述。  
- **版本回滚**：官方 Skill 版本不可手动回退；自定义 Skill 可通过详情页的版本下拉框查看历史版本，但无法一键降级至旧版——需重新上传对应 ZIP 包。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


