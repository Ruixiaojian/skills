# application publishing and sharing

百炼平台支持将已构建的智能体（Agent 1.0）或工作流应用以多种方式对外发布与共享，包括 UI 应用、第三方平台（钉钉/微信）、可复用组件及音视频实时互动渠道。所有发布行为均需基于已发布的应用，并受 Agent 版本、权限空间和计费模型约束。开发者应根据集成场景选择合适渠道，并注意参数配置与调用链路限制。

## 支持的模型/功能

- **仅限 Agent 1.0**：魔笔分享渠道、钉钉机器人、微信公众号、组件发布、音视频实时互动等功能**仅支持 Agent 1.0 智能体应用**；Agent 2.0 仅支持 API 调用，不支持上述任何 UI 或平台集成能力 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **组件来源广泛**：智能体应用和工作流应用均可发布为组件，供其他智能体或工作流引用 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **UI 应用兼容性**：UI 设计器支持接入已发布的智能体应用或工作流应用，但要求二者与 UI 所属的**业务空间必须一致** [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

> **注意**：文档 1 明确指出“Agent 2.0 不支持分享渠道”，而文档 2 和 3 均未提及 Agent 2.0 的组件或 UI 集成能力。当前所有发布功能均以 Agent 1.0 为前提，无例外说明，因此该限制为全局有效。

## 关键参数

| 参数 | 说明 | 约束与建议 |
|------|------|------------|
| `query`（系统预设） | 用户输入文本主参数，类型为 `String`，默认必填 | 不可删除；若无需文本输入，应设为“是否可见=否” |
| `imageList`（系统预设） | 图像公网地址列表，类型为 `Array<String>`，默认非必填 | 仅当组件使用视觉模型时生效；文本类组件建议隐藏 |
| `biz_param`（API 调用） | 用于透传业务参数的顶层字段，适用于含“业务透传”参数的组件调用 | 仅在 API 调用时生效，测试界面需通过“入参变量配置”手动填入 |
| API KEY | 所有外部渠道（钉钉、微信、音视频、UI）均需绑定有效的百炼 API KEY | 必须与应用、UI 同属一个业务空间；未授权时需先完成 SLR 及密钥传输授权 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |

## 使用方式

### 发布流程概览
1. **前提**：确保目标应用已发布（非草稿状态），且位于目标业务空间；
2. **入口**：进入应用详情页 → **发布渠道** 页签（或 **AI实时互动** / **UI应用** 页签）；
3. **选择渠道**：按需选择魔笔分享、钉钉、微信、组件、音视频或 UI 应用；
4. **配置与发布**：完成对应参数（如钉钉 Client ID/Secret、微信 AppID、组件别名/传参方式等），确认发布。

### 渠道差异要点
- **UI 应用**：通过 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 创建，支持拖拽式低代码开发，开发环境链接 24 小时失效，生产环境需订阅套餐；
- **组件发布**：在“发布渠道”页签单击 **+ 创建**，或通过 [组件管理](https://bailian.console.aliyun.com/?tab=app#/component-manage) 统一操作；组件自动随源应用更新；
- **钉钉/微信**：需前置授权计算巢 AppFlow 并获取第三方平台凭证（Client ID/Secret、AppID、卡片模板 ID 等），回调地址/二维码为最终交付物；
- **音视频实时互动**：仅支持图文类应用（智能体/工作流），提供 H5/APP 扫码体验与 SDK 集成两种模式，需开通智能媒体服务并完成 SLR 授权。

## 限制和注意事项

- **版本锁定**：Agent 2.0 应用完全不可用于任何分享渠道，迁移前需确认业务兼容性 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **嵌套与多级调用禁止**：A→B→A 形成循环调用将导致功能不可用；A→B→C 等三级以上调用易触发超时，建议控制在两级以内 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **工作流中“模型识别”无效**：即使组件参数设为“模型识别”，工作流应用仍**必须显式传参**（通过上游节点输出），大模型不会自动推断 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **权限与空间隔离**：API KEY、应用、UI 设计器三者必须归属同一业务空间，否则无法关联 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **计费归属**：所有通过分享链接产生的模型调用、存储、带宽等费用，均由应用创建者 UID 账号承担，与访问者身份无关 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


