from fastapi import WebSocket
from typing import Dict, Set
from collections import defaultdict
import json

class ConnectionManager:
    def __init__(self):
        self.clients: Dict[str, WebSocket] = {}
        self.groups: Dict[str, Set[str]] = defaultdict(set)

    async def connect(self, client_id: str, ws: WebSocket):
        await ws.accept()
        self.clients[client_id] = ws

    def disconnect(self, client_id: str):
        self.clients.pop(client_id, None)
        for members in self.groups.values():
            members.discard(client_id)

    def join_group(self, client_id: str, group: str):
        self.groups[group].add(client_id)

    def leave_group(self, client_id: str, group: str):
        self.groups[group].discard(client_id)

    async def send_to_client(self, client_id: str, message: dict):
        ws = self.clients.get(client_id)
        if ws:
            await ws.send_text(json.dumps(message))

    async def send_to_group(self, group: str, message: dict):
        for client_id in self.groups.get(group, []):
            await self.send_to_client(client_id, message)

    async def broadcast(self, message: dict):
        for ws in self.clients.values():
            await ws.send_text(json.dumps(message))


# SINGLETON
ws_manager = ConnectionManager()
