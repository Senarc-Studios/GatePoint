from gatepoint.object_types import OptionType

from typing import List, Optional

class Interaction:
    def __init__(self, interaction_payload: dict):
        for key, value in interaction_payload.items():
            setattr(self, key, value)

    def respond(self, response: dict):
        return response

    def reply(self, content: str, embeds: list = None, ephemeral: bool = False, flags: int = 0):
        return {
            "type": 4,
            "data": {
                "content": content,
                "embeds": embeds,
                "flags": 64 if ephemeral and not flags else flags
            }
        }

class Choice:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def __dict__(self):
        return {
            "name": self.name,
            "value": self.value
        }

class Option:
    def __init__(
        self,
        type: OptionType,
        name: str,
        description: str,
        options: Optional[list] = [],
        nsfw: Optional[bool] = False,
        required: Optional[bool] = False
    ):
        self.type = type
        self.name = name
        self.description = description
        self.options = options
        self.nsfw = nsfw
        self.required = required

    def __dict__(self):
        return {
            "name": self.name,
            "value": self.value
        }

class CommandInteraction:
    def __init__(
        self,
        name: str,
        description: str,
        guild_ids: List[id] = None,
        options: List[dict] = None,
        dm_permission: bool = True,
        default_permission: bool = True
    ):
        self.name = name
        self.description = description
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

    def __dict__(self):
        return self.register_json