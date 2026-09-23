import time
import pandas as pd

from fastapi import FastAPI, Depends

from app.database import Base, engine
from app.auth import router as auth_router

from app.schemas import CustomerData, BatchCustomerData

from app.predictor import (
    load_pipeline,
    predict,
    predict_probability,
    get_pipeline
)

from app.logger import log_prediction
from app.dependencies import get_current_user
from app.models import User


# =====================================================
# Database
# =====================================================

Base.metadata.create_all(bind=engine)


# =====================================================
# FastAPI App
# =====================================================

app = FastAPI(
    title="Secure Customer Churn Prediction API",
    version="1.0.0"
)


# =====================================================
# Authentication Routes
# =====================================================

app.include_router(auth_router)


# =====================================================
# Load ML Pipeline
# =====================================================

@app.on_event("startup")
def startup():
    load_pipeline()
    print("Pipeline Loaded Successfully")


# =====================================================
# Home
# =====================================================

@app.get("/")
def home():
    return {
        "message": "Secure Customer Churn Prediction API is running!"
    }


# =====================================================
# Health Check
# =====================================================

@app.get("/health")
def health():

    pipeline = get_pipeline()

    return {
        "status": "healthy" if pipeline else "unhealthy",
        "model_loaded": pipeline is not None,
        "model_version": "1.0.0"
    }


# =====================================================
# Prediction (Protected with JWT)
# =====================================================

@app.post("/predict")
def predict_customer(
    customer: CustomerData,
    current_user: User = Depends(get_current_user)
):

    start = time.perf_counter()

    data = pd.DataFrame([customer.model_dump()])

    prediction = predict(data)
    probability = predict_probability(data)

    latency = (time.perf_counter() - start) * 1000

    log_prediction(
        customer.model_dump(),
        int(prediction[0]),
        latency
    )

    return {
        "prediction": int(prediction[0]),
        "probability": float(probability[0][1])
    }


# =====================================================
# Batch Prediction (Protected with JWT)
# =====================================================

@app.post("/predict/batch")
def predict_batch(
    batch: BatchCustomerData,
    current_user: User = Depends(get_current_user)
):

    data = pd.DataFrame(
        [customer.model_dump() for customer in batch.customers]
    )

    predictions = predict(data)

    probabilities = predict_probability(data)

    results = []

    for pred, prob in zip(predictions, probabilities):
        results.append(
            {
                "prediction": int(pred),
                "probability": float(prob[1])
            }
        )

    return results