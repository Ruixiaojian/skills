# application publishing and sharing

百炼平台支持将已构建的智能体应用（Agent 1.0）或工作流应用以多种方式对外发布与共享，包括 UI 应用、钉钉/微信机器人、可复用组件及音视频实时互动渠道。所有发布行为均需基于已发布的应用，并受 Agent 版本、业务空间隔离和权限模型约束。发布后的调用费用由应用创建者 UID 承担。

## 支持的模型/功能

- **仅限 Agent 1.0**：魔笔 UI 应用、钉钉机器人、微信公众号机器人、组件化发布、音视频实时互动等功能**全部仅支持 Agent 1.0 智能体应用**；Agent 2.0 应用不支持上述任何分享渠道，仅可通过 API 调用 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **组件来源广泛**：智能体应用和工作流应用均可发布为组件，供其他智能体或工作流引用 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **UI 设计器兼容性**：UI 应用可集成 Agent 1.0 或工作流应用，但要求 UI、API Key 与目标应用必须位于**同一业务空间** [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

> **注意**：文档 1 明确指出“Agent 2.0 仅支持通过 API 调用”，而文档 2 和文档 3 均未提及 Agent 2.0 对组件或 UI 的支持能力。三者一致确认 Agent 2.0 不参与任何 UI/渠道类发布流程，该限制为当前平台强制约束。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `query`（系统预设） | 用户输入文本主参数，类型为 `String`，默认必填 | 不可删除；若无需使用，须设为“不可见” |
| `imageList`（系统预设） | 图像公网地址数组，类型为 `Array<String>`，默认非必填 | 仅当组件使用视觉模型时生效；否则应设为“不可见” |
| `biz_param`（API 调用） | 用于透传业务参数，替代 `query` 或补充其他字段 | 仅在 API 调用时生效，UI/渠道类发布不支持此参数 |
| 传参方式（`业务透传` / `模型识别`） | 决定参数由调用方显式提供，还是由大模型从上下文推断 | 工作流中无论设置为何，均**必须显式传参**；智能体中 `模型识别` 方式才启用自动填充 |

## 使用方式

1. **UI 应用发布**  
   进入应用「发布渠道」页签 → 选择「UI 应用」→「创建」→ 自动填充基础信息（API Key、智能体等）→ 编辑后发布至开发/生产环境。开发环境链接 24 小时失效，生产环境需订阅付费套餐 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

2. **钉钉/微信机器人**  
   - 需先完成计算巢 AppFlow 授权（SLR + API Key 加密传输）；  
   - 钉钉需在开放平台创建应用、获取 Client ID/Secret、创建 AI 卡片模板并申请 `Card.Streaming.Write` 权限；  
   - 微信需在公众号后台获取 AppID 并完成授权；  
   - 配置完成后，复制回调地址（钉钉）或生成客服二维码（微信）供下游接入 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

3. **组件发布与引用**  
   - 发布：在「发布渠道」→「组件」→「创建」，配置名称、描述、参数别名、可见性及传参方式；  
   - 引用：智能体中作为技能添加；工作流中拖入「组件节点」并绑定输入变量（如 `系统变量/query`）；  
   - 注意：组件自动随源应用重新发布而更新，但禁止 A↔B 嵌套调用或 A→B→C 多级调用 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

4. **音视频实时互动**  
   仅支持图文类应用（智能体/工作流），需配置 API Key → 生成临时体验二维码（24 小时）→ 发布后开通智能媒体服务并授权 SLR → 可选 H5/APP 扫码或 SDK 集成（含快速集成与开发集成两种模式） [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

## 限制和注意事项

- **版本锁定**：Agent 2.0 应用完全不可用于 UI、钉钉、微信、组件、音视频等发布场景，该限制无例外。
- **业务空间强隔离**：UI 设计器、API Key、目标应用三者必须归属同一业务空间，否则无法关联或发布 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **组件调用风险**：嵌套调用（A↔B）必然导致死循环；三级及以上调用（A→B→C→…）易触发超时，建议单层组件调用。
- **权限与计费**：所有分享链接访问者默认为阿里云用户，费用由创建者 UID 承担；UI 生产环境发布需团队版及以上套餐，开发环境免费但链接时效仅 24 小时 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **工作流组件传参**：即使参数设为 `模型识别`，工作流中仍需上游节点显式提供输入值，该行为与文档 1 和文档 2 的描述完全一致，无矛盾。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


