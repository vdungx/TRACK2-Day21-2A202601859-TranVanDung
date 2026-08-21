# BÃ¡o cÃ¡o Lab Day 21 â€“ MLOps Pipeline

## Káº¿t quáº£ thá»±c nghiá»‡m

MLflow ghi nháº­n nhiá»u láº§n cháº¡y vá»›i cÃ¡c cáº¥u hÃ¬nh khÃ¡c nhau. Cáº¥u hÃ¬nh Ä‘Æ°á»£c chá»n cho pipeline lÃ  `random_forest`, `n_estimators=500`, `max_depth=null`, `min_samples_split=2`, `random_state=42`. Khi huáº¥n luyá»‡n trÃªn 5.996 máº«u, mÃ´ hÃ¬nh Ä‘áº¡t accuracy `0.746` vÃ  F1-score khoáº£ng `0.745`, vÆ°á»£t ngÆ°á»¡ng Ä‘Ã¡nh giÃ¡ `0.70`.

## Pipeline vÃ  triá»ƒn khai

- DVC quáº£n lÃ½ cÃ¡c táº­p `train_phase1`, `train_phase2` vÃ  `eval`; remote lÃ  Google Cloud Storage.
- GitHub Actions cháº¡y theo chuá»—i Unit Test â†’ Train â†’ Eval â†’ Deploy.
- Eval gate chá»‰ cho phÃ©p triá»ƒn khai khi accuracy Ä‘áº¡t Ã­t nháº¥t `0.70`; pipeline cÅ©ng so sÃ¡nh vá»›i metrics cá»§a model Ä‘ang cháº¡y Ä‘á»ƒ trÃ¡nh rollback ngoÃ i Ã½ muá»‘n.
- MÃ´ hÃ¬nh Ä‘Æ°á»£c phá»¥c vá»¥ bá»Ÿi FastAPI trÃªn VM GCE táº¡i `/health` vÃ  `/predict`. Kiá»ƒm tra thá»±c táº¿ tráº£ vá» `{"status":"ok"}` vÃ  dá»± Ä‘oÃ¡n há»£p lá»‡.

## KhÃ³ khÄƒn vÃ  cÃ¡ch xá»­ lÃ½

Lá»—i cÃ i Google Cloud SDK do file installer bá»‹ tiáº¿n trÃ¬nh khÃ¡c khÃ³a Ä‘Æ°á»£c xá»­ lÃ½ báº±ng viá»‡c cÃ i/khÃ´i phá»¥c SDK qua winget. Lá»—i xÃ¡c thá»±c DVC trÃªn GitHub Actions Ä‘Æ°á»£c kháº¯c phá»¥c báº±ng cÃ¡ch ghi service-account key vÃ o `$GITHUB_WORKSPACE/sa-key.json`, Ä‘Ãºng vá»›i `credentialpath` trong `.dvc/config`. VM dÃ¹ng systemd Ä‘á»ƒ tá»± khá»Ÿi Ä‘á»™ng láº¡i FastAPI khi cÃ³ model má»›i.

## Báº±ng chá»©ng

- GitHub Actions: workflow hoÃ n táº¥t thÃ nh cÃ´ng cáº£ bá»‘n job Test, Train, Eval vÃ  Deploy.
- GCS chá»©a dá»¯ liá»‡u DVC dÆ°á»›i `dvc/` vÃ  model Ä‘ang cháº¡y táº¡i `models/latest/model.pkl`.
- Endpoint phá»¥c vá»¥: `http://34.60.75.138:8000`.

