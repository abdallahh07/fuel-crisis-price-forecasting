from fastapi import APIRouter
from schemas import PredictionInput, PredictionOutput
from predict import predict

router = APIRouter()

@router.post("/predict", response_model=PredictionOutput)
def make_prediction(input_data: PredictionInput):
    prediction = predict(input_data.dict())
    predicted_value = float(prediction[0])
    return PredictionOutput(wti_crude_close=predicted_value)