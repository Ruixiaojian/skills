# application publishing and sharing

百炼平台支持将智能体应用（Agent 1.0）和工作流应用以多种方式发布与共享，包括 UI 应用、第三方平台（钉钉/微信）、可复用组件及音视频实时互动渠道。所有发布行为均需基于已创建并发布的应用，且不同渠道对应用类型、参数配置和权限模型有明确约束。开发者应根据集成场景选择合适方式，并注意版本兼容性与运行时限制。

## 支持的模型/功能

- **仅限 Agent 1.0**：魔笔分享渠道、钉钉机器人、微信公众号、组件发布、音视频实时互动等功能**仅支持 Agent 1.0 智能体应用**；Agent 2.0 应用不支持上述 UI/渠道类发布，仅可通过 API 调用 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **工作流应用支持范围更广**：工作流应用可发布为组件、接入 UI 设计器、用于音视频实时互动，但**不支持钉钉/微信机器人发布**（该能力仅限 Agent 1.0）[使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **UI 设计器兼容两类应用**：支持将已发布的智能体应用或工作流应用一键发布为网页 UI 应用，也可从零构建 UI 并绑定任一类型后端应用 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

> **注意**：文档 1 明确指出“Agent 2.0 仅支持通过 API 调用”，而文档 2 和文档 3 均未提及 Agent 2.0 对组件或 UI 的支持能力。三者一致确认 Agent 2.0 不具备渠道发布能力，此为当前平台确定限制。

## 关键参数

| 参数类别 | 参数名 | 说明 | 约束 |
|----------|--------|------|------|
| **通用认证** | API Key | 所有发布渠道（钉钉、微信、音视频、UI）均需关联同一业务空间下的有效 API Key | 必须与应用、UI 同属一个[业务空间](https://help.aliyun.com/zh/model-studio/use-workspace) |
| **钉钉配置** | 钉钉 Client ID / Client Secret / 模板 ID | 用于 AppFlow 集成，需在钉钉开放平台创建应用并申请 `Card.Streaming.Write` 和 `Card.Instance.Write` 权限 | 模板 ID 必须为 AI 卡片类型，且关联对应钉钉应用 |
| **微信配置** | AppID（开发者 ID） | 用于微信公众号机器人授权，需在[微信公众号后台](https://mp.weixin.qq.com/) > 设置与开发 > 开发接口管理中获取 | 仅支持服务号/订阅号，不支持小程序 |
| **组件参数** | `query`（系统预设） | 强制存在，类型为 `String`，用于传递用户文本输入；不可删除，但可设为“不可见” | 必填项，接入智能体时由大模型自动填充（模型识别模式）或手动传入（业务透传模式） |
| **组件参数** | `imageList`（系统预设） | 类型为 `Array<String>`，用于传递图像公网地址；仅当组件使用视觉模型时生效 | 非必填，建议按需隐藏（设为“不可见”）以避免误传 |

## 使用方式

1. **UI 应用发布**  
   进入应用管理 → 目标应用卡片 → **发布** → 选择 **UI 应用** → 创建并编辑（可选）→ 发布至开发环境（24 小时有效期）或生产环境（需订阅套餐）。链接默认对持有者开放，支持匿名访问配置 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

2. **钉钉/微信发布**  
   在应用 **发布平台** 页签 → 点击对应卡片右侧 **创建** → 授权 AppFlow（首次需完成 SLR 和 API Key 传输授权）→ 配置平台凭证（Client ID/Secret/模板 ID 或 AppID）→ 获取回调地址（钉钉）或二维码（微信）→ 完成第三方平台侧配置（如钉钉机器人 HTTP 回调地址绑定）[分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

3. **组件发布与引用**  
   - **发布**：在应用编辑页点击 **发布应用** → 勾选“发布应用组件”，或在 **发布渠道** → **组件** → **+ 创建**，填写名称、描述及参数（别名、是否可见、传参方式等）→ **确定发布**。  
   - **引用**：  
     - *智能体中*：在技能配置中选择已发布组件，大模型依据描述自动触发（模型识别）或依赖 `biz_param` 传参（业务透传）；  
     - *工作流中*：拖入组件节点，必须通过上游节点显式传入参数（即使设为“模型识别”，工作流不自动推断）[使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

4. **音视频实时互动**  
   在应用 **AI 实时互动** 页签 → 点击 **语音互动/视频互动** → 配置 API Key → 生成临时体验二维码（24 小时）或发布至 H5/APP/SDK 渠道；需开通智能媒体服务并完成 SLR 授权 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

## 限制和注意事项

- **版本锁定**：Agent 2.0 应用完全不支持除 API 调用外的任何发布渠道，迁移前需确认业务是否依赖 UI/钉钉/微信等能力。
- **组件调用风险**：  
  - 禁止嵌套调用（A→B→A），会导致无限循环；  
  - 多级调用（A→B→C）易超时，建议控制在 2 层以内；  
  - 工作流中组件参数**必须显式传入**，不支持模型识别自动填充 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **环境与计费**：  
  - UI 开发环境链接 24 小时失效，生产环境需订阅付费套餐并绑定自定义域名；  
  - 所有分享链接产生的模型调用费用均由应用创建者 UID 承担；  
  - UI 应用涉及文件存储（1GB 免费）、数据库（0.3GB 免费）等资源，超出按量计费 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **权限隔离**：UI 应用、API Key、智能体/工作流必须归属同一业务空间，跨空间配置将导致发布失败。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


