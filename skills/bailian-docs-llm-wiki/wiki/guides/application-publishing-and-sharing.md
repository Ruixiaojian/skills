# application publishing and sharing

百炼平台支持将智能体应用（Agent 1.0）和工作流应用以多种方式发布与共享，包括生成可访问的 UI 应用、集成至钉钉/微信等第三方平台、发布为可复用组件、以及接入音视频实时互动场景。所有发布行为均需基于已创建并发布的应用，且不同发布渠道对应用类型、模型能力及配置要求存在明确约束。

## 支持的模型/功能

- **仅限 Agent 1.0 应用**：魔笔分享渠道、钉钉机器人、微信公众号、组件发布、音视频实时互动等功能**全部仅支持 Agent 1.0 智能体应用**；Agent 2.0 应用不支持上述任何 UI 或渠道类发布方式，仅可通过 API 调用 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **UI 应用支持范围更广**：UI 设计器不仅支持 Agent 1.0，也支持工作流应用（含任务型与对话型），但需确保应用已发布且与 UI 所属业务空间一致 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **组件来源多样化**：智能体应用和工作流应用均可发布为组件，作为工具被其他智能体或工作流引用 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

> **注意**：文档 1 明确指出“Agent 2.0 仅支持通过 API 调用，不支持上述分享渠道”，而文档 3 在“准备工作”中强调“集成AI对话能力，需要创建并发布百炼[智能体应用]或[工作流应用]”，未限定 Agent 版本。此处以文档 1 的权威性为准——**Agent 2.0 不支持任何非 API 形式的发布与共享**。

## 关键参数

| 参数 | 说明 | 来源场景 |
|------|------|----------|
| `query`（系统预设） | 必填 String 类型参数，用于传递用户输入文本（如“查询杭州天气”）。不可删除，但可通过“是否可见”设为隐藏 | 组件发布与调用 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| `imageList`（系统预设） | 非必填 Array<String> 类型参数，用于传递图像公网地址列表；仅当组件使用视觉模型时生效 | 组件发布与调用 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md) |
| `biz_param` | API 调用时传入业务透传参数的字段名，用于手动填充组件所需入参 | 智能体中测试含业务透传参数的组件 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |
| 回调地址 / 二维码 / 分享链接 | 各渠道唯一访问入口：钉钉需配置回调地址；微信提供客服二维码；UI 应用和音视频互动提供临时链接或长期域名 | 全渠道通用 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |

## 使用方式

1. **统一入口**：所有发布操作均从百炼控制台 **[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)** 页面进入目标应用卡片，点击 **发布** 或切换至对应页签（如“发布平台”、“AI实时互动”、“组件”）。
2. **四类主流发布路径**：
   - **UI 应用**：通过 UI 设计器构建界面，绑定已发布智能体/工作流与 API Key，发布至开发环境（24 小时有效）或生产环境（需订阅套餐） [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)；
   - **第三方平台**：钉钉/微信需先完成平台授权（SLR + API-KEY）、在对应开放平台创建应用并获取凭证（Client ID/Secret、模板 ID、AppID），再回填至百炼发布配置；
   - **组件发布**：在“发布渠道”页签点击“组件”→“创建”，或通过 **[组件管理](https://bailian.console.aliyun.com/?tab=app#/component-manage)** 页面统一操作；支持后续在智能体（作为技能）或工作流（作为节点）中引用；
   - **音视频实时互动**：仅支持图文类应用（智能体/工作流），需配置 API Key 并完成智能媒体服务开通与 SLR 授权，支持 H5/APP 扫码体验或 SDK 集成。
3. **组件调用差异**：
   - 在**智能体中引用**时，“模型识别”传参方式允许大模型自动推断 `query` 等参数值；
   - 在**工作流中引用**时，无论传参方式如何设置，均需上游节点**显式提供输入值**（如 `系统变量/query`），不支持自动推断。

## 限制和注意事项

- **Agent 版本硬性限制**：除 API 调用外，所有可视化/渠道化发布能力（UI、钉钉、微信、组件、音视频）**仅适用于 Agent 1.0**，Agent 2.0 完全不可用。
- **嵌套与多级调用风险**：组件间禁止 A→B→A 的循环调用；A→B→C 的三级及以上调用易触发超时，应严格控制层级深度 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **环境与权限约束**：
  - UI 应用开发环境链接 24 小时失效，生产环境需绑定自定义域名并订阅付费套餐；
  - 所有分享链接默认仅限阿里云用户访问；如需匿名访问，须在 UI 设计器中单独配置权限组 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)；
  - 百炼应用、API Key 与 UI 设计器必须归属**同一业务空间**，否则无法关联资源。
- **计费责任归属**：通过分享链接产生的模型调用、存储、带宽等费用，均由应用创建者 UID 账号承担，与访问者无关 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


