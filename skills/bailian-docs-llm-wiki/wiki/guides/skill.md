# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，支持无需编码即可为智能体赋予文件处理、数据分析等专业功能。它通过语义匹配自动触发，开发者可选用平台预置的官方 Skill，或基于 ZIP 包定义自定义 Skill。所有 Skill 均需通过 `SKILL.md` 描述其能力边界，该描述直接影响智能体调用的准确性 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **官方 Skill**：由平台统一维护，覆盖常见文件处理场景（如 `.xlsx`、`.csv` 解析与生成），开箱即用，无需配置；版本更新后已添加的应用将自动升级 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。  
- **自定义 Skill**：通过上传符合规范的 ZIP 包创建，适用于行业定制需求（如特定格式发票解析、内部数据清洗流程）。其行为完全由 `SKILL.md` 中的 `description` 字段驱动，不依赖模型微调或 API 接入。  
- > **注意**：当前 Skill 机制**不依赖特定大模型底座**，而是作为独立于 LLM 推理链之外的任务路由与执行层；因此在应用配置中启用 Skill 后，无论选用 Qwen、GLM 还是其他支持模型，调用逻辑保持一致 —— 这与部分旧版文档中暗示“Skill 需配合特定模型版本使用”的说法存在矛盾，应以本说明为准。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` 根字段 | 是 | Skill 全局唯一标识，仅限小写字母、数字和连字符（如 `pdf-summarizer`）；重名将导致上传失败。 |
| `description` | `SKILL.md` 根字段 | 是 | **核心参数**：决定智能体是否触发该 Skill。必须明确包含输入类型、支持操作、典型触发词及排除场景，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的完整示例。 |
| ZIP 包大小 | 上传时校验 | — | ≤ 10 MB，超限将被拒绝。 |

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面查看并添加。  
   - 自定义 Skill：编写 `SKILL.md` → 打包为 ZIP（根目录含该文件）→ 控制台「组件 > Skill 管理 > 自定义 Skill」上传。审查约 2 分钟，通过后即可使用。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击「添加到智能体」，选择目标应用；  
   - 方式二：进入智能体「应用配置」→「技能」区域 → 点击 `+` 号选取 Skill。

3. **测试与验证**  
   在应用配置页右侧对话窗格中发送符合 `description` 触发条件的指令（如 `把附件里的销售数据转成带图表的 Excel`），观察是否自动调用并返回预期文件。

## 限制和注意事项

- **ZIP 包限制**：仅允许根目录下存在 `SKILL.md` 和必要执行资源（如 Python 脚本、配置文件），禁止嵌套子目录结构或可执行二进制文件；运行时沙箱环境不支持系统级命令调用。  
- **description 敏感性**：描述中若遗漏关键排除条件（如“不处理加密 PDF”），可能导致误触发；建议始终按规范包含“不适用场景”条目。  
- **版本管理**：官方 Skill 版本由平台控制，自定义 Skill 通过同名 ZIP 重传实现版本迭代；历史版本可在详情页「概览」标签中切换查看，但**已部署应用不会回滚至旧版本**，仅支持向前升级。  
- > **注意**：自定义 Skill 的 `description` 修改后必须重新上传 ZIP 包才能生效，仅编辑控制台中显示的文本描述无效 —— 此点与 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中“更新自定义 Skill”章节一致，但部分用户误以为可在 UI 端直接编辑 description，需特别规避。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


