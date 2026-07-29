# application publishing and sharing

百炼平台支持将已发布的智能体应用（Agent 1.0）或工作流应用以多种方式对外发布与共享，包括 UI 应用、钉钉/微信机器人、可复用组件及音视频实时互动等渠道。所有发布行为均需基于已上线的应用，并依赖统一的业务空间、API Key 和权限体系。Agent 2.0 应用仅支持 API 调用，不支持 UI 或第三方平台分享能力。

## 支持的模型/功能

- **适用应用类型**：仅限 **Agent 1.0 智能体应用** 和 **工作流应用**；Agent 2.0 不支持 UI、钉钉、微信、组件发布等分享渠道 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **UI 应用**：通过魔笔低代码平台构建网页界面，支持 PC/H5 端访问，集成智能体对话能力 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **第三方平台集成**：支持发布为钉钉机器人、微信公众号客服机器人，需完成开放平台授权与凭证配置。
- **组件化能力**：智能体或工作流可发布为可复用组件，供其他智能体（作为工具）或工作流（作为节点）引用 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **音视频实时互动**：仅支持图文类应用（智能体/工作流），提供 H5/APP 扫码体验与 SDK 集成两种接入方式。

> **注意**：文档 1 中称“音视频实时互动仅支持百炼的图文对话类应用（含智能体应用和工作流应用）”，而文档 3 的 UI 设计器说明中明确指出其支持“AI基础对话”“企业AI知识库Lite”等模板，且可绑定智能体或工作流——二者无矛盾，但需注意：UI 应用本身是独立前端容器，其后端能力来源才是智能体/工作流；音视频互动则直接封装语音/视频信令与大模型交互逻辑，二者技术路径不同，不可混用。

## 关键参数

| 参数 | 说明 | 来源场景 |
|------|------|----------|
| `API Key` | 必填，用于身份认证与计费归属；必须与目标应用、UI 设计器处于同一业务空间 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) | 所有发布渠道（UI、钉钉、微信、音视频） |
| `query`（系统预设） | 组件默认文本输入参数，类型 `String`，必填；调用时自动映射用户输入文本 | 组件发布与引用 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| `imageList`（系统预设） | 组件默认图像输入参数，类型 `Array<String>`，非必填；仅当组件使用多模态模型时生效 | 组件发布与引用 |
| `biz_param` | API 调用时传入业务透传参数的字段名；用于手动填充组件中设为“业务透传”的参数 | 智能体组件测试/API 调用场景 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |
| 回调地址 / [Token](../concepts/token.md) / 分享链接 | 钉钉/微信需配置回调地址；音视频互动生成带时效性的 [Token](../concepts/token.md) 链接（24 小时）；UI 应用开发环境链接同样 24 小时失效 | 各渠道发布后生成 |

## 使用方式

1. **前提**：目标应用必须已**发布**（非仅保存），且位于与 API Key、UI 设计器相同的业务空间。
2. **入口统一**：进入百炼控制台 → [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) → 目标应用卡片 → **发布**。
3. **渠道选择**：
   - **UI 应用**：在“发布渠道”页签点击 **UI 应用** → “创建”，或从 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 页面直接创建并绑定已有智能体/工作流。
   - **钉钉/微信**：在“发布平台”页签分别点击对应卡片 → 完成授权 → 配置凭证（Client ID/Secret、模板 ID、AppID）→ 获取回调地址或二维码。
   - **组件**：在“发布渠道”页签 → “组件” → “创建”，填写名称、描述、参数别名/可见性/传参方式等；亦可通过 [组件管理](https://bailian.console.aliyun.com/?tab=app#/component-manage) 独立创建。
   - **音视频互动**：在“AI实时互动”页签 → 配置 API Key → 生成临时体验链接 → 发布后开通智能媒体服务并授权 SLR。
4. **引用组件**：
   - 在智能体中：添加技能 → 选择已发布组件 → 大模型根据描述与上下文自动触发（模型识别）或由用户/调用方传参（业务透传）。
   - 在工作流中：拖入“组件”节点 → 选择组件 → 明确配置上游节点输出到 `query` 等参数（工作流不支持模型识别自动填参）。

## 限制和注意事项

- **Agent 版本限制**：所有 UI、钉钉、微信、组件、音视频发布能力**仅对 Agent 1.0 生效**；Agent 2.0 仅支持 API 调用 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **嵌套与多级调用禁止**：组件 A 调用 B、B 又调用 A 将导致死循环；A→B→C 多级链路易超时，应尽量扁平化设计 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **环境时效性**：UI 应用开发环境链接、音视频临时体验链接、UI 创建后的 24 小时体验链接均**有效期为 24 小时**，过期需重新发布 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **权限与计费归属**：所有通过分享链接产生的模型调用费用，均由应用创建者 UID 账号承担；匿名访问需显式开启权限组配置。
- **参数可见性约束**：组件中设为“是否可见 = 否”的参数，在引用侧完全不可见，适用于隐藏敏感或冗余参数（如图像输入参数在纯文本模型组件中应隐藏）。
- **工作流组件传参强制性**：即使组件参数设为“模型识别”，工作流中仍需**显式连接上游节点输出**，否则运行时报错；该行为与智能体场景不同，需特别注意。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


