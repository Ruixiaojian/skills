# skill

Skill 是百炼平台提供的可插拔能力包，用于扩展智能体在对话中自动处理特定任务（如文件解析、数据清洗等）的能力，无需开发者编写集成代码或调用外部 API。官方 Skill 开箱即用，自定义 Skill 支持通过 ZIP 包上传实现业务定制。其核心机制依赖 `SKILL.md` 中的语义描述驱动智能体自动识别与调用，调用准确性高度依赖 description 的严谨性。

## 支持的模型/功能

Skill 本身不绑定特定大模型，而是作为独立于模型的“能力模块”被智能体调度。当前支持两类 Skill：

- **官方 Skill**：由平台预置并维护，覆盖常见场景（如 `xlsx`、`pdf`、`csv` 等文件处理），无需配置即可添加使用，详见 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面。  
- **自定义 Skill**：通过上传符合规范的 ZIP 包创建，适用于官方 Skill 未覆盖的垂直场景（如行业专用格式解析、私有协议处理等）。ZIP 包必须包含根目录下的 `SKILL.md` 文件，该文件定义 Skill 元信息与触发语义——具体格式要求见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)。

> **注意**：官方 Skill 的功能列表和行为可能随平台更新动态变化，控制台显示的最新列表为准；而自定义 Skill 的行为完全由 `SKILL.md` 中的 `description` 字段决定，[原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 明确指出该字段质量直接影响调用准确率，不可省略或模糊表述。

## 关键参数

所有 Skill 的核心参数均定义在 `SKILL.md` 中，仅含两个必填字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | Skill 唯一标识符，需小写英文+连字符（如 `invoice-parser`），且在同一账号下全局唯一。 |
| `description` | 是 | **最关键字段**：以自然语言描述 Skill 的适用输入类型、支持操作、典型触发关键词及明确排除的不适用场景。智能体据此进行语义匹配，详情参见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的完整示例。 |

ZIP 包本身无其他运行时参数；大小限制为 ≤10 MB，超限将导致上传失败。

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面点击“添加到智能体”；  
   - 自定义 Skill：按规范编写 `SKILL.md`，打包 ZIP 后在控制台 **组件 > Skill 管理 > 自定义 Skill** 中上传，系统自动审查（约 2 分钟）。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击“添加到智能体”，选择目标应用；  
   - 方式二：进入智能体 **应用配置 > 技能** 区域，点击加号从列表选取。

3. **测试与验证**  
   在应用配置页右侧对话窗格发送典型请求（如 `帮我清洗这份 Excel 表格中的重复行`），观察是否触发对应 Skill 并返回预期结果（如下载清洗后的文件）。

## 限制和注意事项

- **版本管理**：官方 Skill 更新后，已添加的应用自动生效新版本；自定义 Skill 需重新上传同名 ZIP 包以创建新版本，旧版本仍可回溯查看，但新调用默认使用最新版。
- **触发可靠性**：Skill 调用完全依赖 LLM 对 `description` 的理解，若描述存在歧义、遗漏关键触发词或未明确排除边界场景，易导致误触发或漏触发——务必严格遵循 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的 description 编写建议。
- **安全与合规**：自定义 Skill 的 ZIP 包在上传时会进行静态审查（如 `SKILL.md` 结构、文件路径合法性），但不执行沙箱运行时检测；用户需自行确保代码逻辑安全，避免引入恶意行为。
- **调试支持有限**：当前平台不提供 Skill 内部执行日志或中间状态输出，问题定位主要依赖 `description` 优化与对话样本测试。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


