from .interactions import (CommandInteraction, SubCommandInteraction,
    SubCommandGroupInteraction, MenuInteraction, ButtonInteraction)

class Chunk:
    def __init__(self):
        self.buttons = {}
        self.commands = {}
        self.menus = {}
        self.events = {}

    @classmethod
    def command(
        self,
        name: str,
        description: str = None,
        guild_ids: List[Snowflake] = None,
        options: List[dict] = None,
        dm_permission: bool = True,
        default_permission: bool = True
    ):
        """## Command Decorator
        Slash Command that can be used in a Discord Server.

        Args:
            `name` (`str`): Name of command.
            `description` (`str`): Description of command. 
            `guild_ids` (`Optional[List[Snowflake]]`): List of guild IDs to register command to. Defaults to `None`.
            `options` (`Optional[list]`): Other options within the command. Defaults to `[]`.
            `dm_permission` (`Optional[bool]`): Whether the command is enabled in DMs. Defaults to `True`.
            `default_permission` (`Optional[bool]`): Whether the command is enabled by default when the app is added to a guild. Defaults to `True`.
        """
        def decorator(func):
            self.commands.append(CommandInteraction(*args, **kwargs).to_dict())
            return func
        return decorator

    def add_option(
        self,
        type: Union[OptionType, str],
        name: str,
        description: str,
        options: Optional[list] = [],
        required: Optional[bool] = False
    ):
        """## Option Decorator
        Command Option that can be used in a Slash Command for parameter inputs.

        Args:
            `type` (`OptionType` or `str`): The type of option.
            `name` (`str`): Name of option parameter.
            `description` (`str`): Description of option parameter. 
            `options` (`Optional[list]`): Other options within the option. Defaults to `[]`.
            `required` (`Optional[bool]`): Is the option required to be filled in. Defaults to `False`.
        """
        def decorator(func: Callable):
            option = CommandOption(
                type = type,
                name = name,
                description = description,
                options = options,
                required = required
            )
            for command_name, command_func in self.commands.items():
                if command_func == func:
                    self.commands[command_name].options.append(option)
            return func
        return decorator

    def add_subcommand_group(
        self,
        name: str,
        description: str = None,
        options: List[dict] = None
    ):
        """## Subcommand Group Decorator
        Subcommand Group to create other Subcommands.   

        Args:
            `name` (`str`): Name of subcommand group.
            `description` (`str`): Description of subcommand group. 
            `options` (`Optional[list]`): Other options within the subcommand group. Defaults to `[]`.
        """
        interaction = SubCommandGroupInteraction(
            name = name,
            description = description,
            options = options
        )
        self.commands[interaction.name] = interaction

    def subcommand(
        self,
        name: str,
        description: str = None,
        options: List[dict] = None
    ):
        """## Subcommand Decorator
        Subcommand that can be used in a Slash Command.

        Args:       
            `name` (`str`): Name of subcommand.
            `description` (`str`): Description of subcommand.
            `options` (`Optional[list]`): Other options within the subcommand. Defaults to `[]`.
        """
        def decorator(func: Callable):
            interaction = SubCommandInteraction(
                name = name,
                description = description,
                options = options
            )
            self.commands[interaction.name] = func
            return func
        return decorator

    def button(self, custom_id: str):
        """## Button Decorator
        Button that can be used in a Discord Bot.

        Args:
            `custom_id` (`str`): Custom ID of button.
        """
        def decorator(func: Callable):
            interaction = ButtonInteraction(custom_id = custom_id)
            self.buttons[interaction.custom_id] = func
            return func
        return decorator

    def menu(self, custom_id: str):
        """## Menu Decorator
        Menu that can be used in a Discord Bot.

        Args:
            `custom_id` (`str`): Custom ID of menu.
        """
        def decorator(func: Callable):
            interaction = MenuInteraction(custom_id = custom_id)
            self.menus[interaction.custom_id] = func
            return func
        return decorator

    @classmethod
    def listen(self, event: str):
        """## Event Decorator
        Events that are fired on your Discord Bot.

        Args:
            `event` (`str`): Event name.
        """
        def decorator(func: Callable):
            event_list = self.events.get(event).append(func) if self.events.get(event) else [func]
            self.events[event] = event_list

            return func
        return decorator