import websockets
from typing import Literal, Callable, Optional
import asyncio
import json
from threading import Thread

class Network:
    def __init__(self, uri:str) -> None:
        self.uri = uri
        self.websocket:websockets.WebSocketClientProtocol|None = None
        self.prev_id = None
        self.connected = False
        self.on_connect = None
        self.on_connection_error = None
        self.on_error_do_default = True
        self.on_reconnect = None
    
    def start_connection(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.connect())


    def set_on_connection_error(self, func:Callable, do_default = True):
        self.on_connection_error = func
        self.on_error_do_default = do_default

    async def connect(self):
        print("run")
        while not self.connected:
            try:
                self.websocket = await websockets.connect(self.uri)
            except ConnectionRefusedError:
                self.connected = False
                continue
            
            self.connected = True
            if self.on_connect:
                self.on_connect()
        print("done")
    
    def set_on_connect(self, func:Callable):
        self.on_connect = func
    
    def set_on_reconnect(self, func:Callable):
        self.on_reconnect = func

    def _on_connection_error(self):
        self.connected = False
        self.prev_id = self.websocket.id
        if self.on_connection_error:
            self.on_connection_error()
        if not self.on_error_do_default:
            return
        asyncio.run_coroutine_threadsafe(self.connect(), self._loop)
    
    async def send(self, data):
        if not self.websocket:
            return False
        try:
            await self.websocket.send(data)
            return True
        except websockets.ConnectionClosedError as e:
            self._on_connection_error()
            raise e
    
    async def recv(self):
        if not self.websocket:
            return False
        try:
            return await asyncio.wait_for(self.websocket.recv(), 5)
        except websockets.ConnectionClosedError:
            self._on_connection_error()
            return False

        







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




