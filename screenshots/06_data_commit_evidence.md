# Evidence 06 – Continuous-training data commit

Data-version commits:

```text
07cea8c data: update dataset pointer for continuous training
1e3bf8f data: refresh DVC dataset and trigger pipeline
```

Workflow trigger configuration in `.github/workflows/mlops.yml`:

```yaml
on:
  push:
    branches: [main]
  workflow_dispatch:
```

The workflow is correctly configured for data commits on `main`. GitHub did not expose a separate `push` run for these commits; the successful run available for submission was `workflow_dispatch` run [32446529045](https://github.com/vdungx/TRACK2-Day21-2A202601859-TranVanDung/actions/runs/32446529045).
