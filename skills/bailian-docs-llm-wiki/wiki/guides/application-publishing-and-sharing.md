# application publishing and sharing

百炼平台支持将已发布的智能体应用（Agent 1.0）或工作流应用以多种方式对外发布与共享，包括 UI 应用、钉钉/微信机器人、可复用组件及音视频实时互动渠道。所有发布行为均需基于已发布的应用，并受 Agent 版本、业务空间隔离和权限模型约束。发布后的调用费用由应用创建者 UID 承担。

## 支持的模型/功能

- **仅限 Agent 1.0**：魔笔分享渠道、钉钉、微信、组件发布、音视频实时互动等功能**仅支持 Agent 1.0 智能体应用**；Agent 2.0 应用不支持上述渠道，仅可通过 API 调用 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **UI 应用**：支持通过[UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)将智能体或工作流应用封装为网页界面，提供低代码拖拽编辑、多端适配（PC/H5）、权限控制及一键发布能力。
- **组件化能力**：智能体或工作流应用可发布为标准化组件，供其他智能体（作为工具）或工作流（作为节点）引用，支持 `query` 和 `imageList` 等预设系统参数 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **音视频实时互动**：仅支持图文类应用（含智能体与工作流），通过 SDK 或 H5/APP 扫码方式实现语音/视频对话，依赖 AICallKit 集成。

> **注意**：文档 1 明确指出“Agent 2.0 仅支持通过 API 调用”，而文档 3 在“快速开始”示例中未限定 Agent 版本，但其组件接入逻辑（如“智能体作为工具”）实际依赖 Agent 1.0 的 MCP 工具调用机制。因此，组件发布与引用**必须基于 Agent 1.0 应用**，否则无法触发自动调用。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `API Key` | 用于身份认证与计费归属，必须与目标应用、UI 设计器位于**同一业务空间** | 不同业务空间的 API Key 不可见；未授权时需先完成计算巢 AppFlow SLR 授权 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md) |
| `query` / `imageList` | 组件预设系统参数，不可删除；`query` 类型为 `String`，建议设为必填；`imageList` 类型为 `Array<String>`，仅在启用视觉模型时生效 | 若组件不需图像输入，应将 `imageList` 的“是否可见”设为否 |
| 传参方式（`业务透传` vs `模型识别`） | `业务透传`：由调用方显式传入（智能体中为用户输入/上游节点输出）；`模型识别`：仅在智能体中由大模型根据参数描述自动填充，**工作流中该模式无效，必须显式传参** | 文档 1 与文档 3 均强调：工作流引用组件时，即使配置为“模型识别”，也**必须从上游节点提供输入值**，否则运行失败 |
| 环境有效期 | 开发环境 UI 链接**24 小时后失效**；生产环境长期有效，但需订阅付费套餐并绑定自定义域名 | [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md) 中明确说明开发环境时效性 |

## 使用方式

1. **前置条件**：确保目标应用已发布，且应用、API Key、UI 设计器（如使用）处于**同一业务空间**。
2. **发布入口**：
   - 控制台 → **应用管理** → 目标应用卡片 → **发布** → 选择渠道（UI/钉钉/微信/组件/音视频）；
   - 或进入应用详情页 → **发布渠道** 页签操作。
3. **典型流程**：
   - **UI 应用**：选择“UI 应用” → 自动填充或手动配置 API Key 与智能体 → 编辑界面 → 发布至开发/生产环境 → 获取应用地址分享；
   - **钉钉/微信**：在“发布平台”页签授权 AppFlow → 配置对应平台凭证（Client ID/Secret、模板 ID、AppID）→ 获取回调地址或二维码；
   - **组件**：在“发布渠道”页签 → “组件” → 创建 → 配置名称、描述、参数（别名、是否可见、传参方式）→ 发布；
   - **音视频**：在“AI 实时互动”页签 → 配置 API Key → 生成体验二维码或发布至 H5/APP/SDK。

## 限制和注意事项

- **版本限制**：Agent 2.0 应用**不支持任何 UI 或渠道发布功能**，仅支持 API 调用 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。
- **嵌套与多级调用禁止**：A 调用 B 且 B 调用 A 会导致死循环；A→B→C 多级链路易超时，应尽量扁平化设计 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。
- **工作流中组件参数约束**：即使参数配置为“模型识别”，工作流也**不会自动推断值**，必须通过上游节点显式传入，否则任务失败。
- **权限与计费**：所有分享链接默认仅限阿里云用户访问；费用由应用创建者 UID 承担，包括模型调用、文件存储（UI 应用）、数据库容量等 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)。
- **环境隔离**：开发环境 UI 链接 24 小时过期，生产环境需付费订阅；UI 应用若使用文件上传或数据库，需关注免费配额（1GB 文件 / 0.3GB 数据库）。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)


