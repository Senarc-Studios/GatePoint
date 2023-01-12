from typing import List

from ..option import Choice

class SelectMenu:
    def __init__(
        self,
        custom_id: str,
        options: List[Choice],
        placeholder: str = None,
        min_values: int = None,
        max_values: int = None,
        disabled: bool = False
    ):
        self.custom_id = custom_id
        self.options = options
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values
        self.disabled = disabled

    def to_dict(self):
        dict_ = {
            "type": 3,
            "custom_id": self.custom_id,
            "options": [
                option.to_dict()
                for option in self.options
            ],
        }

        if self.placeholder:
            dict_["placeholder"] = self.placeholder

        if self.min_values:
            dict_["min_values"] = self.min_values

        if self.max_values:
            dict_["max_values"] = self.max_values

        if self.disabled:
            dict_["disabled"] = self.disabled

        return dict_

class UserSelect:
    def __init__(
        self,
        custom_id: str,
        placeholder: str = None,
        min_values: int = 1,
        max_values: int = 1,
        disabled: bool = False
    ):
        self.custom_id = custom_id
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values
        self.disabled = disabled

    def to_dict(self):
        dict_ = {
            "type": 5,
            "custom_id": self.custom_id,
        }

        if self.placeholder:
            dict_["placeholder"] = self.placeholder

        if self.min_values:
            dict_["min_values"] = self.min_values

        if self.max_values:
            dict_["max_values"] = self.max_values

        if self.disabled:
            dict_["disabled"] = self.disabled

        return dict_

class RoleSelect:
    def __init__(self, custom_id: str, placeholder: str = None, min_values: int = 1, max_values: int = 1, disabled: bool = False):
        self.custom_id = custom_id
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values
        self.disabled = disabled

    def to_dict(self):
        return {
            "type": 6,
            "custom_id": self.custom_id,
            "placeholder": self.placeholder,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "disabled": self.disabled
        }

class MentionableSelect:
    def __init__(self, custom_id: str, placeholder: str = None, min_values: int = 1, max_values: int = 1, disabled: bool = False):
        self.custom_id = custom_id
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values
        self.disabled = disabled

    def to_dict(self):
        return {
            "type": 7,
            "custom_id": self.custom_id,
            "placeholder": self.placeholder,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "disabled": self.disabled
        }

class ChannelSelect:
    def __init__(self, custom_id: str, placeholder: str = None, min_values: int = 1, max_values: int = 1, disabled: bool = False):
        self.custom_id = custom_id
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values
        self.disabled = disabled

    def to_dict(self):
        return {
            "type": 8,
            "custom_id": self.custom_id,
            "placeholder": self.placeholder,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "disabled": self.disabled
        }