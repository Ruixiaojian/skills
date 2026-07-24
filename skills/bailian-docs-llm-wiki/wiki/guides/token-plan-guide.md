> /config
```

## OpenCode

**开启思考模式**：在配置文件`opencode.json`中，为对应模型添加以下配置：

```json
"options": {
  "thinking": {
    "type": "enabled",
    "budget[Token](../concepts/token.md)s": 1024
  }
}
```

**查看思考过程**：使用快捷键 `Ctrl + O` 可查看思考过程。

### **Coding Plan 支持的模型有哪些？**

Coding Plan 支持的模型包括千问、GLM、Kimi、MiniMax 等多个品牌的主流模型。具体支持列表请参见[Coding Plan](https://help.aliyun.com/zh/model-studio/coding-plan#dc0d98da6ev4j)文档。

### **Coding Plan Lite 套餐是否支持图片理解？**

Coding Plan Lite 套餐支持所有套餐模型（含千问、GLM、Kimi、MiniMax），与 Pro 套餐一致，因此也支持 qwen3.7-plus、qwen3.6-plus、kimi-k2.5 等支持图片理解的模型。

### **Coding Plan 是否支持 Harness 工具？**

不支持。Coding Plan 不支持联网搜索、代码解释器等 Harness 工具。

### **Coding Plan 是否支持多模态生成模型？**

不支持。Coding Plan 不支持图像生成、视频生成等多模态生成模型。

### **Coding Plan 是否支持自定义 MCP？**

不支持。Coding Plan 不支持接入自定义 MCP 服务。

### **Coding Plan 是否支持视觉理解能力？**

Coding Plan 支持部分模型（如 qwen3.7-plus）原生视觉理解能力，但不支持通过 Skill 或 Agent 添加视觉能力。

### **Coding Plan 是否支持多模型切换？**

支持。Coding Plan 支持在工具中通过 `/model` 指令切换不同模型。

### **Coding Plan 是否支持 API 调用？**

不支持。Coding Plan 仅限在编程工具中交互式使用，禁止以 API 调用的形式用于自动化脚本或应用后端。

### **Coding Plan 是否支持团队管理？**

不支持。Coding Plan 无团队管理功能，仅面向个人开发者。

### **Coding Plan 是否支持数据安全承诺？**

不支持。Coding Plan 未承诺不使用对话数据训练模型。

### **Coding Plan 是否支持高峰期不排队？**

不支持。Coding Plan 在高峰期可能出现排队等待。

### **Coding Plan 是否支持按量计费？**

不支持。Coding Plan 为固定月费订阅制，不提供按量计费选项。

### **Coding Plan 是否支持退订？**

Lite 套餐已停止续费与升级；Pro 套餐支持退订，但不支持退款。

### **Coding Plan 是否支持 RAM 用户？**

支持。RAM 用户需由主账号完成授权后方可使用。

### **Coding Plan 是否支持自动续费？**

支持。用户可在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=plan#/efm/subscription/coding-plan)开启或关闭自动续费。

### **Coding Plan 是否支持升级？**

Lite 套餐已停止升级；Pro 套餐支持升级，但需注意升级后无法降级。

### **Coding Plan 是否支持降级？**

不支持。Coding Plan 不支持降级操作。

### **Coding Plan 是否支持共享用量包？**

不支持。Coding Plan 无共享用量包功能。

### **Coding Plan 是否支持 SSO 接入？**

不支持。Coding Plan 无 SSO 接入功能。

### **Coding Plan 是否支持钉钉接入？**

不支持。Coding Plan 无钉钉接入功能。

### **Coding Plan 是否支持用量分析？**

不支持。Coding Plan 无用量分析功能。

### **Coding Plan 是否支持 API Key 重置？**

支持。用户可在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=plan#/efm/subscription/coding-plan)重置 API Key。

### **Coding Plan 是否支持 Base URL 更换？**

不支持。Coding Plan 的 Base URL 是固定的，不可更换。

### **Coding Plan 是否支持多地域部署？**

不支持。Coding Plan 仅支持华北2（北京）地域。

### **Coding Plan 是否支持多租户隔离？**

不支持。Coding Plan 无多租户隔离架构。

### **Coding Plan 是否支持预算可控？**

不支持。Coding Plan 为固定月费，无预算控制功能。

### **Coding Plan 是否支持数据安全保障？**

不支持。Coding Plan 未提供企业级数据安全保障。

### **Coding Plan 是否支持稳定运行？**

不支持。Coding Plan 在高峰期可能出现排队等待。

### **Coding Plan 是否支持按模型分档抵扣？**

不支持。Coding Plan 按请求次数计费，不按模型分档抵扣。

### **Coding Plan 是否支持 Credits 统一计量？**

不支持。Coding Plan 使用请求次数作为计量单位，而非 Credits。

### **Coding Plan 是否支持 Harness 工具？**

不支持。Coding Plan 不支持 Harness 工具。

### **Coding Plan 是否支持多模态生成模型？**

不支持。Coding Plan 不支持多模态生成模型。

### **Coding Plan 是否支持自定义 MCP？**

不支持。Coding Plan 不支持自定义 MCP。

### **Coding Plan 是否支持视觉理解能力？**

Coding Plan 支持部分模型（如 qwen3.7-plus）原生视觉理解能力，但不支持通过 Skill 或 Agent 添加视觉能力。

### **Coding Plan 是否支持多模型切换？**

支持。Coding Plan 支持在工具中通过 `/model` 指令切换不同模型。

### **Coding Plan 是否支持 API 调用？**

不支持。Coding Plan 仅限在编程工具中交互式使用，禁止以 API 调用的形式用于自动化脚本或应用后端。

### **Coding Plan 是否支持团队管理？**

不支持。Coding Plan 无团队管理功能，仅面向个人开发者。

### **Coding Plan 是否支持数据安全承诺？**

不支持。Coding Plan 未承诺不使用对话数据训练模型。

### **Coding Plan 是否支持高峰期不排队？**

不支持。Coding Plan 在高峰期可能出现排队等待。

### **Coding Plan 是否支持按量计费？**

不支持。Coding Plan 为固定月费订阅制，不提供按量计费选项。

### **Coding Plan 是否支持退订？**

Lite 套餐已停止续费与升级；Pro 套餐支持退订，但不支持退款。

### **Coding Plan 是否支持 RAM 用户？**

支持。RAM 用户需由主账号完成授权后方可使用。

### **Coding Plan 是否支持自动续费？**

支持。用户可在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=plan#/efm/subscription/coding-plan)开启或关闭自动续费。

### **Coding Plan 是否支持升级？**

Lite 套餐已停止升级；Pro 套餐支持升级，但需注意升级后无法降级。

### **Coding Plan 是否支持降级？**

不支持。Coding Plan 不支持降级操作。

### **Coding Plan 是否支持共享用量包？**

不支持。Coding Plan 无共享用量包功能。

### **Coding Plan 是否支持 SSO 接入？**

不支持。Coding Plan 无 SSO 接入功能。

### **Coding Plan 是否支持钉钉接入？**

不支持。Coding Plan 无钉钉接入功能。

### **Coding Plan 是否支持用量分析？**

不支持。Coding Plan 无用量分析功能。

### **Coding Plan 是否支持 API Key 重置？**

支持。用户可在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=plan#/efm/subscription/coding-plan)重置 API Key。

### **Coding Plan 是否支持 Base URL 更换？**

不支持。Coding Plan 的 Base URL 是固定的，不可更换。

### **Coding Plan 是否支持多地域部署？**

不支持。Coding Plan 仅支持华北2（北京）地域。

### **Coding Plan 是否支持多租户隔离？**

不支持。Coding Plan 无多租户隔离架构。

### **Coding Plan 是否支持预算可控？**

不支持。Coding Plan 为固定月费，无预算控制功能。

### **Coding Plan 是否支持数据安全保障？**

不支持。Coding Plan 未提供企业级数据安全保障。

### **Coding Plan 是否支持稳定运行？**

不支持。Coding Plan 在高峰期可能出现排队等待。

### **Coding Plan 是否支持按模型分档抵扣？**

不支持。Coding Plan 按请求次数计费，不按模型分档抵扣。

### **Coding Plan 是否支持 Credits 统一计量？**

不支持。Coding Plan 使用请求次数作为计量单位，而非 Credits。

### **Coding Plan 是否支持 Harness 工具？**

不支持。Coding Plan 不支持 Harness 工具。

### **Coding Plan 是否支持多模态生成模型？**

不支持。Coding Plan 不支持多模态生成模型。

### **Coding Plan 是否支持自定义 MCP？**

不支持。Coding Plan 不支持自定义 MCP。

### **Coding Plan 是否支持视觉理解能力？**

Coding Plan 支持部分模型（如 qwen3.7-plus）原生视觉理解能力，但不支持通过 Skill 或 Agent 添加视觉能力。

### **Coding Plan 是否支持多模型切换？**

支持。Coding Plan 支持在工具中通过 `/model` 指令切换不同模型。

### **Coding Plan 是否支持 API 调用？**

不支持。Coding Plan 仅限在编程工具中交互式使用，禁止以 API 调用的形式用于自动化脚本或应用后端。

### **Coding Plan 是否支持团队管理？**

不支持。Coding Plan 无团队管理功能，仅面向个人开发者。

### **Coding Plan 是否支持数据安全承诺？**

不支持。Coding Plan 未承诺不使用对话数据训练模型。

### **Coding Plan 是否支持高峰期不排队？**

不支持。Coding Plan 在高峰期可能出现排队等待。

### **Coding Plan 是否支持按量计费？**

不支持。Coding Plan 为固定月费订阅制，不提供按量计费选项。

### **Coding Plan 是否支持退订？**

Lite 套餐已停止续费与升级；Pro 套餐支持退订，但不支持退款。

### **Coding Plan 是否支持 RAM 用户？**

支持。RAM 用户需由主账号完成授权后方可使用。

### **Coding Plan 是否支持自动续费？**

支持。用户可在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=plan#/efm/subscription/coding-plan)开启或关闭自动续费。

### **Coding Plan 是否支持升级？**

Lite 套餐已停止升级；Pro 套餐支持升级，但需注意升级后无法降级。

### **Coding Plan 是否支持降级？**

不支持。Coding Plan 不支持降级操作。

### **Coding Plan 是否支持共享用量包？**

不支持。Coding Plan 无共享用量包功能。

### **Coding Plan 是否支持 SSO 接入？**

不支持。Coding Plan 无 SSO 接入功能。

### **Coding Plan 是否支持钉钉接入？**

不支持。Coding Plan 无钉钉接入功能。

### **Coding Plan 是否支持用量分析？**

不支持。Coding Plan 无用量分析功能。

### **Coding Plan 是否支持 API Key 重置？**

支持。用户可在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=plan#/efm/subscription/coding-plan)重置 API Key。

### **Coding Plan 是否支持 Base URL 更换？**

不支持。Coding Plan 的 Base URL 是固定的，不可更换。

### **Coding Plan 是否支持多地域部署？**

不支持。Coding Plan 仅支持华北2（北京）地域。

### **Coding Plan 是否支持多租户隔离？**

不支持。Coding Plan 无多租户隔离架构。

### **Coding Plan 是否支持预算可控？**

不支持。Coding Plan 为固定月费，无预算控制功能。

### **Coding Plan 是否支持数据安全保障？**

不支持。Coding Plan 未提供企业级数据安全保障。

### **Coding Plan 是否支持稳定运行？**

不支持。Coding Plan 在高峰期可能出现排队等待。

### **Coding Plan 是否支持按模型分档抵扣？**

不支持。Coding Plan 按请求次数计费，不按模型分档抵扣。

### **Coding Plan 是否支持 Credits 统一计量？**

不支持。Coding Plan 使用请求次数作为计量单位，而非 Credits。

### **Coding Plan 是否支持 Harness 工具？**

不支持。Coding Plan 不支持 Harness 工具。

### **Coding Plan 是否支持多模态生成模型？**

不支持。Coding Plan 不支持多模态生成模型。

### **Coding Plan 是否支持自定义 MCP？**

不支持。Coding Plan 不支持自定义 MCP。

### **Coding Plan 是否支持视觉理解能力？**

Coding Plan 支持部分模型（如 qwen3.7-plus）原生视觉理解能力，但不支持通过 Skill 或 Agent 添加视觉能力。

### **Coding Plan 是否支持多模型切换？**

支持。Coding Plan 支持在工具中通过 `/model` 指令切换不同模型。

### **Coding Plan 是否支持 API 调用？**

不支持。Coding Plan 仅限在编程工具中交互式使用，禁止以 API 调用的形式用于自动化脚本或应用后端。

### **Coding Plan 是否支持团队管理？**

不支持。Coding Plan 无团队管理功能，仅面向个人开发者。

### **Coding Plan 是否支持数据安全承诺？**

不支持。Coding Plan 未承诺不使用对话数据训练模型。

### **Coding Plan 是否支持高峰期不排队？**

不支持。Coding Plan 在高峰期可能出现排队等待。

### **Coding Plan 是否支持按量计费？**

不支持。Coding Plan 为固定月费订阅制，不提供按量计费选项。

### **Coding Plan 是否支持退订？**

Lite 套餐已停止续费与升级；Pro 套餐支持退订，但不支持退款。

### **Coding Plan 是否支持 RAM 用户？**

支持。RAM 用户需由主账号完成授权后方可使用。

### **Coding Plan 是否支持自动续费？**

支持。用户可在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=plan#/efm/subscription/coding-plan)开启或关闭自动续费。

### **Coding Plan 是否支持升级？**

Lite 套餐已停止升级；Pro 套餐支持升级，但需注意升级后无法降级。

### **Coding Plan 是否支持降级？**

不支持。Coding Plan 不支持降级操作。

### **Coding Plan 是否支持共享用量包？**

不支持。Coding Plan 无共享用量包功能。

### **Coding Plan 是否支持 SSO 接入？**

不支持。Coding Plan 无 SSO 接入功能。

### **Coding Plan 是否支持钉钉接入？**

不支持。Coding Plan 无钉钉接入功能。

### **Coding Plan 是否支持用量分析？**

不支持。Coding Plan 无用量分析功能。

### **Coding Plan 是否支持 API Key 重置？**

支持。用户可在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=plan#/efm/subscription/coding-plan)重置 API Key。

### **Coding Plan 是否支持 Base URL 更换？**

不支持。Coding Plan 的 Base URL 是固定的，不可更换。

### **Coding Plan 是否支持多地域部署？**

不支持。Coding Plan 仅支持华北2（北京）地域。

### **Coding Plan 是否支持多租户隔离？**

不支持。Coding Plan 无多租户隔离架构。

### **Coding Plan 是否支持预算可控？**

不支持。Coding Plan 为固定月费，无预算控制功能。

### **Coding Plan 是否支持数据安全保障？**

不支持。Coding Plan 未提供企业级数据安全保障。

### **Coding Plan 是否支持稳定运行？**

不支持。Coding Plan 在高峰期可能出现排队等待。

### **Coding Plan 是否支持按模型分档抵扣？**

不支持。Coding Plan 按请求次数计费，不按模型分档抵扣。

### **Coding Plan 是否支持 Credits 统一计量？**

不支持。Coding Plan 使用请求次数作为计量单位，而非 Credits。

### **Coding Plan 是否支持 Harness 工具？**

不支持。Coding Plan 不支持 Harness 工具。

### **Coding Plan 是否支持多模态生成模型？**

不支持。Coding Plan 不支持多模态生成模型。

### **Coding Plan 是否支持自定义 MCP？**

不支持。Coding Plan 不支持自定义 MCP。

### **Coding Plan 是否支持视觉理解能力？**

Coding Plan 支持部分模型（如 qwen3.7-plus）原生视觉理解能力，但不支持通过 Skill 或 Agent 添加视觉能力。

### **Coding Plan 是否支持多模型切换？**

支持。Coding Plan 支持在工具中通过 `/model` 指令切换不同模型。

### **Coding Plan 是否支持 API 调用？**

不支持。Coding Plan 仅限在编程工具中交互式使用，禁止以 API 调用的形式用于自动化脚本或应用后端。

### **Coding Plan 是否支持团队管理？**

不支持。Coding Plan 无团队管理功能，仅面向个人开发者。

### **Coding Plan 是否支持数据安全承诺？**

不支持。Coding Plan 未承诺不使用对话数据训练模型。

### **Coding Plan 是否支持高峰期不排队？**

不支持。Coding Plan 在高峰期可能出现排队等待。

### **Coding Plan 是否支持按量计费？**

不支持。Coding Plan 为固定月费订阅制，不提供按量计费选项。

### **Coding Plan 是否支持退订？**

Lite 套餐已停止续费与升级；Pro 套餐支持退订，但不支持退款。

### **Coding Plan 是否支持 RAM 用户？**

支持。RAM 用户需由主账号完成授权后方可使用。

### **Coding Plan 是否支持自动续费？**

支持。用户可在[Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=plan#/efm/subscription/coding-plan)开启或关闭自动续费。

### **Coding Plan 是否支持升级？**

Lite 套餐已停止升级；Pro 套餐支持升级，但需注意升级后无法降级。

### **Coding Plan 是否支持降级？**

不支持。Coding Plan 不支持降级操作。

### **Coding Plan 是否支持共享用量包？**

不支持。Coding Plan 无共享用量包功能。

### **Coding Plan 是否支持 SSO 接入？**

不支持。Coding Plan 无 SSO 接入功能。

###

## 来源文档

- [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-overview.md)
- [团队管理](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-faq.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-quickstart.md)
- [概述](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-faq.md)
- [快速开始](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-quick-start.md)
- [接入 Harness 工具](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)
- [联网搜索](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/web-search-mcp.md)
- [添加视觉理解能力](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/add-vision-skill.md)
- [接入多模态生成模型](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-multimodal-gen.md)
- [Coding Plan概述](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md)
- [常见问题](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan-faq.md)


