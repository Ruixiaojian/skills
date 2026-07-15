# model high speed inference

百炼平台提供两类面向高吞吐、低延迟场景的推理加速能力：**快速模式（Fast mode）** 与 **TPM 预留（TPM Reservation）**。二者目标一致——提升服务稳定性与响应速度，但技术路径不同：前者通过模型级优化实现更高 TPS，后者通过资源独占保障确定性吞吐。开发者需根据业务对延迟敏感度、流量可预测性及成本结构选择合适方案。

## 支持的模型/功能

- **快速模式**：当前仅支持 `glm-5.2-fast-preview` 模型（北京、新加坡地域），为预览阶段能力，模型 ID 即启用标识，无需额外参数 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。  
- **TPM 预留**：支持多款主流模型，包括 `GLM-5.2`、`GLM-5.1`、`千问3.7-Max-2026-05-20`、`DeepSeek-v4-Pro`、`Kimi-K2.6` 等（具体以控制台实时列表为准），需创建后获取专属模型 code 才能调用 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- > **注意**：文档 1 中 `glm-5.2-fast-preview` 标注为 preview 阶段，而文档 2 中 `GLM-5.2`（无 `-fast-preview` 后缀）列为 TPM 预留支持模型。二者非同一模型变体：前者是专有高速推理版本，后者是标准模型的容量保障通道。不可混用 model ID。

## 关键参数

| 能力类型 | 核心参数 | 说明 |
|----------|----------|------|
| 快速模式 | `model="glm-5.2-fast-preview"` | 唯一启用标识；接入域名固定为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（北京）或对应新加坡地域域名 |
| TPM 预留 | `model="<dedicated-model-code>"` | 创建后生成的唯一字符串；必须替换原 model ID；接入域名与标准 API 一致（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`） |
| 共同参数 | `stream=true/false` | [流式输出](../concepts/streaming-output.md)时，快速模式返回 `delta.reasoning_content` 和 `delta.content` 字段；TPM 预留行为与标准模型一致 |

## 使用方式

- **快速模式**：直接在请求中指定 `model: "glm-5.2-fast-preview"`，其余参数（如 `messages`, `stream`）与标准 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)一致。流式响应需分别处理 `reasoning_content` 与 `content` 字段 [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。  
- **TPM 预留**：创建成功后，在控制台详情页复制专属模型 code，替换 API 请求中的 `model` 参数即可生效。首次调用存在短暂预热期，建议客户端实现重试或排队机制 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
- **共用要求**：均需有效 `API_KEY` 与正确 `base_url`；快速模式强制使用 workspace 绑定域名，TPM 预留使用全局兼容域名。

## 限制和注意事项

- **快速模式限制**：  
  - 仅限 `glm-5.2-fast-preview` 模型，不支持其他模型；  
  - 处于 preview 阶段，接口行为、计费策略或模型能力可能调整；  
  - 超出 TPM 额度时请求进入排队队列，而非立即拒绝。  

- **TPM 预留限制**：  
  - 预留容量按 kTPM（千 tokens/分钟）购买，输入/输出 TPM 分开配置；  
  - 缩容退费按公式 `退款 = 降量部分预付费 - (降量部分预付费 × 已用时长/购买时长 × 1.5)` 计算；  
  - 实例到期后 2 小时内仍可调用，14 小时后彻底删除且不可恢复。  

- **通用注意事项**：  
  - 快速模式与 TPM 预留**不可叠加使用**：`glm-5.2-fast-preview` 不支持 TPM 预留，TPM 预留仅作用于标准模型（如 `GLM-5.2`）；  
  - 缓存折扣仅影响输入容量计算（如 `glm-5.2` 缓存命中部分按 25% 折算），不影响输出；  
  - 超额处理逻辑不同：快速模式排队，TPM 预留自动降级至按量计费 [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

## 来源文档

- [快速模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)
- [TPM 预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)


