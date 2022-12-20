from typing import List

class Interaction:
    def __init__(self, interaction_payload: dict):
        for key, value in interaction_payload.items():
            setattr(self, key, value)

    def respond(self, response: dict):
        return response

    async def reply(self, content: str, embeds: list = None, ephemeral: bool = False, flags: int = 0):
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
    def __init__(self, type: int, name: str, value: str = None, options: list = None):
        self.type = type
        self.name = name
        self.value = value
        self.options = options

    def __dict__(self):
        return {
            "name": self.name,
            "value": self.value
        }

class CommandInteraction:
    def __init__(self, name: str, description: str, options: List[Option] = None, default_permission: bool = True):
        self.name = name
        self.description = description
        self.options = options
        self.default_permission = default_permission

    def __dict__(self):
        return {
            "name": self.name,
            "description": self.description,
            "options": self.options,
            "default_permission": self.default_permission
        }