import websockets
from typing import Literal
from dataclasses import dataclass
import asyncio
import json


class Network:
    def __init__(self, uri:str) -> None:
        self.uri = uri
        self.websocket:websockets.WebSocketClientProtocol = websockets.connect(self.uri)
    
    
    async def send(self, data):
        await self.websocket.send(data)
    
    async def recv(self):
        return await self.websocket.recv()







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




