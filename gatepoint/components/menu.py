from typing import List

from ..option import Option

class SelectMenu:
    def __init__(self, custom_id: str, options: List[Option], placeholder: str = None, min_values: int = 1, max_values: int = 1, disabled: bool = False):
        self.custom_id = custom_id
        self.options = options
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values
        self.disabled = disabled

    def to_dict(self):
        return {
            "type": 3,
            "custom_id": self.custom_id,
            "options": [option.to_dict() for option in self.options],
            "placeholder": self.placeholder,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "disabled": self.disabled
        }

class UserSelect(SelectMenu):
    def __init__(self, custom_id: str, placeholder: str = None, min_values: int = 1, max_values: int = 1, disabled: bool = False):
        super().__init__(custom_id, [], placeholder, min_values, max_values, disabled)

    def to_dict(self):
        return {
            "type": 3,
            "custom_id": self.custom_id,
            "placeholder": self.placeholder,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "disabled": self.disabled
        }

class RoleSelect(SelectMenu):
    def __init__(self, custom_id: str, placeholder: str = None, min_values: int = 1, max_values: int = 1, disabled: bool = False):
        super().__init__(custom_id, [], placeholder, min_values, max_values, disabled)

    def to_dict(self):
        return {
            "type": 3,
            "custom_id": self.custom_id,
            "placeholder": self.placeholder,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "disabled": self.disabled
        }

class MentionableSelect(SelectMenu):
    def __init__(self, custom_id: str, placeholder: str = None, min_values: int = 1, max_values: int = 1, disabled: bool = False):
        super().__init__(custom_id, [], placeholder, min_values, max_values, disabled)

    def to_dict(self):
        return {
            "type": 3,
            "custom_id": self.custom_id,
            "placeholder": self.placeholder,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "disabled": self.disabled
        }

class ChannelSelect(SelectMenu):
    def __init__(self, custom_id: str, placeholder: str = None, min_values: int = 1, max_values: int = 1, disabled: bool = False):
        super().__init__(custom_id, [], placeholder, min_values, max_values, disabled)

    def to_dict(self):
        return {
            "type": 3,
            "custom_id": self.custom_id,
            "placeholder": self.placeholder,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "disabled": self.disabled
        }

class StringSelect(SelectMenu):
    def __init__(self, custom_id: str, options: List[SelectOption], placeholder: str = None, min_values: int = 1, max_values: int = 1, disabled: bool = False):
        super().__init__(custom_id, options, placeholder, min_values, max_values, disabled)

    def to_dict(self):
        return {
            "type": 3,
            "custom_id": self.custom_id,
            "options": [option.to_dict() for option in self.options],
            "placeholder": self.placeholder,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "disabled": self.disabled
        }