from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.orchestrator import MaintenanceOrchestrator
from app.db.deps import get_db
from app.schemas.chat import ChatQueryRequest, ChatQueryResponse
from app.services.chat_service import save_chat_log, format_chat_context

router = APIRouter()
orchestrator = MaintenanceOrchestrator()


@router.post("/chat/query", response_model=ChatQueryResponse, tags=["Chat"])
def chat_query(request: ChatQueryRequest, db: Session = Depends(get_db)):
    request_data = request.model_dump()
    question = request_data.pop("question")

    result = orchestrator.run(data=request_data, question=question)

    save_chat_log(
        db=db,
        question=question,
        input_data=request_data,
        response=result["chatbot_response"],
    )

    formatted = format_chat_context(result)

    return ChatQueryResponse(**formatted)