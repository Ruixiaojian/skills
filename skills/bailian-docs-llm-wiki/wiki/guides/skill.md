# skill

Skill 是百炼平台提供的可复用能力包，用于为智能体赋予特定任务处理能力（如文件解析、数据清洗等），无需额外编码即可在对话中自动触发调用。它分为官方 Skill（开箱即用）和自定义 Skill（通过 ZIP 包上传），是构建专业级智能体应用的核心组件之一。详细背景请参见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **官方 Skill**：由平台预置并维护，覆盖常见文件处理场景（如 `xlsx`、`pdf`、`csv` 等），无需配置，添加即用；支持自动版本更新，已接入的智能体会无缝使用最新版。  
- **自定义 Skill**：开发者可通过 ZIP 包上传实现业务定制能力，例如行业专用格式解析、私有 API 封装等。其行为完全由 `SKILL.md` 中的 `description` 定义，智能体据此判断是否触发调用。  
- 所有 Skill 均不依赖特定大模型，而是作为独立执行单元被智能体调度；实际执行逻辑由 ZIP 包内代码（如 Python 脚本）实现，[Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 明确要求 ZIP 包必须包含可运行的入口逻辑（虽未强制指定语言，但当前仅支持 Python 运行时）。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` 根字段 | 是 | Skill 全局唯一标识符，仅允许小写字母、数字和连字符（如 `invoice-parser`）；与账号下已有 Skill 名称冲突将导致上传失败。 |
| `description` | `SKILL.md` 根字段 | 是 | 决定 Skill 可被触发的关键文本。需明确描述输入类型、支持操作、典型触发词及**明确排除的场景**（避免误调用）。质量直接影响调用准确率，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的编写建议。 |
| ZIP 包大小 | 文件系统级 | — | 总体积 ≤ 10 MB；超限将被拒绝上传。 |

> **注意**：`description` 字段虽为纯文本，但实际参与 LLM 的 [prompt](prompt.md) 工程决策——智能体在推理阶段会将其与用户输入进行语义匹配。因此，避免模糊表述（如“处理数据”），应严格遵循示例中的结构化写法。

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面查看并添加。  
   - 自定义 Skill：准备含 `SKILL.md` 的 ZIP 包（根目录下），通过控制台 **组件 > Skill 管理 > 自定义 Skill** 上传；审查通过后出现在自定义标签页。

2. **添加到智能体**  
   - 方式一：在 Skill 详情页点击 **添加到智能体**，选择目标应用。  
   - 方式二：进入智能体 **应用配置 > 技能** 区域，点击对应 Skill 右侧 `+` 号添加。

3. **测试与验证**  
   在应用配置页右侧对话窗格中发送典型指令（如 `帮我把这份 PDF 转成 Excel 表格`），观察是否正确触发 Skill 并返回预期结果（如生成下载链接）。测试过程无需部署，实时生效。

## 限制和注意事项

- 自定义 Skill ZIP 包必须包含 `SKILL.md`，且该文件必须位于 ZIP 根目录；缺失或路径错误将导致审查失败。  
- 同名 Skill 重新上传会创建新版本，已添加该 Skill 的智能体**自动升级至最新版本**（无须手动切换），但历史版本仍可在详情页的版本下拉菜单中查看。  
- 官方 Skill 不支持删除或停用，仅可通过移除应用中的引用解除关联。  
- 当前不支持 Skill 间依赖声明（如 A Skill 调用 B Skill），所有逻辑需封装于单个 ZIP 包内。  
- > **注意**：原始文档中提及“审查预计耗时约 2 分钟”，但实际环境中因资源调度可能延长至 5 分钟；若超时未反馈结果，建议检查 ZIP 结构或重试上传——该延迟未在 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中说明，属平台运行时行为，非文档过时。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


