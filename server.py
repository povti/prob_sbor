import asyncio
import websockets
from dotenv import load_dotenv
import os
import json
from model import add_problem, update_problem, delete_problem, search

load_dotenv()


class MyWebSocketHandler:
    SECRET = os.getenv("SECRET")
    authenticated = False

    async def handle(self, websocket, path):
        # Message Handling
        async for data in websocket:
            message_type, message_data = await self.parse_message(data)

            if message_type == 'undefined':
                await websocket.send(json.dumps({
                    "status": "error",
                    "message": "undefined type or data"
                }))
                await websocket.close()
                return

            if message_type == 'auth':
                self.authenticated = await self.authenticate(message_data)
                if self.authenticated:
                    await websocket.send(json.dumps({
                        "status": "success",
                        "message": "successfully authorized"
                    }))
                    continue

            if not self.authenticated:
                await websocket.send(json.dumps({
                    "status": "error",
                    "message": "unauthorized"
                }))
                await websocket.close()
                return

            if message_type == 'create':
                res = await self.create(message_data)
                if res:
                    await websocket.send(json.dumps({
                        "status": "success",
                        "message": "task successfully added"
                    }))
                else:
                    await websocket.send(json.dumps({
                        "status": "error",
                        "message": "wrong format"
                    }))
                continue

            if message_type == 'update':
                res = await self.update(message_data)
                if res:
                    await websocket.send(json.dumps({
                        "status": "success",
                        "message": "task successfully updated"
                    }))
                else:
                    await websocket.send(json.dumps({
                        "status": "error",
                        "message": "wrong format"
                    }))
                continue

            if message_type == 'delete':
                res = await self.delete(message_data)
                if res:
                    await websocket.send(json.dumps({
                        "status": "success",
                        "message": "task successfully deleted"
                    }))
                else:
                    await websocket.send(json.dumps({
                        "status": "error",
                        "message": "wrong format"
                    }))
                continue

            if message_type == 'search':
                flag, res = await self.search(message_data)
                if flag:
                    await websocket.send(json.dumps({
                        "status": "success",
                        "message": res
                    }))
                else:
                    await websocket.send(json.dumps({
                        "status": "error",
                        "message": []
                    }))
                continue

            await websocket.send(json.dumps({
                "status": "error",
                "message": "unknown type"
            }))
            # Handle client requests here
            await websocket.send(data)

    async def parse_message(self, data):
        try:
            received_message = json.loads(data)
            message_type = str(received_message['type'])
            message_data = received_message['data']
            return message_type, message_data
        except (json.JSONDecodeError, KeyError):
            return 'undefined', {}

    async def authenticate(self, data):
        try:
            received_secret = str(data['secret'])
            return received_secret == self.SECRET
        except (json.JSONDecodeError, KeyError, ValueError):
            return False

    async def create(self, data):
        try:
            id = int(data['id'])
            title = str(data['title'])
            statement = str(data['statement'])
            add_problem(title, statement, id)
            return True
        except (json.JSONDecodeError, KeyError, ValueError):
            return False

    async def update(self, data):
        try:
            id = int(data['id'])
            title = str(data['title'])
            statement = str(data['statement'])
            update_problem(id, title, statement)
            return True
        except (json.JSONDecodeError, KeyError, ValueError):
            return False

    async def delete(self, data):
        try:
            id = int(data['id'])
            delete_problem(id)
            return True
        except (json.JSONDecodeError, KeyError, ValueError):
            return False

    async def search(self, data):
        # print(data)
        try:
            ids = list([int(id_) for id_ in data['ids']])
            title = str(data['title'])
            statement = str(data['statement'])
            # print(ids, title, statement)
            result = search(title, statement, ids)
            # print(result)
            return True, result
        except (json.JSONDecodeError, KeyError, ValueError):
            return False, []

    async def start_server(self):
        HOST, PORT = "localhost", 9999

        # Create the server, binding to localhost on port 9999
        async with websockets.serve(self.handle, HOST, PORT):
            # Activate the server
            await asyncio.Future()  # Keep the server running indefinitely
