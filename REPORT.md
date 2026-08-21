# Báo cáo Lab Day 21 – MLOps Pipeline

## Kết quả thực nghiệm

MLflow ghi nhận nhiều lần chạy với các cấu hình khác nhau. Cấu hình được chọn cho pipeline là `random_forest`, `n_estimators=500`, `max_depth=null`, `min_samples_split=2`, `random_state=42`. Khi huấn luyện trên 5.996 mẫu, mô hình đạt accuracy `0.746` và F1-score khoảng `0.745`, vượt ngưỡng đánh giá `0.70`.

## Pipeline và triển khai

- DVC quản lý các tập `train_phase1`, `train_phase2` và `eval`; remote là Google Cloud Storage.
- GitHub Actions chạy theo chuỗi Unit Test → Train → Eval → Deploy.
- Eval gate chỉ cho phép triển khai khi accuracy đạt ít nhất `0.70`; pipeline cũng so sánh với metrics của model đang chạy để tránh rollback ngoài ý muốn.
- Mô hình được phục vụ bởi FastAPI trên VM GCE tại `/health` và `/predict`. Kiểm tra thực tế trả về `{"status":"ok"}` và dự đoán hợp lệ.

## Khó khăn và cách xử lý

Lỗi cài Google Cloud SDK do file installer bị tiến trình khác khóa được xử lý bằng việc cài/khôi phục SDK qua winget. Lỗi xác thực DVC trên GitHub Actions được khắc phục bằng cách ghi service-account key vào `$GITHUB_WORKSPACE/sa-key.json`, đúng với `credentialpath` trong `.dvc/config`. VM dùng systemd để tự khởi động lại FastAPI khi có model mới.

## Bằng chứng

- GitHub Actions: workflow hoàn tất thành công cả bốn job Test, Train, Eval và Deploy.
- GCS chứa dữ liệu DVC dưới `dvc/` và model đang chạy tại `models/latest/model.pkl`.
- Endpoint phục vụ: `http://34.60.75.138:8000`.
