from gatepoint.interaction import CommandInteraction, ButtonInteraction

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from fastapi import FastAPI, Request

from typing import Union

class GatewayClient:
    def __init__(self, api_version: int, secret_key: str, public_key: str, token: str, port: int = 80):
        self.api_version = api_version
        self.secret_key = secret_key
        self.public_key = public_key
        self.token = token
        self.port = port

        self.autocomplete = {}
        self.commands = {}
        self.buttons = {}
        self.events = {}

    def register(self, interaction: Union[CommandInteraction, ButtonInteraction]):
        def decorator(func):
            if isinstance(interaction, CommandInteraction):
                self.commands[interaction.name] = func
            elif isinstance(interaction, ButtonInteraction):
                self.buttons[interaction.custom_id] = func
            return func
        return decorator

    def event(self, event: str):
        def decorator(func):
            self.events[event] = func
            return func
        return decorator

    def run(self):
        app = FastAPI()

        @app.get("/")
        async def index(request: Request):
            return "This is a Discord Interaction API.", 200

        @app.post("/interaction")
        async def interaction(request: Request):
            # Verify the request.
            verify_key = VerifyKey(bytes.fromhex(self.public_key))
            signature = request.headers.get("X-Signature-Ed25519")
            timestamp = request.headers.get("X-Signature-Timestamp")
            body = (await request.body()).decode("utf-8")

            try:
                verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
            except BadSignatureError:
                return 'invalid request signature', 401

            # Process the request.
            interaction_payload = await request.json()

            if interaction_payload["type"] == 1:
                return {
                    "type": 1
                }

            elif interaction_payload["type"] == 2:
                if interaction_payload["data"]["name"] in self.commands:
                    await self.events["interaction_receive"](interaction_payload)
                    return await self.commands[interaction_payload["data"]["name"]](interaction_payload)

                return {
                    "type": 4,
                    "data": {
                        "content": "This command is not registered with Interaction Gateway API.",
                        "flags": 64
                    }
                }

            elif interaction_payload["type"] == 3:
                if interaction_payload["data"]["custom_id"] in self.buttons:
                    await self.events["interaction_receive"](interaction_payload)
                    return await self.buttons[interaction_payload["data"]["custom_id"]](interaction_payload)

                return {
                    "type": 4,
                    "data": {
                        "content": "This button is not registered with Interaction Gateway API.",
                        "flags": 64
                    }
                }

            elif interaction_payload["type"] == 4:
                if interaction_payload["data"]["custom_id"] in self.buttons:
                    await self.events["interaction_receive"](interaction_payload)
                    return await self.buttons[interaction_payload["data"]["custom_id"]](interaction_payload)

                return {
                    "type": 4,
                    "data": {
                        "content": "This button is not registered with Interaction Gateway API.",
                        "flags": 64
                    }
                }

        app.run(
            host = "127.0.0.1",
            port = self.port
        )