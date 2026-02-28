from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

# ── app ────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Tunisia Real Estate Price Predictor",
    description="Predict apartment / house prices in Tunisia using ML",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── model ──────────────────────────────────────────────────────────────────────
MODEL_PATH = Path(__file__).parent.parent / "models" / "model.pkl"
pipeline = None


def load_model():
    global pipeline
    if MODEL_PATH.exists():
        pipeline = joblib.load(MODEL_PATH)
    else:
        raise FileNotFoundError(
            "model.pkl not found. Run the modeling notebook first."
        )


@app.on_event("startup")
def startup_event():
    load_model()


# ── schema ─────────────────────────────────────────────────────────────────────
LOCATIONS = [
    "Ariana", "Autre", "Ben Arous", "Bizerte", "Bizerte Nord",
    "Boumhel Bassatine", "Carthage", "Cité El Khadra", "El Menzah",
    "Hammam El Ghezaz", "Hammamet", "Kairouan Ville", "Kélibia",
    "La Goulette", "La Manouba", "La Marsa", "La Soukra", "Le Kram",
    "Mahdia", "Monastir Ville", "Méégrine", "Nabeul", "Rades", "Raoued",
    "Sfax Ville", "Sousse", "Sousse Riadh", "Tantana", "Tunis",
]


class PredictRequest(BaseModel):
    superficie: float = Field(..., gt=0, le=5000, example=120.0)
    chambres: int = Field(..., ge=0, le=20, example=2)
    salles_de_bains: int = Field(..., ge=0, le=20, example=1)
    location: str = Field(..., example="Tunis")
    source: str = Field(default="tayara", example="tayara")


class PredictResponse(BaseModel):
    predicted_price: float
    price_low: float
    price_high: float
    price_per_sqm: float
    location: str
    source: str


# ── endpoints ──────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": pipeline is not None}


@app.get("/locations")
def get_locations():
    return {"locations": LOCATIONS}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model not loaded.")

    sample = pd.DataFrame([{
        "superficie": req.superficie,
        "chambres": req.chambres,
        "salles_de_bains": req.salles_de_bains,
        "location": req.location,
        "source": req.source,
    }])

    log_pred = pipeline.predict(sample)[0]
    price = float(np.expm1(log_pred))

    # conservative 25 % confidence band around the point estimate
    band = 0.25
    return PredictResponse(
        predicted_price=round(price),
        price_low=round(price * (1 - band)),
        price_high=round(price * (1 + band)),
        price_per_sqm=round(price / req.superficie),
        location=req.location,
        source=req.source,
    )
