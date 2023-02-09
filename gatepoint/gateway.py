import uvicorn
import aiohttp
import requests

from .interaction import (Interaction,
    CommandInteraction, ButtonInteraction, MenuInteraction,
    SubCommandInteraction, SubCommandGroupInteraction)
from .chunks.chunk import Chunk
from .objects import Snowflake, OptionType
from .option import CommandOption

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError 

from fastapi import FastAPI, Request, HTTPException 

from typing import Callable, Any, List, Union, Optional

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
        secret_key: str,
        public_key: str,
        token: str,
        api_version: Optional[int] = 10,
        port: Optional[int] = 80,
        verbose: Optional[bool] = False
    ):
        """## GatewayClient
        The main class for building your Interaction API for Discord.

        Args:
            `secret_key` (`str`): The Discord Application's Secret Key.
            `public_key` (`str`): The Discord Application's Public Key.
            `token` (`str`): Bot's token.
            `api_version` (`Optional[int]`): The API version your requests will go through. Defaults to `10`.
            `port` (`Optional[int]`): The port your API will be hosted in. Defaults to `80`.
            `verbose` (`Optional[bool]`): Enable to see errors or requests from discord. Defaults to `False`.

        Raises:
            ValueError: Invalid token provided.
        """
        self.discord_prefix = f"https://discord.com/api/v{api_version}"
        self.secret_key = secret_key
        self.public_key = public_key
        self.token = token
        self.port = port
        self.verbose: bool = verbose
        self.session: Any = None

        self.autocomplete: dict = {}
        self.buttons: dict = {}
        self.commands: dict = {}
        self.guild_commands: dict = {}
        self.events: dict = {}
        self.interactions: dict = {}
        self.loaded_chunks: List[Chunk] = []
        self.menus: dict = {}
        self.subcommands = {}

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

    async def request(self, method: str, endpoint: str, json: dict = None) -> dict:
        """## Discord API Request
        Sends a request to the Discord API.

        Args:
            method (str): HTTP methods such as `GET`, `POST`, `PUT`, `PATCH`, `DELETE`.
            endpoint (str): Discord API endpoint.
            json (dict, optional): The data you want in the request. Defaults to None.

        Returns:
            dict: Response JSON from Discord API.
        """
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

    def command(
        self,
        name: str,
        description: str = None,
        guild_ids: List[Snowflake] = None,
        options: List[dict] = None,
        dm_permission: bool = True,
        default_permission: bool = True
    ):
        """## Command Decorator
        Slash Command that can be used in a Discord Server.

        Args:
            `name` (`str`): Name of command.
            `description` (`str`): Description of command. 
            `guild_ids` (`Optional[List[Snowflake]]`): List of guild IDs to register command to. Defaults to `None`.
            `options` (`Optional[list]`): Other options within the command. Defaults to `[]`.
            `dm_permission` (`Optional[bool]`): Whether the command is enabled in DMs. Defaults to `True`.
            `default_permission` (`Optional[bool]`): Whether the command is enabled by default when the app is added to a guild. Defaults to `True`.
        """
        def decorator(func: Callable):
            interaction = CommandInteraction(
                name = name,
                description = description,
                guild_ids = guild_ids,
                options = options,
                dm_permission = dm_permission,
                default_permission = default_permission
            )
            self.commands[interaction.name] = func
            self.interactions[interaction.name] = interaction.register_json
            return func
        return decorator

    def add_option(
        self,
        type: Union[OptionType, str],
        name: str,
        description: str,
        options: Optional[list] = [],
        required: Optional[bool] = False
    ):
        """## Option Decorator
        Command Option that can be used in a Slash Command for parameter inputs.

        Args:
            `type` (`OptionType` or `str`): The type of option.
            `name` (`str`): Name of option parameter.
            `description` (`str`): Description of option parameter. 
            `options` (`Optional[list]`): Other options within the option. Defaults to `[]`.
            `required` (`Optional[bool]`): Is the option required to be filled in. Defaults to `False`.
        """
        def decorator(func: Callable):
            option = CommandOption(
                type = type,
                name = name,
                description = description,
                options = options,
                required = required
            )
            for command_name, command_func in self.commands.items():
                if command_func == func:
                    self.commands[command_name].options.append(option)
            return func
        return decorator

    def add_subcommand_group(
        self,
        name: str,
        description: str = None,
        options: List[dict] = None
    ) -> SubCommandGroupInteraction:
        """## Subcommand Group Decorator
        Subcommand Group to create other Subcommands.   

        Args:
            `name` (`str`): Name of subcommand group.
            `description` (`str`): Description of subcommand group. 
            `options` (`Optional[list]`): Other options within the subcommand group. Defaults to `[]`.
        """
        interaction = SubCommandGroupInteraction(
            name = name,
            description = description,
            options = options
        )
        self.commands[interaction.name] = interaction
        return interaction

    def basecommand(
        self,
        name: str,
        description: str = None,
        guild_ids: List[Snowflake] = None,
        options: List[dict] = None,
        dm_permission: bool = True,
        default_permission: bool = True
    ):
        """## Base Command Decorator
        Base Command for Slash Commands and Slash Command Groups.

        Args:
            `name` (`str`): Name of base command.
            `description` (`str`): Description of base command. 
            `guild_ids` (`Optional[List[Snowflake]]`): List of guild IDs to register command to. Defaults to `None`.
            `options` (`Optional[list]`): Other options within the command. Defaults to `[]`.
            `dm_permission` (`Optional[bool]`): Whether the command is enabled in DMs. Defaults to `True`.
            `default_permission` (`Optional[bool]`): Whether the command is enabled by default when the app is added to a guild. Defaults to `True`.
        """
        def decorator(func: Callable):
            if name not in self.subcommands:
                self.subcommands[name] = func
            return func
            if not description:
                decorator.parent = description

            else:
                decorator.name = name
                decorator.parent = name
                decorator.description = description
                decorator.guild_ids = guild_ids
                decorator.options = options
                decorator.dm_permission = dm_permission
                decorator.default_permission = default_permission
        return decorator

    def subcommand(
        self,
        name: str,
        description: str = None,
        options: List[dict] = None
    ):
        """## Subcommand Decorator
        Subcommand that can be used in a Slash Command.

        Args:       
            `name` (`str`): Name of subcommand.
            `description` (`str`): Description of subcommand.
            `options` (`Optional[list]`): Other options within the subcommand. Defaults to `[]`.
        """
        def decorator(func: Callable):
            if not getattr(func, "parent", None):
                raise Exception("Base Command not found.")

            interaction = SubCommandInteraction(
                parent = getattr(func, "parent", None),
                name = name,
                description = description,
                options = options
            )

            self.commands[interaction.name] = func
            return func
        return decorator

    def button(self, custom_id: str):
        """## Button Decorator
        Button that can be used in a Discord Bot.

        Args:
            `custom_id` (`str`): Custom ID of button.
        """
        def decorator(func: Callable):
            interaction = ButtonInteraction(custom_id = custom_id)
            self.buttons[interaction.custom_id] = func
            return func
        return decorator

    def menu(self, custom_id: str):
        """## Menu Decorator
        Menu UI Element to pick options on Discord.

        Args:
            `custom_id` (`str`): Custom ID of menu.
        """
        def decorator(func: Callable):
            interaction = MenuInteraction(custom_id = custom_id)
            self.menus[interaction.custom_id] = func
            return func
        return decorator

    def message_command(self, custom_id: str):
        """## Message Command Decorator
        Command that can be invoked in a Discord Message.

        Args:
            `name` (`str`): Name of message command.
        """
        def decorator(func: Callable):
            interaction = MessageCommandInteraction(custom_id = custom_id)
            self.message_commands[interaction.name] = func
            return func
        return decorator

    def on(self, event: str):
        """## Event Decorator
        Events that are fired on your Discord Bot.

        Args:
            `event` (`str`): Event name.
        """
        def decorator(func: Callable):
            event_list = self.events.get(event).append(func) if self.events.get(event) else [func]
            self.events[event] = event_list

            return func
        return decorator

    def import_chunk(self, chunk: Chunk) -> Chunk:
        """## Import Chunk
        Imports a chunk into the bot.

        Args:
            `chunk` (`Chunk`): Chunk to import.
        """
        for command in chunk.package["commands"]:
            self.commands[command.name] = command

        for button in chunk.package["buttons"]:
            self.buttons[button.custom_id] = button

        for menu in chunk.menus:
            self.menus[menu.custom_id] = menu

        return chunk

    def import_chunks(self, chunks: List[Chunk]) -> List[Chunk]:
        """## Import Chunks
        Imports chunks into the bot.

        Args:
            `chunks` (`List[Chunk]`): Chunks to import.
        """
        for chunk in chunks:
            self.import_chunk(chunk)
        return chunks

    def offload_chunk(self, chunk: Chunk) -> Chunk:
        """## Offload Chunk
        Offloads a chunk from the bot.

        Args:
            `chunk` (`Chunk`): Chunk to offload.
        """
        for command in chunk.commands:
            self.commands.pop(command.name)

        for button in chunk.buttons:
            self.buttons.pop(button.custom_id)

        for menu in chunk.menus:
            self.menus.pop(menu.custom_id)

        return chunk

    def offload_chunks(self, chunks: List[Chunk]) -> List[Chunk]:
        """## Offload Chunks
        Offloads chunks from the bot.

        Args:
            `chunks` (`List[Chunk]`): List of `Chunk`s to offload.
        """
        for chunk in chunks:
            self.offload_chunk(chunk)
        return chunks

    def sync_commands(self, guild: Optional[Snowflake] = None) -> None:
        if guild:
            # Fetch commands in guild.
            commands = self.request("GET", f"/applications/{self.client_id}/guilds/{guild}/commands")
            for command in self.guild_commands:
                if command not in commands:
                    self.request("POST", f"/applications/{self.client_id}/guilds/{guild}/commands", json = command)
                else:
                    self.request("PATCH", f"/applications/{self.client_id}/guilds/{guild}/commands/{command.id}", json = command)
            return None

        # Fetch commands in global.
        commands = self.request("GET", f"/applications/{self.client_id}/commands")
        for command in self.commands:
            if command not in commands:
                self.request("POST", f"/applications/{self.client_id}/commands", json = command)
            else:
                self.request("PATCH", f"/applications/{self.client_id}/commands/{command.id}", json = command)
        return None

    def run(self):
        """## Run
        Runs the Interaction API.

        ## Troubleshooting
        - If you require assistance/help, you may contact us at [Discord](https://discord.gg/5YY3W83YWg).
        - If your bot stops as soon as you run it, you can view by specifying `verbose = True` in GatewayClient.
        - If you are getting an error saying that the port is already in use, you fix it by mentioning a port in GatewayClient like `port = 8000` as an argument.
        - If your bot stops responding to interactions, you can fix it by restarting the bot.
        """
        app = FastAPI()

        @app.on_event("startup")
        async def startup_event():
            output("GatePoint API Dispatched, listening for interactions.")
            for event in self.events.get("startup") or []:
                event: Callable
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

                    if interaction_payload.get("data").get("options"):
                        input_tuple = ()
                        for option in interaction_payload["data"]["options"]:
                            input_tuple = input_tuple.__add__((option["value"]))

                        return await self.commands[interaction_payload["data"]["name"]](Interaction(interaction_payload), *input_tuple)

                    else:
                        return await self.commands[interaction_payload["data"]["name"]](Interaction(interaction_payload))

                return {
                    "type": 4,
                    "data": {
                        "content": "This command is not registered with Interaction Gateway API.",
                        "flags": 64
                    }
                }

            elif interaction_payload["type"] == 3:
                print(interaction_payload["data"])
                if interaction_payload["data"]["component_type"] in (3, 4, 5, 6, 7, 8):
                    value = interaction_payload["data"]["values"][0] if interaction_payload["data"]["values"] else None
                    if interaction_payload["data"]["custom_id"] in self.menus:
                        for event in self.events.get("interaction_receive") or []:
                            event: Callable
                            await event(Interaction(interaction_payload))

                        for event in self.events.get("menu_select") or []:
                            event: Callable
                            await event(Interaction(interaction_payload))

                        return await self.menus[interaction_payload["data"]["custom_id"]](Interaction(interaction_payload), interaction_payload["data"]["values"])

                    return {
                        "type": 4,
                        "data": {
                            "content": "This menu is not registered with Interaction Gateway API.",
                            "flags": 64
                        }
                    }

                elif interaction_payload["data"]["custom_id"] in self.buttons:
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

            elif interaction_payload["type"] >= 4 or interaction_payload["type"] < 12:
                return {
                    "type": 4,
                    "data": {
                        "content": "This interaction is not yet supported by Interaction Gateway API.",
                        "flags": 64
                    }
                }

            else:
                raise HTTPException(detail = "Interaction not recognised by Interaction Gateway API.", status_code = 400)

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