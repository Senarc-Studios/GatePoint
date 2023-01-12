from typing import Optional

from .objects import OptionType

class Choice:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value
        }

class CommandOption:
    def __init__(
        self,
        type: OptionType,
        name: str,
        description: str,
        options: Optional[list] = [],
        required: Optional[bool] = False
    ):
        self.type = type
        self.name = name
        self.description = description
        self.options = options
        self.required = required

    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value
        }