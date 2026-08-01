# skill

Skill 是百炼平台中可集成到智能体应用的能力单元，用于在对话中自动识别并执行特定任务（如文件处理、数据分析），无需开发者编写额外代码或对接外部工具。Skill 分为官方预置和用户自定义两类，通过声明式描述（`SKILL.md`）定义其能力边界与触发逻辑。其核心设计目标是提升智能体的任务泛化能力与专业场景适配性，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **官方 Skill**：平台预置、开箱即用，覆盖常见文件处理场景（如 `.xlsx`/`.csv` 解析、PDF 文本提取、图像 OCR 等），由百炼统一维护更新，已添加的 Skill 会自动升级至最新版本。  
- **自定义 Skill**：用户通过 ZIP 包上传实现，适用于官方未覆盖的业务需求（如行业专用格式解析、私有 API 封装等）。ZIP 包必须包含符合规范的 `SKILL.md`，且整体大小 ≤10 MB。详细要求见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

> **注意**：官方 Skill 的具体列表和能力范围以控制台 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面实时展示为准；文档中列举的格式（如 `.xlsm`, `.tsv`）仅为示例，实际支持范围可能随版本演进，需以最新控制台信息为准。

## 关键参数

所有 Skill 的行为由 `SKILL.md` 中的两个必填字段驱动：
- `name`：唯一标识符，仅允许小写字母、数字和连字符（如 `invoice-parser`），同一账号下不可重复。
- `description`：**最关键字段**，直接影响智能体调用准确性。必须明确说明：  
  - 输入类型（如 “仅处理 `.pdf` 文件”）；  
  - 支持操作（如 “提取文本、识别表格、生成摘要”）；  
  - 触发关键词（如 “转成文字”、“提取表格”）；  
  - **不适用场景**（如 “不处理扫描件模糊的 PDF”），避免误触发。  
完整编写规范及示例见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 使用方式

1. **添加 Skill**：  
   - 方式一：在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面点击 Skill 卡片 → **添加到智能体** → 选择目标应用；  
   - 方式二：进入智能体应用的 **应用配置** → **技能** 区域 → 点击 `+` → 从列表选择 Skill。  
2. **测试效果**：在应用配置页右侧对话窗格中输入典型用户指令（如 “把附件里的 Excel 表格按销售额排序”），观察是否自动调用对应 Skill 并返回预期结果。

## 限制和注意事项

- 自定义 Skill ZIP 包大小上限为 **10 MB**，超限将导致上传失败。  
- `description` 描述质量直接决定调用准确率；模糊或遗漏“不适用场景”易引发误触发，建议严格按示例结构编写。  
- 同名自定义 Skill 重新上传后，系统创建新版本，已接入该 Skill 的智能体会**自动切换至最新版本**，无需手动更新应用配置。  
- 官方 Skill 不支持修改 `description` 或 `name`，如需定制行为，应创建自定义 Skill 替代。  
- Skill 调用依赖智能体对用户意图的理解，若对话上下文不足或指令歧义，可能导致 Skill 未被触发——此时需优化 `description` 或引导用户提供更明确输入。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


