from typing import Union, List

from .button import Button
from .menu import SelectMenu, UserSelect, RoleSelect, MentionableSelect, ChannelSelect

class ActionRow:
    def __init__(self, *components: Union[Button, SelectMenu, UserSelect, RoleSelect, MentionableSelect, ChannelSelect]):
        self.components = components
        if self.components > 5:
            raise ValueError("You can only have 5 components per row")

class Component(list):
    def __init__(self, components: Union[ActionRow, List[ActionRow]]):
        if isinstance(components, ActionRow):
            self.components = [components]
        else:
            self.components = components

    def __iter__(self):
        return iter(self.components)