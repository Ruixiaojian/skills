# model deployment 1

百炼平台的 `model deployment 1` 是面向生产环境的模型服务化能力，支持将预置模型或用户调优后的模型（如 LoRA 微调模型）部署为资源独占、性能可预期的专属推理服务。该能力提供三种计费与资源调度模式：预置吞吐（PTU）、模型单元（MU）和按 [Token](../concepts/token.md) 用量计费，分别适配高并发低延迟、高性能定制化及低成本验证等典型场景。部署后可通过标准 API（OpenAI/Anthropic 兼容）调用，所有模式均支持华北2（北京）与新加坡地域。

## 支持的模型与功能

- **预置模型**：千问系列（Qwen3/Qwen2.5/Qwen-VL/Qwen-Omni）、DeepSeek-v3/v4、GLM-4.7/5/5.1/5.2、Kimi-K2.5、CosyVoice 等，具体支持列表以控制台实时可选为准。  
- **调优后模型**：仅支持 LoRA 微调模型（[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)），不支持全参微调模型；导入需满足 rank（8/16/32/64）、词汇表一致性、chat_template 未修改、视觉模型 VIT 冻结等约束。  
- **核心功能**：  
  - PTU 模式支持长输入（最高 1M token）与前缀缓存，通过阶梯容量系数与缓存折扣优化额度消耗；  
  - MU 模式支持 PD 分离计算（降低首 [Token](../concepts/token.md) 延迟）、自定义推理模式（Instruct/Thinking）、最长上下文、RPM/TPM 限流；  
  - [Token](../concepts/token.md) 计费模式仅限部分 LoRA 模型，用于效果验证与低成本试用。

> **注意**：文档 1 中称“部分经过 LoRA 调优后的模型”支持 Token 计费，但文档 4 明确限定“仅支持导入 LoRA 模型”，且文档 3 的 API 示例中 `plan: "lora"` 实际对应 Token 计费模式。三者一致指向 LoRA 是唯一支持 Token 计费的调优类型，不存在矛盾。

## 关键参数

| 参数 | 适用模式 | 说明 | 来源参考 |
|------|----------|------|----------|
| `ptu_capacity.input_tpm` / `output_tpm` | PTU | 预置输入/输出吞吐量（TPM），决定保底服务能力；超出时按溢出策略处理（自动溢出或返回 429） | [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `deploy_spec` / `capacity` / `enable_thinking` | MU | 模型单元规格（如 `MU1 x 8`）、副本数、是否启用思考模式；`max_context_length` 和 `rpm_limit` 仅 MU 模式支持 | [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `cached_tokens` / `provisioned_tokens` | PTU | API 响应中返回的缓存命中 token 数与折算后实际消耗 PTU token 数，用于监控额度使用效率 | [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md) |
| `model_name` | 全模式 | 必填，值为预置模型代码（如 `qwen3.8-max`）或已导入 LoRA 模型 ID（如 `qwen3-8b-ft-202511132025-0260`） | [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |

## 使用方式

1. **控制台操作**：登录百炼控制台 → [模型部署](../concepts/model-deployment.md) → 创建部署，选择地域、模型、计费模式及对应参数（PTU 容量/MU 规格/Token 计费标识），提交即生效。  
2. **API 部署**（推荐自动化）：  
   - PTU 模式：`POST /api/v1/deployments`，`plan: "ptu"`，传入 `ptu_capacity` 对象；  
   - MU 模式：`plan: "mu"`，传入 `deploy_spec`、`capacity`、`enable_thinking` 等字段；  
   - Token 计费：`plan: "lora"`，`capacity` 字段必须填写但实际无效（[使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)）。  
3. **调用与监控**：部署成功（`status: "RUNNING"`）后，使用 `model_name` 作为 API `model` 参数发起推理；通过 [模型监控](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 查看 PTU 利用率、`cached_tokens` 趋势及配额内外调用分布。

## 限制和注意事项

- **地域限制**：API 部署仅支持华北2（北京）地域（文档 3 明确声明），控制台部署支持北京与新加坡双地域。  
- **计费约束**：  
  - PTU 部署创建后计费立即开始，且计费方式不可更改；预付费订单无法提前终止，首月退订按日单价 1.2 倍计费；  
  - MU 后付费资源“先买到先得”，购买失败全额退款；  
  - Token 计费仅对完成 SFT 训练并成功导入的 LoRA 模型开放（文档 1 与文档 4 一致）。  
- **模型限制**：  
  - PTU 模式下，单次输入超过模型上限（如千问 128K、DeepSeek 64K）将自动转为按量计费；  
  - MU 模式支持 PD 分离，但需显式指定 `deploy_spec` 并确认基础模型兼容性（如 `qwen3.6-plus-2026-04-02` 支持 `MU1 x 16（PD分离模式）`）；  
  - OSS 导入的 LoRA 模型不支持增量训练，文件变更后状态变为“已失效”，须重新导入。  
- **权限与授权**：API 部署需确保 API Key 所属业务空间已授权目标模型（[使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)）；OSS 导入需主账号完成服务关联角色授权，并为目标 Bucket 添加 `bailian-datahub-access=read` 标签（[模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)）。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [预置吞吐长输入与缓存](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)


