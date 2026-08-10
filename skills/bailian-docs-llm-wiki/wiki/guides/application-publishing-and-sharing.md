# application publishing and sharing

百炼平台支持将已发布的智能体应用（Agent 1.0）或工作流应用以多种方式对外共享与集成，包括 UI 应用、钉钉/微信机器人、可复用组件、音视频实时互动等。所有发布行为均需基于已发布的应用实例，并受 Agent 版本、业务空间隔离及权限模型约束。开发者应根据目标场景选择适配的发布方式，并注意各渠道对模型能力、参数传递和运行时限制的差异化要求。

## 支持的模型/功能

- **仅限 Agent 1.0**：魔笔 UI 应用、钉钉机器人、微信公众号、组件化发布、音视频实时互动等功能**全部仅支持 Agent 1.0 智能体应用**；Agent 2.0 应用不支持上述任何分享渠道，仅可通过 API 调用 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **工作流应用支持有限**：UI 应用和音视频实时互动支持工作流应用（图文类），但钉钉/微信机器人、组件发布**仅支持智能体应用作为源**（工作流可作为被引用的组件，见下文）；[原文标题](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) 明确说明工作流应用可“发布为组件”并被其他工作流或智能体引用。
- **UI 设计器兼容性**：UI 应用可集成智能体应用或工作流应用，但二者必须与 UI 设计器位于**同一业务空间**，且需配置匹配的 API Key [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

> **注意**：文档 1 称“分享渠道均为 Agent 1.0 功能”，而文档 2 明确允许工作流应用“发布为组件”并在工作流中引用；文档 3 则指出 UI 应用可绑定工作流应用。三者无本质矛盾，但需明确：**Agent 1.0 是分享渠道的唯一源头，工作流仅作为被集成方（UI/组件）存在，不可直接发布为钉钉/微信机器人**。

## 关键参数

| 参数 | 说明 | 约束与注意事项 |
|------|------|----------------|
| `API Key` | 所有外部渠道（钉钉、微信、音视频、UI）均需绑定有效的百炼 API Key | 必须与应用、UI 同属一个业务空间；未创建时需先在 [我的API-KEY](https://bailian.console.aliyun.com/?tab=app#/api-key) 页面创建 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |
| `query` / `imageList` | 组件预设系统参数，不可删除 | `query` 类型为 `String`，建议设为必填；`imageList` 类型为 `Array<String>`，仅当组件使用视觉模型时生效；非必需参数应设为“是否可见=否” [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| 传参方式（`业务透传` vs `模型识别`） | 决定参数值由调用方显式提供，还是由大模型从上下文推断 | 在工作流中引用组件时，即使设为“模型识别”，**也不会自动推断**，必须由上游节点显式传入；仅在智能体中启用模型识别才有效 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |
| 回调地址 / 分享链接 / [Token](../concepts/token.md) 有效期 | 钉钉/微信/音视频/临时体验等渠道的核心访问凭证 | 钉钉回调地址需配置到钉钉机器人 HTTP 模式；音视频临时二维码有效期为 24 小时；H5 分享链接可设置 [Token](../concepts/token.md) 有效时间 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |

## 使用方式

1. **UI 应用（魔笔）**  
   - 进入应用「发布渠道」页签 → 选择「UI 应用」→ 「创建」→ 自动填充基础信息（API Key、智能体、图标等）→ 发布至开发环境（24 小时有效）或生产环境（需订阅套餐）→ 获取应用地址分享 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。  
   - *补充*：开发环境免费，生产环境需绑定自定义域名并订阅团队版及以上套餐。

2. **钉钉/微信机器人**  
   - 前置授权：首次需授权计算巢 AppFlow（SLR + API Key 加密传输）；  
   - 配置依赖：钉钉需提前在开放平台创建应用、获取 Client ID/Secret、创建 AI 卡片模板并申请 `Card.Streaming.Write` 权限；微信需获取公众号 AppID 并完成授权；  
   - 百炼侧操作：在「发布平台」页签选择对应渠道 → 选 API Key → 填写平台凭证 → 获取回调地址（钉钉）或二维码（微信）→ 用户按指引配置机器人或扫码接入 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

3. **组件化发布与引用**  
   - 发布：在应用「发布渠道」→ 「组件」→ 「创建」，填写组件名称、描述，配置 `query`/`imageList` 等参数的别名、可见性、传参方式及默认值；  
   - 引用：  
     - *智能体中*：在「技能」中选择已发布组件，大模型根据描述+上下文自动触发（模型识别）或由用户/调用方传参（业务透传）；  
     - *工作流中*：拖入「组件节点」→ 选择组件 → 显式连接上游节点输出至 `query` 等参数 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

4. **音视频实时互动**  
   - 仅支持图文类应用（智能体/工作流）；  
   - 进入「AI 实时互动」页签 → 配置 API Key → 生成 24 小时临时体验码 → 测试通过后「发布」→ 开通智能媒体服务并授权 SLR → 选择 H5/APP 扫码 或 SDK 集成（含快速集成与开发集成） [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

## 限制和注意事项

- **Agent 版本硬限制**：Agent 2.0 应用**完全不可用于任何分享渠道**，仅支持 API 调用；迁移前务必确认版本 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。  
- **嵌套与多级调用风险**：A 调用 B 且 B 又调用 A 会导致死循环；A→B→C 的三级调用易因总超时（默认 60s）失败；建议单层调用或严格控制链路深度 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。  
- **业务空间隔离**：API Key、智能体/工作流应用、UI 设计器必须归属同一业务空间，否则无法关联或发布 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。  
- **工作流中组件参数强制显式传入**：即使配置为“模型识别”，工作流引擎也不会自动解析上下文填充参数，必须由上游节点明确赋值，否则运行时报错 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。  
- **开发环境时效性**：UI 应用开发环境链接、音视频临时体验码均**24 小时失效**，生产环境需付费订阅；文件存储与数据库超出免费额度（1GB 文件 / 0.3GB DB）后按量计费 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


