# application publishing and sharing

百炼平台支持将已发布的智能体应用（Agent 1.0）以多种方式对外发布与共享，包括生成可访问的 UI 应用、集成至钉钉/微信等第三方平台、发布为可复用组件、以及接入音视频实时互动场景。所有发布行为均需基于已成功发布的应用，并严格遵循 Agent 版本兼容性约束。API 调用是唯一支持 Agent 2.0 的对外集成方式。

## 支持的模型/功能

- **仅限 Agent 1.0**：魔笔分享渠道（UI 应用）、钉钉机器人、微信公众号、组件化发布、音视频实时互动等功能**全部仅支持 Agent 1.0 智能体应用**；Agent 2.0 不支持上述任何 UI 或渠道发布能力，仅可通过 API 调用 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **UI 应用**：基于魔笔低代码平台构建，支持拖放式页面搭建、数据库映射、权限配置及一键发布至开发/生产环境，适用于智能体或工作流应用 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **组件化能力**：智能体或工作流应用均可发布为组件，供其他智能体（作为工具）或工作流（作为节点）引用，实现功能复用 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **音视频实时互动**：仅支持图文类应用（含 Agent 1.0 和工作流），提供 H5/APP 扫码体验与 SDK 集成两种发布路径。

> **注意**：文档 1 明确指出“Agent 2.0 仅支持通过 API 调用”，而文档 3 在“快速开始”示例中未声明版本限制，但其所有操作入口（如应用管理页签、组件管理面板）均位于 Agent 1.0 控制流内。实际开发中，**Agent 2.0 无法创建或发布组件**，该能力完全依赖 Agent 1.0 架构。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `API Key` | 调用百炼服务的身份凭证，必须与目标应用、UI 设计器处于**同一业务空间** [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) | 必填；跨空间不可见 |
| `query` / `imageList` | 组件预设系统参数，`query` 为必填 String 类型，`imageList` 为非必填 Array<String> 类型 | 不可删除；可通过“是否可见”隐藏 |
| `传参方式` | 分为 `业务透传`（调用方显式传入）和 `模型识别`（仅智能体中由大模型自动填充） | 工作流中无论设置为何，均需上游节点显式传值 |
| `回调地址`（钉钉） / `二维码`（微信） | 第三方平台集成所需的唯一接入凭证 | 钉钉需配置为 HTTP 模式；微信二维码有效期永久（除非下线） |

## 使用方式

1. **UI 应用发布**  
   - 进入应用「发布渠道」页签 → 选择「UI 应用」→ 「创建」→ 自动填充基础信息（API Key、智能体、图标等）→ 编辑 UI → 发布至开发环境（24 小时有效）或生产环境（需订阅套餐）[原文标题](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

2. **钉钉/微信发布**  
   - 需先完成计算巢 AppFlow 授权（SLR + API Key 加密传输）；  
   - 钉钉：获取 Client ID/Secret + 卡片模板 ID → 填入百炼配置 → 复制回调地址 → 在钉钉开放平台配置机器人（HTTP 模式）；  
   - 微信：绑定 AppID → 获取凭证 → 生成客服二维码 → 扫码即用 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

3. **组件发布与引用**  
   - 发布：在「发布渠道」→「组件」→「创建」→ 设置名称、描述、参数别名/可见性/传参方式；  
   - 引用：智能体中在「技能」添加组件；工作流中拖入「组件节点」并绑定输入（如 `系统变量/query`）[原文标题](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

4. **音视频实时互动**  
   - 进入「AI 实时互动」页签 → 配置 API Key → 生成临时体验二维码（24 小时）→ 发布后开通智能媒体服务 → 选择 H5/APP 分享或 SDK 集成 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

## 限制和注意事项

- **Agent 版本硬限制**：所有非 API 发布方式（UI、钉钉、微信、组件、音视频）**仅支持 Agent 1.0**；Agent 2.0 无对应发布入口，强行尝试将失败。
- **业务空间隔离**：UI 设计器、API Key、目标应用必须归属同一业务空间，否则无法关联 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **组件调用风险**：禁止 A→B→A 的嵌套调用（死循环）；多级调用（A→B→C）易触发超时，建议单跳深度 ≤2。
- **工作流中模型识别失效**：即使参数设为 `模型识别`，工作流仍强制要求上游节点显式传值，否则运行时报错。
- **开发环境时效性**：UI 开发环境链接 24 小时后自动失效，需重新发布；生产环境需付费订阅且支持自定义域名。
- **计费责任**：所有通过分享链接产生的模型调用、存储、带宽费用，均由应用创建者 UID 账号承担 [原文标题](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)


