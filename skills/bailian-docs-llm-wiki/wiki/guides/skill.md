# skill

Skill 是百炼平台提供的可插拔能力包，用于扩展智能体在对话中自动处理特定任务（如文件解析、数据清洗等）的能力，无需额外编码或工具集成。开发者可通过官方 Skill 快速启用通用功能，或通过自定义 ZIP 技能包实现业务定制化能力。所有 Skill 均由智能体根据 `description` 语义自动触发调用，其准确性高度依赖元信息描述质量。

## 支持的模型/功能

Skill 本身不依赖特定大模型，而是作为独立于模型推理流程的“能力模块”被智能体调度。当前支持两类 Skill：
- **官方 Skill**：平台预置、统一维护的通用能力，覆盖 `.xlsx`/`.csv`/`.pdf` 等常见格式的读写、转换与清洗，详情见 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面；完整说明请参阅 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。
- **自定义 Skill**：通过上传 ZIP 包实现，适用于行业专属逻辑（如医疗报告结构化解析、金融报表校验），需严格遵循 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中定义的 SKILL.md 规范与 ZIP 结构约束。

> **注意**：官方 Skill 的功能列表和触发逻辑可能随平台更新动态调整，而自定义 Skill 的行为完全由其 `description` 字段决定——该字段是智能体调用决策的唯一依据，而非代码逻辑。因此，务必参考 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的 description 编写建议，避免因描述模糊导致误触发或漏触发。

## 关键参数

仅 `SKILL.md` 文件中的两个 YAML 字段为必填且生效：
- `name`：全局唯一标识符，仅支持小写字母、数字和连字符（如 `invoice-parser`），不可与同账号下已有 Skill 名称重复；
- `description`：纯文本字段，必须明确包含四类信息：适用输入类型、支持操作、触发关键词、不适用场景。该字段直接影响智能体调用准确率，是 Skill 行为的“契约声明”。

ZIP 包本身无其他配置参数，但受以下硬性约束：
- 整包体积 ≤ 10 MB；
- 根目录必须存在且仅有一个 `SKILL.md`；
- 不支持嵌套子目录以外的任意执行环境（如 Python 运行时、Docker 镜像等）。

## 使用方式

1. **创建**：
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面点击“添加到智能体”；
   - 自定义 Skill：按 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 要求编写 `SKILL.md` 并打包 ZIP，进入控制台 **组件 > Skill 管理 > 自定义 Skill** 上传。

2. **绑定**：
   - 方式一：在 Skill 详情页点击“添加到智能体”，选择目标应用；
   - 方式二：进入目标智能体的 **应用配置 > 技能** 区域，点击“+”从列表中选取。

3. **测试**：在应用配置页右侧对话窗格输入典型用户指令（如“把附件里的销售数据转成 Excel 并按季度汇总”），观察是否自动调用并返回预期结果。

## 限制和注意事项

- 自定义 Skill 无沙箱执行环境，所有逻辑必须由百炼平台内置能力（如文件解析引擎、表格计算服务）完成，**不支持上传可执行二进制或运行任意代码**；
- 官方 Skill 版本更新后，已绑定的智能体会自动升级，但自定义 Skill 必须手动重新上传 ZIP 才能生效；
- `description` 中若未明确排除某类场景（如“不处理图片中的表格”），智能体可能在不符合预期的输入下错误触发；
- 单个智能体最多绑定 50 个 Skill（含官方与自定义），超出需移除未使用项；
- ZIP 审查失败时，错误提示仅反馈 `SKILL.md` 格式或字段缺失问题，不校验业务逻辑正确性——开发者需自行验证描述与实际能力的一致性。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


