from typing import Dict
from fastapi import WebSocket

from src.messages.dtos.message_answer import MessageAnswerDTO


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(
        self, message: MessageAnswerDTO, websocket: WebSocket
    ):
        await websocket.send_json(message.model_dump())


manager = ConnectionManager()
