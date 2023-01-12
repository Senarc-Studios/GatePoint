import json
from typing import List

from .components.component import ActionRow

class DictObject:
    def __init__(self, json: dict):
        for key, value in json.items():
            if isinstance(value, dict):
                setattr(self, key, DictObject(value))
                continue
            setattr(self, key, value)

class Interaction:
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
        return response

    def reply(
        self,
        content: str = None,
        components: List[ActionRow] = None,
        embeds: list = None,
        ephemeral: bool = False,
        flags: int = 0
    ) -> dict:
        payload = {
            "type": 4,
            "data": {
                "content": content,
                "embeds": embeds,
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

class Snowflake(int):
    def __init__(self, snowflake: int):
        if not len(str(snowflake)) in (17, 18, 19):
            raise ValueError("Invalid snowflake.")

        self.snowflake = snowflake

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

class ButtonInteraction:
    def __init__(
        self,
        custom_id: str
    ):
        self.custom_id = custom_id

class MenuInteraction:
    def __init__(
        self,
        custom_id: str
    ):
        self.custom_id = custom_id