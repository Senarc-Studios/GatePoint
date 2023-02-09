class Snowflake(int):
    def __init__(self, snowflake: int):
        """## Snowflake Object
        Snowflake ID found in any Discord ID.

        Args:
            `snowflake` (`int`): Snowflake ID.

        Raises: 
            `ValueError`: Invalid snowflake.
        """
        if not len(str(snowflake)) in (17, 18, 19):
            raise ValueError("Invalid snowflake.")

        self.snowflake = snowflake

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

class Member(dict):
    def __init__(
        self,
        user: User,
        nick: str = None,
        roles: list = None,
        joined_at: str = None,
        premium_since: str = None,
        deaf: bool = False,
        mute: bool = False,
        pending: bool = False
    ):
        self.user = user
        self.nick = nick
        self.roles = roles
        self.joined_at = joined_at
        self.premium_since = premium_since
        self.deaf = deaf
        self.mute = mute
        self.pending = pending

    def to_dict(self) -> dict:
        return {
            "user": self.user.to_dict(),
            "nick": self.nick,
            "roles": self.roles,
            "joined_at": self.joined_at,
            "premium_since": self.premium_since,
            "deaf": self.deaf,
            "mute": self.mute,
            "pending": self.pending
        }

class Role(dict):
    def __init__(
        self,
        id: int,
        name: str,
        color: int,
        hoist: bool = False,
        position: int = 0,
        permissions: str = "0",
        managed: bool = False,
        mentionable: bool = False
    ):
        self.id = id
        self.name = name
        self.color = color
        self.hoist = hoist
        self.position = position
        self.permissions = permissions
        self.managed = managed
        self.mentionable = mentionable

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "hoist": self.hoist,
            "position": self.position,
            "permissions": self.permissions,
            "managed": self.managed,
            "mentionable": self.mentionable
        }

class Channel(dict):
    def __init__(
        self,
        id: int,
        type: int,
        guild_id: int = None,
        position: int = None,
        permission_overwrites: list = None,
        name: str = None,
        topic: str = None,
        nsfw: bool = False,
        last_message_id: int = None,
        bitrate: int = None,
        user_limit: int = None,
        rate_limit_per_user: int = None,
        recipients: list = None,
        icon: str = None,
        owner_id: int = None,
        application_id: int = None,
        parent_id: int = None,
        last_pin_timestamp: str = None
    ):
        self.id = id
        self.type = type
        self.guild_id = guild_id
        self.position = position
        self.permission_overwrites = permission_overwrites
        self.name = name
        self.topic = topic
        self.nsfw = nsfw
        self.last_message_id = last_message_id
        self.bitrate = bitrate
        self.user_limit = user_limit
        self.rate_limit_per_user = rate_limit_per_user
        self.recipients = recipients
        self.icon = icon
        self.owner_id = owner_id
        self.application_id = application_id
        self.parent_id = parent_id
        self.last_pin_timestamp = last_pin_timestamp

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "guild_id": self.guild_id,
            "position": self.position,
            "permission_overwrites": self.permission_overwrites,
            "name": self.name,
            "topic": self.topic,
            "nsfw": self.nsfw,
            "last_message_id": self.last_message_id,
            "bitrate": self.bitrate,
            "user_limit": self.user_limit,
            "rate_limit_per_user": self.rate_limit_per_user,
            "recipients": self.recipients,
            "icon": self.icon,
            "owner_id": self.owner_id,
            "application_id": self.application_id,
            "parent_id": self.parent_id,
            "last_pin_timestamp": self.last_pin_timestamp
        }

class Attachment(dict):
    def __init__(self, id: int, filename: str, size: int, url: str, proxy_url: str, height: int = None, width: int = None):
        self.id = id
        self.filename = filename
        self.size = size
        self.url = url
        self.proxy_url = proxy_url
        self.height = height
        self.width = width

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "filename": self.filename,
            "size": self.size,
            "url": self.url,
            "proxy_url": self.proxy_url,
            "height": self.height,
            "width": self.width
        }

class Embed(dict):
    def __init__(
        self,
        title: str = None,
        type: str = None,
        description: str = None,
        url: str = None,
        timestamp: str = None,
        color: int = None,
        colour: int = None,
        footer: dict = None,
        image: dict = None,
        thumbnail: dict = None,
        video: dict = None,
        provider: dict = None,
        author: dict = None,
        fields: list = None
    ):
        self.title = title
        self.type = type
        self.description = description
        self.url = url
        self.timestamp = timestamp
        self.color = color or colour
        self.footer = footer
        self.image = image
        self.thumbnail = thumbnail
        self.video = video
        self.provider = provider
        self.author = author
        self.fields = fields

    def set_author(
        self,
        name: str,
        url: str = None,
        icon_url: str = None,
        proxy_icon_url: str = None
    ):
        self.author = {
            "name": name,
            "url": url,
            "icon_url": icon_url,
            "proxy_icon_url": proxy_icon_url
        }

    def set_footer(
        self,
        text: str,
        icon_url: str = None,
        proxy_icon_url: str = None
    ):
        self.footer = {
            "text": text,
            "icon_url": icon_url,
            "proxy_icon_url": proxy_icon_url
        }

    def set_image(
        self,
        url: str,
        proxy_url: str = None,
        height: int = None,
        width: int = None
    ):
        self.image = {
            "url": url,
            "proxy_url": proxy_url,
            "height": height,
            "width": width
        }

    def set_thumbnail(
        self,
        url: str,
        proxy_url: str = None,
        height: int = None,
        width: int = None
    ):
        self.thumbnail = {
            "url": url,
            "proxy_url": proxy_url,
            "height": height,
            "width": width
        }

    def remove_image(self):
        self.image = None

    def remove_thumbnail(self):
        self.thumbnail = None

    def add_field(
        self,
        name: str,
        value: str,
        inline: bool = False
    ):
        if not self.fields:
            self.fields = []
        self.fields.append({
            "name": name,
            "value": value,
            "inline": inline
        })

    def to_dict(self) -> dict:
        payload = {
            "title": self.title,
            "type": self.type,
            "description": self.description,
            "url": self.url,
            "color": 0,
            "video": self.video,
            "provider": self.provider
        }

        if self.fields:
            payload["fields"] = self.fields

        if self.author:
            payload["author"] = self.author

        if self.color:
            payload["color"] = self.color

        if self.footer:
            payload["footer"] = self.footer

        if self.image:
            payload["image"] = self.image

        if self.thumbnail:
            payload["thumbnail"] = self.thumbnail

        if self.timestamp:
            payload["timestamp"] = self.timestamp

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