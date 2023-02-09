import json
from typing import List

from .components.action_row import ActionRow
from .objects import Snowflake

class DictObject:
    def __init__(self, json: dict):
        for key, value in json.items():
            if isinstance(value, dict):
                setattr(self, key, DictObject(value))
                continue
            setattr(self, key, value)

class Interaction:
    """## Interaction Object
    Represents the interaction sent from Discord.
    """
    def __init__(self, interaction_payload: dict):
        self.json_ = interaction_payload
        for key, value in interaction_payload.items():
            if isinstance(value, dict):
                setattr(self, key, DictObject(value))
                continue
            setattr(self, key, value)

    def to_dict(self) -> dict:
        return self.json_

    def respond(self, response: dict) -> dict:
        """## Interaction.respond
        Respond with a JSON to an Interaction from Discord. 
        This is used internally by the InteractionAPI.

        Args:
            `response` (`dict`): Payload to send to Discord.

        Returns:
            `dict`: Payload to send to Discord.
        """
        return response

    def reply(
        self,
        content: str = None,
        components: List[ActionRow] = None,
        embeds: list = None,
        ephemeral: bool = False,
        flags: int = 0
    ) -> dict:
        """## Interaction.reply
        Reply with a JSON to an Interaction from Discord.

        Args:
            `content` (`str`): Content of the message.
            `components` (`List[ActionRow]`): Components of the message.
            `embeds` (`list`): Embeds of the message.
            `ephemeral` (`bool`): Whether the message is ephemeral.
            `flags` (`int`): Message flags.

        Returns:
            `dict`: Payload to send to Discord.

        ## Example::

            @InteractionAPI.command("example")
            async def example(interaction):
                return interaction.reply(
                    content = "Thank you for using GatePoint Library API!",
                    ephemeral = True
                )
            # Test the command by typing `/example` in a Discord Server.
        """
        payload = {
            "type": 4,
            "data": {
                "flags": 64 if ephemeral and not flags else flags
            }
        }

        if not content and not embeds:
            raise ValueError("You must provide a content or embeds.")

        if content:
            payload["data"]["content"] = content

        if embeds:
            payload["data"]["embeds"] = embeds

        if components:
            payload["data"]["components"] = [
                component.to_dict()
                for component in components
            ]
        print(json.dumps(payload))

        return payload

class CommandInteraction:
    def __init__(
        self,
        name: str,
        description: str = None,
        guild_ids: List[Snowflake] = None,
        options: List[dict] = None,
        dm_permission: bool = True,
        default_permission: bool = True
    ):
        """## Command Interaction Object
        Slash Command that can be used in a Discord Server.

        Args:
            `name` (`str`): Name of command.
            `description` (`str`): Description of command. 
            `guild_ids` (`Optional[List[Snowflake]]`): List of guild IDs to register command to. Defaults to `None`.
            `options` (`Optional[list]`): Other options within the command. Defaults to `[]`.
            `dm_permission` (`Optional[bool]`): Whether the command is enabled in DMs. Defaults to `True`.
            `default_permission` (`Optional[bool]`): Whether the command is enabled by default when the app is added to a guild. Defaults to `True`.
        """
        self.name = name
        self.description = description or "No description."
        self.guild_ids = guild_ids
        self.guild_only = True if guild_ids else False
        self.options = options
        self.dm_permission = dm_permission
        self.default_permission = default_permission

        self.register_json = {
            "name": self.name,
            "description": self.description,
            "options": self.options,
            "default_permission": self.default_permission
        }

    def __dict__(self) -> dict:
        return self.register_json

class SubCommandInteraction:
    def __init__(
        self,
        name: str,
        description: str = None,
        options: List[dict] = None
    ):
        """## Sub Command Interaction Object
        Sub Command that can be used in a Discord Server.

        Args:
            `name` (`str`): Name of command.
            `description` (`str`): Description of command.
            `options` (`Optional[list]`): Other options within the command. Defaults to `[]`.
        """
        self.name = name
        self.description = description or "No description."
        self.options = options

        self.register_json = {
            "name": self.name,
            "description": self.description,
            "options": self.options,
            "type": 1
        }

    def __dict__(self) -> dict:
        return self.register_json

class SubCommandGroupInteraction:
    def __init__(
        self,
        name: str,
        description: str = None,
        options: List[dict] = None
    ):
        """## Sub Command Group Interaction Object
        Sub Command Group that can be used in a Discord Server.

        Args:
            `name` (`str`): Name of command.
            `description` (`str`): Description of command.
            `options` (`Optional[list]`): Other options within the command. Defaults to `[]`.
        """
        self.name = name
        self.description = description or "No description."
        self.options = options

        self.register_json = {
            "name": self.name,
            "description": self.description,
            "options": self.options,
            "type": 2
        }

    def __dict__(self) -> dict:
        return self.register_json

class ButtonInteraction:
    def __init__(
        self,
        custom_id: str
    ):
        """## Button Interaction Object
        Button that can be used in a Discord Server.

        Args:
            `custom_id` (`str`): Custom ID of button.
        """
        self.custom_id = custom_id

class MenuInteraction:
    def __init__(
        self,
        custom_id: str
    ):
        """## Menu Interaction Object
        Menu that can be used in a Discord Server.

        Args:
            `custom_id` (`str`): Custom ID of menu.
        """
        self.custom_id = custom_id