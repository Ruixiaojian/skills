# skill

Skill 是百炼平台提供的可插拔能力包，用于扩展智能体在对话中自动处理特定任务的能力（如文件解析、数据清洗等），无需开发者编写集成代码。官方 Skill 开箱即用，自定义 Skill 支持通过 ZIP 包上传实现业务定制。其核心机制依赖 `SKILL.md` 中的语义描述驱动智能体自动识别与调用。

## 支持的模型/功能

Skill 本身不绑定特定大模型，而是作为独立于模型推理链路的“能力模块”，由智能体运行时根据用户意图和 `description` 语义匹配后动态调用。当前支持两类 Skill：

- **官方 Skill**：平台预置，覆盖常见场景（如 `xlsx`、`pdf-parser`、`csv-cleaner` 等），持续更新，无需配置即可添加使用。最新列表请参考 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面。  
- **自定义 Skill**：通过上传符合规范的 ZIP 包创建，适用于行业专属逻辑或非标格式处理。ZIP 包必须包含根目录下的 `SKILL.md` 文件，且整体大小 ≤10 MB。详情见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

> **注意**：官方 Skill 的具体能力范围未在文档中明确列出支持的模型类型（如是否兼容 Qwen 系列或第三方模型），仅说明其调用由智能体统一调度；实际兼容性以控制台 Skill 详情页中标注的「适用模型」为准，该字段在 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中未体现，建议以控制台实时信息为准。

## 关键参数

所有 Skill 的行为由 `SKILL.md` 中的两个必填字段定义：

- `name`：唯一标识符，仅允许小写字母、数字和连字符（如 `invoice-parser`），同一账号下不可重复。  
- `description`：决定 Skill 是否被触发的核心字段，**必须包含**：  
  - 输入类型（如 `.xlsx`, `.pdf`, JSON 数据流）；  
  - 支持操作（如“读取表格”、“提取发票金额”、“转换为 Markdown”）；  
  - 触发关键词（如“帮我整理表格”、“导出为 Excel”）；  
  - 明确排除场景（如“不处理 Word 文档”、“不生成 API 脚本”）。  

该字段质量直接影响调用准确率，示例详见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中 `xlsx` Skill 的完整描述。

## 使用方式

1. **创建 Skill**：  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面点击添加；  
   - 自定义 Skill：打包含 `SKILL.md` 的 ZIP，进入「组件 > Skill 管理 > 自定义 Skill」上传，审查通过后生效（约 2 分钟）。  

2. **添加到智能体**：  
   - 方式一：从 Skill 详情页点击「添加到智能体」；  
   - 方式二：在智能体「应用配置 > 技能」区域点击 `+` 号选择 Skill。  

3. **测试验证**：在应用配置页右侧对话窗格输入典型触发语句（如 `帮我把这张发票转成 Excel 表格`），观察是否自动调用并返回预期结果。

## 限制和注意事项

- ZIP 包总大小严格限制为 ≤10 MB，超限将导致上传失败；  
- `name` 字段全局唯一，重名上传会拒绝，而非覆盖；  
- 自定义 Skill 更新需重新上传 ZIP 包，系统自动创建新版本，已接入的应用**立即生效**（无需重启或手动切换）；  
- 官方 Skill 版本由平台统一升级，已添加的应用自动同步最新版；  
- `description` 中若未明确排除边界场景（如“不处理加密 PDF”），可能导致误触发——务必按规范撰写排除条款。  

如遇审查失败，请依据错误提示修改 `SKILL.md` 后重试；详细规范与示例请查阅 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


