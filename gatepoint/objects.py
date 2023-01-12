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

class User(dict):
    def __init__(
        self,
        username: str,
        discriminator: str,
        id: int,
        avatar: str = None,
        bot: bool = False,
        system: bool = False,
        mfa_enabled: bool = False,
        locale: str = None,
        verified: bool = False,
        email: str = None,
        flags: int = None,
        premium_type: int = None,
        public_flags: int = None
    ):
        self.username = username
        self.discriminator = discriminator
        self.id = id
        self.avatar = avatar
        self.bot = bot
        self.system = system
        self.mfa_enabled = mfa_enabled
        self.locale = locale
        self.verified = verified
        self.email = email
        self.flags = flags
        self.premium_type = premium_type
        self.public_flags = public_flags

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "discriminator": self.discriminator,
            "id": self.id,
            "avatar": self.avatar,
            "bot": self.bot,
            "system": self.system,
            "mfa_enabled": self.mfa_enabled,
            "locale": self.locale,
            "verified": self.verified,
            "email": self.email,
            "flags": self.flags,
            "premium_type": self.premium_type,
            "public_flags": self.public_flags
        }

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