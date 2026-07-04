---
name: repro-pack
description: "Build reproducibility packages for research projects: code, data, environment, configs, exact commands, seeds, logs, result tables, figures, checksums, model cards, artifact appendices, and known issues. Use when the user asks for Repro Pack, reproducibility package, artifact appendix, open-source release prep, or experiment handoff."
---

# Repro Pack

Create a runnable, reviewable package, not just a README.

Recommended structure:

```text
repro-pack/
  README.md
  environment.yml / requirements.txt / Dockerfile
  data/README.md
  data/checksums.txt
  configs/
  scripts/train.sh
  scripts/eval.sh
  scripts/reproduce_tables.sh
  logs/
  results/tables/
  results/figures/
  model_cards/
  commit.txt
  known_issues.md
```

Always capture exact commands, commit hash, dataset version, seeds, hardware, runtime, and expected outputs. Validate by running the smallest representative reproduce command when feasible.
