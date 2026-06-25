# 百炼模型训练→部署闭环

> [English →](README.md)

**阿里云百炼**平台的「训练 → 部署 → 调用」端到端 Skill —— 用百炼 CLI `bl` 走完完整闭环：数据集校验/上传 → 创建 SFT/DPO/CPT 微调任务 → 等待训练 → 导出 checkpoint → 创建推理部署 → 等待就绪 → 交付可调用示例。也可跳过训练，直接部署基座模型。

## 功能简介

告诉 Agent「训练一个模型」或「把我的微调模型部署到百炼」，这个 Skill 会：

1. **前置检查** —— 验证认证（`bl auth status`）、查询训练能力（`bl finetune capability`），选定支持的基座与训练类型
2. **准备数据** —— 本地文件、已上传数据集或生成示例数据；提交前用 `bl dataset validate` 校验通过
3. **创建微调任务** —— `bl finetune create`，选对 `--training-type`（`sft-lora` / `sft` / `dpo` / `cpt`）与合理超参
4. **异步等待** —— 用 Monitor 脚本轮询训练状态（不阻塞），到 `SUCCEEDED` / `FAILED` / `CANCELED` 终态退出
5. **创建部署** —— `bl deploy create`，把微调（或基座）模型变成专属推理实例
6. **等待就绪** —— 轮询部署状态直到 `RUNNING`
7. **交付调用** —— 给出可直接运行的 `bl text chat` 示例和常用运维命令

## 适用场景

**显式训练/部署：**
- "用我的数据微调一个模型并部署"
- "在百炼上训练 SFT/LoRA/DPO 模型"
- "把我的微调模型部署起来，能调用"

**隐式（描述目标，Skill 跑完整链路）：**
- "用我的客服问答训练一个推理模型"
- "在我的领域文档上继续预训练"
- "我想要一个自己部署的 Qwen 实例"

**直接部署基座（跳过训练）：**
- "把 `qwen3-8b` 部署成我自己的服务"

**不适用：**
- 只想调用公共模型 API → 直接用 `bailian-cli`
- 纯粹的模型选型 / 价格查询 → 用 `bailian-model-recommend` 或 `bailian-docs-llm-wiki`

## 使用示例

```
我有一份本地 jsonl 客服问答数据（ChatML 格式），
用 qwen3-8b 做 LoRA 微调，3 个 epoch，
然后部署起来，让我能像普通模型一样调用。
```

Skill 会走两段链路，在两处「等待」用 Monitor 异步轮询：

```
链路 A（先训练后部署）：
数据集 → finetune create → 等 SUCCEEDED → (自动导出) → deploy create → 等 RUNNING → text chat

链路 B（直接部署基座，跳过训练）：
基座 → deploy create → 等 RUNNING → text chat
```

每一步捕获正确的 id（`job_id` / `finetuned_output` → `deployed_model`），并绕开常见坑（例如直接用 `qwen3-8b-ft-...` 名字调用会 404 —— 必须先部署，再用响应里的 `deployed_model` 实例 id 调用）。

## 前置要求

- 已安装 `bl`（bailian-cli）并完成认证（`bl auth status`，或 `bl auth login --api-key sk-...`）
- 文本推理推荐基座：Qwen3 系列（`qwen3-8b` / `qwen3-14b` / `qwen3.6-flash`）

## 内部工作流程

```
用户请求
  → 前置检查：认证 + 训练能力（listFoundationModels，走 API key）
  → 准备并校验数据集（.jsonl ChatML）
  → finetune create（默认 sft-lora；CLI 值映射到服务端字段）
  → Monitor wait.sh finetune <JOB_ID>  （30s 轮询，异步）
  → 自动导出 best checkpoint（通常跳过手动导出）
  → deploy create（按模型来源选 plan：微调用 lora，基座用 ptu/mu）
  → Monitor wait.sh deploy <DEPLOYED_MODEL> （15s 轮询，异步）
  → text chat --model <DEPLOYED_MODEL> + 运维命令
```

Skill 把完整编排和高频避坑点都固化进去（zsh 的 `status` 是只读变量、`--model` 在 `deploy create` 与 `text chat` 里含义不同、刚到 `RUNNING` 时状态传播延迟导致 404、`lora` / `mu` / `ptu` 闲置计费差异），让 Agent 不必重新踩坑。

## License

Apache-2.0
