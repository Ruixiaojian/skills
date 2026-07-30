# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可复用能力包，支持在不编写代码的前提下，让智能体自动识别并执行[文件处理](../concepts/file-processing.md)、数据分析等专业任务。Skill 分为平台预置的官方 Skill 和用户自主开发的自定义 Skill 两类，均通过语义描述驱动调用决策。其核心机制依赖于 `SKILL.md` 中的 `description` 字段对触发条件与能力边界的精准刻画，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **适用模型**：Skill 当前仅支持接入基于百炼大模型（如 Qwen 系列）构建的智能体应用，不适用于纯规则引擎或非百炼托管的推理服务。
- **核心功能**：
  - 自动识别用户意图与输入文件/数据特征，匹配最相关的 Skill；
  - 执行文件解析（如 PDF、Excel、CSV）、结构化数据清洗、格式转换、表格生成等操作；
  - 输出结果以文件形式返回（如 `.xlsx`、`.pdf`），不支持直接返回数据库写入、API 调用或外部系统状态变更；
  - 官方 Skill（如 `xlsx`、`pdf`）由平台统一维护，已内置优化的[文件处理](../concepts/file-processing.md)逻辑；自定义 Skill 的行为完全由 ZIP 包内代码与 `SKILL.md` 描述共同决定。

> **注意**：原始文档中提及“智能体根据 description 判断是否调用该 Skill”，但实际调用还依赖模型对输入上下文、附件 MIME 类型及历史对话状态的联合判断。单纯优化 `description` 不足以解决所有误触发问题，需结合测试反馈迭代——该细节在 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中未明确说明。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` 根级字段 | 是 | Skill 唯一标识符，须全小写+连字符（如 `invoice-parser`），不可与当前账号下任一 Skill 重名；名称变更即视为新 Skill。 |
| `description` | `SKILL.md` 根级字段 | 是 | 决定 Skill 可被调用的关键语义描述。必须包含适用输入类型、支持操作、典型触发关键词、明确的不适用场景（见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 示例）。 |
| ZIP 包大小 | 上传时校验 | — | ≤ 10 MB；超限将拒绝上传，且不提供分片或压缩提示。 |

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面添加，无需配置。  
   - 自定义 Skill：按规范编写 `SKILL.md`，打包全部依赖代码为 ZIP（根目录含 `SKILL.md`），通过控制台「组件 > Skill 管理 > 自定义 Skill」上传。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击「添加到智能体」，选择目标应用；  
   - 方式二：进入智能体「应用配置」→「技能」区域，点击 Skill 右侧 `+` 添加。

3. **测试与验证**  
   - 在应用配置页右侧对话窗格中发送典型指令（如 `帮我把这张发票图片转成 Excel 表格`），观察是否触发对应 Skill 并正确返回文件；  
   - 若未触发，优先检查 `description` 是否覆盖该场景关键词，再确认附件类型是否匹配。

## 限制和注意事项

- **版本更新**：官方 Skill 更新后，已添加的应用**自动生效最新版**；自定义 Skill 需重新上传同名 ZIP 包触发版本升级，旧版本不会被删除，但新调用默认使用最新版。
- **安全限制**：自定义 Skill 运行于沙箱环境，禁止访问外网、读写本地磁盘（除解压临时目录）、执行系统命令（如 `os.system`）或加载动态链接库（`.so`/`.dll`）。
- **调试盲区**：Skill 内部执行日志**不透出至智能体对话流或控制台实时日志**，仅可通过审查失败提示（如 `SKILL.md` 解析错误）或在 ZIP 包中预埋 `print()` 输出到标准输出（需配合平台日志审计权限查看）。
- **触发不确定性**：即使 `description` 描述完备，模型仍可能因上下文歧义或附件元信息缺失（如无文件扩展名）导致漏触发或误触发——建议始终在生产环境部署前，用至少 5 种不同表述+3 类边界输入组合进行回归测试。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)



