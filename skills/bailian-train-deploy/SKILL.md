---
name: bailian-train-deploy
description: 用百炼 CLI (`bl`) 走完"数据→微调训练→导出→部署→调用"的完整闭环，或跳过训练直接部署基座模型。涵盖数据集校验/上传、创建 SFT/DPO/CPT 微调任务、等待训练、导出最佳 checkpoint、创建推理部署、等待就绪、给出调用示例。当用户提到在百炼 / DashScope / 阿里云模型工作室上"训练模型""微调""fine-tune""finetune""部署模型""模型上线""把微调模型跑起来/调用""训练一个推理模型""继续预训练""LoRA/SFT/DPO 训练"等，都应激活本技能——即使用户没明说"用 bl"，只要意图是百炼平台的训练或部署，就用本技能，不要自己拼凑命令。
---

# 百炼模型训练→部署闭环 (`bl`)

用百炼 CLI `bl` 把模型部署成可调用的专属推理服务——可以先微调再部署，也可以跳过训练直接部署基座。两条链路，两处"等待"用 Monitor 异步轮询，不阻塞主流程。

```
链路 A（先训练后部署）：
数据集 → finetune create → 等 SUCCEEDED → 导出模型(通常自动) → deploy create → 等 RUNNING → text chat 调用

链路 B（直接部署基座，跳过训练）：
选基座 → deploy create → 等 RUNNING → text chat 调用
```

链路 B 适用于"只想把某个基座跑成自己的部署服务"——和直接调用 API 在推理上没本质区别，但能拿到独立部署实例、可调速率/计费方式、纳入自己的运维。**仅当用户明确表示不训练 / 跳过训练 / 直接部署基座时才走这条**；用户只是没提训练细节时，默认按链路 A 引导，不要擅自跳过训练。

> 本技能假设 `bl`（bailian-cli）已安装。命令/flag 细节以 `bl <cmd> --help` 为准；本技能聚焦**流程编排与避坑**。

## 前置检查

- 认证：`bl auth status`，确认已配置 API key（`DASHSCOPE_API_KEY` 或 `bl auth login --api-key sk-...`）。
- 基座选型：文本推理推荐 Qwen3 系列（支持思维链），常见 `qwen3-8b` / `qwen3-14b` / `qwen3.6-flash`。查询训练能力用 `bl finetune capability`（查 listFoundationModels，走 API key、无需 console 登录）：
  - `bl finetune capability --model qwen3-8b` —— 该模型支持哪些训练类型（返回 `supported: [sft, sft-lora, dpo, ...]`，其中 `cpt` 为 `false` 表示不支持继续预训练）。
  - `bl finetune capability --training-type sft-lora` —— 反向查：哪些模型支持该训练类型（返回 `models` 列表，含中文名）。
  - 选定基座后可直接进入第 2 步；`bl finetune create` 提交前也会再用 listFoundationModels 校验，不支持会快速失败。

## 第 1 步：准备数据集

支持三种数据来源，由你（Agent）根据用户意图灵活选用，不必写死交互流程——你本身具备主动提问能力，知道有哪些选项后自然向用户确认即可：

1. **本地数据集** —— 用户提供本地文件路径，直接使用。
2. **已上传数据集** —— 从百炼上已有的数据集中选取（`bl dataset list`）。
3. **生成示例数据** —— 征得用户同意后，由你生成一份小规模示例数据，仅用于跑通流程（效果有限，需如实告知用户）。

数据为 `.jsonl` 格式（ChatML，每行一个 `{"messages":[...]}` 对象）。提交训练前用 `bl dataset validate --file <path>` 校验通过再继续。

## 第 2 步：创建微调任务

```bash
bl finetune create \
  --model qwen3-8b \
  --datasets <path-or-file-id> \
  --training-type sft-lora \
  --n-epochs 3 \
  --yes --output json
```

**training-type 取值与映射**（CLI 用 `<method>`/`<method>-lora` 约定，提交时映射到服务端字段）：

| CLI 值 | 服务端 | 适用 |
|---|---|---|
| `sft-lora` | efficient_sft | **默认**，LoRA，便宜快，大多数场景 |
| `sft` | 全参 SFT | 效果上限高，成本显著增加 |
| `dpo-lora` / `dpo` | dpo | 偏好对齐，需 preference 数据 |
| `cpt` | 继续预训练 | 注入领域知识，需非对话格式数据 |

> `cpt` 服务端没有 `-lora` 变体，只有全参；其余方法（sft/dpo）均有 `<method>` 与 `<method>-lora` 两个变体。

**超参建议：**
- `n-epochs` 默认 3。小数据集（几百条）3 够用；过拟合降到 1-2。
- `batch-size` 按数据量自适应（<100KB 自动设 8），一般不手动设。
- `learning-rate` 以**字符串**传入避免 JSON 精度丢失，如 `"1e-4"`。LoRA 默认 `3e-4`（平台对小数据集的设定），过拟合可调小。
- `--validations <path>` 可选，传验证集观察指标。

从响应记下：`output.job_id`、`output.finetuned_output`（输出模型名，形如 `qwen3-8b-ft-<ts>-<id>`）。

## 第 3 步：等待训练完成（异步）

用 Monitor 工具运行本技能自带的等待脚本——它会在状态变化时通知，到终态退出：

