from typing import Callable, Dict, List, Awaitable

Handler = Callable[[dict, str], Awaitable[None]]

class WsEventBus:
    def __init__(self):
        self.handlers: Dict[str, List[Handler]] = {}

    def on(self, event_type: str, handler: Handler):
        self.handlers.setdefault(event_type, []).append(handler)

    async def emit(self, event: dict, source: str):
        event_type = event.get("type")
        for handler in self.handlers.get(event_type, []):
            await handler(event, source)


# SINGLETON
ws_event_bus = WsEventBus()
