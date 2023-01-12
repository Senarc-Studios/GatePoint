from typing import Union, List

from .button import Button
from .menu import SelectMenu, UserSelect, RoleSelect, MentionableSelect, ChannelSelect

class ActionRow:
    def __init__(self, *components: Union[Button, SelectMenu, UserSelect, RoleSelect, MentionableSelect, ChannelSelect]):
        self.components = components
        if len(self.components) > 5:
            raise ValueError("You can only have 5 components per row")

