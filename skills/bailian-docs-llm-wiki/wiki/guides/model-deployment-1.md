# model deployment 1

百炼平台提供模型部署能力，将预置模型或调优后的模型部署为独立、资源专享的推理服务，以满足高并发、低延迟等业务需求。本主题汇总了模型部署的三种计费方式、API 部署流程，以及从 OSS 导入自定义 LoRA 模型的要求与操作。

> **注意**：以下所有部署能力**仅适用于"中国内地（北京）"地域**。

## 支持的模型与功能

百炼平台支持的部署对象包括：

- **平台预置模型**：千问系列（Max / Plus / Flash / VL / Omni）、DeepSeek、GLM、MiniMax、Kimi、CosyVoice 等，最长上下文从 64K 到 128K Token 不等。
- **调优后的自定义模型**：仅支持 **LoRA**（Low-Rank Adaptation）微调模型，不支持全参微调模型。
- **本地训练的 LoRA 模型**：通过 OSS 导入。当前可作为基础模型导入的有千问3（32B/14B/8B/4B-Instruct-2507）、千问3-VL-8B-Instruct、千问2.5（72B/32B/14B/7B-Instruct）、千问2.5-VL（72B/7B-Instruct）。

完整的模型清单与单价请见 [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

## 三种计费方式

部署模型时必须选择一种计费方式，**服务创建后无法更改**；如需切换，必须先下线再重新部署。

| 计费方式 | 适用场景 | 资源特性 | 性能可调性 |
| --- | --- | --- | --- |
| **预置吞吐（PTU）** | 高负载生产环境，流量稳定可预估 | 平台预留资源、按 TPM 保障吞吐 | 不可调（吞吐/生成速度由平台预置），相比 Token 用量 TPS 提升约 1.5～2.0 倍 |
| **模型单元（MU）** | 调优后大规模推理、需独占资源 | 资源独占，按使用时长 × 模型单元数 | 可自定义最长上下文、RPM/TPM 限流，支持 PD 分离模式 |
| **按 Token 用量** | 调优后效果验证、低并发高性价比 | 不使用不计费 | 不可调，**仅支持部分 SFT/LoRA 调优后的模型** |

各方式的扩缩容方式：
- PTU：自助增减吞吐量
- MU：自助增减模型单元数量
- Token 用量：控制台提交申请，等待人工审核

更多计费公式、单价表、PD 分离模式说明参考 [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

## 通过 API 部署（关键参数）

通用入口为 `POST https://dashscope.aliyuncs.com/api/v1/deployments`，请求体中通过 `plan` 字段切换计费方式。完整示例见 [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

### PTU（预置吞吐）

```json
{
  "name": "my_qwen_flash",
  "model_name": "qwen-flash-2025-07-28",
  "plan": "ptu",
  "ptu_capacity": { "input_tpm": 10000, "output_tpm": 1000 }
}
```

### MU（模型单元）

```json
{
  "name": "my_qwen_plus",
  "model_name": "qwen-plus-2025-12-01",
  "plan": "mu",
  "deploy_spec": "MU1",
  "enable_thinking": true,
  "capacity": 4,
  "max_context_length": 10000,
  "rpm_limit": 500,
  "tpm_limit": 1000
}
```

关键字段：
- `deploy_spec`：模型单元规格（如 MU1、MU2 等，规格能力差异见单价表）
- `capacity`：模型单元数量
- `enable_thinking`：是否开启思考模式（仅 Instruct/Thinking 双模式模型支持）
- `max_context_length`：最长上下文，依赖模型类型
- `rpm_limit` / `tpm_limit`：服务级限流

### Token 用量（LoRA）

```json
{
  "model_name": "qwen3-8b-ft-202511132025-0260",
  "plan": "lora",
  "capacity": 1,
  "name": "qwen3-8b-ft"
}
```

> **注意**：`capacity` 字段在 `plan=lora` 时**填写无效但必须传**，扩缩容需在控制台提交人工申请。

### 图片/视频模型（按算力单元 cu）

```json
{
  "model_name": "animate-anyone-detect",
  "capacity": 2,
  "plan": "cu",
  "name": "my_animate"
}
```

### 部署后查询、调用与删除

- 查询：`GET /api/v1/deployments/{deployed_model}`，`status` 为 `RUNNING` 表示已就绪
- 调用：`model` 参数传入返回值中的 `deployed_model`（即模型 code），可用 OpenAI 兼容协议、DashScope SDK、Assistant SDK 任一方式
- 删除：`DELETE /api/v1/deployments/{deployed_model}`，**立即下线、停止计费、不可恢复**

## 导入自定义 LoRA 模型

通过 **我的模型** → **导入模型** 可将本地训练的 LoRA 适配器从 OSS 拉到百炼平台。详细步骤、授权方法、子账号 RAM 策略示例见 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

### OSS 准备要点

- Bucket 不能是归档/冷归档/深度冷归档存储类型；支持私有 Bucket、内容加密 Bucket。
- 模型文件夹必须放在 Bucket 的**子目录**下，不支持根目录访问。
- 必须为 Bucket 添加标签 `bailian-datahub-access` = `read`，否则百炼无法读取。
- 首次导入需开通 OSS 服务关联角色；子账号还需主账号在 RAM 中授予 `ram:CreateServiceLinkedRole` 权限（限定 `ram:ServiceName=datahub.sfm.aliyuncs.com`）。

### 文件要求

- 必需文件：`adapter_model.safetensors`（LoRA 权重）+ `adapter_config.json`（含 rank、alpha）
- `rank` 取值只能是 **8、16、32、64**，且同一模型所有 LoRA 层必须一致
- **禁止修改词汇表**：训练中新增 token 或改动 vocab 的模型无法导入
- **禁止修改 chat_template**：必须与基础模型默认配置一致（检查 `config.json` 与 `tokenizer_config.json`）
- **VL 模型必须冻结 VIT**：`adapter_model.safetensors` 中不能包含以 `visual` 开头的权重键

### 推理参数对齐

> **注意**：导入模型后若发现与本地 vLLM/SGLang 推理结果不一致，主要原因是采样参数默认值不同。建议调用时显式对齐 `temperature=1.0`、`top_p=1.0`、`top_k>100`（或 None）、`presence_penalty=0`、`repetition_penalty=1.0`，以贴近 vLLM 默认行为。

## 限制与常见问题

- **计费即开始**：部署成功立即开始计费，即便未发起任何调用。
- **预付费规则**：PTU 预付费按天，MU 预付费按月；首月内提前退订，日单价按 **1.2 倍** 计费，且无法提前终止预付费订单。
- **欠费保留**：后付费欠费后资源继续保留并计费 24 小时，之后自动释放。
- **超量降级**：PTU 超出购买 TPM 时自动降级为按量付费，响应头返回 `x-dashscope-ptu-overflow: true`，并受业务空间公共流量限流。
- **Token 用量模式自动释放**：1 个月未使用将自动释放部署。
- **权限报错**：API 报 `Workspace xxx does not have deployment privilege for model xxxx` 时，需在业务空间的"模型权限流控设置"中为目标模型授权；报 `Workspace access denied` 时，需在业务空间的"权限管理"中加入 API Key 归属账号。
- **业务空间一致性**：调用专属服务的 API Key 必须与部署所在的业务空间相同。

## 来源文档

- [模型部署简介](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [使用 API或命令行进行模型部署](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)


