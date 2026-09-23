from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import joblib
import logging

app = FastAPI()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log",
    filemode="a"
)



logger = logging.getLogger(__name__)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "Something went wrong"
        }
    )

model = None


@app.on_event("startup")
def load_model():
    global model
    model = joblib.load("model.joblib")
    logger.info("Model loaded successfully.")
    
    
    

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


@app.get("/")
def home():
    return {"message": "Iris Prediction API is running!"}



@app.post("/predict")
def predict(data: IrisInput):

    logger.info("Prediction request received.")

    if model is None:
        raise HTTPException(
        status_code=500,
        detail={
           "success": False,
           "error_code": "MODEL_NOT_LOADED",
           "message": "The prediction model is unavailable"
    }
)

    try:
        prediction = model.predict([[
            data.sepal_length,
            data.sepal_width,
            data.petal_length,
            data.petal_width
        ]])
        logger.info(f"Prediction generated: {prediction[0]}")

    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")

        raise HTTPException(
           status_code=500,
           detail={
             "success": False,
              "error_code": "PREDICTION_FAILED",
              "message": "Unable to generate prediction"
    }
)

    flower_names = [
        "setosa",
        "versicolor",
        "virginica"
    ]

    predicted_flower = flower_names[prediction[0]]

    return {
        "prediction": predicted_flower
    }