```
Monitor command: bash <本技能目录>/scripts/wait.sh finetune <JOB_ID>
```

`<本技能目录>` 即本技能的 base 目录（技能加载时会给出，含 `scripts/wait.sh`），用实际路径替换。脚本每 30s 轮询，终态为 `SUCCEEDED`/`FAILED`/`CANCELED`/`PARTIALLY_SUCCEEDED`。

⚠️ **避坑：不要在 zsh 里手写 `status=...` 轮询循环。** `status` 是 zsh 的只读内置变量，赋值会报 `read-only variable` 并让脚本 exit 1。用本技能的 bash 脚本（`#!/usr/bin/env bash`）规避，或自写时改用 `st` 等变量名。

## 第 4 步：导出最佳模型（通常可跳过）

任务 SUCCEEDED 后，平台**会自动导出 best checkpoint** 为可部署模型——直接进第 5 步即可，无需手动导出。

只有要部署**非 best** 的某个 checkpoint 时才显式导出：
```bash
bl finetune checkpoints --job-id <JOB_ID>          # 列出可用 checkpoint
bl finetune export --job-id <JOB_ID> --checkpoint <name> --model-name <自定义名>
```

## 第 5 步：创建部署

⚠️ **关键避坑：微调后的模型不能直接用 `qwen3-8b-ft-...` 名字调用，会 404 `Model not exist`。必须先创建部署。**（链路 B 部署基座同理——直接 `bl text chat --model qwen3-8b` 走的是公共推理，不经过你的部署实例。）

```bash
bl deploy create \
  --model <model-name> \              # 微调输出名(链路A，如 qwen3-8b-ft-...) 或基座名(链路B，如 qwen3-8b)
  --name <display-name> \
  --plan <lora|ptu|mu> \              # 链路A 可用 lora；链路B 通常只能 ptu/mu，见下方说明
  --yes --output json
```

- `--model`：链路 A 传第 2 步的 `finetuned_output`；链路 B 直接传基座模型名（如 `qwen3-8b`）。
- `--plan`：可用计划**随模型来源不同而不同，不要盲目用 `lora`**——
  - 链路 A（微调输出）：`lora`（按 token 计费，默认，适合验证/低负载）；也支持 `mu`。
  - 链路 B（基座）：通常只支持 `ptu`（预留吞吐，需 `--input-tpm`/`--output-tpm`）或 `mu`（独占资源，需 `--template-id`/`--capacity`），**不支持 `lora`**。
- 不确定支持哪些 plan：链路 A 用 `bl deploy models --source custom`，链路 B 用 `bl deploy models --source base`，按返回的 `plans` 选。

⚠️ **避坑（最高频错误）：`--model` 在不同命令里含义不同，切勿混用。**
- `bl deploy create --model` 传的是**导出模型名**（`qwen3-8b-ft-...`，来自第 2 步）。
- 响应里返回的 `output.deployed_model`（如 `qwen3-8b-b98a331831a7`）才是**部署实例 id**。
- 下一步推理 `bl text chat --model` 必须用响应里的 `deployed_model`，**不是**你传给 deploy create 的名字。两个 `--model` 指向不同值，不要复用。

从响应记下：`output.deployed_model`。

## 第 6 步：等待部署就绪（异步）

```
Monitor command: bash <本技能目录>/scripts/wait.sh deploy <DEPLOYED_MODEL>
```

`<本技能目录>` 同第 3 步。每 15s 轮询，`RUNNING` 即就绪（`FAILED`/`STOPPED` 终止）。

⚠️ **避坑：状态传播延迟。** 部署刚到 `RUNNING` 时立即调用，可能短暂返回 404 `Model not exist`——这是服务端状态传播延迟，不是用错模型名。`bl deploy get` 也可能还显示 `PENDING`。约 1 分钟内会稳定，遇 404 等十几秒重试即可；若持续 404，先核对用的是 `deployed_model` 而非微调输出名。

## 第 7 步：调用与交付

```bash
bl text chat --model <DEPLOYED_MODEL> --message "你的问题"
```

向用户交付时给出：
- **部署实例 id**（`deployed_model`）——调用用它，不是 `qwen3-8b-ft-...`
- 一条可直接运行的 `bl text chat` 示例（建议带一个推理类问题演示效果）
- 常用运维命令：`bl deploy get --deployed-model <id>` 查状态；`bl deploy delete --deployed-model <id>` 删除部署；`bl finetune list` 查历史任务。

## 收尾提示
- **闲置计费**：`lora` 按 token 计费，闲置一般不计费，留着无妨；`mu`/`ptu` 是预留资源，闲置也计费，不用要及时清理。注意 `bl deploy delete` 只能删 `STOPPED`/`FAILED` 状态的部署，而 CLI 暂无 stop 命令——RUNNING 状态的 mu/ptu 需先到百炼控制台停用，再删；或用 `bl deploy delete --deployed-model <id> --skip-precheck` 尝试（跳过本地前置检查，但服务端仍可能拒绝 RUNNING 删除）。
- **复用数据集**：多次训练同一数据时，先 `bl dataset upload` 拿 file-id，再用 `--datasets <file-id>` 避免重复上传。
- **效果不好**：优先加数据（量与质量），其次调 `n-epochs`/`learning-rate`，最后才考虑全参 `sft`。小数据集（<100 条）效果上限有限，要管理预期。
