# application publishing and sharing

百炼平台支持将智能体应用（Agent 1.0）和工作流应用以多种方式发布与共享，包括 UI 应用、钉钉/微信机器人、可复用组件及音视频实时互动渠道。该能力面向开发者提供标准化的集成路径，便于将 AI 能力嵌入业务系统或终端用户场景。**Agent 2.0 应用不支持除 API 调用外的任何分享渠道**，此限制贯穿所有发布方式。

## 支持的模型/功能

- **适用应用类型**：仅限 **Agent 1.0 智能体应用** 和 **工作流应用**；Agent 2.0 仅支持 API 调用，[不支持魔笔分享、钉钉、微信、组件或音视频互动等渠道](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **UI 应用**：基于魔笔低代码平台构建网页界面，支持拖放式编辑、数据库集成与多端适配（PC/H5），详见 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **第三方平台集成**：支持发布为钉钉机器人、微信公众号客服，需分别配置钉钉 Client ID/Secret/模板 ID 及微信 AppID，并完成计算巢 AppFlow 授权。
- **组件化复用**：智能体或工作流可发布为组件，供其他智能体（作为工具）或工作流（作为节点）引用，支持 `query` 和 `imageList` 等预设系统参数，[详细参数规则见组件配置文档](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **音视频实时互动**：仅支持图文类应用（智能体/工作流），提供 H5/APP 扫码体验与 SDK 集成两种方式，依赖 AICallKit。

> **注意**：文档 1 明确指出“Agent 2.0 仅支持通过 API 调用”，而文档 2 和文档 3 均未提及 Agent 2.0 的任何发布能力。三者一致确认 Agent 2.0 不参与本主题所述的 UI、组件、钉钉/微信等发布流程，无矛盾。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `query`（String，必填） | 用户输入文本，由系统自动注入；在组件中不可删除，可通过“是否可见”隐藏 | [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| `imageList`（Array<String>，非必填） | 图像公网地址列表，仅当组件使用视觉模型时生效；同样不可删除 | 同上 |
| `biz_param` | API 调用时传入业务透传参数的字段名，用于覆盖组件中“业务透传”类参数 | [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) 中测试说明部分 |
| 回调地址 / [Token](../concepts/token.md) 有效时间 / 分享 ID | 钉钉/微信/音视频渠道的核心交付物，用于下游平台配置机器人或 SDK 集成 | 文档 1 中各渠道配置章节 |

## 使用方式

1. **入口统一**：所有发布操作均从百炼控制台 **[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)** 页面的目标应用卡片进入，点击 **发布** 或切换至对应页签（如“发布平台”、“AI实时互动”、“组件”）。
2. **UI 应用**：  
   - 方式一：从已有应用发布 → 选择“UI应用” → 自动填充基础信息（API Key、智能体、图标等）→ 编辑并发布；  
   - 方式二：独立创建 → 进入 [UI设计器](https://bailian.console.aliyun.com/?tab=app#/app-ui) → 选模板 → 配置 API Key 与智能体 → 拖放编辑 → 发布至开发/生产环境。  
   > 开发环境链接 **24 小时失效**，生产环境需订阅付费套餐并绑定自定义域名，详见 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
3. **组件发布**：  
   - 在应用发布流程中勾选“发布应用组件”，或在“发布渠道”页签单击“组件”区域的 **+ 创建**；  
   - 必填组件名称、描述，配置 `query`/`imageList` 等参数的别名、可见性、传参方式（“业务透传”或“模型识别”）；  
   - 在智能体中作为技能引用，在工作流中作为节点拖入并连接上游数据。
4. **钉钉/微信**：  
   - 首次需授权计算巢 AppFlow（SLR + API Key 加密传输）；  
   - 钉钉需提前在开放平台创建应用、获取 Client ID/Secret、创建 AI 卡片模板并申请 `Card.Streaming.Write` 权限；微信需在公众号后台获取 AppID；  
   - 百炼侧配置完成后，复制回调地址（钉钉）或生成二维码（微信）交付下游平台配置。

## 限制和注意事项

- **Agent 版本限制**：所有非 API 渠道（UI、钉钉、微信、组件、音视频）**仅支持 Agent 1.0**，Agent 2.0 应用无法使用，[原文明确强调此前提](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **组件调用风险**：  
  - 禁止嵌套调用（A→B→A），会导致无限循环；  
  - 多级调用（A→B→C）易触发超时，因应用有最长运行时间限制；  
  - 工作流中即使设置“模型识别”，也**必须显式传参**，不会自动推断（与智能体行为不同）。
- **环境与权限**：  
  - UI 应用、API Key、目标智能体/工作流 **必须归属同一业务空间**，否则无法关联；  
  - UI 开发环境链接 24 小时后失效，生产环境需付费订阅；  
  - 默认分享链接仅限阿里云用户访问，如需匿名访问需在 UI 设计器中单独配置权限组。
- **计费责任**：所有通过分享链接产生的模型调用、存储、带宽等费用，均由应用创建者 UID 账号承担。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


