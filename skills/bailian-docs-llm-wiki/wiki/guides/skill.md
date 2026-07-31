# skill

Skill 是百炼平台提供的可插拔能力包，用于扩展智能体在对话中自动处理特定任务的能力（如文件解析、数据清洗等），无需开发者编写集成代码。官方 Skill 由平台预置并维护，自定义 Skill 则通过符合规范的 ZIP 包上传实现。其核心机制依赖 `SKILL.md` 中的 `description` 字段驱动智能体的调用决策，因此描述质量直接影响任务匹配准确率。

## 支持的模型/功能

- **官方 Skill**：覆盖常见文件处理场景（如 `.xlsx`, `.csv`, `.pdf` 解析与生成），由平台统一维护，添加后即用，版本自动更新。最新列表请参考 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面，详情见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。
- **自定义 Skill**：支持 ZIP 包形式上传，适用于行业专属逻辑（如定制发票解析、私有格式日志提取）。必须包含根目录下的 `SKILL.md` 文件，并满足命名唯一性、10 MB 大小限制等要求，详见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

> **注意**：官方 Skill 不支持用户修改其 `description` 或行为逻辑；自定义 Skill 的 `description` 可通过重新上传 ZIP 包更新，但历史版本不可编辑——此行为与 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中“更新自定义 Skill”章节一致，无矛盾。

## 关键参数

所有 Skill 的行为由 `SKILL.md` 中的两个必填字段定义：
- `name`：唯一标识符，仅允许小写字母、数字和连字符（如 `invoice-parser`），重复名称将导致上传失败。
- `description`：YAML 字段，**决定智能体是否触发该 Skill**。必须明确说明：  
  - 输入类型（如 `.xlsx`, JSON API 响应）；  
  - 支持操作（如“读取第3列求和”“导出为 CSV”）；  
  - 触发关键词（如“帮我整理表格”“转成 Excel”）；  
  - **不适用场景**（如“不处理 Word 文档”“不调用外部 API”），避免误触发。  
  官方 xlsx Skill 的完整示例见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 使用方式

1. **添加 Skill**：  
   - 方式一：在 [Skill 管理](../../raw/application-user-guide/skill/introduction-to-skill.md) 页面点击 Skill 卡片 → “添加到智能体” → 选择目标应用；  
   - 方式二：进入智能体应用的“应用配置” → “技能”区域 → 点击 Skill 右侧加号 → 从列表选择。  
2. **测试效果**：在应用配置页右侧对话窗格输入典型指令（如“把附件里的销售数据按季度汇总成表格”），观察是否自动调用对应 Skill 并返回预期结果（如生成 `.xlsx` 文件）。

## 限制和注意事项

- ZIP 包总大小 ≤ 10 MB，且必须包含 `SKILL.md`（路径为 ZIP 根目录）；  
- 自定义 Skill 审查耗时约 2 分钟，失败时需根据错误提示修改 `SKILL.md` 后重传；  
- 同名 Skill 重新上传会创建新版本，已接入该 Skill 的智能体**自动升级至最新版**（官方 Skill 同理）；  
- `description` 中若未明确排除边界场景（如“不处理图片中的表格”），可能导致误触发——强烈建议按规范补充“不适用场景”；  
- Skill 仅在智能体启用“自动工具调用”模式下生效，需确认应用配置中未禁用该能力。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


