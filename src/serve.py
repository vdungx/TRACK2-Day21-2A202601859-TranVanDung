import os
from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException
from google.cloud import storage
from pydantic import BaseModel

app = FastAPI()
GCS_BUCKET = os.environ.get("GCS_BUCKET")
GCS_MODEL_KEY = "models/latest/model.pkl"
MODEL_PATH = Path(os.path.expanduser("~/models/model.pkl"))
LABELS = {0: "thap", 1: "trung_binh", 2: "cao"}


def download_model():
    if not GCS_BUCKET:
        raise RuntimeError("GCS_BUCKET environment variable is required")
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    client = storage.Client()
    blob = client.bucket(GCS_BUCKET).blob(GCS_MODEL_KEY)
    blob.download_to_filename(str(MODEL_PATH))
    print(f"Model downloaded from gs://{GCS_BUCKET}/{GCS_MODEL_KEY}")


download_model()
model = joblib.load(MODEL_PATH)


class PredictRequest(BaseModel):
    features: list[float]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(req: PredictRequest):
    if len(req.features) != 12:
        raise HTTPException(
            status_code=400,
            detail="Expected 12 features (wine quality)",
        )
    prediction = int(model.predict([req.features])[0])
    if prediction not in LABELS:
        raise HTTPException(status_code=500, detail=f"Unknown model prediction: {prediction}")
    return {"prediction": prediction, "label": LABELS[prediction]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)