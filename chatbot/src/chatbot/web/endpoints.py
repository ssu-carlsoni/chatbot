import os
from contextlib import asynccontextmanager
import json

from dependency_injector.wiring import inject, Provide
from fastapi import Request, APIRouter, Depends
from fastapi.templating import Jinja2Templates
from langchain.chains import ConversationalRetrievalChain

from chatbot.containers import Container
from chatbot.rag.chatbot import Chatbot

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
@inject
async def get(
        request: Request,
        chatbot: Chatbot = Depends(Provide[Container.chatbot]),
):
    docs = chatbot.test()
    return docs
#     return templates.TemplateResponse(
#         "index.html",
#         {"request": request}
#     )
#
#
# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#
#     try:
#         while True:
#             data = await websocket.receive_text()
#             message = json.loads(data)
#
#             response = await app.container.chatbot().get_response(message[
#                                                                     'text'])
#
#             await websocket.send_json({
#                 "text": response,
#                 "sender": "bot"
#             })
#     except Exception as e:
#         print(f"Error: {e}")
#         await websocket.close()