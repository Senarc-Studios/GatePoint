class Emoji(dict):
    def __init__(self, name: str, id: int = None, animated: bool = False):
        self.name = name
        self.id = id
        self.animated = animated
        self._dict = {
            "name": self.name,
            "id": self.id,
            "animated": self.animated
        } if not animated else {
            "name": self.name,
            "id": self.id
        }

    def to_dict(self) -> dict:
        return self._dict

class OptionType:
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8

class InteractionType:
    SLASH_COMMAND = 1
    USER_COMMAND = 2
    MESSAGE_COMMAND = 3

class ButtonStyle:
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5