# Báo cáo Lab Day 21 – MLOps Pipeline

## Kết quả thực nghiệm

MLflow hiện có 11 lần chạy. Mỗi lần chạy đều ghi nhận đầy đủ `accuracy` và `f1_score`. Bộ siêu tham số được chọn là `random_forest`, `n_estimators=500`, `max_depth=null`, `min_samples_split=2`, `random_state=42`. Lần chạy Bước 3 trên 5.996 mẫu đạt accuracy `0.746` và F1-score `0.745111`, vượt ngưỡng đánh giá `0.70`.

So sánh trước và sau khi bổ sung dữ liệu:

| Chỉ số | Bước 2 – 2.998 mẫu | Bước 3 – 5.996 mẫu |
|---|---:|---:|
| Accuracy | 0.676 | 0.746 |
| F1-score | 0.674809 | 0.745111 |

Kết quả cho thấy việc bổ sung dữ liệu giúp tăng accuracy khoảng 0.070 và F1-score khoảng 0.070302.

## Pipeline và triển khai

- DVC quản lý các tập dữ liệu `train_phase1`, `train_phase2` và `eval`; remote lưu trên Google Cloud Storage.
- GitHub Actions chạy theo thứ tự Unit Test → Train → Eval → Deploy.
- Eval gate chặn triển khai nếu accuracy thấp hơn `0.70`.
- FastAPI phục vụ model trên VM GCE qua hai endpoint `/health` và `/predict`.
- Kết quả kiểm tra sau deploy Bước 3: `{"status":"ok"}` và `{"prediction":0,"label":"thap"}`.

## Khó khăn và cách xử lý

File cài Google Cloud SDK ban đầu bị tiến trình khác khóa nên đã chuyển sang cài bằng winget. GitHub Actions từng lỗi xác thực DVC vì đường dẫn credential không khớp vị trí service-account key. Workflow hiện ghi key vào `$GITHUB_WORKSPACE/sa-key.json`, đúng với cấu hình trong `.dvc/config`. VM sử dụng systemd để duy trì dịch vụ FastAPI.

## Bằng chứng

- MLflow UI hiển thị 7 lần chạy với các siêu tham số và chỉ số đánh giá.
- DVC push thành công; bucket có dữ liệu DVC và các file `models/latest/model.pkl`, `models/latest/metrics.json`.
- Workflow Bước 2 thành công: [MLOps Pipeline #32446529045](https://github.com/vdungx/TRACK2-Day21-2A202601859-TranVanDung/actions/runs/32446529045).
- API triển khai: `http://34.60.75.138:8000`.
- Workflow trigger khi thay đổi `data/**.dvc`, `src/**.py` hoặc `params.yaml` trên nhánh `main`. Commit dữ liệu `0007119` đã tự động kích hoạt [MLOps Pipeline #32451053806](https://github.com/vdungx/TRACK2-Day21-2A202601859-TranVanDung/actions/runs/32451053806); cả Unit Test, Train, Eval và Deploy đều hoàn thành thành công trên dataset 5.996 mẫu.
