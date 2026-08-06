# model deployment 1

`model deployment 1` 指百炼平台中以 **预置吞吐（PTU）** 方式部署模型的核心能力，面向高并发、低延迟、流量可预估的生产场景。它通过预留固定 TPM（每分钟 [Token](../concepts/token.md) 数）容量保障服务确定性，支持长输入、前缀缓存、自动溢出等关键特性，并与按量计费无缝衔接。本文档聚焦 PTU 部署的实操要点，不涵盖模型单元（MU）或按 [Token](../concepts/token.md) 计费等其他部署模式。

## 支持的模型/功能

- **核心模型支持**：当前 PTU 部署仅支持部分预置模型，包括 `glm-5.1`、`deepseek-v4-pro`、`qwen3.7-plus-2026-05-26` 等（详见[额度消耗规则](#sec-billing)表格），不支持 LoRA 导入模型直接部署为 PTU 服务。LoRA 模型需先通过[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)流程上传，再选择「模型单元」或「按 [Token](../concepts/token.md) 计费」方式部署。
  
- **长输入支持**：部分模型支持远超 32K token 的输入（如 `glm-5.1` 最高 200K，`deepseek-v4-pro` 和 `qwen3.7-plus-2026-05-26` 最高 256K），超出基础长度的部分按阶梯系数折算 TPM 消耗。单次输入超过模型硬上限（如千问系列 128K、DeepSeek 系列 64K）时，请求将自动转为按量计费 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

- **前缀缓存（Context Cache）**：对具备缓存能力的模型（如 `glm-5.1`、`deepseek-v4-pro`），重复的输入前缀可被缓存并按折扣系数（如 `glm-5.1` 为 0.2）折算额度消耗，显著降低多轮对话和长文档分析场景的成本。缓存命中情况可通过 API 响应中的 `cached_tokens` 字段验证 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

> **注意**：文档 2 中“支持模型”表格列出 `qwen3.8-max`（输入上限 1M）并标注为 PTU 可用，但文档 1 的“额度消耗规则”表格及全文均未提及该模型支持长输入阶梯系数或缓存折扣。实际使用时请以控制台创建页动态展示的 PTU 可选模型为准，避免依赖静态表格。

## 关键参数

PTU 部署的核心参数为 `input_tpm` 和 `output_tpm`，单位均为 KTPM（千 Token/分钟），代表购买的吞吐容量：

- `input_tpm`：保障每分钟可处理的**输入 token 总量**（已含阶梯系数折算）。
- `output_tpm`：保障每分钟可处理的**输出 token 总量**（已含阶梯系数折算）。

其他关键配置：
- **溢出策略**：创建时必选，决定超额行为：
  - `auto_overflow`（默认）：超额请求自动转为按量计费，服务不中断，响应头含 `x-dashscope-ptu-overflow:true`；
  - `ptu_only`：超额请求直接返回 HTTP 429，不产生额外费用。
- **模型代码（model_name）**：必须使用平台定义的精确模型代码（如 `glm-5.1`），而非显示名称。

## 使用方式

### 控制台操作
1. 进入[百炼控制台 → 模型部署 → 创建部署](https://bailian.console.aliyun.com/#/efm/model_deploy/create)，选择「预置吞吐（PTU）」。
2. 选择支持 PTU 的模型（列表动态加载，非静态表格）。
3. 展开「预置吞吐额度计算器」，输入业务参数（RPM、平均输入/输出长度、缓存命中率）获取推荐 `input_tpm`/`output_tpm` 值 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
4. 设置溢出策略，确认购买并提交。

### API 调用（HTTP）
```bash
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "name": "my_ptu_service",
    "model_name": "glm-5.1",
    "plan": "ptu",
    "ptu_capacity": {
      "input_tpm": 20000,
      "output_tpm": 2000
    }
  }'
```

部署成功后，API 响应 `status` 为 `PENDING`，待变为 `RUNNING` 即可调用。调用时，API 响应体包含 `service_tier`（值为 `ptu-standard` 表示使用 PTU）、`provisioned_tokens`（折算后消耗额度）和 `cached_tokens`（缓存命中数）等关键字段，用于监控和计费核验 [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。

## 限制和注意事项

- **模型限制**：PTU 仅支持平台预置模型，**不支持通过[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)上传的 LoRA 模型**。LoRA 模型只能选择「模型单元」或「按 Token 计费」方式部署。
  
- **额度计算复杂性**：实际 TPM 消耗受长输入阶梯系数和缓存折扣双重影响。例如 `glm-5.1` 输入 50K token 且无缓存时，消耗为 `32K×1.0 + 18K×1.33 = 55.94 KTPM`，而非简单 50K。务必使用「预置吞吐额度计算器」进行估算，避免额度不足导致意外按量计费。

- **监控指标解读**：PTU 利用率可能超过 100%，这是因阶梯系数使折算消耗 > 原始 token 数所致，属正常现象。监控中应重点关注 `cached_tokens` 占比和 `配额内/外调用次数`，而非单纯看利用率数值。

- **地域限制**：API 部署示例明确标注“仅适用于华北2（北京）地域”，其他地域需确认对应 endpoint 和可用模型。

## 来源文档

- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)


