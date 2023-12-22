import websockets
from typing import Literal, Callable, Optional
import asyncio
import json
from threading import Thread

class Network:
    def __init__(self, uri:str) -> None:
        self.uri = uri
        self.websocket:websockets.WebSocketClientProtocol|None = None
        self.connected = False
        self.on_connection_error = None
        self.on_error_do_default = True
        self.on_reconnect = None
        loop = asyncio.new_event_loop()
        self._loop = loop
        self._network_conn_thread = Thread(target=loop.run_forever).start()
    
    def start_connection(self):
        asyncio.run_coroutine_threadsafe(self.connect(), self._loop)

    def set_on_connection_error(self, func:Callable, do_default = True):
        self.on_connection_error = func
        self.on_error_do_default = do_default

    async def connect(self):
        while not self.connected:
            try:
                self.websocket = await websockets.connect(self.uri)
                self.connected = True
            except ConnectionRefusedError:
                self.connected = False
                continue
    
    def set_on_reconnect(self, func:Callable):
        self.on_reconnect = func

    def _on_connection_error(self):
        self.on_connection_error()
        if not self.on_error_do_default:
            return
        asyncio.run_coroutine_threadsafe(self.connect(), self._loop)
    
    async def send(self, data):
        try:
            await self.websocket.send(data)
        except websockets.ConnectionClosedError:
            self._on_connection_error()
    
    async def recv(self):
        try:
            return await self.websocket.recv()
        except websockets.ConnectionClosedError:
            self._on_connection_error()
        







async def main():
    async with websockets.connect("ws://localhost:8765") as websocket:
        mode = input("login/signup ")
        if mode == "reconnect":
            prev_id = input("prev_id: ")
            login_info = {"mode":mode, "prev_id":"48b68032-49b8-4ce3-83cd-a2663436f016"}
        else:
            username = input("username: ")
            password = input("password: ")
            login_info = {"mode":mode, "username":username, "password":password}

        await websocket.send(json.dumps(login_info))

        login_response = json.loads(await websocket.recv())
        if login_response["failed"]:
            print(f"{mode} failed: ", login_response["error_message"])
            return
        print(login_response["id"])

        
        







if __name__ == "__main__":
    asyncio.run(main())




