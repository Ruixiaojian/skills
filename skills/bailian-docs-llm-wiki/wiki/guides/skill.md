# skill

Skill 是百炼平台提供的可复用能力包，用于扩展智能体在对话中自动处理特定任务的能力（如文件解析、数据清洗等），无需额外编码即可集成。开发者可通过官方 Skill 快速启用通用能力，或通过自定义 ZIP 包构建业务专属 Skill。Skill 的调用由智能体根据 `SKILL.md` 中的 `description` 自动触发，其准确性高度依赖描述的严谨性。

## 支持的模型/功能

- **官方 Skill**：平台预置、开箱即用的通用能力，覆盖 `.xlsx`/`.csv`/`.pdf` 等常见文件格式的读写、转换与清洗等操作，由平台统一维护和更新。最新列表请参考 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面。  
- **自定义 Skill**：通过上传符合规范的 ZIP 包实现，适用于官方未覆盖的垂直场景（如行业专用报表解析、私有协议文件处理等）。ZIP 包必须包含根目录下的 `SKILL.md` 文件，且整体大小 ≤10 MB。详细要求见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。  
- 所有 Skill 均不依赖特定大模型底座，调用逻辑由百炼运行时统一调度，与底层模型解耦。> **注意**：部分旧版文档提及“Skill 需绑定特定模型版本”，该说法已过时；实际使用中 Skill 可被任意支持 Skill 调用的模型（如 Qwen 系列、Baichuan 系列）调用，详见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 关键参数

- `name`（必填）：Skill 唯一标识符，仅允许小写字母、数字和连字符（如 `invoice-parser`），同一账号下不可重复。  
- `description`（必填）：决定 Skill 是否被触发的核心字段。必须明确说明**适用输入类型**、**支持操作**、**典型触发关键词**及**明确排除的场景**。描述模糊将导致误触发或漏触发。完整编写规范与示例见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。  
- 版本控制：每次重新上传同名 ZIP 包即生成新版本；官方 Skill 自动更新，自定义 Skill 需手动重传以生效。

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面点击添加。  
   - 自定义 Skill：按规范编写 `SKILL.md` 并打包为 ZIP，进入 **组件 > Skill 管理 > 自定义 Skill** 上传，系统约 2 分钟完成审查。  

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击 **添加到智能体**，选择目标应用。  
   - 方式二：在智能体 **应用配置 > 技能** 区域点击加号，勾选所需 Skill。  

3. **验证效果**  
   在应用配置页右侧对话窗格中输入典型触发语句（如 `把这份 CSV 按销售额排序并导出为 Excel`），观察是否自动调用对应 Skill 并返回预期结果。

## 限制和注意事项

- ZIP 包大小上限为 10 MB，超限将拒绝上传。  
- `description` 中若未明确排除不适用场景（如“不产出 Word 文档”），可能导致智能体在错误上下文中调用 Skill。务必参照 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的完整示例编写。  
- 自定义 Skill 审查失败时，需根据控制台提示修改 `SKILL.md` 后重新上传；常见错误包括 `name` 冲突、`description` 缺失或 YAML 格式错误。  
- 已添加的 Skill 在智能体中实时生效，但历史对话记录不会回溯重执行；新对话将基于最新版本 Skill 运行。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


