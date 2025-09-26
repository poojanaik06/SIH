import os
import requests
from fastapi import APIRouter, Depends, HTTPException
from .. import schemas
from .auth import get_current_user

router = APIRouter()

MODEL_API_URL = os.getenv("MODEL_API_URL")
MODEL_API_KEY = os.getenv("MODEL_API_KEY")

@router.post("/", response_model=schemas.PredictionOutput)
def create_prediction(
    payload: schemas.PredictionInput,
    current_user: schemas.User = Depends(get_current_user)
):
    if not MODEL_API_URL or not MODEL_API_KEY:
        raise HTTPException(status_code=500, detail="Model API not configured")

    headers = {"Authorization": f"Bearer {MODEL_API_KEY}", "Content-Type": "application/json"}

    try:
        response = requests.post(MODEL_API_URL, headers=headers, json=payload.dict())
        response.raise_for_status()
        prediction_data = response.json()
        
        # Adjust key based on what your friend's API returns
        predicted_yield = prediction_data.get("predicted_yield")
        
        if predicted_yield is None:
            raise HTTPException(status_code=500, detail="Invalid API response")
            
        return schemas.PredictionOutput(predicted_yield=predicted_yield)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Model API connection error: {e}")