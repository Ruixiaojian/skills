# model high speed inference

快速模式（Fast mode）是百炼平台面向低延迟、高吞吐场景提供的高性能推理能力，当前处于 preview 阶段。它通过优化底层调度与计算路径，在保持标准 API 接口兼容的前提下，将输出 TPS 提升至 1.5~2 倍（典型值 80~100 TPS）。该能力适用于 AI 编程助手、Agent 多步推理、实时对话等对响应速度敏感的生产场景。

## 支持的模型/功能

- 当前仅支持 `glm-5.2-fast-preview` 模型，分华北2（北京）和新加坡地域部署，计费单价按地域不同略有差异（详见[原文标题](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)）。
- 支持同步与流式调用；流式响应中，思考过程（`reasoning_content`）与最终回答（`content`）分离推送，便于前端渐进渲染。
- 输出结构兼容 OpenAI 格式，但扩展了 `reasoning_content` 字段及 `usage.completion_tokens_details.reasoning_tokens` 统计项，用于精细化 token 分析。

## 关键参数

| 参数 | 说明 |
|------|------|
| `model` | 必填，固定为 `glm-5.2-fast-preview`；**不支持其他模型 ID**，即使同名非 fast 版本亦无法触发高速路径。 |
| `base_url` | 必须使用专用域名：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（华北2）或对应新加坡地域域名；该地址与标准 API 不互通，详见[原文标题](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。 |
| `stream` | 可选，设为 `true` 启用[流式输出](../concepts/streaming-output.md)；此时需分别处理 `delta.reasoning_content` 和 `delta.content`。 |
| `temperature` / `top_p` 等采样参数 | 行为与标准 API 一致，但因内部优化，实际生成随机性可能略低于标准模式（preview 阶段未承诺完全一致）。 |

> **注意**：文档中提及“按 token 计费，逻辑与标准 API 一致”，但实测发现 `reasoning_tokens` 被计入 `completion_tokens` 并全额计费（而非缓存减免），这与部分旧版文档中“思考内容可缓存”的描述存在矛盾。请以[原文标题](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)中最新计费说明为准，并关注后续更新。

## 使用方式

1. 确保已开通对应地域的业务空间，并在控制台获取 `workspace_id`（路径：[业务空间管理](https://bailian.console.aliyun.com/cn-beijing?tab=globalset#/efm/business_management)）；
2. 构造请求，`model` 设为 `glm-5.2-fast-preview`，`base_url` 指向专用域名；
3. （推荐）启用 `stream: true` 并按字段区分消费 `reasoning_content` 与 `content`；
4. 注意处理排队行为：超出 TPM 额度时请求进入队列，而非直接返回 429，需做好客户端超时与重试策略。

示例（cURL）：
```bash
curl -X POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-5.2-fast-preview",
    "messages": [{"role": "user", "content": "你是谁"}],
    "stream": true
}'
```

## 限制和注意事项

- **Preview 限制**：能力、模型列表、SLA 及计费规则可能随时调整，不建议用于核心链路长期依赖；
- **地域绑定**：模型仅在指定地域（华北2/新加坡）可用，跨地域调用将失败；
- **无额外参数开关**：无需设置 `fast_mode=true` 等 flag，仅靠 `model` ID 和专用域名识别；
- **限流策略特殊**：采用排队机制而非硬限流，需监控端到端延迟，避免队列积压导致长尾延迟；
- **不支持 function calling / tool use**：当前版本暂未开放工具调用能力，相关字段传入将被忽略。

## 来源文档

- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


