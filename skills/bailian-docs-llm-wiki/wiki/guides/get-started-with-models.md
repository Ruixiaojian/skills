# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）全系列及主流第三方模型。开发者无需自行部署或运维，只需配置 API Key 和 Base URL 即可发起首次请求。平台同时支持可视化应用构建、微调与部署等全链路能力，适用于从快速验证到生产级落地的各类场景。

## 支持的模型与功能

百炼提供覆盖文本、图像、音频、视频等多模态的模型服务，核心包括：

- **千问（Qwen）系列**：按能力与成本分层，推荐优先选用 `qwen3.7-plus`（效果、速度、成本均衡）；复杂任务可选 `qwen3.7-max`；低延迟简单任务适用 `qwen3.7-flash`。[选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 文档详细列出了各模型在不同地域的可用性、ID 及上下文长度。
- **第三方模型**：支持 DeepSeek、Kimi、GLM 等，但部分模型（如 DeepSeek）仅限华北2（北京）地域使用，详见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。
- **功能扩展**：除基础文本生成外，还支持视觉理解、图像生成、语音识别与合成、嵌入向量、长文本处理、法律/意图/角色扮演等细分领域模型。

> **注意**：文档 3（`models.md`）中列出 `qwen3.8-max-preview` 仅限 [Token](../concepts/token.md) Plan 用户，而文档 1（`what-is-model-studio.md`）未提及该限制，实际使用需以控制台模型广场为准。

## 关键参数

调用模型必需的核心参数如下：

- **API Key**：在 [API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建并管理，**不同地域的 API Key 不通用**。
- **Base URL**：必须与 API Key 所属地域及计费方案严格匹配：
  - **业务空间专属域名**（推荐生产环境）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，其中 `{WorkspaceId}` 需从 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management) 获取；
  - **Dashscope 域名**（兼容存量）：如 `https://dashscope.aliyuncs.com/compatible-mode/v1`（北京）、`https://dashscope-us.aliyuncs.com/compatible-mode/v1`（美国）；
  - **试用域名**（限流严格）：如 `https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。
  详细对比见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。
- **模型 ID**：如 `"qwen3.7-plus"`，需与所选地域支持的模型一致。部分模型带地域后缀（如 `qwen3.7-plus-us`），用于限定推理位置。

## 使用方式

1. **环境准备**：
   - 注册阿里云账号并完成实名认证；
   - 开通百炼服务，在控制台创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`（[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 提供各系统配置指南）；
   - 获取业务空间 ID（若使用专属域名）。

2. **代码调用（OpenAI SDK 示例）**：
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为实际 WorkspaceId
   )
   response = client.chat.completions.create(
       model="qwen3.7-plus",
       messages=[{"role": "user", "content": "你是谁？"}]
   )
   print(response.choices[0].message.content)
   ```

3. **其他方式**：支持 Node.js SDK、curl、DashScope SDK 及可视化工具（如 Chatbox）。完整接入方式参见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

## 限制和注意事项

- **地域隔离**：各地域（北京、新加坡、美国、德国、日本）的 API Key、Base URL、模型列表、功能支持均相互独立，**严禁跨地域混用**。例如，德国法兰克福地域不支持 DashScope 域名，仅支持业务空间专属域名（见 [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)）。
- **限流策略**：按主账号维度统一计算 RPM（每分钟请求数）和 TPM（每分钟 [Token](../concepts/token.md) 数），不同模型额度独立。稳定版模型（如 `qwen3.7-plus`）限流宽松（RPM 30,000 / TPM 5,000,000），快照版（如 `qwen-plus-2025-07-28`）则显著收紧（RPM 60 / TPM 1,000,000）。触发限流时错误码为 `429`，可通过 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 文档排查与优化。
- **费用与安全**：
  - 新用户享有北京地域免费额度，用尽后自动转为按量付费（已认证用户）或停止服务（未认证用户）；
  - 数据全程加密传输，阿里云承诺**不将用户数据用于模型训练**；
  - 模型推理与知识库（RAG）计费完全独立，不可用节省计划抵扣。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


