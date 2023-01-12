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

class MenuOption:
    def __init__(
        self,
        label: str,
        value: str,
        description: Optional[str] = None,
        emoji: Optional[dict] = None,
        default: Optional[bool] = False
    ):
        self.type = type
        self.label = label
        self.value = value
        self.description = description
        self.emoji = emoji
        self.default = default

    def to_dict(self):
        dict_ = {
            "label": self.label,
            "value": self.value
        }

        if self.description:
            dict_["description"] = self.description

        if self.emoji:
            dict_["emoji"] = self.emoji

        if self.default:
            dict_["default"] = self.default

        return dict_