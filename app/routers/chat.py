from fastapi import APIRouter, Depends
from app.dependencies import get_jwt_payload
from ..infrastructure.data_schemas import JWTPayload, SendMessageForm, ReceiptLogin

router = APIRouter()

CHAT_TAG = "chat"


@router.post("/chat/sendMessage", tags=[CHAT_TAG])
async def send_message(data: SendMessageForm, causer: JWTPayload = Depends(get_jwt_payload)):
    # TODO IT
    return {"response": "success"}


@router.post("/chat/history", tags=[CHAT_TAG])
async def retieve_message_history(data: ReceiptLogin, causer: JWTPayload = Depends(get_jwt_payload)):
    # TODO IT
    return {"response": "success"}
