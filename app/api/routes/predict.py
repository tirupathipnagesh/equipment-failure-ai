from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.orchestrator import MaintenanceOrchestrator
from app.db.deps import get_db
from app.schemas.predict import FailurePredictionRequest, FailurePredictionResponse
from app.services.prediction_service import save_prediction

router = APIRouter()
orchestrator = MaintenanceOrchestrator()


@router.post("/predict/failure", response_model=FailurePredictionResponse, tags=["Prediction"])
def predict_failure(request: FailurePredictionRequest, db: Session = Depends(get_db)):
    input_data = request.model_dump()
    result = orchestrator.run(data=input_data)

    save_prediction(db, input_data, result)

    return FailurePredictionResponse(**result)