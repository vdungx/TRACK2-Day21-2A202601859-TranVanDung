# Day 21 MLOps Lab Report

## Experiment result

MLflow contains 7 recorded runs. Every run records both `accuracy` and `f1_score`. The selected configuration is `random_forest`, `n_estimators=500`, `max_depth=null`, `min_samples_split=2`, and `random_state=42`. The best run, trained with 5,996 samples, achieved accuracy `0.746` and F1-score `0.745111`, above the evaluation threshold `0.70`.

## Pipeline and deployment

- DVC tracks `train_phase1`, `train_phase2`, and `eval`; the remote is Google Cloud Storage.
- GitHub Actions runs Unit Test, Train, Eval, and Deploy in sequence.
- The Eval gate stops deployment when accuracy is below `0.70`.
- The pipeline compares the new accuracy with the deployed model before uploading the new model.
- FastAPI serves the model on the GCE VM at `/health` and `/predict`.
- Verified responses were `{"status":"ok"}` and `{"prediction":0,"label":"thap"}`.

## Difficulties and solutions

The Google Cloud SDK installer was locked by another process, so the SDK was installed through winget. DVC authentication in GitHub Actions initially failed because the credential path did not match the generated key location. The workflow now writes the service-account key to `$GITHUB_WORKSPACE/sa-key.json`, matching `.dvc/config`. The VM uses systemd to keep the FastAPI service running.

## Evidence

- MLflow UI: 7 runs with tracked parameters and metrics.
- DVC push completed successfully; the bucket contains the DVC objects and `models/latest/model.pkl` plus `metrics.json`.
- Successful workflow: [MLOps Pipeline #32446529045](https://github.com/vdungx/TRACK2-Day21-2A202601859-TranVanDung/actions/runs/32446529045).
- API endpoint: `http://34.60.75.138:8000`.
- The workflow is configured for `push` events on `main`. The successful run available for submission was started with `workflow_dispatch`; GitHub did not expose a separate `push` run for the data commits, so this is reported honestly rather than presented as an automatic push run.
