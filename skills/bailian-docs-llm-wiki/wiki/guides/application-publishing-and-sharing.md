# application publishing and sharing

百炼平台支持将智能体应用（Agent 1.0）和工作流应用以多种方式发布与共享，包括 UI 应用、钉钉/微信渠道、可复用组件及音视频实时互动等形态，便于集成至业务系统或面向终端用户交付。所有发布行为均需基于已发布的应用，并受 Agent 版本、权限空间和计费策略约束。开发者应根据使用场景选择适配的发布路径，并注意参数配置与调用限制。

## 支持的模型/功能

- **仅限 Agent 1.0**：魔笔分享渠道、钉钉机器人、微信公众号、组件发布、音视频实时互动等功能**全部仅支持 Agent 1.0 智能体应用**；Agent 2.0 仅支持 API 调用，不支持任何 UI 或渠道类发布能力（见 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)）。
- **UI 应用支持范围更广**：UI 设计器不仅支持接入 Agent 1.0，也支持已发布的**工作流应用**（见 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)）。
- **组件来源多样化**：智能体应用和工作流应用均可发布为组件，且组件可在智能体或工作流中被引用（见 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)）。

> **注意**：文档 1 明确限定“分享渠道均为 Agent 1.0 功能”，而文档 3 在“从已有应用发布为 UI”章节中未强调版本限制，但其前提条件要求“创建并发布百炼[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)”——该链接指向官方文档中明确标注为 Agent 1.0 的页面。因此，UI 应用虽技术上可接入工作流，但对智能体的依赖仍为 Agent 1.0，不存在版本兼容性例外。

## 关键参数

| 参数 | 说明 | 使用场景 | 约束 |
|------|------|----------|------|
| `query`（系统预设） | 用户输入的文本指令，类型为 `String`，默认必填 | 所有组件接入场景（智能体/工作流） | 不可删除；若无需使用，须设为“是否可见=否” |
| `imageList`（系统预设） | 图像公网地址数组，类型为 `Array<String>`，默认非必填 | 组件调用图像理解模型时生效 | 仅当组件底层模型支持多模态时有效 |
| `biz_param`（API 调用） | 用于透传业务参数的 JSON 字段，替代 `query` 或补充其他字段 | API 方式调用含“业务透传”参数的组件时 | 必须在请求体中显式传入，不可由模型自动填充 |
| 回调地址 / [Token](../concepts/token.md) / 分享链接 | 渠道级访问凭证，有效期各异（如 UI 开发环境链接 24 小时失效） | 钉钉/微信/音视频/H5 分享 | 生成后需及时分发，过期需重新获取 |

## 使用方式

1. **统一入口**：所有发布操作均从百炼控制台 **[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)** 页面的目标应用卡片进入，点击 **发布** 或切换至 **发布渠道** 页签。
2. **四类主流路径**：
   - **UI 应用**：通过“UI 应用”卡片创建，依托魔笔低代码能力生成网页界面，支持开发/生产双环境部署（见 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)）；
   - **钉钉/微信**：在“发布平台”页签授权计算巢 AppFlow 后，配置对应平台的凭据（Client ID/Secret、模板 ID、AppID），获取回调地址或客服二维码；
   - **组件**：在“发布渠道”页签点击“组件”→“创建”，填写名称、描述及参数（别名、是否必填、传参方式等），发布后可在其他智能体或工作流中作为节点/技能引用；
   - **音视频实时互动**：在“AI 实时互动”页签配置 API KEY，生成临时体验二维码或发布至 H5/APP/SDK，需开通智能媒体服务并完成 SLR 授权。
3. **组件接入差异**：
   - 在**智能体中引用**：大模型依据组件描述与上下文自动决策是否调用；若含“模型识别”参数，模型尝试从对话中提取内容填充；
   - 在**工作流中引用**：必须手动连接上游节点输出至组件输入；即使参数设为“模型识别”，**也不会自动推断值**，必须显式传参（见 [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)）。

## 限制和注意事项

- **Agent 版本硬限制**：除 API 调用外，所有图形化/渠道化发布能力（魔笔、钉钉、微信、UI、音视频）**仅适用于 Agent 1.0**，Agent 2.0 应用无法出现在发布渠道列表中。
- **业务空间强绑定**：UI 设计器、API KEY、目标智能体/工作流**必须归属同一业务空间**，否则无法在创建 UI 或配置组件时被选中（见 [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)）。
- **组件调用风险**：
  - **禁止嵌套调用**（A→B→A）：导致无限循环，服务不可用；
  - **慎用多级调用**（A→B→C）：受最长运行时间限制，易超时失败；
  - **组件自动更新**：原应用重新发布后，已发布的组件同步更新，可能影响下游依赖方，建议灰度验证。
- **环境与计费**：
  - UI 开发环境链接**24 小时失效**，生产环境需订阅付费套餐并绑定自定义域名；
  - 所有分享链接产生的模型调用费用，均由应用创建者 UID 账号承担（见 [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)）；
  - 文件存储、数据库等 UI 相关资源超出免费配额后按量计费。

## 来源文档

- [分享智能体应用](../../raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/application-publishing-and-sharing/ui-designer.md)


