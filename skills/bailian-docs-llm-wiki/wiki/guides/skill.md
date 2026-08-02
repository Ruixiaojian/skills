# skill

Skill 是百炼平台提供的可插拔能力包，用于扩展智能体在对话中自动处理特定任务的能力（如文件解析、数据清洗等），无需开发者编写集成代码。官方 Skill 开箱即用，自定义 Skill 支持通过 ZIP 包上传实现业务定制。其核心机制依赖 `SKILL.md` 中的语义描述驱动智能体自动识别与调用 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **官方 Skill**：平台预置、统一维护的通用能力，覆盖 `.xlsx`, `.csv`, `.pdf`, `.docx` 等常见格式的读写、转换、清洗等操作，无需配置即可添加使用。最新列表请参考控制台 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。
- **自定义 Skill**：通过上传符合规范的 ZIP 包实现，适用于行业专属逻辑（如发票结构化、医疗报告解析）。ZIP 包必须包含根目录下的 `SKILL.md` 文件，并满足命名唯一性、10 MB 大小限制等要求 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 关键参数

所有 Skill 的行为由 `SKILL.md` 中的 YAML 字段决定：
- `name`（必填）：唯一标识符，仅支持小写字母、数字和连字符（如 `invoice-parser`）。
- `description`（必填）：**决定调用准确性的核心字段**，需明确说明适用输入类型、支持操作、触发关键词及不适用场景。描述越精确，智能体匹配越可靠。

> **注意**：`description` 不是简单功能说明，而是供大模型推理的语义指令。示例中 xlsx Skill 明确排除“产出 Word 文档”等场景，避免误触发——此设计直接影响实际调用效果，不可省略 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 使用方式

1. **添加 Skill**  
   - 方式一：在 [Skill 管理](../../raw/application-user-guide/skill/introduction-to-skill.md) 页点击 Skill 卡片 → “添加到智能体” → 选择目标应用。  
   - 方式二：进入智能体应用的“应用配置” → “技能”区域 → 点击 Skill 右侧“+”号添加。

2. **测试效果**  
   在应用配置页右侧对话窗格中发送典型用户指令（如“把附件里的销售数据按季度汇总成表格”），观察是否自动调用对应 Skill 并返回预期结果（如生成 `.xlsx` 文件）。

3. **更新自定义 Skill**  
   修改本地 ZIP 包（含更新后的 `SKILL.md`）并重新上传同名包，审查通过后已接入该 Skill 的智能体将自动升级至新版本。

## 限制和注意事项

- ZIP 包总大小 ≤ 10 MB；`SKILL.md` 必须位于 ZIP 根目录。
- `name` 在当前账号下全局唯一，重复上传同名包会创建新版本而非覆盖。
- 官方 Skill 版本由平台自动更新，无需手动操作；自定义 Skill 需主动上传新 ZIP 包触发版本迭代。
- `description` 中若未明确排除不适用场景（如“不处理图片中的文字”），可能导致误触发——这是当前最常见的配置错误根源。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


