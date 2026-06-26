# bailian-train-deploy

> [中文版 / Chinese →](README.zh.md)

End-to-end **train → deploy → call** skill for **Alibaba Cloud Model Studio (Bailian)** — drives the full closed loop with the Bailian CLI (`bl`): dataset validation/upload → SFT/DPO/CPT fine-tune → wait for training → export checkpoint → create inference deployment → wait for ready → hand off a callable example. Can also skip training and deploy a base model directly.

## What it does

Tell your agent "train a model" or "deploy my fine-tuned model on Bailian," and this skill will:

1. **Pre-check** — verify auth (`bl auth status`) and query training capabilities (`bl finetune capability`) to pick a supported base model and training type
2. **Prepare data** — local file, an already-uploaded dataset, or a generated sample; validate with `bl dataset validate` before submitting
3. **Create the fine-tune job** — `bl finetune create` with the right `--training-type` (`sft-lora` / `sft` / `dpo` / `cpt`) and sensible hyperparameters
4. **Wait asynchronously** — poll training status via a Monitor script (non-blocking), exit on `SUCCEEDED` / `FAILED` / `CANCELED`
5. **Deploy** — `bl deploy create` to turn the fine-tuned (or base) model into a dedicated inference instance
6. **Wait for ready** — poll deployment status until `RUNNING`
7. **Hand off** — a ready-to-run `bl text chat` example plus common ops commands

## When to use

**Explicit training/deployment:**
- "Fine-tune a model on my data and deploy it"
- "Train an SFT/LoRA/DPO model on Bailian"
- "Deploy my fine-tuned model so I can call it"

**Implicit (describe a goal, the skill runs the loop):**
- "Train a reasoning model on my customer Q&A"
- "Continued-pretrain on my domain docs"
- "I want my own deployed Qwen instance"

**Direct base-model deployment (skip training):**
- "Just deploy `qwen3-8b` as my own service"

**Not for this skill (reverse-trigger routing):**
- Just want to try a model / one-off chat → `bailian-cli`: `bl text chat --model qwen3-8b --message "..."`
- Don't know which base model to pick → `bailian-model-recommend`
- Pure parameter / pricing / context-window lookup → `bailian-docs-llm-wiki`
- Lifecycle management of existing jobs/deployments (list/stop/delete) → `bl` directly: `bl finetune list` / `bl deploy list` / `bl deploy delete`

## Safety guardrails

`bl finetune create` and `bl deploy create` are real write operations that create billable resources. `bl` has **no `--dry-run`**, so the skill substitutes real pre-checks + a billing gate:

1. **Pre-checks instead of dry-run** — `bl finetune capability --model <base>` (training support), `bl deploy models --source custom|base` (deployable + available plans), `bl deploy list --status RUNNING` (reuse an existing deployment of the same model instead of creating a second billable instance).
2. **Billing gate on `mu`/`ptu`** — `lora` (token-billed, idle usually free) is the safe default; `mu`/`ptu` are reserved resources that bill even when idle, so the skill **asks the user for explicit confirmation before creating them** and never auto-approves reserved resources with `--yes` in non-interactive (agent/CI) contexts.
3. **Account readiness** — `bl auth status` first; stop if not authenticated.

## Prerequisites

- `bl` (bailian-cli) installed and authenticated (`bl auth status`, or `bl auth login --api-key sk-...`)
- Recommended base for text reasoning: Qwen3 series (`qwen3-8b` / `qwen3-14b` / `qwen3.6-flash`)

## Example

```
I have a local jsonl of customer-service Q&A (ChatML format).
Fine-tune qwen3-8b with LoRA, 3 epochs, then deploy it so I can
call it like a normal model.
```

The skill walks the two-link pipeline, polling at the two wait points via Monitor:

```
Link A (train then deploy):
dataset → finetune create → wait SUCCEEDED → (auto-export) → deploy create → wait RUNNING → text chat

Link B (deploy base, skip training):
base model → deploy create → wait RUNNING → text chat
```

It captures the right IDs at each step (`job_id` / `finetuned_output` → `deployed_model`) and steers around the common pitfalls (e.g. calling the fine-tuned model by its `qwen3-8b-ft-...` name returns 404 — you must deploy first and call the `deployed_model` instance id).

## How it works under the hood

```
User request
  → Pre-check auth + training capability (listFoundationModels via API key)
  → Prepare & validate dataset (.jsonl ChatML)
  → finetune create (sft-lora default; map CLI value → server field)
  → Monitor wait.sh finetune <JOB_ID>   (30s poll, async)
  → Auto-export best checkpoint (usually skip manual export)
  → deploy create (pick plan by model source: lora for ft, ptu/mu for base)
  → Monitor wait.sh deploy <DEPLOYED_MODEL>  (15s poll, async)
  → text chat --model <DEPLOYED_MODEL> + ops commands
```

The skill encodes the full orchestration plus the gotchas (zsh `status` is read-only, `--model` means different things in `deploy create` vs `text chat`, state-propagation 404 right after `RUNNING`, idle-billing differences between `lora` / `mu` / `ptu`) so the agent doesn't have to rediscover them.

## License

Apache-2.0
