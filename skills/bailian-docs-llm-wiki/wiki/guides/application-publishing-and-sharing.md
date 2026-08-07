# application publishing and sharing

百炼平台支持将智能体（Agent 1.0）和工作流应用以多种方式发布与共享，包括生成可访问的 UI 应用、集成至钉钉/微信等第三方平台、封装为可复用组件、以及接入音视频实时互动场景。所有发布行为均需基于已创建并发布的应用，且不同渠道对应用类型、模型能力和参数配置有明确约束。

## 支持的模型/功能

- **仅限 Agent 1.0**：魔笔分享渠道、钉钉机器人、微信公众号、组件发布、音视频实时互动等功能**均不支持 Agent 2.0**，后者仅可通过 API 调用 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **UI 应用支持范围更广**：UI 设计器既支持智能体应用，也支持工作流应用，且可集成大模型、数据库、HTTP 服务及 MCP 工具 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **组件来源兼容性**：智能体应用和工作流应用均可发布为组件，并被其他智能体或工作流引用 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

> **注意**：文档 1 明确限定“分享渠道均为 Agent 1.0 功能”，而文档 2 和文档 3 均未提及 Agent 2.0 兼容性，但文档 2 的“快速开始”示例中使用了 `千问-Max-Latest`（属 Agent 2.0 常用模型），且未声明限制；实践中应以文档 1 的权威声明为准——**Agent 2.0 不支持任何 UI/渠道类发布能力，仅支持 API 调用**。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `query`（系统预设） | 必填 String 类型，传递用户原始输入文本 | 不可删除；在智能体中调用时，若设为“模型识别”，大模型将自动填充；在工作流中必须由上游节点显式传入 |
| `imageList`（系统预设） | 非必填 Array<String>，传递图像公网地址列表 | 仅当组件使用视觉模型时生效；可设为“是否可见=false”隐藏 |
| `biz_param`（API 调用） | 用于透传业务参数，覆盖“业务透传”类参数 | 仅在 API 调用时生效，测试界面需通过“入参变量配置”手动填写 |
| 回调地址 / [Token](../concepts/token.md) 有效期 / 分享链接 | 各渠道生成的访问凭证 | 钉钉/微信回调地址长期有效；UI 开发环境链接**24 小时失效**；音视频临时二维码有效期也为 24 小时 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) |

## 使用方式

1. **UI 应用发布**  
   - 进入应用「发布渠道」页签 → 选择「UI 应用」→ 「创建」→ 自动填充基础信息（API Key、智能体、图标等）→ 编辑后发布至开发/生产环境。  
   - 开发环境免费、24 小时有效；生产环境需订阅套餐并绑定自定义域名 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

2. **第三方平台集成（钉钉/微信）**  
   - 前置授权：首次需授权计算巢 AppFlow 的 SLR 角色及 API-KEY 加密传输权限。  
   - 钉钉：需在钉钉开放平台创建应用，获取 Client ID/Secret 及 AI 卡片模板 ID，并申请 `Card.Streaming.Write` 权限；百炼侧配置回调地址供钉钉机器人调用。  
   - 微信：需在微信公众号后台获取 AppID，并完成开发者授权；发布后生成客服二维码供扫码体验 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

3. **发布为组件**  
   - 在应用「发布渠道」页签 → 「组件」→ 「创建」→ 设置组件名称、描述、参数别名、是否必填/可见、传参方式（业务透传 or 模型识别）。  
   - 发布后可在其他智能体（作为技能）或工作流（作为组件节点）中引用；工作流中即使设为“模型识别”，也**必须显式传参** [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

4. **音视频实时互动**  
   - 仅支持图文对话类应用（智能体/工作流）→ 进入「AI实时互动」页签 → 配置 API Key → 生成临时二维码或分享链接（H5/APP 扫码）→ 或通过 SDK 集成（WEB/IOS/安卓） [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

## 限制和注意事项

- **Agent 版本硬限制**：Agent 2.0 应用**无法使用任何 UI 或渠道发布功能**，仅支持 API 调用；该限制在所有发布路径中均生效。
- **组件调用风险**：  
  - 禁止嵌套调用（A→B→A），会导致无限循环；  
  - 多级调用（A→B→C）易触发超时，因应用有最长运行时间限制 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **环境与权限隔离**：UI 设计器、API Key、智能体应用**必须归属同一业务空间**，否则无法关联 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **计费责任归属**：所有通过分享链接产生的模型调用、存储、带宽等费用，均由应用创建者 UID 账号承担 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **工作流中参数处理差异**：组件参数若设为“模型识别”，在工作流中**不会自动推断**，必须由上游节点提供值；此行为与智能体场景不同，需特别注意配置一致性 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


