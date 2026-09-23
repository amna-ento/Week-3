import time
import pandas as pd

from fastapi import FastAPI, HTTPException

from app.schemas import CustomerData, BatchCustomerData

from app.predictor import (
    load_pipeline,
    predict,
    predict_probability,
    get_pipeline
)

from app.logger import log_prediction

app = FastAPI(
    title="Customer Churn Prediction API",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    load_pipeline()
    print("Pipeline Loaded Successfully")


@app.get("/")
def home():
    return {
        "message": "Customer Churn Prediction API is running!"
    }
    
    
@app.get("/health")
def health():
    pipeline = get_pipeline()

    return {
        "status": "healthy" if pipeline else "unhealthy",
        "model_loaded": pipeline is not None,
        "model_version": "1.0.0"
    }   
    
@app.post("/predict")
def predict_customer(customer: CustomerData):

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
    
    
@app.post("/predict/batch")
def predict_batch(batch: BatchCustomerData):

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