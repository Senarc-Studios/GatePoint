from typing import Optional, Union

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
        type: Union[OptionType, int],
        name: str,
        description: str,
        options: Optional[list] = [],
        required: Optional[bool] = False
    ):
        """## Command Option
        Command Option that can be used in a Slash Command for parameter inputs.

        Args:
            `type` (`OptionType` or `str`): The type of option.
            `name` (`str`): Name of option parameter.
            `description` (`str`): Description of option parameter. 
            `options` (`Optional[list]`): Other options within the option. Defaults to `[]`.
            `required` (`Optional[bool]`): Is the option required to be filled in. Defaults to `False`.
        """
        self.type = type
        self.name = name
        self.description = description
        self.options = options
        self.required = required

    def to_dict(self):
        return {
            "type": self.type,
            "name": self.name,
            "description": self.description,
            "options": self.options,
            "required": self.required
        }

class SubCommand:
    def __init__(
        self,
        name: str,
        description: str,
        options: Optional[list] = []
    ):
        self.type = OptionType.sub_command
        self.name = name
        self.description = description
        self.options = options

    def to_dict(self):
        return {
            "type": self.type,
            "name": self.name,
            "description": self.description,
            "options": self.options
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