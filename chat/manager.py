from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.admins = {}
        self.clients = {}
    async def connect(self, websocket: WebSocket, role: str,user_id:str):
        await websocket.accept()

        if role == "admin":
            self.admins[user_id]=websocket
        else:
            self.clients[user_id]=websocket
            
    def disconnect(self, websocket: WebSocket):
        if websocket in self.admins:
            self.admins.remove(websocket)
        if websocket in self.clients:
            self.clients.remove(websocket)
    '''
    async def send_to_admins(self, message: str):
        for admin in self.admins:
            await admin.send_text(message)

    async def send_to_clients(self, message: str):
        for client in self.clients:
            await client.send_text(message)

    async def broadcast(self, message: str):
        for ws in self.admins + self.clients:
            await ws.send_text(message)
    '''        
