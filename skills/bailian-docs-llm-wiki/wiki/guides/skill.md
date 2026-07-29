# skill

Skill 是百炼平台提供的可插拔能力包，用于扩展智能体在对话中自动处理特定任务的能力（如文件解析、数据清洗等），无需开发者编写集成代码。通过官方 Skill 或自定义 ZIP 技能包，智能体可根据用户输入语义自动识别并调用匹配的 Skill。该机制依赖 `SKILL.md` 中的 `description` 字段进行意图匹配，描述质量直接影响调用准确率。

## 支持的模型/功能

Skill 本身不依赖特定大模型，而是作为独立于模型推理层的工具能力模块，由智能体调度引擎统一调用。当前支持两类 Skill：

- **官方 Skill**：平台预置、开箱即用，覆盖 `.xlsx`/`.csv`/`.pdf` 等常见格式的读写、转换与清洗任务，持续更新，详情见 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面。  
- **自定义 Skill**：通过上传符合规范的 ZIP 包实现，适用于行业定制场景（如医疗报告解析、合同条款提取）。ZIP 包必须包含根目录下的 `SKILL.md` 文件，且整体大小 ≤10 MB —— 具体要求详见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

> **注意**：官方 Skill 的功能列表和触发逻辑可能随版本迭代调整，实际行为以控制台最新文档为准；自定义 Skill 的 `description` 字段若未明确排除边界场景（如“不产出 HTML”），可能导致误触发 —— 建议严格参照 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的编写示例。

## 关键参数

所有 Skill 的核心元信息均定义在 `SKILL.md`（YAML 格式）中，仅两个必填字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | Skill 唯一标识符，需小写字母+连字符（如 `invoice-parser`），同一账号下不可重复。 |
| `description` | 是 | 决定智能体是否调用该 Skill 的关键文本。必须包含：适用输入类型、支持操作、典型触发关键词、**明确的不适用场景**（避免误调用）。质量直接影响召回与精度 —— 详细规范见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。 |

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面启用。  
   - 自定义 Skill：打包含 `SKILL.md` 的 ZIP，通过控制台「组件 > Skill 管理 > 自定义 Skill」上传；审查通过后自动生效。

2. **添加到智能体**  
   - 方式一：在 Skill 详情页点击「添加到智能体」，选择目标应用。  
   - 方式二：进入智能体「应用配置」→「技能」区域，点击对应 Skill 右侧的 `+` 添加。

3. **测试与验证**  
   在应用配置页右侧对话窗格发送典型指令（如 `把附件里的销售数据转成带图表的 Excel`），观察是否自动调用并返回预期结果（如 `.xlsx` 文件下载链接）。

## 限制和注意事项

- 自定义 Skill ZIP 包大小上限为 **10 MB**，超限将拒绝上传。  
- `name` 字段全局唯一（同账号内），重名上传会失败，需修改 `SKILL.md` 后重试。  
- 官方 Skill 版本由平台统一升级，已添加的应用**自动使用最新版**；自定义 Skill 需重新上传同名 ZIP 才能更新版本，旧版本仍保留在历史记录中。  
- `description` 中若缺失“不适用场景”说明（例如未声明“不处理图像内容”），可能导致智能体在 PDF 图文混排场景下错误调用文本解析 Skill —— 此类问题已在 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 的示例中重点强调，务必复用其结构化写法。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


