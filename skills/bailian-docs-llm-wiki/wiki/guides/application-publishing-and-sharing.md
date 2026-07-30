# application publishing and sharing

百炼平台支持将已发布的智能体应用（Agent 1.0）或工作流应用以多种方式对外发布与共享，包括 UI 应用、钉钉/微信机器人、可复用组件及音视频实时互动渠道。所有发布行为均需基于已发布的应用，并受 Agent 版本、业务空间隔离和权限模型约束。发布后的调用费用由应用创建者 UID 承担。

## 支持的模型/功能

- **仅限 Agent 1.0**：魔笔 UI 应用、钉钉机器人、微信公众号、组件化发布、音视频实时互动等功能**全部仅支持 Agent 1.0 智能体应用**；Agent 2.0 应用不支持上述任何分享渠道，仅可通过 API 调用 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **UI 应用**：依托魔笔低代码能力，支持拖拽式界面构建，集成智能体/工作流、数据库、HTTP 服务等资源，可发布至开发环境（免费、24 小时有效期）或生产环境（需订阅套餐）[UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **组件化能力**：智能体或工作流应用均可发布为组件，供其他智能体（作为工具自动调用）或工作流（作为节点手动接入）复用；组件支持预设系统参数 `query` 和 `imageList`，并可配置别名、可见性、传参方式等 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **音视频实时互动**：仅支持图文类应用（含智能体和工作流），提供 H5/APP 扫码体验与 SDK 集成两种发布路径，依赖 AICallKit SDK。

> **注意**：文档 1 中称“音视频实时互动仅支持百炼的图文对话类应用（含智能体应用和工作流应用）”，而文档 3 的 UI 设计器部分未提及音视频能力，且其核心定位是 Web UI 发布——二者功能边界明确，无矛盾；但需注意音视频互动与 UI 应用属不同发布通道，不可混用。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `API Key` | 所有发布渠道（钉钉、微信、音视频、UI）均需绑定同一业务空间下的有效 API Key。若不可选，请检查业务空间一致性 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。 | 必填；跨业务空间无效 |
| `query` / `imageList` | 组件预设系统参数：`query`（String，必填）用于传递用户文本输入；`imageList`（Array<String>，非必填）用于图像理解场景。不可删除，但可通过“是否可见”控制暴露 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。 | 仅组件场景生效 |
| `传参方式` | 分 `业务透传`（调用方显式传入）与 `模型识别`（仅智能体中由大模型自动填充）；**工作流中无论设置为何，均需上游节点显式传值** [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。 | 工作流不支持模型识别自动填充 |
| `回调地址` / `二维码` / `分享链接` | 钉钉/微信发布后生成的唯一访问入口；UI 应用和音视频互动提供临时二维码（24 小时）或长期链接；生产环境 UI 需绑定自定义域名 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。 | 时效性差异显著，生产部署需规划 |

## 使用方式

1. **前置条件**：确保目标应用已**发布成功**，且与 API Key、UI 设计器、钉钉/微信配置处于**同一业务空间** [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
2. **统一入口**：进入百炼控制台 → **应用管理** → 打开目标应用 → 切换至对应页签：
   - `发布` 或 `发布渠道`：操作魔笔 UI、钉钉、微信、组件；
   - `AI实时互动`：配置音视频；
   - `UI设计器`：独立入口（`#/app-ui`）用于从零构建或导入已有应用。
3. **组件发布流程**：
   - 方式一：发布应用时勾选“发布应用组件”；
   - 方式二：在 `组件管理` 页面（`#/component-manage`）或应用发布渠道页签点击 `+ 创建`；
   - 配置名称、描述、参数（别名、是否可见、传参方式、默认值）后确认 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
4. **UI 应用发布**：
   - 从应用发布渠道选择 `UI应用` → 自动填充基础信息（API Key、智能体等）→ 编辑 → 发布；
   - 或直接进入 UI 设计器 → 选模板 → 配置 → 拖拽编辑 → 发布至开发/生产环境 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

## 限制和注意事项

- **Agent 版本硬限制**：Agent 2.0 应用**完全不支持**魔笔、钉钉、微信、组件、音视频等所有分享渠道，仅开放 API 接口 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **嵌套与多级调用风险**：组件间禁止 A→B→A 循环调用（导致死循环）；A→B→C 多级调用易触发超时，建议扁平化设计 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **工作流中组件参数约束**：即使配置为 `模型识别`，工作流也**不会自动推断参数值**，必须由上游节点显式传入 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **环境与计费差异**：
  - UI 开发环境链接 24 小时失效，生产环境需订阅付费套餐并配置域名；
  - 所有分享渠道产生的模型调用费用均由应用创建者 UID 承担；
  - 文件存储与数据库超出免费配额（1GB 文件 / 0.3GB DB）后按量计费 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **权限与访问控制**：默认仅阿里云用户可访问分享链接；如需匿名访问，须在 UI 设计器中启用“允许匿名访问”并配置权限组 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


