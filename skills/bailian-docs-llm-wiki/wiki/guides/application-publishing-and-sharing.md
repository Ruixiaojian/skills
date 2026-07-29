# application publishing and sharing

百炼平台支持将已发布的智能体应用（Agent 1.0）或工作流应用以多种方式对外共享与集成，包括 UI 应用、钉钉/微信机器人、可复用组件及音视频实时互动等渠道。所有发布行为均需基于已成功发布的应用，并受 Agent 版本、权限空间和计费模型约束。开发者应根据目标场景选择合适发布方式，并注意参数配置与调用限制。

## 支持的模型/功能

- **仅限 Agent 1.0**：魔笔分享渠道、钉钉、微信、组件发布、音视频实时互动等功能**均不支持 Agent 2.0** 应用，后者仅可通过 API 调用接入 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **UI 应用**：支持智能体应用与工作流应用作为后端能力，通过魔笔低代码平台构建网页界面，支持 PC/H5 多端访问 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **组件化能力**：智能体或工作流应用可发布为可复用组件，供其他智能体（作为工具）或工作流（作为节点）引用，实现功能解耦与复用 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **音视频实时互动**：仅支持图文对话类应用（含智能体与工作流），提供 H5/APP 扫码体验及 SDK 集成两种发布路径。

> **注意**：文档 1 明确指出“Agent 2.0 仅支持通过 API 调用”，而文档 2 和文档 3 均未提及 Agent 2.0 对组件或 UI 的支持能力，因此当前所有发布渠道均严格限定于 Agent 1.0 应用，该限制具有一致性，无矛盾。

## 关键参数

| 参数类别 | 参数名 | 说明 | 来源依据 |
|----------|--------|------|----------|
| **通用认证** | API Key | 所有发布渠道（钉钉、微信、音视频、UI）均需绑定同一业务空间下的有效 API Key；未匹配时无法完成授权或配置 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) |
| **组件参数** | `query`（预设） | 系统级必填 String 参数，用于传递用户文本输入；不可删除，但可设为“不可见” [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| **组件参数** | `imageList`（预设） | Array<String> 类型，用于传递图像公网地址；仅当组件使用视觉模型时生效，否则建议设为“不可见” [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| **组件传参** | `biz_param` | API 调用时显式传入业务参数的字段名，用于填充“业务透传”类参数 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |

## 使用方式

1. **入口统一**：所有发布操作均从百炼控制台 **[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)** 页面进入，点击目标应用卡片的 **发布** 按钮。
2. **渠道选择**：
   - **UI 应用**：在“发布渠道”页签选择“UI 应用” → 创建 → 编辑界面 → 发布至开发/生产环境；开发环境链接有效期为 24 小时 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
   - **钉钉/微信**：在“发布平台”页签分别点击对应卡片的“创建”，完成第三方平台授权（需 SLR 角色与 API Key）、凭证配置（Client ID/Secret、模板 ID、AppID）及回调地址/二维码分发 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
   - **组件**：在“发布渠道”页签点击“组件” → “+ 创建”，填写名称、描述、参数别名/可见性/传参方式（业务透传 或 模型识别）→ 发布；后续可在智能体“技能”或工作流画布中拖入引用 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
   - **音视频实时互动**：在“AI 实时互动”页签配置 API Key → 生成临时二维码测试 → 发布后开通智能媒体服务并完成 SLR 授权 → 选择 H5/APP 分享或 SDK 集成 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

## 限制和注意事项

- **Agent 版本硬约束**：Agent 2.0 应用**完全不可用于任何 UI、钉钉、微信、组件或音视频发布渠道**，仅支持 API 调用，此为平台级限制 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **业务空间一致性**：UI 设计器、API Key、目标应用必须归属同一业务空间，否则无法在 UI 创建流程中选择对应资源 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **组件调用风险**：
  - **禁止嵌套调用**（A→B→A）：将导致无限循环，应用不可用；
  - **慎用多级调用**（A→B→C）：受最长运行时间限制，易超时失败 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **环境与计费**：
  - UI 开发环境免费但链接 24 小时失效；生产环境需订阅付费套餐并绑定自定义域名 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)；
  - 所有通过分享链接产生的模型调用费用，均由应用创建者 UID 账号承担 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **工作流中“模型识别”无效**：即使组件参数设为“模型识别”，在工作流中仍需上游节点显式传入值，大模型不会自动推断 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


