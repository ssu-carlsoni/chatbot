import json
import os

from dependency_injector.wiring import inject, Provide
from fastapi import Request, APIRouter, Depends
from fastapi.templating import Jinja2Templates
from langchain.chains import ConversationalRetrievalChain
from starlette.websockets import WebSocket

from chatbot.containers import Container
from chatbot.rag.chatbot import Chatbot


router = APIRouter()
templates = Jinja2Templates(directory="src/chatbot/web/templates")


@router.get("/")
async def get(request: Request):
    return templates.TemplateResponse(request, "index.html")


@router.websocket("/ws")
@inject
async def websocket_endpoint(
    websocket: WebSocket,
    chatbot: Chatbot = Depends(Provide[Container.chatbot]),
):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            response = await chatbot.get_response(message['text'])

            await websocket.send_json({
                "text": response,
                "sender": "bot"
            })
    except Exception as e:
        print(f"Error: {e}")
        await websocket.close()