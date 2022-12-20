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