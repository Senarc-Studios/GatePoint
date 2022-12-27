import uvicorn
import aiohttp
import asyncio
import requests

from gatepoint.interaction import Interaction, CommandInteraction, ButtonInteraction

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from fastapi import FastAPI, Request, HTTPException

from typing import Union

def output(content, type_ = None):
    if type_ == "ERROR":
        return print(f"ERR: {content}")

    elif type_ == "WARNING":
        return print(f"WARN: {content}")

    return print(f"INFO: {content}")

class Bot:
    def __init__(self, json: dict):
        setattr(self, "id", json["id"])
        setattr(self, "avatar", json["avatar"])
        setattr(self, "username", json["username"])
        setattr(self, "discriminator", json["discriminator"])

class GatewayClient:

    def __init__(
        self,
        api_version: int,
        secret_key: str,
        public_key: str,
        token: str,
        port: int = 80,
        verbose: bool = False
    ):
        self.discord_prefix = f"https://discord.com/api/v{api_version}"
        self.secret_key = secret_key
        self.public_key = public_key
        self.token = token
        self.port = port
        self.verbose = verbose
        self.session = None

        self.autocomplete = {}
        self.commands = {}
        self.buttons = {}
        self.events = {}

        response = requests.get(
            f"{self.discord_prefix}/users/@me",
            headers = {
                "Authorization": f"Bot {self.token}",
                "Content-Type": "application/json",
                "User-Agent": "GatePoint API Gateway"
            }
        )
        if response.status_code == 200:
            self.bot = Bot(response.json())

        else:
            raise ValueError("Invalid token provided.")

    async def request(self, method: str, endpoint: str, json: dict = None):
        async with aiohttp.ClientSession(
            headers = {
                "Authorization": f"Bot {self.token}",
                "Content-Type": "application/json",
                "User-Agent": "GatePoint API Gateway"
            }
        ) as session:
            async with session.request(
                method,
                f"{self.discord_prefix}{endpoint}",
                json = json
            ) as response:
                return await response.json()

        def decorator(func):
    def command(self, *args, **kwargs):
            interaction = CommandInteraction(*args, **kwargs)
            self.commands[interaction.name] = func
            if interaction.guild_only:
                for id_ in interaction.guild_ids:
                    asyncio.run(
                        self.request(
                            "POST",
                            f"/applications/{self.bot.id}/guilds/{id_}/commands",
                            json = interaction.register_json
                        )
                    )

            else:
                asyncio.run(
                    self.request(
                        "POST",
                        f"/applications/{self.bot.id}/commands",
                        json = interaction.register_json
                    )
                )
            return func
        return decorator

    def button(self, *args, **kwargs):
            interaction = ButtonInteraction(*args, **kwargs)
            self.buttons[interaction.custom_id] = func
            return func
        return decorator

    def on(self, event: str):
            event_list = self.events.get(event).append(func) if self.events.get(event) else [func]
            self.events[event] = event_list

            return func
        return decorator

    def run(self):
        app = FastAPI()

        @app.on_event("startup")
        async def startup_event():
            output("GatePoint API Dispatched, listening for interactions.")
            for event in self.events.get("startup") or []:
                await event()

        @app.get("/")
        async def index():
            return "This is a Discord Interaction API."

        @app.post("/interaction")
        async def interaction(request: Request):
            # Verify the request.
            verify_key = VerifyKey(bytes.fromhex(self.public_key))
            signature = request.headers.get("X-Signature-Ed25519")
            timestamp = request.headers.get("X-Signature-Timestamp")

            if not signature or not timestamp:
                raise HTTPException(
                    detail = 'missing request signature',
                    status_code = 401
                )

            body = (await request.body()).decode("utf-8")

            try:
                verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
            except BadSignatureError:
                return HTTPException(
                    detail = 'invalid request signature',
                    status_code = 401
                )

            # Process the request.
            interaction_payload = await request.json()

            if interaction_payload["type"] == 1:
                return {
                    "type": 1
                }

            elif interaction_payload["type"] == 2:
                if interaction_payload["data"]["name"] in self.commands:
                    print(self.events)
                    for event in self.events.get("interaction_receive") or []:
                        event: Callable
                        await event(Interaction(interaction_payload))

                    for event in self.events.get("command_receive") or []:
                        event: Callable
                        await event(Interaction(interaction_payload))

                    return await self.commands[interaction_payload["data"]["name"]](Interaction(interaction_payload))

                return {
                    "type": 4,
                    "data": {
                        "content": "This command is not registered with Interaction Gateway API.",
                        "flags": 64
                    }
                }

            elif interaction_payload["type"] == 3:
                if interaction_payload["data"]["custom_id"] in self.buttons:
                    for event in self.events.get("interaction_receive") or []:
                        event: Callable
                        await event(Interaction(interaction_payload))

                    for event in self.events.get("button_click") or []:
                        event: Callable
                        await event(Interaction(interaction_payload))

                    return await self.buttons[interaction_payload["data"]["custom_id"]](Interaction(interaction_payload))

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
                    return await self.buttons[interaction_payload["data"]["custom_id"]](Interaction(interaction_payload))

                return {
                    "type": 4,
                    "data": {
                        "content": "This button is not registered with Interaction Gateway API.",
                        "flags": 64
                    }
                }

        uvicorn.run(
            app,
            host = "127.0.0.1",
            port = self.port
        ) if self.verbose else uvicorn.run(
            app,
            log_level = "critical",
            host = "127.0.0.1",
            port = self.port
        )