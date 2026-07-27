# skill

Skill 是百炼平台提供的可插拔能力包，用于扩展智能体在对话中自动处理特定任务的能力（如文件解析、数据清洗等），无需开发者编写集成代码。通过官方 Skill 或自定义 ZIP 技能包，智能体可根据用户意图自动识别并调用匹配的 Skill。其核心依赖于 `SKILL.md` 中声明的语义描述，由模型动态决策是否触发。

## 支持的模型/功能

Skill 本身不绑定具体大模型，而是作为能力抽象层被所有支持智能体编排的模型（如 Qwen 系列、Baichuan 等）统一调用。当前支持两类 Skill：
- **官方 Skill**：平台预置、开箱即用，覆盖 `.xlsx`, `.csv`, `.pdf`, `.docx` 等常见格式的读写与转换，持续更新，详见 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面；  
- **自定义 Skill**：通过上传 ZIP 包实现业务定制，需严格遵循 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中定义的结构规范。  
> **注意**：部分旧版文档提及“仅支持 Qwen-72B 调用 Skill”，该说法已过时；实际所有启用智能体编排能力的模型均支持 Skill 调用，以 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 为准。

## 关键参数

自定义 Skill 的行为完全由 ZIP 包根目录下的 `SKILL.md` 决定，关键字段如下：
- `name`（必填）：唯一标识符，仅允许小写字母、数字和连字符（如 `invoice-parser`）；  
- `description`（必填）：决定模型是否触发该 Skill 的核心依据，必须包含：  
  - 输入类型（如 “`.pdf` 文件”）；  
  - 支持操作（如 “提取文本、识别表格、生成摘要”）；  
  - 触发关键词（如 “帮我读一下这个合同”）；  
  - 明确排除场景（如 “不处理扫描件 OCR 失败的文件”）。  
完整示例见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中 xlsx Skill 的 `SKILL.md`。

## 使用方式

1. **创建**：  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面添加；  
   - 自定义 Skill：打包含 `SKILL.md` 的 ZIP（≤10 MB），在控制台 **组件 > Skill 管理 > 自定义 Skill** 上传；  
2. **添加到智能体**：  
   - 方式一：从 Skill 详情页点击 **添加到智能体**；  
   - 方式二：在目标应用的 **应用配置 > 技能** 区域点击加号选择；  
3. **测试**：在应用配置页右侧对话窗格输入典型指令（如 “把附件里的销售数据转成图表”），观察是否自动调用并返回预期结果。

## 限制和注意事项

- ZIP 包大小上限为 10 MB，超限将导致审查失败；  
- `name` 在同一账号下全局唯一，重复上传同名包会创建新版本（旧版本仍可用，但新添加的智能体默认使用最新版）；  
- `description` 描述质量直接影响调用准确率：模糊或遗漏排除条件易导致误触发；  
- 官方 Skill 版本由平台自动升级，已添加的应用即时生效；自定义 Skill 需手动重新上传 ZIP 才能更新；  
- Skill 不支持嵌套调用（即一个 Skill 内部不能调用另一个 Skill）。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


